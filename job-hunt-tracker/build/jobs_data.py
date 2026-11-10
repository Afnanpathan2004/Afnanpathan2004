# Research dataset compiled 2026-11-10 from web-search results.
# Every row cites the URL it was found at. Nothing below is invented:
# where a listing did not state a value, the field says "Unknown" / "Not disclosed".
# Skill tokens use the canonical names in the My Profile skill list so formulas can match them.

C1, C2, C3, C4, C5 = ("Cloud & DevOps", "Data Analytics & Data Science", "AI Engineering",
                      "Software Development", "Cybersecurity")

# Location fit values (scored on My Profile)
IN_OK = "Eligible - India-based role"
REM_OK = "Eligible - Remote open to India"
SPON = "Sponsorship explicitly offered"
SPON_UNK = "Sponsorship unknown"
NOT_OK = "Not eligible - restricted"

FIELDS = ["id", "pri", "title", "cat", "company", "website", "url", "source", "location", "country",
          "locgroup", "mode", "exp", "minexp", "level", "emp", "salary", "cur", "visa", "reloc",
          "remote_india", "edu", "req", "pref", "langs", "clouds", "tools", "certs", "expdetail",
          "hard", "locfit", "deadline", "posted", "conf", "lstatus", "jd", "reqtype", "notes"]

J = []
def add(**k):
    for f in FIELDS:
        k.setdefault(f, "")
    J.append(k)

V_IDX = "Search-indexed listing; page not opened (proxy blocked) - re-verify before applying"

# ------------------------------------------------------------------ P1 CLOUD & DEVOPS (INDIA)
add(id="JOB-0001", pri="P1", title="Cloud Support Associate", cat=C1, company="Amazon Web Services (AWS)",
    website="https://aws.amazon.com", url="https://amazon.jobs/en/jobs/2866105/cloud-support-associate",
    source="Company Careers (amazon.jobs)", location="Hyderabad / Bengaluru (varies by req)", country="India",
    locgroup="India", mode="On-site", exp="0-1 years (per aggregator)", minexp=0, level="Entry-Level",
    emp="Full-time", salary="Not disclosed", cur="INR", visa="Not required (India)", reloc="Unknown",
    remote_india="N/A (on-site)", edu="Bachelor's degree (per listing family) - verify",
    req="Troubleshooting, Communication, Linux, Networking, Databases",
    pref="AWS, Python, Bash", langs="Python, Bash (preferred)", clouds="AWS",
    tools="TCP/IP, DNS, Linux", certs="None stated",
    expdetail="Troubleshooting or support experience; basic Linux/Unix, TCP/IP, DNS and databases preferred.",
    hard="Shift-based: some reqs 7PM-4AM or 11PM-8AM IST", locfit=IN_OK, posted="", conf="Medium",
    lstatus="Active (search-verified)",
    jd="Resolve AWS customer cases via phone/email/chat; reproduce issues with internal teams.",
    reqtype="Mandatory: troubleshooting, communication. Preferred: Linux, networking, DB basics. Trainable: AWS services. Hard: night shifts on some reqs.",
    notes="Other India reqs seen in search: 2831370, 2831357, 2831384, 2850436, 2815273. Pick the one matching your city/shift.")

add(id="JOB-0002", pri="P1", title="Associate DevOps & Cloud Engineer", cat=C1, company="Nutanix",
    website="https://www.nutanix.com", url="https://in.indeed.com/q-devops-engineer-roles-with-0-2-years-jobs.html",
    source="Indeed India", location="Pune", country="India", locgroup="India", mode="Unknown",
    exp="Fresher / 0-1 years", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Linux, Docker, CI/CD, Cloud", pref="Kubernetes, Python", langs="Unknown", clouds="Unknown",
    tools="Docker, CI/CD", certs="None stated", expdetail="Listed on job board as Fresher / 0-1 years.",
    hard="None stated", locfit=IN_OK, deadline="2026-11-23", posted="2026-08-19", conf="Low",
    lstatus="Active (search-verified)", jd="Associate-level DevOps/cloud role at Nutanix Pune (valid-through 23 Nov 2026 per structured data).",
    reqtype="Skills inferred from job-board tags only - open the JD.",
    notes="Direct link not captured - search the title on Indeed or nutanix.com/company/careers. Deadline soon.")

add(id="JOB-0003", pri="P1", title="Site Reliability Engineer I - India", cat=C1, company="CME Group",
    website="https://www.cmegroup.com", url="https://builtin.com/job/site-reliability-engineer-i-india/7826214",
    source="Built In", location="Bengaluru (Bagmane Tridib)", country="India", locgroup="India", mode="On-site",
    exp="0-1 years (2025/2026 graduates)", minexp=0, level="Entry-Level", emp="Full-time",
    salary="Not disclosed by employer (aggregators conflict: 8-12 / 15-20 LPA)", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Degree (CS/related) - verify",
    req="Python, Bash, Linux, Monitoring, Observability", pref="AWS, GCP, Azure, Docker, Kubernetes",
    langs="Python, Java, C++ or Bash", clouds="GCP, AWS, Azure (familiarity)", tools="Docker, Kubernetes",
    certs="None stated",
    expdetail="Foundational scripting via coursework/projects/internships; shadow senior SREs on observability, monitoring and alerting.",
    hard="None stated", locfit=IN_OK, posted="2026-10-23", conf="Medium", lstatus="Active (search-verified)",
    jd="Build observability, monitoring and alerting for trading/clearing platform services; learn from senior SREs.",
    reqtype="Mandatory: scripting + Linux. Preferred: cloud, Docker/K8s. Trainable: observability stack.",
    notes="Strong fresher fit for P1. Also on foundit.in and talentd.in mirrors.")

add(id="JOB-0004", pri="P1", title="Site Reliability Engineer I", cat=C1, company="PAR Technology",
    website="https://partech.com",
    url="https://jobfound.org/job/par-technology-is-hiring-for-site-reliability-engineer-i-gurugram-haryana-india-india-17-october-2026",
    source="JobFound (aggregator)", location="Gurugram / Jaipur", country="India", locgroup="India", mode="Hybrid",
    exp="2-4 years", minexp=2, level="Early-Career (1-3 yrs)", emp="Full-time", salary="8-12 LPA (aggregator)", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Monitoring, Observability, SRE, Linux", pref="Prometheus, Grafana", langs="Unknown", clouds="Unknown",
    tools="SLIs/SLOs tooling", certs="None stated", expdetail="About 2-4 years; focus on SLIs/SLOs and observability.",
    hard="None stated", locfit=IN_OK, posted="2026-10-17", conf="Low", lstatus="Active (search-verified)",
    jd="SRE role focused on monitoring, SLIs/SLOs and observability.",
    reqtype="Experience gap is the main blocker; apply as stretch only.", notes="Stretch role (2+ yrs).")

add(id="JOB-0005", pri="P1", title="Associate Cloud Engineer (Fresher) - AWS / Azure", cat=C1, company="Inspired Infotech",
    website="https://inspiredinfotech.com", url="https://inspiredinfotech.com/jobs/associate-cloud-engineer-fresher-hyderabad.html",
    source="Company Careers", location="Hyderabad", country="India", locgroup="India", mode="Unknown",
    exp="Fresher", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Bachelor's degree",
    req="AWS, Azure, Linux, Networking", pref="", langs="Unknown", clouds="AWS, Azure", tools="Unknown",
    certs="None stated", expdetail="Fresher; bachelor's degree; must be eligible to work in India.",
    hard="Must be eligible to work in India", locfit=IN_OK, posted="2026-10-09", conf="Low", lstatus="Active (search-verified)",
    jd="Associate cloud engineer track for freshers on AWS/Azure.",
    reqtype="Low-information listing from a small firm - check company legitimacy before sharing documents.",
    notes="Never pay any 'training fee' to get hired.")

add(id="JOB-0006", pri="P1", title="Monitoring / NOC - Associate Engineer", cat=C1, company="Credera",
    website="https://www.credera.com", url="https://offcampusjobs4u.com/credera-recruitment-2026-noc-associate-engineer-hyderabad/",
    source="OffCampusJobs4u (aggregator)", location="Hyderabad", country="India", locgroup="India", mode="On-site",
    exp="Fresher to 2 years", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="B.E/B.Tech in CS, IT or related",
    req="Monitoring, Networking, Linux, Incident Management", pref="", langs="Unknown", clouds="Unknown",
    tools="Monitoring tools", certs="None stated", expdetail="Freshers to 2 years; B.E/B.Tech CS/IT.",
    hard="Likely rotational shifts (NOC) - verify", locfit=IN_OK, posted="", conf="Low", lstatus="Active (search-verified)",
    jd="Monitoring/NOC associate at Credera's Hyderabad technology delivery center.",
    reqtype="Mandatory: degree. Trainable: monitoring tools.", notes="No deadline shown.")

