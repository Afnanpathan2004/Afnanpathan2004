"""Turn RawJobs into scored master-row dicts that match the workbook schema.

The Python match score mirrors the workbook's Match Percentage formula exactly, so a job added
because it scored >= min_match shows the same score once it lands in Excel.
"""
from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass

IN_OK = "Eligible - India-based role"
REM_OK = "Eligible - Remote open to India"
SPON = "Sponsorship explicitly offered"
SPON_UNK = "Sponsorship unknown"
NOT_OK = "Not eligible - restricted"
LOC_SCORE_DEFAULT = {IN_OK: 1.0, REM_OK: 1.0, SPON: 0.85, SPON_UNK: 0.4, NOT_OK: 0.0}
PROF = {"None": 0, "Beginner": 1, "Intermediate": 2, "Advanced": 3, "Expert": 4}

# Extra spellings for skill detection. Default for any other skill = the skill name as a whole word.
ALIASES = {
    "Kubernetes": [r"kubernetes", r"\bk8s\b", r"\beks\b", r"\baks\b", r"\bgke\b", r"openshift"],
    "CI/CD": [r"ci\s*/\s*cd", r"continuous (integration|delivery|deployment)", r"(build|deployment|release|ci) pipelines?"],
    "AWS": [r"\baws\b", r"amazon web services", r"\bec2\b", r"\bs3\b", r"\blambda\b"],
    "Azure": [r"\bazure\b"], "GCP": [r"\bgcp\b", r"google cloud"],
    "Cloud": [r"\bcloud\b", r"\baws\b", r"\bazure\b", r"\bgcp\b"],
    "Go": [r"\bgolang\b", r"\bGo\b(?!\s+(to|through|live|beyond|above|over))"],
    "Networking": [r"\bnetworking\b", r"tcp/ip", r"\bdns\b", r"\bsubnet", r"\brouting\b", r"\bvpc\b"],
    "Infrastructure as Code": [r"infrastructure[- ]as[- ]code", r"\biac\b"],
    "SRE": [r"\bsre\b", r"site reliability"], "Monitoring": [r"\bmonitoring\b", r"\balerting\b"],
    "Observability": [r"observability", r"\btracing\b", r"\bslos?\b"],
    "Incident Management": [r"incident management", r"\bon-?call\b", r"post-?mortem"],
    "ELK Stack": [r"\belk\b", r"elasticsearch", r"kibana", r"logstash"],
    "Bash": [r"\bbash\b", r"shell script"], "Linux": [r"\blinux\b", r"\bunix\b"],
    "SQL": [r"\bsql\b", r"postgres", r"mysql"], "Advanced SQL": [r"window functions", r"advanced sql", r"query optimi[sz]ation"],
    "Power BI": [r"power\s?bi"], "Excel": [r"\b(ms |microsoft )?excel\b(?! (in|at)\b)"],
    "Machine Learning": [r"machine learning", r"\bml\b"], "Deep Learning": [r"deep learning", r"neural network"],
    "Data Visualization": [r"data visuali[sz]ation", r"dashboards?"], "Scikit-learn": [r"scikit", r"sklearn"],
    "Data Engineering": [r"data engineering", r"data pipelines?", r"data warehous"], "ETL": [r"\betl\b", r"\belt\b"],
    "Spark": [r"\bspark\b", r"pyspark", r"databricks"], "Airflow": [r"airflow"],
    "LLMs": [r"\bllms?\b", r"large language model", r"\bgpt", r"generative ai", r"\bgenai\b"],
    "RAG": [r"\brag\b", r"retrieval[- ]augmented"], "Vector Databases": [r"vector (database|db|store)", r"pinecone", r"qdrant", r"weaviate", r"pgvector", r"faiss", r"chroma"],
    "AI Agents": [r"\bai agents?", r"agentic", r"autonomous agents?", r"llm agents?"], "MCP": [r"model context protocol", r"\bmcp\b"],
    "API Development": [r"api (development|design)", r"(build|develop|design)\w* (rest(ful)? )?apis?"], "REST APIs": [r"\brest(ful)?\b"], "Model Deployment": [r"model (deployment|serving)", r"inference"],
    "Prompt Engineering": [r"prompt (engineering|design)"], "Evaluation Frameworks": [r"\bevals?\b", r"evaluation framework"],
    "Data Structures and Algorithms": [r"data structures", r"algorithms", r"\bdsa\b"], "OOP": [r"object[- ]oriented", r"\boop\b"],
    "System Design": [r"system design", r"distributed systems"], "JavaScript": [r"javascript", r"\bjs\b"],
    "Node.js": [r"node\.?js"], "React": [r"\breact\b"], "NoSQL": [r"nosql", r"mongodb", r"dynamodb", r"cassandra", r"redis"],
    "Testing": [r"\btesting\b", r"unit tests?", r"pytest", r"\bjunit\b"], "Git": [r"\bgit\b", r"github", r"gitlab"],
    "SIEM": [r"\bsiem\b"], "SIEM Tools": [r"splunk", r"sentinel", r"qradar", r"\belastic security"], "SOC Operations": [r"\bsoc\b", r"security operations"],
    "Vulnerability Management": [r"vulnerabilit"], "Penetration Testing": [r"penetration test", r"pentest"],
    "IAM": [r"\biam\b", r"identity and access"], "Cloud Security": [r"cloud security"], "Incident Response": [r"incident response"],
    "Threat Detection": [r"threat detection", r"threat hunting"], "Security Automation": [r"security automation", r"\bsoar\b"],
    "DevSecOps": [r"devsecops", r"\bsast\b", r"\bdast\b"], "Firewalls": [r"firewall"],
    "Troubleshooting": [r"troubleshoot"], "Communication": [r"communication skills", r"\bcommunicat"],
    "Databases": [r"\bdatabases?\b"], "C++": [r"c\+\+"], "Hugging Face": [r"hugging ?face", r"transformers"],
    "GitHub Actions": [r"github actions"], "Prometheus": [r"prometheus"], "Grafana": [r"grafana"],
}
CERT_PATTERNS = [r"AWS Certified[\w\s-]{0,40}", r"\bCKA\b", r"\bCKAD\b", r"AZ-\d{3}", r"\bCCNA\b", r"Security\+",
                 r"\bCEH\b", r"\bCISSP\b", r"\bRHCSA\b", r"Terraform Associate", r"SC-\d{3}", r"\bPL-300\b"]
