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

## Regenerate
`build/` contains the generator (`python build.py out.xlsx`, needs `openpyxl`). The research data is in `jobs_data.py` and the reference data in `ref_data.py`.