add(id="JOB-0007", pri="P1", title="Associate Engineer I (NOC)", cat=C1, company="CBTS India",
    website="https://www.cbts.com", url="https://ats.rippling.com/cbtsindia/jobs/863bd6a1-96f0-49de-a6a2-f42164fdc3a0",
    source="Company ATS (Rippling)", location="Chennai", country="India", locgroup="India", mode="On-site",
    exp="Fresher", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Networking, Monitoring, Troubleshooting", pref="Linux", langs="Unknown", clouds="Unknown", tools="Unknown",
    certs="None stated", expdetail="Hiring freshers for NOC role; work from office 5 days.", hard="5 days WFO",
    locfit=IN_OK, posted="", conf="Medium", lstatus="Active (search-verified)",
    jd="NOC fresher role; applications also accepted by email to recruiter (per listing).", reqtype="", notes="")

add(id="JOB-0008", pri="P1", title="Graduate Engineer, Operations (NOC L1)", cat=C1, company="Mavenir",
    website="https://www.mavenir.com", url="https://freshershunt.in/mavenir-off-campus-drive-2026/",
    source="FreshersHunt (aggregator)", location="Bengaluru", country="India", locgroup="India", mode="On-site",
    exp="Fresher", minexp=0, level="Graduate Program", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Networking, Monitoring, Linux", pref="", langs="", clouds="", tools="", certs="None stated",
    expdetail="NOC L1 in a 24x7 Network Operations Centre.", hard="24x7 shifts", locfit=IN_OK,
    deadline="2026-09-20", posted="", conf="Low", lstatus="Closed / Expired",
    jd="NOC L1 graduate role.", reqtype="", notes="EXPIRED - kept for tracking; excluded from active counts.")

add(id="JOB-0009", pri="P1", title="Junior Platform Engineer", cat=C1, company="Ecolibrium",
    website="", url="https://employmenthero.com/jobs/position/ecolibrium-junior-platform-engineer-v4wkm/",
    source="Employment Hero (company ATS)", location="Bengaluru", country="India", locgroup="India", mode="Unknown",
    exp="0-2 years", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Python, Linux, Cloud", pref="Networking", langs="Python", clouds="Unknown", tools="IoT platform",
    certs="None stated", expdetail="0-2 years in a technical role related to IoT or platform engineering; Python for scripting/automation.",
    hard="None stated", locfit=IN_OK, posted="", conf="Medium", lstatus="Active (search-verified)",
    jd="Hardware-to-cloud side of the SmartSense IoT platform.", reqtype="", notes="")

add(id="JOB-0010", pri="P1", title="Platform Engineer L1", cat=C1, company="Wipro",
    website="https://www.wipro.com", url="https://careers.wipro.com/job/Platform-Engineer-L1/182562-en_US/",
    source="Company Careers", location="Pune", country="India", locgroup="India", mode="Unknown",
    exp="Unknown (L1 = entry band)", minexp="", level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown", req="Unknown - open JD",
    pref="", langs="", clouds="", tools="", certs="None stated", expdetail="Start date 6/20/26 listed; Pan-India band.",
    hard="None stated", locfit=IN_OK, posted="2026-06-20", conf="Medium", lstatus="Possibly Closed",
    jd="Platform Engineer L1 (details not in search snippet).", reqtype="", notes="Posting from June - confirm it is still open.")

add(id="JOB-0011", pri="P1", title="Platform Engineer I", cat=C1, company="HCLTech",
    website="https://www.hcltech.com", url="https://careers.hcltech.com/job/Platform-Engineer-I/1358533355/",
    source="Company Careers", location="Bengaluru", country="India", locgroup="India", mode="Unknown",
    exp="Unknown", minexp="", level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown", req="Unknown - open JD",
    certs="None stated", hard="None stated", locfit=IN_OK, conf="Medium", lstatus="Active (search-verified)",
    jd="Platform Engineer I at HCLTech (cached page had little detail).", notes="")

add(id="JOB-0012", pri="P1", title="Platform Engineer (Junior/Senior)", cat=C1, company="Quantiphi",
    website="https://quantiphi.com", url="https://www.employbl.com/jobs/platform-engineer-Quantiphi-1728117",
    source="Employbl (aggregator)", location="Bengaluru", country="India", locgroup="India", mode="Unknown",
    exp="1-6 years", minexp=1, level="Early-Career (1-3 yrs)", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Kubernetes, Terraform, Cloud", pref="", certs="None stated", hard="None stated", locfit=IN_OK,
    posted="2026-09-15", conf="Low", lstatus="Active (search-verified)", jd="Platform role open at junior or senior level; updated Sep 2026.",
    notes="Posted date approximate (listing 'updated September 2026').")

add(id="JOB-0013", pri="P1", title="DevOps Engineer Associate", cat=C1, company="Heaptrace Technology",
    website="", url="https://in.indeed.com/q-devops-engineer-roles-with-0-2-years-jobs.html",
    source="Indeed India", location="Pune", country="India", locgroup="India", mode="Unknown",
    exp="0-2 years (freshers)", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="AWS, Linux, Docker, CI/CD", pref="", clouds="AWS", tools="Docker, CI/CD", certs="None stated",
    hard="None stated", locfit=IN_OK, conf="Low", lstatus="Active (search-verified)",
    jd="Associate DevOps role for freshers: AWS, Linux, Docker, CI/CD.", notes="Direct link not captured - search on Indeed.")

add(id="JOB-0014", pri="P1", title="Junior DevOps Engineer (Freshers)", cat=C1, company="Reizend",
    website="", url="https://in.indeed.com/q-devops-fresher-jobs.html",
    source="Indeed India", location="Thiruvananthapuram", country="India", locgroup="India", mode="On-site",
    exp="Fresher (2026 UG/PG, 2027 PG)", minexp=0, level="Entry-Level", emp="Full-time", salary="4-6 LPA", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="CS/IT or related; 2026 UG/PG or 2027 PG",
    req="Linux, CI/CD, Docker", pref="", certs="None stated", hard="Immediate joining required", locfit=IN_OK,
    conf="Low", lstatus="Active (search-verified)", jd="Fresher DevOps role; full-time, immediate engagement.",
    notes="Direct link not captured - search on Indeed.")

add(id="JOB-0015", pri="P1", title="DevOps Engineer I", cat=C1, company="Netomi",
    website="https://www.netomi.com", url="https://www.remoterocketship.com/country/india/jobs/junior-devops/",
    source="Remote Rocketship", location="India - Remote", country="India", locgroup="Remote - India Eligible", mode="Remote",
    exp="Junior (unspecified)", minexp="", level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="N/A", remote_india="Yes - India Remote", edu="Unknown", req="Unknown - open JD",
    certs="None stated", hard="None stated", locfit=REM_OK, conf="Low", lstatus="Active (search-verified)",
    jd="Junior-tagged DevOps Engineer I open to India-based remote candidates.", notes="")

add(id="JOB-0016", pri="P1", title="Junior DevOps Engineer", cat=C1, company="Alchemyst AI",
    website="", url="https://wellfound.com/role/r/devops-engineer",
    source="Wellfound", location="Remote - Everywhere", country="Remote", locgroup="Remote - India Eligible", mode="Remote",
    exp="~1 year", minexp=1, level="Early-Career (1-3 yrs)", emp="Full-time", salary="1.8L - 3L per year", cur="INR",
    visa="N/A (remote)", reloc="N/A", remote_india="Yes - Everywhere", edu="Unknown", req="Unknown - open JD",
    certs="None stated", hard="None stated", locfit=REM_OK, conf="Low", lstatus="Active (search-verified)",
    jd="Startup junior DevOps role, remote only.", notes="Low pay band. Direct link not captured - search on Wellfound.")

add(id="JOB-0017", pri="P1", title="Junior DevOps Engineer - Entry Level", cat=C1, company="Accenture",
    website="https://www.accenture.com",
    url="https://www.tryapplynow.com/jobs/accenture-junior-devops-engineer-entry-level-c92420ba-d47f-4f91-afaa-aeb77ea72f5a",
    source="TryApplyNow (aggregator)", location="Hyderabad", country="India", locgroup="India", mode="Hybrid",
    exp="Entry level", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown", req="CI/CD, Linux, Cloud",
    certs="None stated", hard="None stated", locfit=IN_OK, conf="Low", lstatus="Active (search-verified)",
    jd="Internship-style hybrid junior DevOps role with training (per aggregator).",
    notes="Confirm on accenture.com/in-en/careers before applying.")

add(id="JOB-0018", pri="P1", title="Consultant | Cloud DevOps | Engineering", cat=C1, company="Deloitte",
    website="https://www.deloitte.com",
    url="https://southasiacareers.deloitte.com/job/Bengaluru-Consultant-Cloud-DevOps-Bengaluru-Engineering/53378244",
    source="Company Careers", location="Bengaluru", country="India", locgroup="India", mode="Unknown",
    exp="1-4 years", minexp=1, level="Early-Career (1-3 yrs)", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown", req="CI/CD, Cloud, Docker, Kubernetes, Terraform",
    certs="None stated", hard="None stated", locfit=IN_OK, conf="Medium", lstatus="Active (search-verified)",
    jd="Cloud DevOps consultant, 1-4 years DevOps/cloud experience.", reqtype="Experience gap of 1 year.", notes="Stretch.")