PREF_SPLIT = re.compile(r"(?i)(preferred|nice[- ]to[- ]have|bonus points|good[- ]to[- ]have|pluses|desirable|additional qualifications)")
EXP_RX = re.compile(r"(?i)(\d{1,2})\s*(?:\+|plus)?\s*(?:-|–|to)?\s*(\d{1,2})?\s*\+?\s*(?:years|yrs)")
VISA_NEG = re.compile(r"(?i)(no visa|not (?:be )?able to sponsor|unable to (?:provide )?sponsor|(?:does not|do not|will not|can ?not|can't|won't|don't|doesn't|are not able to) (?:offer |provide |support )?(?:any )?(?:visa |work permit )?sponsor|without (?:the need for )?(?:visa )?sponsorship|sponsorship is not (?:available|provided)|must (?:already )?have (?:the )?(?:right|authori[sz]ation) to work|eu work permit required)")
VISA_POS = re.compile(r"(?i)(visa sponsorship (?:is )?(?:available|provided|offered|possible)|(?:we|will) sponsor|sponsor(?:ship)? (?:your |a )?(?:work )?visa|blue card support|relocation and visa)")
RELOC_POS = re.compile(r"(?i)(relocation (?:package|support|assistance|bonus|allowance)|help(?:s)? you relocate|we (?:will )?(?:help|support) (?:with )?relocat)")
EDU_RX = re.compile(r"(?i)((?:bachelor|master|b\.?\s?tech|b\.?e\b|m\.?tech|bsc|msc|degree)[^.\n]{0,90})")


@dataclass
class Profile:
    skills: dict          # skill -> proficiency level 0..4
    years: float = 0
    has_degree: bool = True
    certs: str = ""
    weights: tuple = (40, 20, 10, 15, 10, 5)
    loc_scores: dict = None

    def level(self, s):
        return self.skills.get(s, 0)


def _rx(skill):
    pats = ALIASES.get(skill) or [r"(?<![\w+#])" + re.escape(skill) + r"(?![\w+#])"]
    flags = 0 if skill == "Go" else re.I
    return [re.compile(p, flags) for p in pats]


