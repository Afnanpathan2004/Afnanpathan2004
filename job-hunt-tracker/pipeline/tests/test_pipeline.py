"""Offline tests for the hourly pipeline (no network): python -m unittest discover -s tests -v"""
import copy
import datetime as dt
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml
from openpyxl import load_workbook

HERE = Path(__file__).resolve().parent
PIPE = HERE.parent
ROOT = PIPE.parent
sys.path.insert(0, str(PIPE))
sys.path.insert(0, str(ROOT / "build"))

import enrich  # noqa: E402
import sources  # noqa: E402
import state as wbstate  # noqa: E402

TODAY = dt.date(2026, 11, 12)
DESC_SRE = ("<p>We are hiring an entry-level SRE. Requirements: 0-1 years of experience, Bachelor's degree in Computer Science. "
            "Strong Linux, Python and Bash. Experience with AWS and Docker. Understanding of networking (TCP/IP, DNS).</p>"
            "<p>Nice to have: Kubernetes, Terraform, Prometheus and Grafana.</p>")


def gh_job(jid, title, loc, desc=DESC_SRE, days_ago=2):
    return {"id": jid, "title": title, "location": {"name": loc},
            "absolute_url": f"https://job-boards.greenhouse.io/cloudflare/jobs/{jid}",
            "updated_at": (TODAY - dt.timedelta(days=days_ago)).isoformat() + "T10:00:00-04:00",
            "content": desc.replace("<", "&lt;").replace(">", "&gt;")}   # greenhouse double-encodes


def fixtures_day1():
    return {
        "boards-api.greenhouse.io_v1_boards_cloudflare_jobs.json": {"jobs": [
            gh_job(1, "Site Reliability Engineer I", "Bengaluru, India"),
            gh_job(2, "Senior Site Reliability Engineer", "Bengaluru, India"),                     # senior -> excluded
            gh_job(3, "Associate Cloud Support Engineer", "Hyderabad, India"),
            gh_job(4, "DevOps Engineer", "Austin, TX"),                                            # not a target location
            gh_job(5, "Account Executive", "Bengaluru, India"),                                    # not a tech role
            gh_job(6, "Platform Engineer", "Pune, India", desc="<p>5+ years of experience with Kubernetes.</p>"),  # too senior
            gh_job(7, "Junior DevOps Engineer", "Bengaluru, India", days_ago=60),                  # too old
        ]},
        "api.lever.co_v0_postings_cred.json": [
            {"text": "Data Analyst", "hostedUrl": "https://jobs.lever.co/cred/abc", "createdAt": int(dt.datetime(2026, 11, 10, tzinfo=dt.timezone.utc).timestamp() * 1000),
             "categories": {"location": "Bangalore", "commitment": "Full-time"}, "workplaceType": "onsite",
             "descriptionPlain": "0-2 years of experience. SQL, Excel, Power BI and Python. Bachelor's degree.", "lists": []}],
        "api.ashbyhq.com_posting-api_job-board_together-ai.json": {"jobs": [
            {"title": "Junior Software Engineer, Inference", "location": "Remote - India", "isRemote": True,
             "jobUrl": "https://jobs.ashbyhq.com/together-ai/xyz", "publishedAt": "2026-11-10T00:00:00Z",
             "employmentType": "FullTime", "descriptionPlain": "1+ years of experience. Python, Kubernetes, Linux, model serving and inference."}]},
        "remotive.com_api_remote-jobs.json": {"jobs": [
            {"title": "Junior DevOps Engineer", "company_name": "Acme", "url": "https://remotive.com/remote-jobs/devops/junior-devops-1",
             "candidate_required_location": "Worldwide", "publication_date": "2026-11-09T08:00:00", "job_type": "full_time",
             "description": "Docker, CI/CD pipelines with GitHub Actions, AWS, Linux. 1 year of experience."},
            {"title": "Junior Cloud Engineer", "company_name": "USCo", "url": "https://remotive.com/remote-jobs/devops/junior-cloud-2",
             "candidate_required_location": "USA Only", "publication_date": "2026-11-09T08:00:00",
             "description": "AWS, Terraform."}]},                                                     # US-only remote -> excluded
        "www.arbeitnow.com_api_job-board-api.json": {"data": [
            {"title": "Junior Cloud Engineer (m/w/d)", "company_name": "BerlinTech", "url": "https://www.arbeitnow.com/jobs/companies/berlintech/junior-cloud",
             "location": "Berlin", "remote": False, "created_at": int(dt.datetime(2026, 11, 9, tzinfo=dt.timezone.utc).timestamp()), "visa_sponsorship": True,
             "description": "<p>AWS, Terraform, Kubernetes, Linux, Python, Docker, CI/CD. We offer visa sponsorship and a relocation package.</p>"},
            {"title": "Junior Backend Developer", "company_name": "NoVisa GmbH", "url": "https://www.arbeitnow.com/jobs/companies/novisa/backend",
             "location": "Munich", "remote": False, "created_at": int(dt.datetime(2026, 11, 9, tzinfo=dt.timezone.utc).timestamp()),
             "description": "Python, REST APIs. Unfortunately we cannot offer visa sponsorship."}]},  # explicit no-visa -> excluded
        "www.amazon.jobs_en_search.json.json": {"jobs": [
            {"title": "Cloud Support Associate", "job_path": "/en/jobs/2999999/cloud-support-associate",
             "normalized_location": "Hyderabad, Telangana, IND", "posted_date": "November 8, 2026",
             "description": "Troubleshoot customer issues.", "basic_qualifications": "Linux, networking (TCP/IP, DNS), communication skills.",
             "preferred_qualifications": "AWS, Python"}]},
    }


