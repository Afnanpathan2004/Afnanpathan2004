"""Job-source connectors. Each returns a list of RawJob; failures are isolated per board.

Only public, documented-or-public job APIs are used (company ATS boards and remote-job APIs).
LinkedIn, Naukri, Indeed and Glassdoor offer no public job API and forbid scraping, so they are
not fetched here - Adzuna/Jooble (free API keys) cover the broad Indian market instead.
"""
from __future__ import annotations

import datetime as dt
import html
import os
import re
from dataclasses import dataclass, field

import requests

UA = "job-hunt-tracker/1.0 (personal job search; contact via GitHub repo)"
TIMEOUT = 25


@dataclass
class RawJob:
    source: str                 # e.g. "Greenhouse API"
    source_kind: str            # "ats" (employer board) | "aggregator"
    board: str                  # board identity used for closure detection, e.g. "greenhouse:cloudflare"
    company: str
    title: str
    url: str
    location: str = ""
    remote: bool = False
    posted: dt.date | None = None
    description: str = ""
    employment_type: str = ""
    salary: str = ""
    currency: str = ""
    extra: dict = field(default_factory=dict)


class SourceError(Exception):
    pass


def _get(session, url, **kw):
    r = session.get(url, timeout=TIMEOUT, headers={"User-Agent": UA, "Accept": "application/json"}, **kw)
    if r.status_code != 200:
        raise SourceError(f"HTTP {r.status_code}")
    return r.json()


def _post(session, url, payload, **kw):
    r = session.post(url, json=payload, timeout=TIMEOUT,
                     headers={"User-Agent": UA, "Accept": "application/json", "Content-Type": "application/json"}, **kw)
    if r.status_code != 200:
        raise SourceError(f"HTTP {r.status_code}")
    return r.json()


_TAG = re.compile(r"<[^>]+>")


def strip_html(text: str | None) -> str:
    if not text:
        return ""
    text = html.unescape(text)          # Greenhouse double-encodes HTML
    text = re.sub(r"(?i)<\s*(br|/p|/li|/h\d|/div)\s*/?>", "\n", text)
    text = _TAG.sub(" ", text)
    text = html.unescape(text)
    return re.sub(r"[ \t\r\f\v]+", " ", text).strip()


def parse_date(v) -> dt.date | None:
    if v in (None, "", 0):
        return None
    try:
        if isinstance(v, (int, float)):
            v = v / 1000 if v > 1e11 else v          # ms vs s epoch
            return dt.datetime.fromtimestamp(v, tz=dt.timezone.utc).date()
        s = str(v).strip()
        m = re.match(r"(\d{4}-\d{2}-\d{2})", s)
        if m:
            return dt.date.fromisoformat(m.group(1))
        for fmt in ("%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%a, %d %b %Y %H:%M:%S %z"):
            try:
                return dt.datetime.strptime(s, fmt).date()
            except ValueError:
                pass
        m = re.search(r"posted\s+(today|yesterday|(\d+)\+?\s+days?\s+ago)", s, re.I)   # Workday
        if m:
            today = dt.datetime.now(dt.timezone.utc).date()
            if m.group(1).lower() == "today":
                return today
            if m.group(1).lower() == "yesterday":
                return today - dt.timedelta(days=1)
            return today - dt.timedelta(days=int(m.group(2)))
    except Exception:
        return None
    return None