_RX_CACHE = {}


def detect_skills(text, skill_names):
    found = []
    for s in skill_names:
        if s not in _RX_CACHE:
            _RX_CACHE[s] = _rx(s)
        if any(r.search(text) for r in _RX_CACHE[s]):
            found.append(s)
    return found


def classify(title, cfg):
    t = title.lower()
    if any(re.search(p, t) for p in cfg.get("exclude_title_patterns", [])):
        return None
    for g in cfg["roles"]:
        if any(re.search(p, t) for p in g["patterns"]):
            return g["priority"], g["category"]
    return None


def min_experience(text):
    best = None
    for m in EXP_RX.finditer(text or ""):
        ctx = text[max(0, m.start() - 80): m.end() + 80].lower()
        if "experience" not in ctx and "exp" not in ctx:
            continue
        lo = int(m.group(1))
        if lo > 25:
            continue
        best = lo if best is None else min(best, lo)
    return best


def job_level(title, minexp):
    t = title.lower()
    if re.search(r"\bintern(ship)?\b|working student|werkstudent|trainee", t):
        return "Internship"
    if "apprentice" in t:
        return "Apprenticeship"
    if re.search(r"graduate|new grad|campus|fresher|early career", t):
        return "Graduate Program"
    if re.search(r"junior|\bjr\b|associate|entry|\bi\b|\b1\b|level 1|\bl1\b", t):
        return "Entry-Level"
    if minexp is None:
        return "Entry-Level" if not re.search(r"\bii\b|\b2\b", t) else "Early-Career (1-3 yrs)"
    return "Entry-Level" if minexp <= 1 else "Early-Career (1-3 yrs)" if minexp <= 3 else "Experienced"


def location_fit(job, desc, cfg):
    """Return (location_group, country, fit, remote_eligibility_text) or None if not a target location."""
    loc = (job.location or "").lower()
    L = cfg["locations"]
    is_india = any(t in loc for t in L["india_terms"])
    if is_india and not job.remote:
        return "India", "India", IN_OK, "N/A"
    if job.remote or "remote" in loc:
        restr = loc.replace("remote", "").strip(" -:,;()")
        if is_india or any(t in loc for t in L["remote_ok_terms"]):
            return "Remote - India Eligible", "Remote", REM_OK, "Yes - " + (job.location or "Remote")
        if restr in ("", "unspecified"):
            if re.search(r"(?i)(work from anywhere|anywhere in the world|globally remote|fully remote worldwide)", desc):
                return "Remote - India Eligible", "Remote", REM_OK, "Yes - worldwide per description"
            return "Remote - Restricted / Unclear", "Remote", SPON_UNK, "Unclear - verify"
        return "Remote - Restricted / Unclear", "Remote", NOT_OK, "No - " + (job.location or "")
    for country, terms in L["relocation_countries"].items():
        if any(t in loc for t in terms):
            group = country if country in ("Germany", "UAE") else "Other International"
            fit = SPON if VISA_POS.search(desc) and not VISA_NEG.search(desc) else (NOT_OK if VISA_NEG.search(desc) else SPON_UNK)
            return group, country, fit, "N/A"
    return None


def score(req, pref, minexp, fit, certs, profile: Profile):
    def skill_score(skills):
        if not skills:
            return 0.5
        pts = sum(1 if profile.level(s) >= 2 else 0.5 if profile.level(s) == 1 else 0 for s in skills)
        return pts / len(skills)
    s_tech, s_pref = skill_score(req), skill_score(pref)
    y = profile.years
    if minexp is None:
        s_exp = 0.5
    else:
        gap = minexp - y
        s_exp = 1 if gap <= 0 else 0.75 if gap <= 1 else 0.45 if gap <= 2 else 0.2 if gap <= 3 else 0
    s_edu = 0.9 if profile.has_degree else 0.6
    s_loc = (profile.loc_scores or LOC_SCORE_DEFAULT).get(fit, 0.4)
    s_cert = 1 if not certs or certs.lower() in (profile.certs or "").lower() else 0.4
    w = profile.weights
    return (s_tech * w[0] + s_exp * w[1] + s_edu * w[2] + s_loc * w[3] + s_pref * w[4] + s_cert * w[5]) / sum(w)