add(id="JOB-0019", pri="P1", title="Associate DevOps Engineer (Sovereign Cloud)", cat=C1, company="SAP",
    website="https://www.sap.com",
    url="https://flexa.careers/jobs/sap-associate-devops-engineer-jenkins-concourse-landscaper-blr-ggn-sovereign-cloud-690c17ab537f80f281f078f8",
    source="Flexa (aggregator of jobs.sap.com)", location="Bengaluru / Gurugram", country="India", locgroup="India", mode="Unknown",
    exp="Graduates", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Graduate", req="Jenkins, CI/CD, Kubernetes, Linux",
    pref="", tools="Jenkins, Concourse, Landscaper", certs="None stated", hard="Sovereign-cloud roles may need security clearance - verify",
    locfit=IN_OK, posted="2025-11-12", conf="Low", lstatus="Possibly Closed",
    jd="Associate DevOps supporting SAP Sovereign Cloud landscape.", notes="Posted Nov 2025 - likely closed; re-check jobs.sap.com for a new req.")

add(id="JOB-0020", pri="P1", title="Associate Engineer - SAP Basis, S/4HANA Public Cloud (1-3Y), Sovereign Cloud", cat=C1, company="SAP",
    website="https://www.sap.com",
    url="https://jobs.sap.com/job/Bangalore-Associate-Engineer-SAP-Basis%2C-S4HANA%2C-Public-Cloud-%28Ex-1-3Y%29-Sovereign-Cloud-560066/1266787101",
    source="Company Careers", location="Bengaluru", country="India", locgroup="India", mode="Unknown",
    exp="1-3 years", minexp=1, level="Early-Career (1-3 yrs)", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown", req="Linux, Cloud, Databases",
    certs="None stated", hard="None stated", locfit=IN_OK, conf="Medium", lstatus="Active (search-verified)",
    jd="SAP Basis operations on S/4HANA public cloud (Software-Development Operations).", notes="")

add(id="JOB-0021", pri="P1", title="Services Automation Engineer", cat=C1, company="Nutanix",
    website="https://www.nutanix.com", url="https://jobs.jobvite.com/nutanix/job/oAKUyfww",
    source="Company ATS (Jobvite)", location="Pune", country="India", locgroup="India", mode="Unknown",
    exp="Unknown", minexp="", level="Early-Career (1-3 yrs)", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Cloud, CI/CD, Python, Ansible, Terraform", certs="None stated", hard="None stated", locfit=IN_OK,
    conf="Medium", lstatus="Active (search-verified)",
    jd="Automation engineer with background in cloud infrastructure and DevOps practices.",
    notes="Posting date unknown. Skills partly inferred from Nutanix automation-team listings - open JD.")

add(id="JOB-0022", pri="P1", title="Associate TSE I (Cloud Technical Services Engineer)", cat=C1, company="MongoDB",
    website="https://www.mongodb.com", url="https://builtin.com/job/associate-tse-i/9680104",
    source="Built In", location="Bengaluru", country="India", locgroup="India", mode="Hybrid",
    exp="Associate (entry)", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Troubleshooting, Networking, NoSQL, Cloud, Communication", pref="Linux", clouds="MongoDB Atlas",
    certs="None stated", hard="Must be based in Bengaluru (hybrid)", locfit=IN_OK, posted="2026-07-31",
    conf="Medium", lstatus="Active (search-verified)",
    jd="Front line of cloud support: connectivity, Atlas availability, UI/platform questions.",
    notes="Your MongoDB experience is a plus here. Associate TSE II also open (Bengaluru, Gurugram).")

add(id="JOB-0023", pri="P1", title="Associate TSE I", cat=C1, company="MongoDB",
    website="https://www.mongodb.com", url="https://swooped.co/job-postings/associate-tse-i-gurugram-mongodb-2bcb4",
    source="Swooped (aggregator)", location="Gurugram", country="India", locgroup="India", mode="Hybrid",
    exp="Associate (entry)", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Troubleshooting, Networking, NoSQL, Cloud, Communication", certs="None stated",
    hard="Must be based in Gurugram (hybrid)", locfit=IN_OK, posted="2026-06-10", conf="Low", lstatus="Active (search-verified)",
    jd="Technical Services Engineer (support) for MongoDB in Gurugram.", notes="Separate req from JOB-0022 (different city).")

add(id="JOB-0024", pri="P1", title="Technical Support Engineer 1", cat=C1, company="Datadog",
    website="https://www.datadoghq.com", url="https://www.indexventures.com/startup-jobs/datadog/technical-support-engineer-1-19/",
    source="Index Ventures job board", location="Bengaluru", country="India", locgroup="India", mode="Hybrid",
    exp="~2 years SaaS support", minexp=2, level="Early-Career (1-3 yrs)", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Troubleshooting, Communication, Linux, Monitoring", pref="Python, Docker, Kubernetes", certs="None stated",
    hard="3-5 office days per week", locfit=IN_OK, posted="2026-07-15", conf="Medium", lstatus="Active (search-verified)",
    jd="Multi-channel technical support for Datadog observability platform.",
    notes="Posted date approximate ('last published July 2026'). Prometheus/Grafana knowledge transfers well.")

add(id="JOB-0025", pri="P1", title="Technical Support Engineering (Azure)", cat=C1, company="Microsoft",
    website="https://www.microsoft.com", url="https://jobs.anitab.org/companies/microsoft/jobs/64856723-technical-support-engineering",
    source="AnitaB.org job board", location="Bengaluru", country="India", locgroup="India", mode="Hybrid",
    exp="Recent graduates", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Relevant degree",
    req="Troubleshooting, Azure, Networking, Communication", pref="Python", langs="PowerShell or Python", clouds="Azure",
    certs="None stated", hard="None stated", locfit=IN_OK, posted="2025-08-15", conf="Low", lstatus="Possibly Closed",
    jd="Customer Service & Support technical support engineering.", notes="Posting from Aug 2025 - search careers.microsoft.com for the current req.")

add(id="JOB-0026", pri="P1", title="Level 2 Azure Support Engineer", cat=C1, company="World Wide Technology",
    website="https://www.wwt.com",
    url="https://joinsaarthi.com/jobs/world-wide-technology/level-2-azure-support-engineer-mumbai/c5ee1b04-7a24-453a-81fc-cdcdeae4e8de",
    source="JoinSaarthi (aggregator)", location="Mumbai / Gurugram / Pune / Bengaluru / Hyderabad", country="India",
    locgroup="India", mode="Unknown", exp="0-3 years", minexp=0, level="Entry-Level", emp="Full-time",
    salary="Not disclosed", cur="INR", visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Azure, Networking, Troubleshooting", clouds="Azure", certs="AZ-104 (commonly expected for Azure roles)",
    hard="None stated", locfit=IN_OK, conf="Low", lstatus="Active (search-verified)",
    jd="Intermediate technical support for Azure infrastructure services.",
    notes="Cert note is a market observation, not stated in this listing.")

add(id="JOB-0027", pri="P1", title="Software Engineer - Cloud DevOps", cat=C1, company="Cisco",
    website="https://www.cisco.com", url="https://jobs.joindevops.com/jobs/508124412-software-engineer-cloud-devops-|-cisco-hiring-2026",
    source="JoinDevOps (aggregator)", location="Bengaluru (verify)", country="India", locgroup="India", mode="Unknown",
    exp="Unknown", minexp="", level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown", req="Unknown - open JD",
    certs="None stated", hard="None stated", locfit=IN_OK, conf="Low", lstatus="Active (search-verified)",
    jd="Cisco Cloud DevOps software engineer (2026 hiring).", notes="Match on jobs.cisco.com before applying.")

add(id="JOB-0028", pri="P1", title="Technical Support Engineer", cat=C1, company="Zoho",
    website="https://www.zoho.com", url="https://testingsociety.com/?p=14900",
    source="TestingSociety (aggregator)", location="Chennai", country="India", locgroup="India", mode="On-site",
    exp="Fresher", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Troubleshooting, Communication, Networking", certs="None stated", hard="None stated", locfit=IN_OK,
    posted="2026-05-16", conf="Low", lstatus="Possibly Closed", jd="Zoho technical support engineer.",
    notes="May 2026 - check zoho.com/careers.")

# ------------------------------------------------------------------ P1 CLOUD & DEVOPS (INTERNATIONAL)
add(id="JOB-0029", pri="P1", title="(Junior) Cloud Engineer (m/f/d)", cat=C1, company="HomeToGo",
    website="https://www.hometogo.com", url="https://www.ziprecruiter.de/jobs/551879121-junior-cloud-engineer-m-f-d-bei-hometogo",
    source="ZipRecruiter Germany", location="Berlin", country="Germany", locgroup="Germany", mode="On-site",
    exp="Junior", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="EUR",
    visa="Yes (explicit in listing)", reloc="Yes (explicit in listing)", remote_india="N/A", edu="Unknown",
    req="Cloud, Linux, Infrastructure as Code", pref="AWS, Terraform, Kubernetes", certs="None stated",
    hard="Blue Card salary threshold applies", locfit=SPON, posted="2026-06-27", conf="Medium", lstatus="Possibly Closed",
    jd="Junior cloud engineer in Berlin; listing advertises full visa sponsorship and relocation support.",
    notes="remotely.de mirror marks it 'Bereits vergeben' (filled). Check HomeToGo careers for a re-post.")