# ------------------------------------------------------------------ company ATS boards
def greenhouse(session, slug, company):
    data = _get(session, f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs", params={"content": "true"})
    out = []
    for j in data.get("jobs", []):
        loc = (j.get("location") or {}).get("name", "") or ""
        out.append(RawJob("Greenhouse API (official board)", "ats", f"greenhouse:{slug}", company,
                          (j.get("title") or "").strip(), j.get("absolute_url") or "", loc,
                          remote="remote" in loc.lower(),
                          posted=parse_date(j.get("first_published") or j.get("updated_at")),
                          description=strip_html(j.get("content"))))
    return out


def lever(session, slug, company):
    data = _get(session, f"https://api.lever.co/v0/postings/{slug}", params={"mode": "json"})
    out = []
    for j in data if isinstance(data, list) else []:
        cat = j.get("categories") or {}
        locs = cat.get("allLocations") or [cat.get("location") or ""]
        loc = "; ".join(x for x in locs if x)
        desc = " ".join(filter(None, [j.get("descriptionPlain"),
                                      " ".join(strip_html(x.get("content")) for x in j.get("lists") or []),
                                      j.get("additionalPlain")]))
        sal = j.get("salaryRange") or {}
        out.append(RawJob("Lever API (official board)", "ats", f"lever:{slug}", company,
                          (j.get("text") or "").strip(), j.get("hostedUrl") or "", loc,
                          remote=(j.get("workplaceType") == "remote") or "remote" in loc.lower(),
                          posted=parse_date(j.get("createdAt")), description=desc,
                          employment_type=cat.get("commitment") or "",
                          salary=f"{sal.get('min')} - {sal.get('max')}" if sal.get("min") else "",
                          currency=sal.get("currency") or ""))
    return out


def ashby(session, slug, company):
    data = _get(session, f"https://api.ashbyhq.com/posting-api/job-board/{slug}", params={"includeCompensation": "true"})
    out = []
    for j in data.get("jobs", []):
        if j.get("isListed") is False:
            continue
        locs = [j.get("location") or ""] + [(x.get("location") or "") for x in j.get("secondaryLocations") or []]
        loc = "; ".join(x for x in locs if x)
        comp = (j.get("compensation") or {}).get("compensationTierSummary") or ""
        out.append(RawJob("Ashby API (official board)", "ats", f"ashby:{slug}", company,
                          (j.get("title") or "").strip(), j.get("jobUrl") or j.get("applyUrl") or "", loc,
                          remote=bool(j.get("isRemote")) or j.get("workplaceType") == "Remote",
                          posted=parse_date(j.get("publishedAt")),
                          description=j.get("descriptionPlain") or strip_html(j.get("descriptionHtml")),
                          employment_type=j.get("employmentType") or "", salary=comp))
    return out


def smartrecruiters(session, company_id, company):
    out, offset = [], 0
    while offset < 500:
        data = _get(session, f"https://api.smartrecruiters.com/v1/companies/{company_id}/postings",
                    params={"limit": 100, "offset": offset})
        content = data.get("content", [])
        for j in content:
            loc = j.get("location") or {}
            loc_txt = ", ".join(x for x in [loc.get("city"), loc.get("region"), loc.get("country")] if x)
            out.append(RawJob("SmartRecruiters API (official board)", "ats", f"smartrecruiters:{company_id}", company,
                              (j.get("name") or "").strip(),
                              f"https://jobs.smartrecruiters.com/{company_id}/{j.get('id')}", loc_txt,
                              remote=bool(loc.get("remote")), posted=parse_date(j.get("releasedDate")),
                              employment_type=((j.get("typeOfEmployment") or {}).get("label") or "")))
        offset += 100
        if len(content) < 100:
            break
    return out


WORKDAY_QUERIES = ["devops", "site reliability", "cloud", "data analyst", "data engineer", "machine learning",
                   "software engineer", "security"]


def workday(session, cfg):
    host, tenant, site, company = cfg["host"], cfg["tenant"], cfg["site"], cfg["company"]
    out, seen = [], set()
    for q in cfg.get("queries", WORKDAY_QUERIES):
        data = _post(session, f"https://{host}/wday/cxs/{tenant}/{site}/jobs",
                     {"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": q})
        for j in data.get("jobPostings", []):
            path = j.get("externalPath") or ""
            if not path or path in seen:
                continue
            seen.add(path)
            out.append(RawJob("Workday careers API (official)", "ats", f"workday:{tenant}:{q}", company,
                              (j.get("title") or "").strip(), f"https://{host}/en-US/{site}{path}",
                              j.get("locationsText") or "", posted=parse_date(j.get("postedOn"))))
    return out


def amazon(session, cfg):
    out, seen = [], set()
    for loc in cfg.get("locations", ["India"]):
        for q in cfg.get("queries", []):
            data = _get(session, "https://www.amazon.jobs/en/search.json",
                        params={"base_query": q, "loc_query": loc, "result_limit": 50, "sort": "recent"})
            for j in data.get("jobs", []):
                path = j.get("job_path") or ""
                if not path or path in seen:
                    continue
                seen.add(path)
                desc = " ".join(filter(None, [strip_html(j.get("description")), strip_html(j.get("basic_qualifications")),
                                              "Preferred qualifications: " + strip_html(j.get("preferred_qualifications") or "")]))
                out.append(RawJob("Amazon Jobs API (official)", "ats", f"amazon:{q}:{loc}", "Amazon",
                                  (j.get("title") or "").strip(), "https://www.amazon.jobs" + path,
                                  j.get("normalized_location") or j.get("location") or "",
                                  posted=parse_date(j.get("posted_date")), description=desc))
    return out


# ------------------------------------------------------------------ aggregators / remote boards
def remotive(session, cfg):
    out = []
    for cat in cfg.get("categories", []):
        data = _get(session, "https://remotive.com/api/remote-jobs", params={"category": cat, "limit": 200})
        for j in data.get("jobs", []):
            out.append(RawJob("Remotive API", "aggregator", "remotive", j.get("company_name") or "",
                              (j.get("title") or "").strip(), j.get("url") or "",
                              "Remote - " + (j.get("candidate_required_location") or "unspecified"), remote=True,
                              posted=parse_date(j.get("publication_date")), description=strip_html(j.get("description")),
                              employment_type=j.get("job_type") or "", salary=j.get("salary") or ""))
    return out


def remoteok(session, cfg):
    data = _get(session, "https://remoteok.com/api")
    out = []
    for j in data[1:] if isinstance(data, list) else []:       # element 0 is the legal notice
        sal = f"{j.get('salary_min')} - {j.get('salary_max')}" if j.get("salary_min") else ""
        out.append(RawJob("Remote OK API", "aggregator", "remoteok", j.get("company") or "",
                          (j.get("position") or "").strip(), j.get("url") or "",
                          "Remote - " + (j.get("location") or "unspecified"), remote=True,
                          posted=parse_date(j.get("date") or j.get("epoch")),
                          description=strip_html(j.get("description")) + " " + " ".join(j.get("tags") or []),
                          salary=sal, currency="USD" if sal else ""))
    return out


def himalayas(session, cfg):
    out = []
    for p in range(cfg.get("pages", 3)):
        data = _get(session, "https://himalayas.app/jobs/api", params={"limit": 100, "offset": p * 100})
        for j in data.get("jobs", []):
            restr = j.get("locationRestrictions") or []
            loc = "Remote - " + (", ".join(restr) if restr else "worldwide")
            sal = f"{j.get('minSalary')} - {j.get('maxSalary')}" if j.get("minSalary") else ""
            out.append(RawJob("Himalayas API", "aggregator", "himalayas", j.get("companyName") or "",
                              (j.get("title") or "").strip(), j.get("applicationLink") or j.get("guid") or "", loc,
                              remote=True, posted=parse_date(j.get("pubDate")),
                              description=strip_html(j.get("description") or j.get("excerpt")),
                              employment_type=j.get("employmentType") or "", salary=sal,
                              currency=j.get("currency") or ""))
    return out


def jobicy(session, cfg):
    out = []
    for tag in cfg.get("tags", []):
        data = _get(session, "https://jobicy.com/api/v2/remote-jobs", params={"count": 50, "tag": tag})
        for j in data.get("jobs", []):
            out.append(RawJob("Jobicy API", "aggregator", "jobicy", j.get("companyName") or "",
                              html.unescape(j.get("jobTitle") or "").strip(), j.get("url") or "",
                              "Remote - " + (j.get("jobGeo") or "unspecified"), remote=True,
                              posted=parse_date(j.get("pubDate")), description=strip_html(j.get("jobDescription")),
                              employment_type=", ".join(j.get("jobType") or []) if isinstance(j.get("jobType"), list) else (j.get("jobType") or "")))
    return out


def arbeitnow(session, cfg):
    out = []
    for p in range(1, cfg.get("pages", 3) + 1):
        data = _get(session, "https://www.arbeitnow.com/api/job-board-api", params={"page": p})
        for j in data.get("data", []):
            desc = strip_html(j.get("description")) + (" visa sponsorship available" if j.get("visa_sponsorship") else "")
            out.append(RawJob("Arbeitnow API", "aggregator", "arbeitnow", j.get("company_name") or "",
                              (j.get("title") or "").strip(), j.get("url") or "", j.get("location") or "",
                              remote=bool(j.get("remote")), posted=parse_date(j.get("created_at")), description=desc,
                              employment_type=", ".join(j.get("job_types") or [])))
    return out


def adzuna(session, cfg):
    app_id, key = os.environ.get("ADZUNA_APP_ID"), os.environ.get("ADZUNA_APP_KEY")
    if not (app_id and key):
        raise SourceError("skipped: ADZUNA_APP_ID / ADZUNA_APP_KEY secrets not set")
    out = []
    for c in cfg.get("countries", ["in"]):
        for q in cfg.get("queries", []):
            data = _get(session, f"https://api.adzuna.com/v1/api/jobs/{c}/search/1",
                        params={"app_id": app_id, "app_key": key, "what": q, "results_per_page": 50, "max_days_old": 7,
                                "content-type": "application/json"})
            for j in data.get("results", []):
                sal = f"{int(j['salary_min'])} - {int(j.get('salary_max') or j['salary_min'])}" \
                    if j.get("salary_min") and str(j.get("salary_is_predicted")) != "1" else ""
                out.append(RawJob("Adzuna API", "aggregator", f"adzuna:{c}", (j.get("company") or {}).get("display_name") or "",
                                  strip_html(j.get("title")), j.get("redirect_url") or "",
                                  (j.get("location") or {}).get("display_name") or c.upper(),
                                  posted=parse_date(j.get("created")), description=strip_html(j.get("description")),
                                  employment_type=j.get("contract_time") or "", salary=sal))
    return out


def jooble(session, cfg):
    key = os.environ.get("JOOBLE_API_KEY")
    if not key:
        raise SourceError("skipped: JOOBLE_API_KEY secret not set")
    out = []
    for q in cfg.get("queries", []):
        data = _post(session, f"https://jooble.org/api/{key}", {"keywords": q, "location": cfg.get("location", "India")})
        for j in data.get("jobs", []):
            out.append(RawJob("Jooble API", "aggregator", "jooble", j.get("company") or "", strip_html(j.get("title")),
                              j.get("link") or "", j.get("location") or "", posted=parse_date(j.get("updated")),
                              description=strip_html(j.get("snippet")), employment_type=j.get("type") or "",
                              salary=j.get("salary") or ""))
    return out


def fetch_all(cfg, session=None):
    """Run every configured source. Returns (jobs, health) where health = [(source_name, ok, count, error)]."""
    session = session or requests.Session()
    src = cfg.get("sources", {})
    tasks = []
    for slug, name in (src.get("greenhouse") or {}).items():
        tasks.append((f"greenhouse:{slug}", lambda s=slug, n=name: greenhouse(session, s, n)))
    for slug, name in (src.get("lever") or {}).items():
        tasks.append((f"lever:{slug}", lambda s=slug, n=name: lever(session, s, n)))
    for slug, name in (src.get("ashby") or {}).items():
        tasks.append((f"ashby:{slug}", lambda s=slug, n=name: ashby(session, s, n)))
    for cid, name in (src.get("smartrecruiters") or {}).items():
        tasks.append((f"smartrecruiters:{cid}", lambda s=cid, n=name: smartrecruiters(session, s, n)))
    for w in src.get("workday") or []:
        tasks.append((f"workday:{w['tenant']}", lambda w=w: workday(session, w)))
    simple = {"amazon": amazon, "remotive": remotive, "remoteok": remoteok, "himalayas": himalayas,
              "jobicy": jobicy, "arbeitnow": arbeitnow}
    for name, fn in simple.items():
        c = src.get(name) or {}
        if c.get("enabled"):
            tasks.append((name, lambda fn=fn, c=c: fn(session, c)))
    for name, fn in (("adzuna", adzuna), ("jooble", jooble)):
        if src.get(name):
            tasks.append((name, lambda fn=fn, c=src[name]: fn(session, c)))

    jobs, health = [], []
    for name, task in tasks:
        try:
            got = task()
            jobs.extend(got)
            health.append((name, True, len(got), ""))
        except Exception as e:  # one broken board never stops the run
            health.append((name, False, 0, f"{type(e).__name__}: {e}"[:160]))
    return jobs, health