def enrich(job, cfg, profile: Profile, today: dt.date):
    """Return (row_dict, match) or (None, reason)."""
    cls = classify(job.title, cfg)
    if not cls:
        return None, "role/seniority"
    pri, cat = cls
    desc = job.description or ""
    if job.posted and (today - job.posted).days > cfg["selection"]["max_age_days"]:
        return None, "too old"
    lf = location_fit(job, desc, cfg)
    if not lf:
        return None, "location"
    group, country, fit, remote_txt = lf
    if fit == NOT_OK:
        return None, "location restricted"
    if group == "Remote - Restricted / Unclear" and not cfg["selection"].get("include_unknown_location_remote"):
        return None, "remote eligibility unclear"
    minexp = min_experience(desc)
    if minexp is not None and minexp > cfg["selection"]["max_years_required"]:
        return None, "experience"
    skill_names = list(profile.skills.keys())
    m = PREF_SPLIT.search(desc)
    main, tail = (desc[:m.start()], desc[m.start():]) if m else (desc, "")
    req = detect_skills(job.title + "\n" + main, skill_names)
    pref = [s for s in detect_skills(tail, skill_names) if s not in req]
    certs = ""
    for p in CERT_PATTERNS:
        mm = re.search(p, main)
        if mm:
            certs = mm.group(0).strip()
            break
    match = score(req, pref, minexp, fit, certs, profile)
    edu = EDU_RX.search(desc)
    visa = "Not required (India)" if group == "India" else ("N/A (remote)" if group.startswith("Remote") else
           "Yes" if fit == SPON else "No" if VISA_NEG.search(desc) else "Unknown")
    reloc = "Yes" if RELOC_POS.search(desc) else ("N/A" if group.startswith("Remote") else "Unknown")
    langs = [s for s in req + pref if s in ("Python", "Java", "Go", "JavaScript", "TypeScript", "C++", "Bash", "SQL")]
    clouds = [s for s in req + pref if s in ("AWS", "Azure", "GCP")]
    tools = [s for s in req + pref if s in ("Docker", "Kubernetes", "Terraform", "Ansible", "Jenkins", "GitHub Actions",
                                            "Prometheus", "Grafana", "ELK Stack", "Airflow", "Spark", "LangChain", "Power BI", "Tableau")]
    sentences = [x.strip() for x in re.split(r"(?<=[.!?])\s+|\n", desc) if 40 < len(x.strip()) < 260]
    exp_sent = next((x for x in sentences if EXP_RX.search(x) and "experience" in x.lower()), "")
    is_ats = job.source_kind == "ats"
    row = {
        "pri": pri, "title": job.title[:200], "cat": cat, "company": job.company or "Unknown", "website": "",
        "url": job.url, "source": job.source, "location": (job.location or "")[:120], "country": country,
        "locgroup": group, "mode": "Remote" if group.startswith("Remote") else "Unknown",
        "exp": f"{minexp}+ years (from description)" if minexp is not None else "Not stated",
        "minexp": minexp, "level": job_level(job.title, minexp), "emp": job.employment_type or "Full-time",
        "salary": job.salary or "Not disclosed", "cur": job.currency or ("INR" if group == "India" else ""),
        "visa": visa, "reloc": reloc, "remote_india": remote_txt, "edu": edu.group(1).strip()[:120] if edu else "Not stated",
        "edu_ok": "Unknown", "req": ", ".join(req) if req else "Unknown - open JD", "pref": ", ".join(pref),
        "langs": ", ".join(langs), "clouds": ", ".join(clouds), "tools": ", ".join(tools),
        "certs": certs or "None stated", "expdetail": exp_sent[:300],
        "hard": "None stated" if fit != SPON_UNK or group.startswith("Remote") else "Work authorization / sponsorship needed",
        "locfit": fit, "deadline": None, "posted": job.posted, "disc": today, "verified": today,
        "conf": "High" if is_ats else "Medium", "lstatus": "Active (API-verified)", "status": "Not Applied",
        "cover": "No", "jd": (sentences[0] if sentences else "")[:300],
        "reqtype": "Auto-extracted: skills before a 'preferred/nice-to-have' heading are treated as required; review the JD.",
        "notes": f"Auto-added by hourly pipeline on {today.isoformat()} (match {match:.0%}).",
    }
    return row, match