def write_fixtures(d: Path, files: dict):
    d.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        (d / name).write_text(json.dumps(data), encoding="utf-8")


def test_config(tmp: Path):
    cfg = yaml.safe_load((PIPE / "config.yaml").read_text(encoding="utf-8"))
    cfg["selection"]["min_match"] = 0.5
    cfg["sources"] = {"greenhouse": {"cloudflare": "Cloudflare", "notarealboard": "Ghost"},   # second one fails (404)
                      "lever": {"cred": "CRED"}, "ashby": {"together-ai": "Together AI"},
                      "amazon": {"enabled": True, "queries": ["cloud support"], "locations": ["India"]},
                      "remotive": {"enabled": True, "categories": ["devops"]},
                      "arbeitnow": {"enabled": True, "pages": 1}}
    p = tmp / "config.yaml"
    p.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    return p


class UnitTests(unittest.TestCase):
    cfg = yaml.safe_load((PIPE / "config.yaml").read_text(encoding="utf-8"))

    def test_classify(self):
        self.assertEqual(enrich.classify("Site Reliability Engineer I", self.cfg), ("P1", "Cloud & DevOps"))
        self.assertEqual(enrich.classify("DevSecOps Engineer", self.cfg)[0], "P5")
        self.assertEqual(enrich.classify("Machine Learning Engineer", self.cfg)[0], "P3")
        self.assertEqual(enrich.classify("Data Analyst", self.cfg)[0], "P2")
        self.assertEqual(enrich.classify("Backend Developer (Node.js)", self.cfg)[0], "P4")
        self.assertIsNone(enrich.classify("Senior DevOps Engineer", self.cfg))
        self.assertIsNone(enrich.classify("Staff Software Engineer", self.cfg))
        self.assertIsNone(enrich.classify("Software Engineer III", self.cfg))
        self.assertIsNone(enrich.classify("Account Executive", self.cfg))

    def test_experience(self):
        self.assertEqual(enrich.min_experience("Requires 2-4 years of experience in DevOps"), 2)
        self.assertEqual(enrich.min_experience("3+ yrs experience"), 3)
        self.assertIsNone(enrich.min_experience("Founded 25 years ago"))

    def test_skills(self):
        names = ["Go", "Kubernetes", "SQL", "NoSQL", "CI/CD", "AI Agents"]
        got = enrich.detect_skills("We use golang, k8s and NoSQL stores; customer support agents. Let's go now.", names)
        self.assertIn("Go", got); self.assertIn("Kubernetes", got); self.assertIn("NoSQL", got)
        self.assertNotIn("SQL", got); self.assertNotIn("AI Agents", got)
        self.assertNotIn("Go", enrich.detect_skills("Ready to go the extra mile", ["Go"]))

    def test_visa_patterns(self):
        self.assertTrue(enrich.VISA_NEG.search("We are unable to sponsor visas"))
        self.assertTrue(enrich.VISA_NEG.search("Candidates must have the right to work in the UK"))
        self.assertTrue(enrich.VISA_POS.search("Visa sponsorship is available"))
        self.assertFalse(enrich.VISA_POS.search("No visa sponsorship"))
        self.assertTrue(enrich.VISA_NEG.search("Unfortunately we cannot offer visa sponsorship."))
        self.assertTrue(enrich.VISA_NEG.search("We don't sponsor work permits"))

    def test_greenhouse_html(self):
        self.assertEqual(sources.strip_html("&lt;p&gt;Linux &amp;amp; AWS&lt;/p&gt;"), "Linux & AWS")

    def test_dates(self):
        self.assertEqual(sources.parse_date(1762905600000), dt.date(2025, 11, 12))
        self.assertEqual(sources.parse_date("November 8, 2026"), dt.date(2026, 11, 8))
        self.assertEqual(sources.parse_date("2026-11-10T00:00:00Z"), dt.date(2026, 11, 10))