add(id="JOB-0030", pri="P1", title="Junior DevOps Engineer (f/m/x)", cat=C1, company="Seven Senders",
    website="https://www.sevensenders.com", url="https://jobs.b2venture.vc/companies/seven-senders/jobs/91962263-junior-devops-engineer-f-m-x",
    source="b2venture job board", location="Berlin", country="Germany", locgroup="Germany", mode="Unknown",
    exp="Junior", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="EUR",
    visa="Unknown", reloc="Unknown", remote_india="N/A", edu="Unknown", req="CI/CD, Docker, Cloud, Linux",
    certs="None stated", hard="Work authorization for Germany needed unless sponsored", locfit=SPON_UNK,
    posted="2026-09-15", conf="Medium", lstatus="Active (search-verified)", jd="Junior DevOps at a Berlin logistics-tech company.",
    notes="Ask about visa sponsorship before investing time. Posted date approximate (Sep 2026).")

add(id="JOB-0031", pri="P1", title="IT System Engineer - Cloud Infrastructure & DevOps", cat=C1, company="ALTEN",
    website="https://www.alten.com", url="https://jobmetasearch.ai/visa-sponsorship/devops-engineer",
    source="JobMetaSearch (aggregator)", location="Munich", country="Germany", locgroup="Germany", mode="Unknown",
    exp="Entry level (per aggregator)", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="EUR",
    visa="Unknown (aggregator tag only)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Cloud, Linux, CI/CD", certs="None stated", hard="German language may be required - verify", locfit=SPON_UNK,
    conf="Low", lstatus="Active (search-verified)", jd="Cloud infra/DevOps system engineer at ALTEN Munich.",
    notes="Aggregator tags it 'visa sponsorship' - not confirmed by employer, so recorded as Unknown.")

add(id="JOB-0032", pri="P1", title="Junior DevOps Engineer", cat=C1, company="Caliberly",
    website="", url="https://www.bayt.com/en/uae/jobs/junior-devops-engineer-74731805/",
    source="Bayt", location="Dubai", country="UAE", locgroup="UAE", mode="On-site",
    exp="Junior", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="AED",
    visa="Unknown", reloc="Unknown", remote_india="N/A", edu="Unknown", req="CI/CD, Docker, Cloud, Linux",
    certs="None stated", hard="UAE employment visa needed (employer-arranged if hired)", locfit=SPON_UNK,
    posted="2026-06-18", conf="Medium", lstatus="Active (search-verified)", jd="Office-based junior DevOps role in Dubai.",
    notes="UAE employers usually arrange the work visa for hires, but this listing does not state it.")

add(id="JOB-0033", pri="P1", title="Junior Cloud Field Engineer", cat=C1, company="Canonical",
    website="https://canonical.com", url="https://boards.greenhouse.io/canonicaljobs/jobs/6792944",
    source="Greenhouse (company board)", location="Home-based - Middle East", country="UAE", locgroup="UAE", mode="Remote",
    exp="Junior", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="Unknown",
    visa="Unknown", reloc="Unknown", remote_india="No - Middle East region", edu="Degree (Canonical emphasises academics)",
    req="Linux, Networking, Python", pref="Kubernetes, Cloud", langs="Python (intermediate-advanced)", certs="None stated",
    hard="Region-based remote (Middle East)", locfit=SPON_UNK, posted="2025-04-10", conf="Medium", lstatus="Possibly Closed",
    jd="Field engineering for Canonical cloud deployments.", notes="Last seen dated Apr 2025; Canonical often reposts - check canonical.com/careers.")

add(id="JOB-0034", pri="P1", title="Junior DevOps Engineer", cat=C1, company="Miratech",
    website="https://www.miratechgroup.com", url="https://remotive.com/remote/jobs/devops/junior-devops-engineer-4202261",
    source="Remotive", location="Remote - Worldwide (Arc says restrictions apply)", country="Remote",
    locgroup="Remote - Restricted / Unclear", mode="Remote", exp="Junior", minexp=0, level="Entry-Level", emp="Full-time",
    salary="Not disclosed", cur="Unknown", visa="N/A (remote)", reloc="N/A", remote_india="Unclear - verify",
    edu="Unknown", req="Cloud, CI/CD, Linux", certs="None stated", hard="Possible country restriction",
    locfit=SPON_UNK, conf="Medium", lstatus="Active (search-verified)",
    jd="Build/maintain cloud infra for a cloud contact-center software client.", notes="Confirm India eligibility on the apply page.")

add(id="JOB-0035", pri="P1", title="Junior Systems and Cloud Management Engineer", cat=C1, company="GDi",
    website="https://www.gdi.net", url="https://remotive.com/remote/jobs/devops/junior-systems-and-cloud-management-engineer-4308081",
    source="Remotive", location="Remote - Worldwide", country="Remote", locgroup="Remote - India Eligible", mode="Remote",
    exp="Junior", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="Unknown",
    visa="N/A (remote)", reloc="N/A", remote_india="Yes - Worldwide (per Remotive)", edu="Unknown",
    req="Linux, Cloud", certs="None stated", hard="None stated", locfit=REM_OK, conf="Medium", lstatus="Active (search-verified)",
    jd="Junior systems/cloud management (details limited in snippet).", notes="")

add(id="JOB-0036", pri="P1", title="Junior Cloud Operations & SRE Engineer", cat=C1, company="NEORIS",
    website="https://www.neoris.com", url="https://remotive.com/remote/jobs/devops/junior-cloud-operations-sre-engineer-4926793",
    source="Remotive", location="Remote - Spain only", country="Spain", locgroup="Remote - Restricted / Unclear", mode="Remote",
    exp="Junior", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="EUR",
    visa="No", reloc="No", remote_india="No - Spain only", edu="Unknown", req="Cloud, SRE, Linux",
    certs="None stated", hard="Location restricted to Spain", locfit=NOT_OK, conf="Medium", lstatus="Active (search-verified)",
    jd="Junior cloud ops/SRE, remote within Spain.", notes="NOT open to India-based applicants - kept to show restriction handling.")

add(id="JOB-0037", pri="P1", title="Junior DevOps Engineer", cat=C1, company="Vultr",
    website="https://www.vultr.com", url="https://job-boards.greenhouse.io/vultr/jobs/4619147006",
    source="Greenhouse (company board)", location="Remote (country not stated)", country="Remote",
    locgroup="Remote - Restricted / Unclear", mode="Remote", exp="Junior", minexp=0, level="Entry-Level", emp="Full-time",
    salary="Not disclosed", cur="Unknown", visa="Unknown", reloc="Unknown", remote_india="Unclear - verify", edu="Unknown",
    req="Kubernetes, Docker, Linux, CI/CD", certs="None stated", hard="Possible US-only remote", locfit=SPON_UNK,
    conf="Medium", lstatus="Active (search-verified)", jd="Junior DevOps on Kubernetes and cloud-native tooling.", notes="")

add(id="JOB-0038", pri="P1", title="DevOps Engineer", cat=C1, company="Swisscom",
    website="https://www.swisscom.ch", url="https://relocate.me/the-netherlands/rotterdam/swisscom/devops-engineer-9731",
    source="Relocate.me", location="Rotterdam", country="Netherlands", locgroup="Other International", mode="On-site",
    exp="Junior-friendly ('young talented')", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="EUR",
    visa="Yes (visa services in package)", reloc="Yes (advanced package)", remote_india="N/A", edu="Unknown",
    req="CI/CD, Docker, Linux, Cloud", certs="None stated", hard="HSM permit salary threshold", locfit=SPON,
    conf="Medium", lstatus="Closed / Expired", jd="DevOps with advanced relocation package (housing, visa, bonus).",
    notes="Marked 'Archive vacancy' on Relocate.me - EXPIRED. Watch Relocate.me for similar.")

add(id="JOB-0039", pri="P1", title="Cloud Developer (Graduate)", cat=C1, company="SimplifyNext",
    website="", url="https://job-boards.greenhouse.io/simplifynext/jobs/5026261007",
    source="Greenhouse (company board)", location="Singapore", country="Singapore", locgroup="Other International", mode="Unknown",
    exp="Graduate", minexp=0, level="Graduate Program", emp="Full-time", salary="Not disclosed", cur="SGD",
    visa="Unknown", reloc="Unknown", remote_india="N/A", edu="Degree", req="Cloud, Python", certs="None stated",
    hard="Employment Pass needed (employer applies; COMPASS)", locfit=SPON_UNK, conf="Medium", lstatus="Active (search-verified)",
    jd="Graduate cloud developer role in Singapore.", notes="Ask whether they sponsor an EP before applying.")

add(id="JOB-0040", pri="P1", title="Graduate Cloud Infrastructure Engineer (Fresh Graduates Welcome)", cat=C1, company="Unknown (see listing)",
    website="", url="https://grabjobs.co/singapore/job/full-time/engineering-and-technicians/graduate-cloud-infrastructure-engineer-fresh-graduates-welcome-159745120",
    source="GrabJobs", location="Singapore", country="Singapore", locgroup="Other International", mode="Unknown",
    exp="Fresh graduates", minexp=0, level="Graduate Program", emp="Full-time", salary="4,900 - 6,800 / month", cur="SGD",
    visa="Unknown", reloc="Unknown", remote_india="N/A", edu="Degree", req="Cloud, Linux, Networking", certs="None stated",
    hard="Employment Pass needed", locfit=SPON_UNK, conf="Low", lstatus="Active (search-verified)",
    jd="Graduate cloud infrastructure engineer.", notes="Employer not named in snippet.")

