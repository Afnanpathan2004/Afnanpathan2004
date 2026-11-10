"""Master Job Tracker column schema, shared by build.py and the hourly pipeline."""

SCHEMA_VERSION = 2

MC = [  # header, key, width, is_formula
 ("Job ID", "id", 10, False), ("Priority", "pri", 8, False), ("Job Title", "title", 38, False),
 ("Job Category", "cat", 22, False), ("Company", "company", 24, False), ("Company Website", "website", 24, False),
 ("Job Application URL", "url", 40, False), ("Job Source", "source", 22, False), ("Location", "location", 24, False),
 ("Country", "country", 13, False), ("Location Group", "locgroup", 20, False), ("Work Mode", "mode", 10, False),
 ("Experience Required", "exp", 22, False), ("Min Experience Yrs", "minexp", 10, False), ("Job Level", "level", 18, False),
 ("Employment Type", "emp", 14, False), ("Salary Range", "salary", 22, False), ("Currency", "cur", 9, False),
 ("Visa Sponsorship", "visa", 14, False), ("Relocation Assistance", "reloc", 12, False),
 ("Remote Eligibility for India", "remote_india", 18, False), ("Required Education", "edu", 24, False),
 ("Education Eligible", "edu_ok", 11, False), ("Required Skills", "req", 34, False), ("Preferred Skills", "pref", 24, False),
 ("Programming Languages", "langs", 18, False), ("Cloud Platforms", "clouds", 14, False),
 ("Tools and Technologies", "tools", 22, False), ("Certifications", "certs", 16, False),
 ("Experience Requirements", "expdetail", 40, False), ("Hard Eligibility Restrictions", "hard", 26, False),
 ("Location Work Auth Fit", "locfit", 26, False), ("Application Deadline", "deadline", 12, False),
 ("Date Posted", "posted", 12, False), ("Date Discovered", "disc", 12, False), ("Date Verified", "verified", 12, False),
 ("Data Confidence", "conf", 11, False), ("Listing Status", "lstatus", 18, False),
 ("Application Status", "status", 18, False), ("Date Applied", "applied", 12, False),
 ("Recruiter Name", "rname", 16, False), ("Recruiter LinkedIn", "rlink", 18, False),
 ("Interview Status", "istatus", 18, True), ("Next Interview Date", "nextint", 12, True),
 ("Follow-up Date", "fup", 12, False), ("Expected Salary", "expsal", 12, False), ("Resume Version", "resume", 12, False),
 ("Cover Letter", "cover", 9, False), ("Job Description", "jd", 44, False),
 ("Tech Skills Score", "s_tech", 9, True), ("Experience Score", "s_exp", 9, True), ("Education Score", "s_edu", 9, True),
 ("Location Score", "s_loc", 9, True), ("Preferred Skills Score", "s_pref", 9, True), ("Certification Score", "s_cert", 9, True),
 ("Match Percentage", "match", 10, True), ("Match Band", "band", 16, True), ("Missing Skills", "missing", 30, True),
 ("Requirement Types", "reqtype", 40, False), ("Active Flag", "active", 12, True), ("Duplicate Check", "dup", 14, True),
 ("Pipeline Stage", "stage", 14, True), ("Pipeline Key", "pkey", 12, True), ("First Interview Date", "firstint", 12, True),
 ("Offer Date", "offer", 12, False), ("Days to Interview", "d_int", 10, True), ("Days to Offer", "d_off", 10, True),
 ("Apply Score", "ascore", 9, True), ("Apply Rank", "arank", 8, True), ("Search Flag", "sflag", 8, True),
 ("Search Rank", "srank", 8, True), ("Notes", "notes", 44, False),
]