class PipelineIntegration(unittest.TestCase):
    """End-to-end on a copy of the real workbook with simulated user edits."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.wb = cls.tmp / "tracker.xlsx"
        shutil.copy(ROOT / "Global_Job_Hunt_Tracker.xlsx", cls.wb)
        cls.db = cls.tmp / "jobs_db.json"
        cls.cfg = test_config(cls.tmp)
        cls.fx1 = cls.tmp / "fx1"
        write_fixtures(cls.fx1, fixtures_day1())
        subprocess.run([sys.executable, str(PIPE / "refresh.py"), "--workbook", str(cls.wb), "--db", str(cls.db),
                        "--config", str(cls.cfg), "--init-only"], check=True, capture_output=True)   # as shipped in the repo
        # --- simulate the user's own edits before the bot runs
        wb = load_workbook(cls.wb)
        mt = wb["Master Job Tracker"]
        hdr = {mt.cell(4, c).value: c for c in range(1, mt.max_column + 1)}
        mt.cell(7, hdr["Application Status"]).value = "Applied"            # JOB-0003
        mt.cell(7, hdr["Date Applied"]).value = dt.datetime(2026, 11, 11)
        mt.cell(7, hdr["Notes"]).value = "Referred by a friend"
        for c in range(1, mt.max_column + 1):                               # user deletes JOB-0084 (clears the row)
            if not (isinstance(mt.cell(88, c).value, str) and str(mt.cell(88, c).value).startswith("=")):
                mt.cell(88, c).value = None
        it = wb["Interview Tracker"]
        it["B5"], it["E5"], it["F5"], it["S5"] = "JOB-0003", "Technical Round 1", dt.datetime(2026, 11, 20), "Scheduled"
        pf = wb["My Profile"]
        pf["B6"] = "AWS Cloud Practitioner"
        wb["Daily Job Hunting Log"]["D6"] = 4
        wb.save(cls.wb)
        shutil.copy(cls.wb, cls.tmp / "before_first_run.xlsx")

    def refresh(self, fixtures, today):
        cmd = [sys.executable, str(PIPE / "refresh.py"), "--workbook", str(self.wb), "--db", str(self.db),
               "--config", str(self.cfg), "--fixtures", str(fixtures), "--today", today.isoformat()]
        r = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r.stdout

    def master(self):
        return {r["id"]: r for r in wbstate.read_workbook(self.wb)["rows"]}

    def test_1_first_refresh_adds_suitable_and_keeps_edits(self):
        out = self.refresh(self.fx1, TODAY)
        rows = self.master()
        new = {i: r for i, r in rows.items() if int(i[4:]) > 84}
        self.assertNotIn("JOB-0084", rows)                                  # deleted ID is never reused
        titles = sorted(r["title"] for r in new.values())
        self.assertIn("Site Reliability Engineer I", titles)
        self.assertIn("Associate Cloud Support Engineer", titles)
        self.assertIn("Data Analyst", titles)
        self.assertIn("Junior Software Engineer, Inference", titles)
        self.assertIn("Junior DevOps Engineer", titles)                     # remotive worldwide
        self.assertIn("Junior Cloud Engineer (m/w/d)", titles)              # Berlin with explicit sponsorship
        self.assertIn("Cloud Support Associate", titles)                    # amazon
        for bad in ("Senior Site Reliability Engineer", "DevOps Engineer", "Account Executive", "Platform Engineer",
                    "Junior Cloud Engineer", "Junior Backend Developer"):
            self.assertNotIn(bad, titles, bad)
        berlin = next(r for r in new.values() if r["company"] == "BerlinTech")
        self.assertEqual(berlin["visa"], "Yes"); self.assertEqual(berlin["reloc"], "Yes")
        self.assertEqual(berlin["locfit"], enrich.SPON)
        sre = next(r for r in new.values() if r["title"] == "Site Reliability Engineer I")
        self.assertNotIn("Munich", [r["location"] for r in new.values()])  # "cannot offer visa sponsorship" excluded
        self.assertEqual(sre["conf"], "High"); self.assertEqual(sre["lstatus"], "Active (API-verified)")
        self.assertIn("Linux", sre["req"]); self.assertIn("Kubernetes", sre["pref"]); self.assertNotIn("Kubernetes", sre["req"])
        # user's edits survived the rebuild
        self.assertEqual(rows["JOB-0003"]["status"], "Applied")
        self.assertEqual(rows["JOB-0003"]["notes"], "Referred by a friend")
        self.assertNotIn("JOB-0084", rows)
        wb = load_workbook(self.wb)
        self.assertEqual(wb["Interview Tracker"]["B5"].value, "JOB-0003")
        self.assertEqual(wb["Interview Tracker"]["F5"].value.date(), dt.date(2026, 11, 20))
        self.assertEqual(wb["My Profile"]["B6"].value, "AWS Cloud Practitioner")
        self.assertEqual(wb["Daily Job Hunting Log"]["D6"].value, 4)
        self.assertIn("Pipeline Runs", wb.sheetnames)
        self.assertIn("greenhouse:notarealboard | no", out)                               # failing board reported, run still succeeded

    def test_1b_stale_copy_does_not_lose_bot_jobs(self):
        """User pushes an older copy (from before the bot's run): bot-added jobs must come back, not count as deleted."""
        tmp = Path(tempfile.mkdtemp())
        stale, db = tmp / "stale.xlsx", tmp / "db.json"
        shutil.copy(self.tmp / "before_first_run.xlsx", stale)
        shutil.copy(self.db, db)
        expected = {i for i in self.master() if int(i[4:]) > 84}
        cmd = [sys.executable, str(PIPE / "refresh.py"), "--workbook", str(stale), "--db", str(db),
               "--config", str(self.cfg), "--fixtures", str(self.fx1), "--today", TODAY.isoformat()]
        r = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("restored", r.stdout)
        got = {x["id"] for x in wbstate.read_workbook(stale)["rows"]}
        self.assertTrue(expected <= got, expected - got)
        ids = [x["id"] for x in wbstate.read_workbook(stale)["rows"]]
        self.assertEqual(len(ids), len(set(ids)))                          # no duplicates

    def test_2_second_refresh_same_data_no_change(self):
        before = self.wb.stat().st_mtime_ns
        out = self.refresh(self.fx1, TODAY)
        self.assertIn("Workbook unchanged", out)
        self.assertEqual(self.wb.stat().st_mtime_ns, before)

    def test_3_deleted_job_not_readded_and_closure_detection(self):
        rows = self.master()
        sre_id = next(i for i, r in rows.items() if r["title"] == "Site Reliability Engineer I" and r["company"] == "Cloudflare")
        sup_id = next(i for i, r in rows.items() if r["title"] == "Associate Cloud Support Engineer" and r["company"] == "Cloudflare")
        # user deletes the support job row; user sets their own listing status on the SRE job? no - keep pipeline-owned
        wb = load_workbook(self.wb)
        mt = wb["Master Job Tracker"]
        r_sup = next(r for r in range(5, mt.max_row + 1) if mt.cell(r, 1).value == sup_id)
        for c in range(1, mt.max_column + 1):
            if not (isinstance(mt.cell(r_sup, c).value, str) and str(mt.cell(r_sup, c).value).startswith("=")):
                mt.cell(r_sup, c).value = None
        wb.save(self.wb)
        # SRE I disappears from the Cloudflare board for 3 runs -> Possibly Closed
        fx2 = self.tmp / "fx2"
        d2 = copy.deepcopy(fixtures_day1())
        d2["boards-api.greenhouse.io_v1_boards_cloudflare_jobs.json"]["jobs"] = [
            j for j in d2["boards-api.greenhouse.io_v1_boards_cloudflare_jobs.json"]["jobs"] if j["id"] != 1]
        write_fixtures(fx2, d2)
        for _ in range(3):
            self.refresh(fx2, TODAY)
        rows = self.master()
        self.assertEqual(rows[sre_id]["lstatus"], "Possibly Closed")
        self.assertNotIn(sup_id, rows)                                      # deleted by user, still seen on board, not re-added
        # user overrides the status; pipeline must leave it alone even when job keeps missing
        wb = load_workbook(self.wb)
        mt = wb["Master Job Tracker"]
        hdr = {mt.cell(4, c).value: c for c in range(1, mt.max_column + 1)}
        r_sre = next(r for r in range(5, mt.max_row + 1) if mt.cell(r, 1).value == sre_id)
        mt.cell(r_sre, hdr["Listing Status"]).value = "Active (page verified)"
        wb.save(self.wb)
        for _ in range(2):
            self.refresh(fx2, TODAY + dt.timedelta(days=1))
        self.assertEqual(self.master()[sre_id]["lstatus"], "Active (page verified)")

    def test_4_recalc_clean(self):
        if not shutil.which("soffice"):
            self.skipTest("LibreOffice not installed")
        r = subprocess.run([sys.executable, str(PIPE / "recalc.py"), str(self.wb)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("formula errors: 0", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