add(id="JOB-0041", pri="P1", title="Working Student - DevOps (w/m/d)", cat=C1, company="Everphone",
    website="https://everphone.com", url="https://www.arbeitnow.com/jobs/companies/everphone-gmbh/working-student-devops-berlin-440242",
    source="Arbeitnow", location="Berlin", country="Germany", locgroup="Germany", mode="Hybrid",
    exp="Student", minexp=0, level="Internship", emp="Internship / Working Student", salary="Not disclosed", cur="EUR",
    visa="No", reloc="No", remote_india="N/A", edu="Enrolled student in Germany",
    req="Linux, Docker, CI/CD", certs="None stated", hard="Must be eligible to work as Werkstudent in Germany (enrolled)",
    locfit=NOT_OK, conf="Medium", lstatus="Active (search-verified)", jd="Working-student DevOps role.",
    notes="Only relevant if you enrol in a German university.")

add(id="JOB-0042", pri="P1", title="Junior DevOps / Machine Learning Engineer", cat=C1, company="Power Reply",
    website="https://www.reply.com", url="https://en.devjobs.de/job/6351c2d3d95a2948603f85dd8bb041de",
    source="devjobs.de", location="Berlin / Munich", country="Germany", locgroup="Germany", mode="Unknown",
    exp="Junior", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="EUR",
    visa="Unknown", reloc="Unknown", remote_india="N/A", edu="Unknown", req="CI/CD, Python, Cloud, Machine Learning",
    certs="None stated", hard="German may be required - verify", locfit=SPON_UNK, conf="Low", lstatus="Active (search-verified)",
    jd="Junior DevOps/ML role at Reply group.", notes="")

# ------------------------------------------------------------------ P2 DATA
add(id="JOB-0043", pri="P2", title="Business Intelligence Engineer I, Amazon Wholesale", cat=C2, company="Amazon",
    website="https://www.amazon.jobs",
    url="https://jobs.anitab.org/companies/amazon-3-60ad394d-c673-4474-9694-344b0cae748f/jobs/89086924-business-intelligence-engineer-amazon-wholesale",
    source="AnitaB.org job board", location="Bengaluru", country="India", locgroup="India", mode="On-site",
    exp="Level I (entry BIE)", minexp=1, level="Early-Career (1-3 yrs)", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Bachelor's (typical) - verify",
    req="SQL, Data Visualization, Excel", pref="Python", tools="SQL, dashboards", certs="None stated",
    hard="None stated", locfit=IN_OK, posted="2026-08-15", conf="Medium", lstatus="Active (search-verified)",
    jd="Build and maintain SQL datasets and dashboards for wholesale/B2B programs.",
    notes="Amazon BIE I usually expects ~1 yr analytics experience - verify on amazon.jobs. Posted date approximate.")

add(id="JOB-0044", pri="P2", title="Business Intelligence Engineer I, FinOps", cat=C2, company="Amazon",
    website="https://www.amazon.jobs",
    url="https://jobs.anitab.org/companies/amazon-3-60ad394d-c673-4474-9694-344b0cae748f/jobs/69998699-business-intel-engineer-i-finops",
    source="AnitaB.org job board", location="Bengaluru", country="India", locgroup="India", mode="On-site",
    exp="Level I", minexp=1, level="Early-Career (1-3 yrs)", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="SQL, Advanced SQL, Data Engineering", pref="AWS, Python", certs="None stated", hard="None stated",
    locfit=IN_OK, posted="2026-03-15", conf="Medium", lstatus="Possibly Closed",
    jd="Large data-warehouse work; design and business use of large datasets.", notes="Posted Mar 2026.")

add(id="JOB-0045", pri="P2", title="Data Analyst (Entry Level)", cat=C2, company="Unknown (see listing)",
    website="", url="https://builtin.com/job/data-analyst/4585323", source="Built In", location="Pune", country="India",
    locgroup="India", mode="Unknown", exp="0-1 years", minexp=0, level="Entry-Level", emp="Full-time",
    salary="Not disclosed", cur="INR", visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="SQL, Power BI, Tableau, Excel", certs="None stated", hard="None stated", locfit=IN_OK, conf="Medium",
    lstatus="Active (search-verified)", jd="Entry-level data analyst: SQL plus Power BI or Tableau.",
    notes="Employer name not in snippet - open listing.")

add(id="JOB-0046", pri="P2", title="Associate - Investment Analytics", cat=C2, company="Amgen",
    website="https://www.amgen.com", url="https://www.glassdoor.co.in/Job/india-entry-level-data-scientist-jobs-SRCH_IL.0,5_IN115_KO6,32.htm",
    source="Glassdoor", location="Hyderabad", country="India", locgroup="India", mode="Unknown",
    exp="Entry (Level L3)", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="SQL, Excel, Statistics, Data Visualization", certs="None stated", hard="None stated", locfit=IN_OK,
    posted="2026-09-15", conf="Low", lstatus="Active (search-verified)",
    jd="Analytical/structured problem solving with structured learning and on-the-job exposure.",
    notes="Direct link not captured - search on careers.amgen.com. Skills inferred from role type.")

add(id="JOB-0047", pri="P2", title="Junior Data Engineer", cat=C2, company="ALP (Computational Finance, AI & Data Engineering)",
    website="", url="https://jobfound.org/job/alp-computational-finance-ai-and-data-engineering-is-hiring-for-junior-data-engineer-bengaluru-karnataka-india-india-31-october-2026",
    source="JobFound (aggregator)", location="Bengaluru", country="India", locgroup="India", mode="Unknown",
    exp="2-4 years", minexp=2, level="Early-Career (1-3 yrs)", emp="Full-time", salary="7-15 LPA", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Python, SQL, ETL, Data Engineering, AWS", pref="Airflow, Spark", tools="Airflow/Prefect, PySpark/Databricks, S3, Glue",
    clouds="AWS", certs="None stated", hard="None stated", locfit=IN_OK, posted="2026-10-31", conf="Low",
    lstatus="Active (search-verified)", jd="Data pipelines with Airflow/Prefect, PySpark/Databricks on AWS.", notes="Stretch (2+ yrs).")

add(id="JOB-0048", pri="P2", title="Jr. Data Scientist", cat=C2, company="ABB",
    website="https://global.abb", url="https://job4freshers.co.in/category/data-science/",
    source="Job4Freshers (aggregator)", location="Bengaluru", country="India", locgroup="India", mode="Unknown",
    exp="Fresher (off-campus)", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Python, Machine Learning, Statistics, SQL", certs="None stated", hard="None stated", locfit=IN_OK,
    conf="Low", lstatus="Active (search-verified)", jd="ABB off-campus junior data scientist notification.",
    notes="Eligibility not visible - check careers.abb.")

add(id="JOB-0049", pri="P2", title="Associate Data Scientist", cat=C2, company="Multi Recruit (client undisclosed)",
    website="", url="https://in.linkedin.com/jobs/data-scientist-fresher-jobs", source="LinkedIn Jobs",
    location="Bengaluru", country="India", locgroup="India", mode="Unknown", exp="Associate", minexp=0,
    level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR", visa="Not required (India)", reloc="Unknown",
    remote_india="N/A", edu="Unknown", req="Python, Machine Learning, SQL", certs="None stated", hard="None stated",
    locfit=IN_OK, posted="2026-08-10", conf="Low", lstatus="Possibly Closed", jd="Associate DS via recruiter.",
    notes="~3 months old at time of search. Direct link not captured.")

# ------------------------------------------------------------------ P3 AI
add(id="JOB-0050", pri="P3", title="Generative AI Engineer", cat=C3, company="Evnek Technologies",
    website="", url="https://jobfound.org/job/evnek-technologies-pvt-ltd-is-hiring-for-generative-ai-engineer-bangalore-india-4-november-2026",
    source="JobFound (aggregator)", location="Bengaluru", country="India", locgroup="India", mode="Unknown",
    exp="0-1 years", minexp=0, level="Entry-Level", emp="Full-time", salary="4-6 LPA", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Python, LLMs, RAG, LangChain", pref="Vector Databases", tools="LangChain or LlamaIndex", certs="None stated",
    hard="None stated", locfit=IN_OK, posted="2026-11-04", conf="Low", lstatus="Active (search-verified)",
    jd="Build RAG pipelines with LangChain/LlamaIndex; Python + LLMs.", notes="Very recent; strong match for your LangChain/LangGraph work.")

add(id="JOB-0051", pri="P3", title="AI Engineer (LLM / RAG)", cat=C3, company="StackOrbit",
    website="", url="https://freehire.me/jobs/ai-engineer-llm-rag-india-stackorbit-p5xmorrh",
    source="freehire (aggregator)", location="Kolhapur", country="India", locgroup="India", mode="Unknown",
    exp="Not stated", minexp="", level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="LLMs, RAG, Python, Cloud", certs="None stated", hard="None stated", locfit=IN_OK, posted="2026-11-08",
    conf="Low", lstatus="Active (search-verified)", jd="LLM and RAG features for cloud automation.",
    notes="Cloud-automation + AI overlap suits your profile.")

