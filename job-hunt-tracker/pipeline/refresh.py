"""Hourly refresh: fetch -> filter/score -> merge with the user's workbook -> rebuild only if something changed.

    python refresh.py                       # live run (used by GitHub Actions)
    python refresh.py --fixtures tests/fixtures   # offline run on saved API responses (tests)

Outputs: rebuilt workbook (if changed), data/jobs_db.json (memory of every job ever seen), run summary markdown,
and 'changed=true|false' in $GITHUB_OUTPUT.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import yaml
from openpyxl import load_workbook

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "build"))

import enrich  # noqa: E402
import sources  # noqa: E402
import state as wbstate  # noqa: E402
from schema import SCHEMA_VERSION  # noqa: E402

FULL_BOARD_PREFIXES = ("greenhouse:", "lever:", "ashby:", "smartrecruiters:")   # complete listings -> closure detection
PIPELINE_LSTATUSES = {"Active (API-verified)", "Possibly Closed", "Closed / Expired"}
PRE_APPLY = {"Not Applied", "", None}


# ------------------------------------------------------------------ helpers
def norm_url(u: str) -> str:
    if not u:
        return ""
    p = urlsplit(u.strip())
    query = "" if any(h in p.netloc for h in ("greenhouse", "lever.co", "ashbyhq", "smartrecruiters", "amazon.jobs", "myworkdayjobs")) else p.query
    query = "&".join(x for x in query.split("&") if x and not x.lower().startswith(("utm_", "ref=", "source=", "gh_src")))
    return urlunsplit((p.scheme.lower() or "https", p.netloc.lower().removeprefix("www."), p.path.rstrip("/"), query, ""))


def norm_text(s) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(s or "").lower()).strip()


def keys_for(company, title, location, url):
    ks = []
    nu = norm_url(url)
    if nu:
        ks.append("u:" + nu)
    if title and company:
        ks.append("t:" + "|".join(norm_text(x) for x in (company, title, (location or "").split(";")[0])))
    return ks


def id_num(i):
    m = re.match(r"JOB-(\d+)$", str(i or ""))
    return int(m.group(1)) if m else 0


def to_jsonable(rows):
    out = []
    for r in rows:
        o = {}
        for k, v in r.items():
            o[k] = v.isoformat() if isinstance(v, (dt.date, dt.datetime)) else v
        out.append(o)
    return out


def load_db(path: Path):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"jobs": {}, "keys": {}, "runs": [], "schema_version": 0}


def load_fixtures(cfg, fixtures: Path):
    """Offline mode: route every HTTP call to a saved JSON file named after the host + path."""
    class FakeResp:
        def __init__(self, data, code=200):
            self._d, self.status_code = data, code

        def json(self):
            return self._d

    class FakeSession:
        def _load(self, url):
            p = urlsplit(url)
            name = (p.netloc + p.path).replace("/", "_").replace(":", "_") + ".json"
            f = fixtures / name
            return FakeResp(json.loads(f.read_text(encoding="utf-8"))) if f.exists() else FakeResp({}, 404)

        def get(self, url, **kw):
            return self._load(url)

        def post(self, url, **kw):
            return self._load(url)
    return sources.fetch_all(cfg, session=FakeSession())


# ------------------------------------------------------------------ main
def run(args):
    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    sel, life = cfg["selection"], cfg["lifecycle"]
    now = dt.datetime.now(dt.timezone.utc)
    today = dt.date.fromisoformat(args.today) if args.today else now.date()
    wb_path, db_path = Path(args.workbook), Path(args.db)

    # 1) what the user has now
    st = wbstate.read_workbook(wb_path)
    rows, cells, profile = st["rows"], st["cells"], st["profile"]
    db = load_db(db_path)
    jobs_db, keys = db["jobs"], db["keys"]
    first_run = not jobs_db

    present = set()
    for r in rows:                                   # sync DB with the workbook (manual rows, user-added rows)
        jid = r["id"]
        present.add(jid)
        meta = jobs_db.setdefault(jid, {"origin": "manual", "first_seen": today.isoformat()})
        meta["removed"] = False
        for k in keys_for(r.get("company"), r.get("title"), r.get("location"), r.get("url")):
            keys.setdefault(k, jid)
    file_run = st.get("last_run")                    # newest pipeline run this copy of the workbook has seen
    restored = []
    for jid, meta in sorted(jobs_db.items()):
        if jid in present or meta.get("removed"):
            continue
        added = meta.get("added_ts")
        if meta.get("origin") == "api" and meta.get("snapshot") and added and (file_run is None or added > file_run):
            # the workbook predates this job (e.g. you pushed an older copy) -> put it back, it was never deleted
            rows.append(dict(meta["snapshot"]))
            present.add(jid)
            restored.append(jid)
        else:                                        # rows the user deleted stay remembered, never re-added
            meta["removed"] = True
            meta["removed_on"] = today.isoformat()

    if args.init_only:                               # just record the current workbook in the job memory
        db["max_id"] = max([id_num(i) for i in jobs_db] + [db.get("max_id", 0)])
        if "Pipeline Runs" in load_workbook(wb_path, read_only=True).sheetnames:
            db["schema_version"] = SCHEMA_VERSION    # workbook already has the current layout
        db_path.parent.mkdir(parents=True, exist_ok=True)
        db_path.write_text(json.dumps(db, indent=1, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        print(f"initialised {db_path} with {len(jobs_db)} jobs")
        return False, {}

    # 2) fetch
    raw, health = load_fixtures(cfg, Path(args.fixtures)) if args.fixtures else sources.fetch_all(cfg)
    ok_boards = {name for name, ok, _, _ in health if ok}

    # 3) known jobs: mark seen; unknown: score
    seen_ids, candidates, cand_keys, reasons = set(), [], set(), {}
    for j in raw:
        ks = keys_for(j.company, j.title, j.location, j.url)
        known = next((keys[k] for k in ks if k in keys), None)
        if known:
            seen_ids.add(known)
            m = jobs_db.get(known, {})
            if m.get("origin") == "api":
                m["last_seen"] = today.isoformat()
            continue
        if any(k in cand_keys for k in ks):
            continue
        row, match = enrich.enrich(j, cfg, profile, today)
        if row is None:
            reasons[match] = reasons.get(match, 0) + 1
            continue
        if match < sel["min_match"]:
            reasons["below min match"] = reasons.get("below min match", 0) + 1
            continue
        cand_keys.update(ks)
        candidates.append((match, row, ks, j))
    relevant = len(candidates)

    # 4) choose the most suitable: match first, then priority (P1 best)
    candidates.sort(key=lambda c: (c[0] * 100 + (6 - int(c[1]["pri"][1])) * 3), reverse=True)
    chosen = candidates[: sel["max_new_per_run"]]
    referenced = [id_num(v[1]) for sh in cells.values() for v in sh.values() if isinstance(v[1], str) and v[1].startswith("JOB-")]
    next_id = max([id_num(i) for i in jobs_db] + referenced + [db.get("max_id", 0), 0]) + 1   # never reuse an ID
    new_rows, new_ids = [], []
    for match, row, ks, j in chosen:
        jid = f"JOB-{next_id:04d}"
        next_id += 1
        row["id"] = jid
        new_rows.append(row)
        new_ids.append(jid)
        jobs_db[jid] = {"origin": "api", "board": j.board, "source_kind": j.source_kind, "first_seen": today.isoformat(),
                        "last_seen": today.isoformat(), "missing_runs": 0, "pipeline_lstatus": row["lstatus"],
                        "posted": j.posted.isoformat() if j.posted else None, "match_at_add": round(match, 4),
                        "added_ts": now.strftime("%Y-%m-%d %H:%M"), "snapshot": to_jsonable([row])[0]}
        for k in ks:
            keys[k] = jid

    # 5) lifecycle of API jobs already in the workbook
    changed = bool(new_rows) or bool(restored) or first_run or db.get("schema_version") != SCHEMA_VERSION or not wb_path.exists()
    n_pc = n_closed = 0
    kept = []
    archived = []
    for r in rows:
        m = jobs_db.get(r["id"], {})
        if m.get("origin") != "api":
            kept.append(r)
            continue
        board = m.get("board", "")
        if board.startswith(FULL_BOARD_PREFIXES) and board in ok_boards:
            m["missing_runs"] = 0 if r["id"] in seen_ids else m.get("missing_runs", 0) + 1
        miss = m.get("missing_runs", 0)
        want = "Active (API-verified)"
        if miss >= life["closed_after_missing_runs"]:
            want = "Closed / Expired"
        elif miss >= life["possibly_closed_after_missing_runs"]:
            want = "Possibly Closed"
        elif not board.startswith(FULL_BOARD_PREFIXES):
            ref = m.get("last_seen") or m.get("first_seen")
            if ref and (today - dt.date.fromisoformat(ref)).days >= life["aggregator_possibly_closed_after_days"]:
                want = "Possibly Closed"
        cur = r.get("lstatus")
        if cur == m.get("pipeline_lstatus") and cur != want:      # user hasn't overridden it -> pipeline may update
            r["lstatus"] = want
            m["pipeline_lstatus"] = want
            changed = True
            n_pc += want == "Possibly Closed"
            n_closed += want == "Closed / Expired"
            if want == "Closed / Expired":
                m["closed_since"] = today.isoformat()
        ls = m.get("last_seen")
        if ls and str(r.get("verified") or "")[:10] != ls:
            r["verified"] = dt.date.fromisoformat(ls)
            changed = True
        untouched = r.get("status") in PRE_APPLY and not r.get("applied")
        cs = m.get("closed_since")
        if (r.get("lstatus") == "Closed / Expired" and untouched and cs and
                (today - dt.date.fromisoformat(cs)).days >= life["archive_untouched_closed_after_days"]):
            m["removed"], m["archived_on"] = True, today.isoformat()
            archived.append(r["id"])
            changed = True
            continue
        kept.append(r)

    rows_out = kept + new_rows
    db["max_id"] = max([id_num(i) for i in jobs_db] + [db.get("max_id", 0)])
    failed = [f"{n} ({e})" for n, ok, _, e in health if not ok]
    run_entry = {"ts": now.strftime("%Y-%m-%d %H:%M"), "sources_ok": len(ok_boards), "sources_failed": len(failed),
                 "fetched": len(raw), "relevant": relevant, "added": len(new_rows), "possibly_closed": n_pc,
                 "closed": n_closed, "archived": len(archived), "restored": len(restored), "new_ids": new_ids, "failed": [n for n, ok, _, _ in health if not ok]}

    # 6) rebuild only when the pipeline changed something
    if changed:
        db["runs"] = (db.get("runs", []) + [run_entry])[-300:]
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / "rows.json").write_text(json.dumps(to_jsonable(rows_out), ensure_ascii=False), encoding="utf-8")
            (td / "state.json").write_text(json.dumps({"cells": cells}, ensure_ascii=False, default=str), encoding="utf-8")
            (td / "runs.json").write_text(json.dumps(db["runs"], ensure_ascii=False), encoding="utf-8")
            out_tmp = td / "out.xlsx"
            res = subprocess.run([sys.executable, str(ROOT / "build" / "build.py"), str(out_tmp), "--rows", str(td / "rows.json"),
                                  "--state", str(td / "state.json"), "--runs", str(td / "runs.json")],
                                 capture_output=True, text=True, cwd=str(ROOT / "build"))
            if res.returncode != 0:
                print(res.stdout, res.stderr)
                raise SystemExit("workbook build failed - original workbook left untouched")
            # safety net: the rebuilt file must contain every row we meant to write
            check = wbstate.read_workbook(out_tmp)
            if {r["id"] for r in check["rows"]} != {r["id"] for r in rows_out}:
                raise SystemExit("row check failed after rebuild - original workbook left untouched")
            out_tmp.replace(wb_path)
        db["schema_version"] = SCHEMA_VERSION
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db_path.write_text(json.dumps(db, indent=1, ensure_ascii=False, sort_keys=True), encoding="utf-8")

    # 7) summary
    lines = [f"## Job tracker refresh - {run_entry['ts']} UTC", "",
             f"**Workbook {'updated' if changed else 'unchanged'}** · fetched {len(raw)} postings from {len(ok_boards)} sources · "
             f"{relevant} passed filters · **{len(new_rows)} added** · {n_pc} possibly closed · {n_closed} closed · {len(archived)} archived"
             + (f" · {len(restored)} restored (workbook copy was older than the last run)" if restored else ""), ""]
    if new_rows:
        lines += ["| Job ID | Pri | Title | Company | Location | Match | Link |", "|---|---|---|---|---|---|---|"]
        for (match, row, _, _) in chosen:
            lines.append(f"| {row['id']} | {row['pri']} | {row['title']} | {row['company']} | {row['location'][:40]} | {match:.0%} | [open]({row['url']}) |")
        lines.append("")
    if reasons:
        lines.append("Filtered out: " + ", ".join(f"{k} {v}" for k, v in sorted(reasons.items(), key=lambda x: -x[1])))
        lines.append("")
    lines += ["<details><summary>Source health</summary>", "", "| Source | OK | Jobs | Error |", "|---|---|---|---|"]
    for n, ok, cnt, e in health:
        lines.append(f"| {n} | {'yes' if ok else 'no'} | {cnt} | {e} |")
    lines += ["", "</details>"]
    summary = "\n".join(lines)
    if args.summary:
        Path(args.summary).write_text(summary, encoding="utf-8")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as fh:
            fh.write(summary + "\n")
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as fh:
            fh.write(f"changed={'true' if changed else 'false'}\nadded={len(new_rows)}\n")
    print(summary)
    return changed, run_entry


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workbook", default=str(ROOT / "Global_Job_Hunt_Tracker.xlsx"))
    ap.add_argument("--db", default=str(ROOT / "data" / "jobs_db.json"))
    ap.add_argument("--config", default=str(HERE / "config.yaml"))
    ap.add_argument("--fixtures", help="offline mode: directory of saved API responses")
    ap.add_argument("--today", help="override today's date (YYYY-MM-DD), for tests")
    ap.add_argument("--summary", help="also write the markdown summary to this file")
    ap.add_argument("--init-only", action="store_true", help="only record the current workbook rows in the job memory")
    run(ap.parse_args())


if __name__ == "__main__":
    main()
