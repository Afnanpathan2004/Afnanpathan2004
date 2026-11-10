# Global Job Hunting, Recruitment & Interview Tracker

**File:** [`Global_Job_Hunt_Tracker.xlsx`](Global_Job_Hunt_Tracker.xlsx). It is a personal recruitment CRM and career-intelligence dashboard. Research pass: **10 Nov 2026**.

## What's inside (15 sheets)
| Sheet | Purpose |
|---|---|
| README | How to use the workbook, how scoring works, colour legend, data-quality rules |
| Dashboard | 10 application KPIs, 10 performance rates, category and location breakdowns, the 5 key questions, 6 charts |
| Master Job Tracker | `tblJobs`: 84 researched listings and room for 600 rows; 72 columns incl. the automatic match score |
| Job Search | Keyword and filter search over the master table, ranked by Match % |
| Interview Tracker | One row per round; feeds interview status and dates back into the master |
| Skills & Requirements Matrix | Skill × category demand counted live from listings, your gap, learning priority, resources and certifications |
| Company Database | 40 companies: careers pages, fresher/intern/remote/visa notes, live job and application counts |
| Application Pipeline | Kanban with 11 stages plus "Inactive"; counts and job cards are automatic |
| Daily Job Hunting Log | Daily inputs with automatic weekly and monthly summaries |
| Job Description Analysis | 15 shortlisted roles: requirements, likely interview topics, ATS keywords, missing skills, prep checklist |
| Follow-up & Reminders | Next follow-up defaults to last contact + 7 days; overdue rows turn red |
| Research Sources / Research Summary | Provenance per listing, platforms searched, findings, priorities, limitations |
| My Profile | Your skills (pre-filled from this repo's profile README), scoring weights and settings |

## Research summary (live numbers are in the workbook)
- **84 listings** captured, all with source URLs: **82 not expired**. Of those, 66 are "Active" and 16 are "Verify" (older postings). **2** are expired or closed and excluded from active counts.
- **By category:** Cloud & DevOps 42 · Data 7 · AI Engineering 9 · Software 18 · Cybersecurity 8.
- **Fresher-friendly** (internship, apprenticeship, graduate or entry-level, active): **61**.
- **Remote:** 11 in total, 7 confirmed open to India-based applicants. **International:** 15 (Germany 6, UAE 2, NL/UK/Singapore 7).
- **Explicit employer-stated visa sponsorship:** 3 (HomeToGo Berlin, which may already be filled; Softwire UK 2027 graduate scheme; Swisscom NL, which has expired).
- **Most-required skills:** Linux (31), Python (29), cloud fundamentals (23), CI/CD (18), Networking (17), Docker (10), SQL (9), DSA (9), OOP (9).
- **Top hiring companies in the sample:** Amazon/AWS, Cisco, Nutanix, Microsoft, SAP, Cloudflare, MongoDB, Zoho.
- **Biggest gaps vs. your profile (demand-weighted):** SQL, DSA, Kubernetes, Monitoring/Observability, Azure.
- **Apply first:** Nutanix Associate DevOps (JOB-0002, closes 23 Nov), CME Group SRE I (JOB-0003), AWS Cloud Support Associate (JOB-0001), MongoDB Associate TSE I (JOB-0022), Ecolibrium Junior Platform Engineer (JOB-0009).

## Limitations
- The research environment's network policy blocked direct access to job boards and careers APIs. Listings were captured from search-engine indexes, so **no row is marked High confidence** (39 Medium, 45 Low). Open each link and confirm it before applying.
- Salary, experience and visa fields are recorded only as the source stated them. Anything not stated is "Unknown" or "Not disclosed".
- Match % depends on the self-ratings in *My Profile*, which were inferred from the profile README. Correct them first.
- There are no PivotTables or slicers, because the file was generated and validated programmatically. Every metric is a live formula. You can add slicers in Excel through Table Design → Insert Slicer.


## Automatic hourly refresh (GitHub Actions)

The workflow `.github/workflows/job-tracker-refresh.yml` runs **every hour (at :17 UTC)** and can also be started by hand from the Actions tab (**Run workflow**).

```
public job APIs ──► filter ──► score (same Match % formula as the workbook) ──► top 25 new ──► merge with your edits ──► rebuild ──► recalc ──► commit
```

1. **Fetch** from every source in [`pipeline/config.yaml`](pipeline/config.yaml):
   - **Employer boards** (marked High confidence): Greenhouse, Lever, Ashby, SmartRecruiters and Workday careers boards for about 40 companies, plus Amazon Jobs.
   - **Remote and aggregator APIs** (marked Medium): Remotive, Remote OK, Himalayas, Jobicy and Arbeitnow.
   - **Optional, free API key needed:** Adzuna (India, UK, Germany, Netherlands, Singapore) and Jooble (India).
2. **Filter**:
   - Roles must match P1–P5; senior, staff, lead and manager titles are dropped.
   - Postings asking for more than 3 years of experience, or older than 21 days, are dropped.
   - Locations must be India, remote open to India, or Germany/UAE/Netherlands/Ireland/UK/Singapore.
   - Remote jobs restricted to other countries are dropped, as are relocation jobs that explicitly refuse visa sponsorship.
3. **Score**: skills, experience, visa and relocation details are extracted from the description, then scored against **My Profile**. Jobs below `min_match` (60%) are skipped. Of the rest, the best 25 per run are added, best match first, with P1 ahead on ties.
4. **Merge**: everything you typed is kept, on every sheet. For jobs the bot added, it only updates **Listing Status** and **Date Verified**, and it stops touching Listing Status once you set it yourself.
5. **Lifecycle**: if a job disappears from its employer's board, it becomes *Possibly Closed* after 3 runs and *Closed / Expired* after about a day. Closed jobs you never acted on are archived after 7 days. Jobs you delete are remembered and never re-added.
6. **Commit**: this happens only when something changed. Each change is logged on the **Pipeline Runs** sheet, and each run's summary (new jobs table and source health) appears on the Actions run page.

**Setup (one time):**
1. **Merge this branch into `main`.** GitHub only runs scheduled workflows on the default branch.
2. *(Optional, recommended for India coverage)* Add free API keys under **Settings → Secrets and variables → Actions**: `ADZUNA_APP_ID` and `ADZUNA_APP_KEY` (developer.adzuna.com), and `JOOBLE_API_KEY` (jooble.org/api/about).
3. Run the workflow once by hand, then open the run summary. Any board marked **no** in *Source health* has a wrong slug or the company changed ATS. Fix or remove it in `config.yaml`.

**Editing the workbook while the bot runs:**
- Pull, edit, commit and push as usual.
- If your push is rejected because the bot committed first: keep your file, run `git pull --no-rebase -X ours` (or re-download and redo the edit), then push. The next run puts back any jobs the bot had added that your copy didn't have yet. It tells "you deleted it" apart from "your copy was older" using the Pipeline Runs sheet.
- Before sorting the master table, paste the Job IDs as values first.

**Tuning:** edit `pipeline/config.yaml`. You can change `min_match`, `max_new_per_run`, `max_years_required` and `max_age_days`, the role patterns, the locations, and the companies.

**Limits:**
- LinkedIn, Naukri, Indeed and Glassdoor have no public jobs API and forbid scraping, so they are not fetched. Adzuna and Jooble cover the broad Indian market instead.
- The connectors were tested offline against saved API responses. The board slugs could not be checked live from the build environment, so the first run's *Source health* table is the real check.
- On a public repo, Actions minutes are free. On a private repo, hourly runs use roughly 1,000+ minutes a month.

## Development
```bash
cd job-hunt-tracker/pipeline
pip install -r requirements.txt
python -m unittest discover -s tests -v     # offline tests (11), no network needed
python refresh.py --help                    # --fixtures DIR for offline runs, --init-only, --today
python ../build/build.py out.xlsx           # regenerate the workbook from the seed research data
```
`build/schema.py` defines the master columns shared by the generator and the pipeline. `data/jobs_db.json` is the pipeline's memory of every job it has seen.