add(id="JOB-0052", pri="P3", title="Generative AI / LLM RAG Engineer (Fresher)", cat=C3, company="Tredence",
    website="https://www.tredence.com", url="https://cloudsoftsol.com/blog/tredence-generative-ai-llm-rag-engineer-fresher-bangalore-2026/",
    source="Blog alert (training institute)", location="Bengaluru", country="India", locgroup="India", mode="Unknown",
    exp="Fresher (2024-2026 grads)", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="2024-2026 graduates",
    req="Python, LLMs, RAG", certs="None stated", hard="Graduation year 2024-2026", locfit=IN_OK, conf="Low",
    lstatus="Active (search-verified)", jd="Fresher GenAI/RAG track.", notes="Blog source - confirm on tredence.com/careers.")

add(id="JOB-0053", pri="P3", title="Software Engineer - AI", cat=C3, company="Cloudflare",
    website="https://www.cloudflare.com", url="https://resumegeni.com/jobs/software-engineer-ai-cloudflare-d262d81d88",
    source="ResumeGeni (aggregator)", location="Bengaluru", country="India", locgroup="India", mode="Hybrid",
    exp="Unknown", minexp="", level="Early-Career (1-3 yrs)", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="LLMs, API Development, Python", pref="TypeScript", tools="Cloudflare Workers AI, AI Gateway", certs="None stated",
    hard="None stated", locfit=IN_OK, conf="Low", lstatus="Active (search-verified)",
    jd="Production AI applications on Cloudflare's ecosystem incl. AI Gateway.", notes="Check job-boards.greenhouse.io/cloudflare.")

add(id="JOB-0054", pri="P3", title="Backend + AI Engineer", cat=C3, company="Narrative (YC W23)",
    website="", url="https://www.workatastartup.com/jobs/79469", source="YC Work at a Startup",
    location="Remote (India)", country="India", locgroup="Remote - India Eligible", mode="Remote",
    exp="1+ years", minexp=1, level="Early-Career (1-3 yrs)", emp="Full-time", salary="24K - 36K per year", cur="USD",
    visa="N/A (remote India)", reloc="N/A", remote_india="Yes - IN / Remote (IN)", edu="Unknown",
    req="Python, LLMs, API Development", pref="AI Agents", certs="None stated", hard="None stated", locfit=REM_OK,
    conf="Medium", lstatus="Active (search-verified)", jd="AI-powered QA testing platform; backend + AI.", notes="Good stretch.")

add(id="JOB-0055", pri="P3", title="Junior/Senior/Staff Software Engineer, Inference / Compute Infrastructure", cat=C3, company="Together AI",
    website="https://www.together.ai",
    url="https://jobs.generalcatalyst.com/companies/together-ai-2/jobs/90599711-junior-senior-or-staff-software-engineer-inference-compute-infrastructure-engineering",
    source="General Catalyst job board", location="Remote - India", country="India", locgroup="Remote - India Eligible", mode="Remote",
    exp="Junior to Staff", minexp="", level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="Unknown",
    visa="N/A (remote India)", reloc="N/A", remote_india="Yes - Remote India", edu="Unknown",
    req="Python, Kubernetes, Linux, Model Deployment", pref="Go", certs="None stated", hard="None stated", locfit=REM_OK,
    posted="2026-08-15", conf="Medium", lstatus="Active (search-verified)", jd="GPU inference/compute infrastructure.",
    notes="Blends P1 infra with P3 AI - high strategic fit. Posted date approximate.")

add(id="JOB-0056", pri="P3", title="AI Inference Junior Engineer (WFH)", cat=C3, company="Qubrid AI",
    website="", url="https://www.ziprecruiter.in/jobs/546239181-ai-inference-junior-engineer-wfh-at-qubrid-ai",
    source="ZipRecruiter India", location="Remote - India", country="India", locgroup="Remote - India Eligible", mode="Remote",
    exp="Junior", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="N/A", reloc="N/A", remote_india="Yes - WFH India", edu="Unknown", req="Python, Model Deployment, Linux",
    certs="None stated", hard="None stated", locfit=REM_OK, posted="2026-06-15", conf="Low", lstatus="Possibly Closed",
    jd="Junior AI inference / GPU infrastructure.", notes="June 2026.")

add(id="JOB-0057", pri="P3", title="Junior AI Software Engineer / AI Engineer Intern", cat=C3, company="RB DesignTech",
    website="", url="https://jobs.weekday.works/junior-ai-software-engineers-ai-engineer-interns-at-rb-design-tech-wkdy0gz7sd",
    source="Weekday", location="Hyderabad / Remote India", country="India", locgroup="India", mode="Hybrid",
    exp="0-2 years", minexp=0, level="Internship", emp="Internship / Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="Yes", edu="Unknown", req="Python, LLMs, Machine Learning",
    certs="None stated", hard="None stated", locfit=IN_OK, conf="Low", lstatus="Active (search-verified)",
    jd="Junior AI engineers and interns.", notes="")

add(id="JOB-0058", pri="P3", title="AI/ML Engineer (Fresher)", cat=C3, company="LTIMindtree",
    website="https://www.ltimindtree.com", url="https://cloudsoftsol.com/jobs/ltimindtree-ai-ml-engineer-fresher-pune-2026/",
    source="Blog alert (training institute)", location="Pune", country="India", locgroup="India", mode="Unknown",
    exp="Fresher", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown", req="Python, Machine Learning",
    certs="None stated", hard="None stated", locfit=IN_OK, conf="Low", lstatus="Active (search-verified)",
    jd="Fresher AI/ML engineer.", notes="Unverified blog source - confirm on ltimindtree.com/careers.")

# ------------------------------------------------------------------ P4 SOFTWARE
add(id="JOB-0059", pri="P4", title="Software Engineer - Network/Embedded/Application Development (New Grad) - India UHR", cat=C4,
    company="Cisco", website="https://www.cisco.com",
    url="https://jobs.cisco.com/jobs/ProjectDetail/Software-Engineer-Test-Full-Time-India-Engineering-UHR/1403775",
    source="Company Careers", location="Bengaluru", country="India", locgroup="India", mode="Hybrid",
    exp="New grad", minexp=0, level="Graduate Program", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Degree (batch eligibility varies by source)",
    req="Data Structures and Algorithms, Networking, Python", pref="Linux, Testing", certs="None stated",
    hard="Graduation batch restriction - verify", locfit=IN_OK, conf="Medium", lstatus="Active (search-verified)",
    jd="New-grad SWE (network/embedded/app). Process: OA, technical (DSA, core CS), managerial, HR.",
    notes="Networking knowledge is an edge here.")

add(id="JOB-0060", pri="P4", title="Software Engineer Trainee (Technical Graduate Apprentice) - India UHR", cat=C4,
    company="Cisco", website="https://www.cisco.com",
    url="https://jobs.weekday.works/cisco-software-engineer-trainee_technical-graduate-apprentice---india-uhr",
    source="Weekday", location="Bengaluru", country="India", locgroup="India", mode="On-site",
    exp="Fresher", minexp=0, level="Apprenticeship", emp="Apprenticeship (12 months)", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Python, Testing, Networking", certs="None stated", hard="Apprenticeship Act eligibility rules may apply",
    locfit=IN_OK, posted="2026-09-01", conf="Low", lstatus="Possibly Closed",
    jd="12-month apprenticeship starting Sep 2026.", notes="Cohort likely started; watch for next intake.")

add(id="JOB-0061", pri="P4", title="Software Developer 1", cat=C4, company="Oracle",
    website="https://www.oracle.com",
    url="https://jobs.anitab.org/companies/oracle-2-2edaf908-7a2f-4ec2-a440-aed90715dc36/jobs/64065943-software-developer-1",
    source="AnitaB.org job board", location="Bengaluru / Hyderabad", country="India", locgroup="India", mode="Unknown",
    exp="Freshers / 0-2 years (campus page); some reqs ask 2+", minexp=0, level="Entry-Level", emp="Full-time",
    salary="Not disclosed", cur="INR", visa="Not required (India)", reloc="Unknown", remote_india="N/A",
    edu="BE/BTech/MCA/MSc CS/IT; batch 2024-2026", req="Data Structures and Algorithms, Java, OOP",
    pref="Cloud", certs="None stated", hard="Batch 2024/2025/2026", locfit=IN_OK, posted="2026-01-07", conf="Medium",
    lstatus="Possibly Closed", jd="Oracle SD1 (IC1).", notes="Jan 2026 posting; Oracle reposts SD1 often - check oracle.com/careers.")

add(id="JOB-0062", pri="P4", title="Associate Software Engineer (Subscription Management)", cat=C4, company="Red Hat",
    website="https://www.redhat.com", url="https://builtin.com/job/associate-software-engineer/8371443",
    source="Built In", location="Pune", country="India", locgroup="India", mode="Hybrid",
    exp="1+ year industry", minexp=1, level="Early-Career (1-3 yrs)", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Python, Linux, Git, REST APIs", certs="None stated", hard="None stated", locfit=IN_OK, conf="Medium",
    lstatus="Active (search-verified)", jd="Associate SWE on subscription management team.",
    notes="Red Hat also runs 'Trainee - Associate Software Engineer' (Jun-Dec cohorts) - watch for 2027 intake.")

add(id="JOB-0063", pri="P4", title="Software Dev Engineer I (University Talent Acquisition)", cat=C4, company="Amazon",
    website="https://www.amazon.jobs", url="https://freshershunt.in/amazon-sde-1-2026/",
    source="FreshersHunt (aggregator)", location="Bengaluru / Hyderabad / Chennai", country="India", locgroup="India", mode="On-site",
    exp="Fresh graduates 2024-2026 (some reqs need 1+ yr)", minexp=0, level="Entry-Level", emp="Full-time",
    salary="Not disclosed by employer", cur="INR", visa="Not required (India)", reloc="Unknown", remote_india="N/A",
    edu="Bachelor's/Master's CS or related", req="Data Structures and Algorithms, OOP, System Design, Java",
    pref="AWS", certs="None stated", hard="Graduation batch", locfit=IN_OK, conf="Low", lstatus="Active (search-verified)",
    jd="SDE-1 via University TA; reported Job ID 10454438 - search it on amazon.jobs.",
    notes="Process (per aggregator): OA aptitude, coding OA, technical, HR.")

add(id="JOB-0064", pri="P4", title="Software Engineer 2", cat=C4, company="Microsoft",
    website="https://www.microsoft.com", url="https://jobs.anitab.org/companies/microsoft-2/jobs/91196366-software-engineer-2",
    source="AnitaB.org job board", location="Bengaluru / Noida / Hyderabad", country="India", locgroup="India", mode="Hybrid",
    exp="Unknown (SE2 is above new-grad level)", minexp=2, level="Experienced", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Data Structures and Algorithms, System Design, OOP", certs="None stated", hard="None stated", locfit=IN_OK,
    posted="2026-08-26", conf="Medium", lstatus="Active (search-verified)",
    jd="SE2 across Microsoft India sites.", notes="Min-experience value is an estimate from level naming - verify. Low priority.")

add(id="JOB-0065", pri="P4", title="Junior Backend Developer", cat=C4, company="Planso",
    website="", url="https://wellfound.com/jobs/4717817-junior-backend-developer", source="Wellfound",
    location="Unknown (check listing)", country="Unknown", locgroup="Remote - Restricted / Unclear", mode="Unknown",
    exp="Junior", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="Unknown",
    visa="Unknown", reloc="Unknown", remote_india="Unclear", edu="Unknown",
    req="Python, REST APIs, Node.js", pref="Go, Java", certs="None stated", hard="Unknown location", locfit=SPON_UNK,
    conf="Medium", lstatus="Active (search-verified)",
    jd="Backend in Python/Node.js/Java/Go; REST API understanding.", notes="")

add(id="JOB-0066", pri="P4", title="Junior Backend Developer (Node.js / React.js / Python)", cat=C4, company="Conexus Tech Labs",
    website="", url="https://jobs.weekday.works/junior-backend-developer-node-js-react-js-python-at-conexus-tech-labs-4382261578",
    source="Weekday", location="New Delhi", country="India", locgroup="India", mode="Unknown",
    exp="~1 year (internships/projects count)", minexp=1, level="Early-Career (1-3 yrs)", emp="Full-time",
    salary="Not disclosed", cur="INR", visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Node.js, React, Python, REST APIs", tools="Express.js", certs="None stated", hard="None stated", locfit=IN_OK,
    posted="2026-03-19", conf="Low", lstatus="Possibly Closed", jd="Junior backend with Express.js.", notes="March 2026.")

add(id="JOB-0067", pri="P4", title="Software Developer (Off-Campus 2026)", cat=C4, company="Zoho",
    website="https://www.zoho.com", url="https://www.fresheroffcampus.com/zoho-off-campus/",
    source="FresherOffCampus (aggregator)", location="Chennai / Salem / Coimbatore / Tirunelveli / Madurai", country="India",
    locgroup="India", mode="On-site", exp="Fresher", minexp=0, level="Entry-Level", emp="Full-time",
    salary="Not disclosed", cur="INR", visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Any (batch list varies)",
    req="Data Structures and Algorithms, Java, OOP", certs="None stated", hard="None stated", locfit=IN_OK,
    conf="Low", lstatus="Active (search-verified)", jd="Zoho off-campus SWE drive.",
    notes="Zoho hires year-round via zoho.com/careers; confirm there.")

add(id="JOB-0068", pri="P4", title="Java Developer (Freshers)", cat=C4, company="Persistent Systems",
    website="https://www.persistent.com",
    url="https://offcampusready.blogspot.com/2026/03/persistent-systems-recruitment-2026-java-developer-freshers.html",
    source="Blog (aggregator)", location="Pune", country="India", locgroup="India", mode="Hybrid",
    exp="Fresher", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Java, OOP, SQL", pref="AWS, Terraform", certs="None stated", hard="None stated", locfit=IN_OK,
    posted="2026-03-15", conf="Low", lstatus="Possibly Closed",
    jd="Java fresher role; AWS (EC2, S3, CloudWatch) and basic Terraform listed as expectations.",
    notes="Verify on careers.persistent.com.")

add(id="JOB-0069", pri="P4", title="Member of Technical Staff 1", cat=C4, company="Nutanix",
    website="https://www.nutanix.com", url="https://jobs.anitab.org/companies/nutanix/jobs/72590945-member-of-technical-staff-1",
    source="AnitaB.org job board", location="Pune", country="India", locgroup="India", mode="Unknown",
    exp="1-2 years", minexp=1, level="Early-Career (1-3 yrs)", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="Linux, Python, Go", certs="None stated", hard="None stated", locfit=IN_OK, posted="2026-03-29",
    conf="Medium", lstatus="Possibly Closed", jd="Systems engineer in software product development.", notes="")

add(id="JOB-0070", pri="P4", title="Associate System Engineer", cat=C4, company="IBM",
    website="https://www.ibm.com", url="https://justforcareer.pages.dev/jobs/ibm-associate-system-engineer",
    source="Aggregator", location="India (IBM Consulting CICs)", country="India", locgroup="India", mode="On-site",
    exp="Fresher (2024-2026 batches)", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="BE/BTech CS/IT/related, min 60% or 6 CGPA",
    req="Data Structures and Algorithms, OOP, SQL", certs="None stated", hard="60% / 6 CGPA minimum", locfit=IN_OK,
    conf="Low", lstatus="Active (search-verified)", jd="IBM Consulting Client Innovation Centre entry role.",
    notes="IBM off-campus drives typically run Sep-Dec - verify on ibm.com/careers.")

add(id="JOB-0071", pri="P4", title="Graduate Consultant Software Engineer 2027", cat=C4, company="Softwire",
    website="https://www.softwire.com", url="https://www.softwire.com/careers/open-roles/graduate-consultant-software-engineer-2027",
    source="Company Careers", location="London / Cambridge / Manchester", country="United Kingdom", locgroup="Other International",
    mode="Hybrid", exp="Graduate (2027 intake)", minexp=0, level="Graduate Program", emp="Full-time", salary="Not disclosed", cur="GBP",
    visa="Yes (company states Skilled Worker sponsorship for permanent roles)", reloc="Unknown", remote_india="N/A",
    edu="Degree", req="Data Structures and Algorithms, OOP, Git", certs="None stated",
    hard="Skilled Worker salary thresholds apply", locfit=SPON, conf="Medium", lstatus="Active (search-verified)",
    jd="~50 entry-level consultant SWEs for 2027; covers Skilled Worker visa / ILR costs (per company page).",
    notes="Best-confirmed sponsorship lead found.")

add(id="JOB-0072", pri="P4", title="Software Engineering Graduate (Sep 2027)", cat=C4, company="Saab UK",
    website="https://www.saab.com", url="https://huntukvisasponsors.com/job/software-engineering-graduate-at-saab-uk-gmsz-jc7vlj5",
    source="Hunt UK Visa Sponsors", location="United Kingdom", country="United Kingdom", locgroup="Other International",
    mode="On-site", exp="Graduate", minexp=0, level="Graduate Program", emp="Full-time", salary="Not disclosed", cur="GBP",
    visa="Unknown (licensed sponsor; CoS at employer discretion)", reloc="Unknown", remote_india="N/A", edu="Degree",
    req="OOP, Testing", certs="None stated", hard="Defence employer - security clearance/nationality rules likely",
    locfit=SPON_UNK, conf="Low", lstatus="Active (search-verified)", jd="Software graduate programme starting Sep 2027.", notes="")

add(id="JOB-0073", pri="P4", title="Software Engineer - New Grad", cat=C4, company="Scale AI",
    website="https://scale.com", url="https://tarve.co.uk/jobs/software-engineer-new-grad-scale-ai-12007135",
    source="Tarve (aggregator)", location="London", country="United Kingdom", locgroup="Other International", mode="On-site",
    exp="New grad (Fall 2026 / Spring 2027)", minexp=0, level="Graduate Program", emp="Full-time", salary="Not disclosed", cur="GBP",
    visa="Unknown", reloc="Unknown", remote_india="N/A", edu="Degree", req="Data Structures and Algorithms, Python",
    certs="None stated", hard="Graduation window", locfit=SPON_UNK, conf="Low", lstatus="Active (search-verified)",
    jd="New-grad SWE, London.", notes="")

add(id="JOB-0074", pri="P4", title="Software Engineer (Nucleus Graduate Programme)", cat=C4, company="Singtel",
    website="https://www.singtel.com",
    url="https://groupcareers.singtel.com/job/Software-Engineer-(Nucleus-Graduate-Programme)-Sing/1059572966/",
    source="Company Careers", location="Singapore", country="Singapore", locgroup="Other International", mode="On-site",
    exp="Graduate", minexp=0, level="Graduate Program", emp="Full-time", salary="Not disclosed", cur="SGD",
    visa="Unknown", reloc="Unknown", remote_india="N/A", edu="Degree", req="Data Structures and Algorithms, OOP",
    certs="None stated", hard="Employment Pass needed", locfit=SPON_UNK, posted="2025-12-15", conf="Medium",
    lstatus="Possibly Closed", jd="Graduate SWE programme.", notes="Dec 2025 posting.")

add(id="JOB-0075", pri="P4", title="Junior Python Developer", cat=C4, company="Cuculus",
    website="", url="https://startupjobs.htgf.de/companies/cuculus/jobs/91451201-junior-python-developer",
    source="HTGF startup jobs", location="Germany (verify city)", country="Germany", locgroup="Germany", mode="Unknown",
    exp="Junior", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="EUR",
    visa="Unknown", reloc="Unknown", remote_india="N/A", edu="Unknown", req="Python, Git, REST APIs",
    certs="None stated", hard="Work authorization needed", locfit=SPON_UNK, conf="Low", lstatus="Active (search-verified)",
    jd="Junior Python developer.", notes="")

# ------------------------------------------------------------------ P5 SECURITY
add(id="JOB-0076", pri="P5", title="Junior DevSecOps Engineer", cat=C5, company="Checkmarx",
    website="https://checkmarx.com", url="https://checkmarx.com/job-openings/position/AA.B6D/",
    source="Company Careers", location="Pune", country="India", locgroup="India", mode="Unknown",
    exp="1-2 years (DevOps/SRE/platform with security focus)", minexp=1, level="Early-Career (1-3 yrs)", emp="Full-time",
    salary="Not disclosed", cur="INR", visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="DevSecOps, CI/CD, Docker, Kubernetes, Cloud", certs="None stated", hard="None stated", locfit=IN_OK,
    conf="Medium", lstatus="Active (search-verified)", jd="Checkmarx One platform engineering DevOps group.",
    notes="Bridges P1 and P5 - worth prioritising.")

add(id="JOB-0077", pri="P5", title="Software Development Engineer (DevSecOps)", cat=C5, company="Zscaler",
    website="https://www.zscaler.com", url="https://builtinbengaluru.in/job/software-development-engineer-devsecops/10039721",
    source="Built In Bengaluru", location="Bengaluru", country="India", locgroup="India", mode="Unknown",
    exp="1-2 years", minexp=1, level="Early-Career (1-3 yrs)", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="DevSecOps, CI/CD, Python, Cloud Security", certs="None stated", hard="None stated", locfit=IN_OK,
    conf="Medium", lstatus="Active (search-verified)", jd="Junior-level SDE in DevSecOps.", notes="")

add(id="JOB-0078", pri="P5", title="Software Engineer - I - DevSecOps", cat=C5, company="Orange Health Labs",
    website="https://www.orangehealth.in",
    url="https://jobs.generalcatalyst.com/companies/orange-health-labs/jobs/96906598-software-engineer-i-devsecops",
    source="General Catalyst job board", location="Bengaluru", country="India", locgroup="India", mode="Unknown",
    exp="SE-I (entry)", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="DevSecOps, CI/CD, Cloud, Linux", certs="None stated", hard="None stated", locfit=IN_OK, conf="Medium",
    lstatus="Active (search-verified)", jd="Entry DevSecOps engineer at a health-tech startup.", notes="")

add(id="JOB-0079", pri="P5", title="SOC Trainee / Fresher", cat=C5, company="Secure Network Solutions",
    website="", url="https://in.indeed.com/q-fresher-soc-analyst-l-tamil-nadu-jobs.html", source="Indeed India",
    location="Chennai", country="India", locgroup="India", mode="On-site", exp="Fresher / trainee", minexp=0,
    level="Entry-Level", emp="Full-time", salary="~3.75 LPA", cur="INR", visa="Not required (India)", reloc="Unknown",
    remote_india="N/A", edu="Degree", req="Networking, SIEM, SOC Operations", pref="Firewalls", certs="CCNA",
    hard="CCNA mandatory", locfit=IN_OK, posted="2026-09-24", conf="Low", lstatus="Active (search-verified)",
    jd="SOC trainee; basic firewall and endpoint security knowledge.", notes="Direct link not captured - search on Indeed.")

add(id="JOB-0080", pri="P5", title="SOC Analyst I", cat=C5, company="Alvaria",
    website="https://www.alvaria.com", url="https://in.indeed.com/q-soc-analyst-fresher-entry-level-junior-trainee-jobs.html",
    source="Indeed India", location="Bengaluru", country="India", locgroup="India", mode="Unknown",
    exp="1+ year cybersecurity/technical", minexp=1, level="Early-Career (1-3 yrs)", emp="Full-time",
    salary="Not disclosed", cur="INR", visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="SIEM, Incident Response, Networking, Threat Detection", certs="None stated", hard="None stated", locfit=IN_OK,
    conf="Low", lstatus="Active (search-verified)", jd="Entry SOC analyst.", notes="Direct link not captured.")

add(id="JOB-0081", pri="P5", title="Cyber Architecture - AWS Cloud Security & DevSecOps - Staff", cat=C5, company="EY (GDS)",
    website="https://www.ey.com",
    url="https://jobs.anitab.org/companies/ey-2/jobs/83301418-tc-cs-cyber-architecture-ot-and-engineering-aws-cloud-security-and-devsecops-staff",
    source="AnitaB.org job board", location="India (EY GDS)", country="India", locgroup="India", mode="Unknown",
    exp="Unknown (Staff = junior grade at EY)", minexp="", level="Early-Career (1-3 yrs)", emp="Full-time",
    salary="Not disclosed", cur="INR", visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="AWS, Cloud Security, DevSecOps, IAM", clouds="AWS", certs="None stated", hard="None stated", locfit=IN_OK,
    conf="Medium", lstatus="Active (search-verified)", jd="AWS cloud security and DevSecOps in EY Technology Consulting.", notes="")

add(id="JOB-0082", pri="P5", title="Product Security Engineer", cat=C5, company="Cloudflare",
    website="https://www.cloudflare.com", url="https://jobsbyculture.com/jobs/cloudflare/product-security-engineer",
    source="JobsByCulture (aggregator)", location="Bengaluru", country="India", locgroup="India", mode="Hybrid",
    exp="Unknown", minexp="", level="Experienced", emp="Full-time", salary="Not disclosed", cur="INR",
    visa="Not required (India)", reloc="Unknown", remote_india="N/A", edu="Unknown",
    req="OWASP, Security Automation, Python", certs="None stated", hard="None stated", locfit=IN_OK, conf="Low",
    lstatus="Active (search-verified)", jd="Product security at Cloudflare.", notes="Level unknown - likely mid-level.")

add(id="JOB-0083", pri="P5", title="SOC Intern", cat=C5, company="Eyne Tech Services",
    website="", url="https://www.glassdoor.co.in/Job/india-soc-analyst-jobs-SRCH_IL.0,5_IN115_KO6,17.htm", source="Glassdoor",
    location="India (verify)", country="India", locgroup="India", mode="Unknown", exp="Intern", minexp=0,
    level="Internship", emp="Internship", salary="Not disclosed", cur="INR", visa="Not required (India)", reloc="Unknown",
    remote_india="N/A", edu="Unknown", req="SIEM, Networking, SOC Operations", certs="None stated", hard="None stated",
    locfit=IN_OK, conf="Low", lstatus="Active (search-verified)", jd="SOC internship.", notes="")

# ---- AI (P3) extra: Qubrid backend AI as P4
add(id="JOB-0084", pri="P4", title="Junior Back End Engineer - AI (WFH)", cat=C4, company="Qubrid AI",
    website="", url="https://www.ziprecruiter.in/jobs/544801178-junior-back-end-engineer-ai-wfh-at-qubrid-ai",
    source="ZipRecruiter India", location="Remote - India", country="India", locgroup="Remote - India Eligible", mode="Remote",
    exp="Junior", minexp=0, level="Entry-Level", emp="Full-time", salary="Not disclosed", cur="INR", visa="N/A",
    reloc="N/A", remote_india="Yes - WFH India", edu="Unknown", req="Python, REST APIs, FastAPI", certs="None stated",
    hard="None stated", locfit=REM_OK, posted="2026-06-15", conf="Low", lstatus="Possibly Closed",
    jd="Junior backend for AI products.", notes="FastAPI inferred from 'backend for AI' - open JD.")

# Shortlist for JD analysis (job ids)
SHORTLIST = ["JOB-0003", "JOB-0001", "JOB-0022", "JOB-0002", "JOB-0009", "JOB-0024", "JOB-0076", "JOB-0055",
             "JOB-0050", "JOB-0029", "JOB-0071", "JOB-0059", "JOB-0043", "JOB-0007", "JOB-0030"]
