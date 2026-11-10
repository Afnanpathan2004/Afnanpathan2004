import datetime as dt
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.formula import ArrayFormula
from openpyxl.formatting.rule import FormulaRule, CellIsRule
from openpyxl.chart import PieChart, BarChart, LineChart, Reference
from openpyxl.chart.label import DataLabelList as _DLL
def DataLabelList():
    d = _DLL(); d.showVal = False; d.showCatName = False; d.showSerName = False; d.showLegendKey = False; d.showPercent = False
    return d
from openpyxl.comments import Comment

import jobs_data as JD_
from ref_data import PROFILE, SM, RES, CO, JD

OUT = sys.argv[1] if len(sys.argv) > 1 else "Job_Hunt_Tracker.xlsx"
TODAY = dt.date(2026, 11, 10)
FONT = "Arial"
CAP = 600                      # master table capacity rows
M0, M1 = 5, 4 + CAP            # master data rows
NAVY, TEAL, GREY, LIGHT = "1F3864", "0E6E6E", "F2F2F2", "DDEBF7"

def f(bold=False, size=10, color="000000", italic=False):
    return Font(name=FONT, bold=bold, size=size, color=color, italic=italic)
def fill(c): return PatternFill("solid", start_color=c, end_color=c)
thin = Side(style="thin", color="BFBFBF")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)

wb = Workbook()
def sheet(name, first=False):
    ws = wb.active if first else wb.create_sheet(name)
    ws.title = name
    ws.sheet_view.showGridLines = False
    return ws

def title(ws, text, sub=None, width_to=12):
    ws["A1"] = text; ws["A1"].font = f(True, 16, NAVY)
    if sub:
        ws["A2"] = sub; ws["A2"].font = f(False, 9, "595959", True)

def header(ws, row, cols, formula_cols=()):
    for i, h in enumerate(cols, 1):
        c = ws.cell(row, i, h)
        c.font = f(True, 10, "FFFFFF")
        c.fill = fill(TEAL if h in formula_cols else NAVY)
        c.alignment = CENTER; c.border = BOX

def add_table(ws, name, ref, style="TableStyleLight9"):
    t = Table(displayName=name, ref=ref)
    t.tableStyleInfo = TableStyleInfo(name=style, showRowStripes=True)
    ws.add_table(t)

def dv_list(ws, rng, src, strict=True, prompt=None):
    dv = DataValidation(type="list", formula1=src, allow_blank=True,
                        errorStyle="stop" if strict else "warning", showErrorMessage=True)
    if prompt: dv.prompt = prompt; dv.showInputMessage = True
    ws.add_data_validation(dv); dv.add(rng)

# =====================================================================================  LISTS
STATUSES = ["Not Applied", "Researching", "Interested", "Shortlisted", "Applied", "Assessment Pending",
            "Assessment Completed", "Interview Scheduled", "Interview In Progress", "HR Round", "Technical Round",
            "Managerial Round", "Offer Received", "Accepted", "Rejected", "Withdrawn", "On Hold", "Job Closed", "No Response"]
STAGE_OF = {"Not Applied": "Discovered", "Researching": "Researching", "Interested": "Interested",
            "Shortlisted": "Ready to Apply", "Applied": "Applied", "Assessment Pending": "Assessment",
            "Assessment Completed": "Assessment", "Interview Scheduled": "Interview", "Interview In Progress": "Interview",
            "Technical Round": "Interview", "Managerial Round": "Interview", "HR Round": "HR",
            "Offer Received": "Offer", "Accepted": "Accepted", "Rejected": "Rejected", "Withdrawn": "Inactive",
            "On Hold": "Inactive", "Job Closed": "Inactive", "No Response": "Inactive"}
STAGES = ["Discovered", "Researching", "Interested", "Ready to Apply", "Applied", "Assessment", "Interview",
          "HR", "Offer", "Accepted", "Rejected", "Inactive"]
CATS = [JD_.C1, JD_.C2, JD_.C3, JD_.C4, JD_.C5]
LISTS = {
    "Priority": ["P1", "P2", "P3", "P4", "P5"], "Job Category": CATS,
    "Work Mode": ["Remote", "Hybrid", "On-site", "Unknown"],
    "Job Level": ["Internship", "Apprenticeship", "Graduate Program", "Entry-Level", "Early-Career (1-3 yrs)", "Experienced"],
    "Employment Type": ["Full-time", "Contract", "Internship", "Internship / Working Student", "Internship / Full-time",
                        "Apprenticeship (12 months)", "Part-time"],
    "Visa Sponsorship": ["Yes", "No", "Unknown", "Not required (India)", "N/A (remote)"],
    "Relocation": ["Yes", "No", "Unknown", "N/A"],
    "Location Group": ["India", "Remote - India Eligible", "Remote - Restricted / Unclear", "Germany", "UAE", "Other International"],
    "Location Fit": [JD_.IN_OK, JD_.REM_OK, JD_.SPON, JD_.SPON_UNK, JD_.NOT_OK],
    "Data Confidence": ["High", "Medium", "Low"],
    "Listing Status": ["Active (search-verified)", "Active (page verified)", "Possibly Closed", "Closed / Expired"],
    "Yes/No/Unknown": ["Yes", "No", "Unknown"], "Yes/No": ["Yes", "No"],
    "Interview Round": ["Recruiter Screening", "Online Assessment", "Technical Round 1", "Technical Round 2",
                        "System Design", "Managerial", "HR", "Final Interview"],
    "Interview Format": ["Phone", "Video", "On-site", "Online Assessment", "Take-home", "Group Discussion"],
    "Interview Result": ["Scheduled", "Awaiting Result", "Passed", "Failed", "Cancelled", "Rescheduled"],
    "Rating": ["1", "2", "3", "4", "5"],
    "Contact Method": ["Email", "LinkedIn", "Phone", "Portal Message", "Referral", "WhatsApp"],
    "Follow-up Status": ["Pending", "Sent", "Replied", "No Response", "Closed"],
    "Proficiency": ["None", "Beginner", "Intermediate", "Advanced", "Expert"],
    "Filter All": ["All"],
}
lst = sheet("Lists", first=True)
lst["A1"], lst["B1"] = "Application Status", "Pipeline Stage"
for c in ("A1", "B1"): lst[c].font = f(True)
for i, s in enumerate(STATUSES, 2):
    lst.cell(i, 1, s); lst.cell(i, 2, STAGE_OF[s])
LREF = {"Application Status": f"Lists!$A$2:$A${1+len(STATUSES)}"}
col = 4
for name, vals in LISTS.items():
    lst.cell(1, col, name).font = f(True)
    for i, v in enumerate(vals, 2): lst.cell(i, col, v)
    LREF[name] = f"Lists!${L(col)}$2:${L(col)}${1+len(vals)}"
    lst.column_dimensions[L(col)].width = 26
    col += 1
# "All" + values lists for search filters
for name in ["Priority", "Job Category", "Location Group"]:
    vals = ["All"] + LISTS[name]
    lst.cell(1, col, name + " (filter)").font = f(True)
    for i, v in enumerate(vals, 2): lst.cell(i, col, v)
    LREF[name + " F"] = f"Lists!${L(col)}$2:${L(col)}${1+len(vals)}"
    col += 1
vals = ["All"] + STATUSES
lst.cell(1, col, "Status (filter)").font = f(True)
for i, v in enumerate(vals, 2): lst.cell(i, col, v)
LREF["Status F"] = f"Lists!${L(col)}$2:${L(col)}${1+len(vals)}"
lst.column_dimensions["A"].width = 24; lst.column_dimensions["B"].width = 18
lst.sheet_properties.tabColor = "808080"

# =====================================================================================  MY PROFILE
P = "'My Profile'!"
pf = sheet("My Profile")
title(pf, "My Profile & Scoring Settings",
      "Pre-filled from your GitHub profile README (self-rating estimates). Edit the yellow cells - every match score recalculates.")
pf["A3"] = "SETTINGS"; pf["A3"].font = f(True, 11, NAVY)
settings = [("My years of professional experience", 0),
            ("Do I hold / am I completing a Bachelor's in CS/IT/related? (Yes/No)", "Yes"),
            ("My certifications (comma-separated, e.g. AWS SAA, CKA)", ""),
            ("My base location", "India"),
            ("Open to relocation? (Yes/No)", "Yes")]
for i, (k, v) in enumerate(settings, 4):
    pf.cell(i, 1, k).font = f(); c = pf.cell(i, 2, v); c.fill = fill("FFFF00"); c.font = f(color="0000FF"); c.border = BOX
pf["B5"].comment = Comment("ASSUMPTION: your degree is not stated in your README. Change to No if this is wrong.", "Tracker")
pf["B4"].comment = Comment("ASSUMPTION: 0 years (fresher). Enter full-time experience in years, e.g. 0.5.", "Tracker")
dv_list(pf, "B5", '"Yes,No"'); dv_list(pf, "B8", '"Yes,No"')
pf["D3"], pf["E3"] = "MATCH WEIGHTS (%)", ""
pf["D3"].font = f(True, 11, NAVY)
weights = [("Technical Skills Match", 40), ("Experience Compatibility", 20), ("Educational Eligibility", 10),
           ("Location / Work Authorization", 15), ("Preferred Skills Match", 10), ("Certifications", 5)]
for i, (k, v) in enumerate(weights, 4):
    pf.cell(i, 4, k).font = f(); c = pf.cell(i, 5, v); c.fill = fill("FFFF00"); c.font = f(color="0000FF"); c.border = BOX
pf["D10"] = "Total (must be 100)"; pf["D10"].font = f(True)
pf["E10"] = "=SUM(E4:E9)"; pf["E10"].font = f(True)
pf["G3"] = "LOCATION / WORK-AUTH SCORE"; pf["G3"].font = f(True, 11, NAVY)
for i, (k, v) in enumerate([(JD_.IN_OK, 1), (JD_.REM_OK, 1), (JD_.SPON, 0.85), (JD_.SPON_UNK, 0.4), (JD_.NOT_OK, 0)], 4):
    pf.cell(i, 7, k).font = f(); c = pf.cell(i, 8, v); c.fill = fill("FFFF00"); c.font = f(color="0000FF"); c.number_format = "0%"
pf["J3"] = "PROFICIENCY SCALE"; pf["J3"].font = f(True, 11, NAVY)
for i, (k, v) in enumerate([("None", 0), ("Beginner", 1), ("Intermediate", 2), ("Advanced", 3), ("Expert", 4)], 4):
    pf.cell(i, 10, k).font = f(); pf.cell(i, 11, v).font = f()
PH = ["Skill", "Skill Group", "My Proficiency", "Level (0-4)", "Listings Requiring (all)", "Listings Preferring (all)",
      "% of All Listings", "Demand Rank Helper", "Gap Weight", "Gap Rank Helper"]
header(pf, 12, PH, formula_cols=PH[3:])
S0, S1 = 13, 200
for r in range(S0, S1 + 1):
    i = r - S0
    if i < len(PROFILE):
        s, g, p = PROFILE[i]
        pf.cell(r, 1, s); pf.cell(r, 2, g); pf.cell(r, 3, p).font = f(color="0000FF")
    pf.cell(r, 4, f'=IF(A{r}="","",IFERROR(INDEX($K$4:$K$8,MATCH(C{r},$J$4:$J$8,0)),0))')
    pf.cell(r, 5, f'=IF(A{r}="","",SUMPRODUCT(--ISNUMBER(SEARCH(", "&A{r}&",",", "&tblJobs[Required Skills]&","))))')
    pf.cell(r, 6, f'=IF(A{r}="","",SUMPRODUCT(--ISNUMBER(SEARCH(", "&A{r}&",",", "&tblJobs[Preferred Skills]&","))))')
    pf.cell(r, 7, f'=IF(A{r}="","",IFERROR(E{r}/COUNTIF(tblJobs[Job Title],"?*"),0))').number_format = "0%"
    pf.cell(r, 8, f'=IF(A{r}="",-1,E{r}+({S1}-ROW())/100000)')
    pf.cell(r, 9, f'=IF(A{r}="",0,IF(D{r}>=2,0,(E{r}+0.5*F{r})*(2-D{r})))')
    pf.cell(r, 10, f'=IF(OR(A{r}="",I{r}=0),-1,I{r}+({S1}-ROW())/100000)')
    for c in range(1, 11): pf.cell(r, c).border = BOX
    for c in range(4, 11): pf.cell(r, c).fill = fill(GREY)
add_table(pf, "tblProfile", f"A12:J{S1}")
dv_list(pf, f"C{S0}:C{S1}", LREF["Proficiency"])
for c, w in zip("ABCDEFGHIJK", [34, 18, 16, 11, 14, 14, 11, 10, 10, 10, 8]): pf.column_dimensions[c].width = w
pf.column_dimensions["D"].width = 30; pf.column_dimensions["G"].width = 34
pf.freeze_panes = "A13"
pf.sheet_properties.tabColor = "FFC000"
SK = f"{P}$A${S0}:$A${S1}"; SKL = f"{P}$D${S0}:$D${S1}"

# =====================================================================================  MASTER JOB TRACKER
MT = "'Master Job Tracker'!"
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
CL = {k: L(i) for i, (_, k, _, _) in enumerate(MC, 1)}
HN = {k: h for h, k, _, _ in MC}
NC = len(MC)
def T(k): return f"tblJobs[{HN[k]}]"          # structured reference

mt = sheet("Master Job Tracker")
title(mt, "Master Job Tracker",
      "Navy headers = your input  |  Teal headers = automatic formulas (do not overwrite)  |  Use the filter arrows to filter by category, company, location or status.")
mt["A3"] = "Next free Job ID:"; mt["A3"].font = f(True, 9)
mt["C3"] = ArrayFormula("C3", f'="JOB-"&TEXT(MAX(IFERROR(--MID($A${M0}:$A${M1},5,4),0))+1,"0000")')
mt["C3"].font = f(True, 9, "C00000")
mt["D3"] = "New rows: type the Job Title and the Job ID fills in automatically. Avoid sorting once interviews are linked (see README)."
mt["D3"].font = f(False, 9, "595959", True)
header(mt, 4, [h for h, *_ in MC], formula_cols={h for h, _, _, fm in MC if fm})

def norm_visa(v):
    if v.startswith("Yes"): return "Yes"
    if v.startswith("No"): return "No"
    if v.startswith("Not required"): return "Not required (India)"
    if v.startswith("N/A"): return "N/A (remote)"
    return "Unknown"
def norm_rel(v):
    if v.startswith("Yes"): return "Yes"
    if v.startswith("No"): return "No"
    if v.startswith("N/A"): return "N/A"
    return "Unknown"
def todate(s): return dt.date.fromisoformat(s) if s else None

known = {p[0].lower() for p in PROFILE}
unknown_tokens = set()
jobs = JD_.J
for idx in range(CAP):
    r = M0 + idx
    j = jobs[idx] if idx < len(jobs) else None
    if j:
        notes = j["notes"]
        if norm_visa(j["visa"]) != j["visa"] and j["visa"] not in ("Unknown",):
            notes = (f"Visa detail: {j['visa']}. " + notes).strip()
        if norm_rel(j["reloc"]) != j["reloc"] and j["reloc"] not in ("Unknown",):
            notes = (f"Relocation detail: {j['reloc']}. " + notes).strip()
        for tok in [t.strip() for t in (j["req"] + "," + j["pref"]).split(",") if t.strip()]:
            if tok.lower() not in known: unknown_tokens.add(tok)
        vals = dict(j)
        vals.update(visa=norm_visa(j["visa"]), reloc=norm_rel(j["reloc"]), notes=notes, edu_ok="Unknown",
                    disc=TODAY, verified=TODAY, deadline=todate(j["deadline"]), posted=todate(j["posted"]),
                    status="Job Closed" if j["lstatus"] == "Closed / Expired" else "Not Applied",
                    cover="No", resume="", minexp=j["minexp"] if j["minexp"] != "" else None)
        for k in ("rname", "rlink", "applied", "fup", "expsal", "offer"): vals[k] = None
        for h, k, _, fm in MC:
            if not fm and k != "id":
                v = vals.get(k)
                mt[f"{CL[k]}{r}"] = v if v != "" else None
        mt[f"A{r}"] = j["id"]
        if j["url"]: mt[f"{CL['url']}{r}"].hyperlink = j["url"]; mt[f"{CL['url']}{r}"].font = f(color="0563C1")
        if j["website"]: mt[f"{CL['website']}{r}"].hyperlink = j["website"]; mt[f"{CL['website']}{r}"].font = f(color="0563C1")
    else:
        mt[f"A{r}"] = f'=IF($C{r}="","","JOB-"&TEXT(ROW()-{M0-1},"0000"))'
    c = CL
    blank = f'$C{r}=""'
    req, pref = f"${c['req']}{r}", f"${c['pref']}{r}"
    def skillsum(cell, weighted):
        base = f'ISNUMBER(SEARCH(", "&{SK}&",",", "&{cell}&","))*({SK}<>"")'
        return f"SUMPRODUCT({base}*(({SKL}>=2)+0.5*({SKL}=1)))" if weighted else f"SUMPRODUCT({base})"
    IT = "'Interview Tracker'!"
    F = {
     "istatus": f'=IF({blank},"",IFERROR(LOOKUP(2,1/({IT}$B$5:$B$1004=$A{r}),{IT}$E$5:$E$1004),"No interviews yet"))',
     "nextint": f'=IF({blank},"",IFERROR(1/(1/_xlfn.MINIFS({IT}$F$5:$F$1004,{IT}$B$5:$B$1004,$A{r},{IT}$F$5:$F$1004,">="&TODAY())),""))',
     "s_tech": f'=IF({blank},"",IF({skillsum(req,False)}=0,0.5,{skillsum(req,True)}/{skillsum(req,False)}))',
     "s_exp": f'=IF({blank},"",IF(${c["minexp"]}{r}="",0.5,IF(${c["minexp"]}{r}<={P}$B$4,1,IF(${c["minexp"]}{r}-{P}$B$4<=1,0.75,IF(${c["minexp"]}{r}-{P}$B$4<=2,0.45,IF(${c["minexp"]}{r}-{P}$B$4<=3,0.2,0))))))',
     "s_edu": f'=IF({blank},"",IF(${c["edu_ok"]}{r}="Yes",1,IF(${c["edu_ok"]}{r}="No",0,IF({P}$B$5="Yes",0.9,0.6))))',
     "s_loc": f'=IF({blank},"",IFERROR(INDEX({P}$H$4:$H$8,MATCH(${c["locfit"]}{r},{P}$G$4:$G$8,0)),0.4))',
     "s_pref": f'=IF({blank},"",IF({skillsum(pref,False)}=0,0.5,{skillsum(pref,True)}/{skillsum(pref,False)}))',
     "s_cert": f'=IF({blank},"",IF(OR(${c["certs"]}{r}="",LEFT(${c["certs"]}{r},4)="None"),1,IF(ISNUMBER(SEARCH(${c["certs"]}{r},{P}$B$6)),1,0.4)))',
     "match": f'=IF({blank},"",(${c["s_tech"]}{r}*{P}$E$4+${c["s_exp"]}{r}*{P}$E$5+${c["s_edu"]}{r}*{P}$E$6+${c["s_loc"]}{r}*{P}$E$7+${c["s_pref"]}{r}*{P}$E$8+${c["s_cert"]}{r}*{P}$E$9)/{P}$E$10)',
     "band": f'=IF({blank},"",IF(${c["locfit"]}{r}="{JD_.NOT_OK}","Not Eligible - Hard Restriction",IF(${c["match"]}{r}>=0.8,"Strong Match",IF(${c["match"]}{r}>=0.65,"Good Match",IF(${c["match"]}{r}>=0.5,"Moderate Match","Low Match")))))',
     "active": f'=IF({blank},"",IF(OR(${c["lstatus"]}{r}="Closed / Expired",${c["status"]}{r}="Job Closed",AND(${c["deadline"]}{r}<>"",${c["deadline"]}{r}<TODAY())),"Expired/Closed",IF(${c["lstatus"]}{r}="Possibly Closed","Verify","Active")))',
     "dup": f'=IF({blank},"",IF(SUMPRODUCT(($E${M0}:$E${M1}=$E{r})*($C${M0}:$C${M1}=$C{r})*($I${M0}:$I${M1}=$I{r}))>1,"Possible Duplicate",IF(SUMPRODUCT(--(${c["url"]}${M0}:${c["url"]}${M1}=${c["url"]}{r}))>1,"Shared Source URL","Unique")))',
     "stage": f'=IF({blank},"",IFERROR(INDEX(Lists!$B$2:$B${1+len(STATUSES)},MATCH(${c["status"]}{r},Lists!$A$2:$A${1+len(STATUSES)},0)),"Discovered"))',
     "pkey": f'=IF({blank},"",${c["stage"]}{r}&"#"&COUNTIF(${c["stage"]}${M0}:${c["stage"]}{r},${c["stage"]}{r}))',
     "firstint": f'=IF({blank},"",IFERROR(1/(1/_xlfn.MINIFS({IT}$F$5:$F$1004,{IT}$B$5:$B$1004,$A{r})),""))',
     "d_int": f'=IF(OR(${c["firstint"]}{r}="",${c["applied"]}{r}=""),"",${c["firstint"]}{r}-${c["applied"]}{r})',
     "d_off": f'=IF(OR(${c["offer"]}{r}="",${c["applied"]}{r}=""),"",${c["offer"]}{r}-${c["applied"]}{r})',
     "ascore": f'=IF(OR({blank},${c["active"]}{r}="Expired/Closed",LEFT(${c["band"]}{r},3)="Not",ISNA(MATCH(${c["status"]}{r},{{"Not Applied","Researching","Interested","Shortlisted"}},0))),"",ROUND(${c["match"]}{r}*100+(6-VALUE(RIGHT($B{r},1)))*3+IF(${c["active"]}{r}="Active",2,0)+IF(${c["conf"]}{r}="High",2,IF(${c["conf"]}{r}="Medium",1,0)),2))',
     "arank": f'=IF(${c["ascore"]}{r}="","",COUNTIF(${c["ascore"]}${M0}:${c["ascore"]}${M1},">"&${c["ascore"]}{r})+COUNTIF(${c["ascore"]}${M0}:${c["ascore"]}{r},${c["ascore"]}{r}))',
     "sflag": (f"=IF({blank},0,IF(AND(OR('Job Search'!$C$4=\"\",ISNUMBER(SEARCH('Job Search'!$C$4,$C{r}&\" \"&$E{r}&\" \"&$I{r}&\" \"&${c['req']}{r}&\" \"&${c['tools']}{r}&\" \"&${c['pref']}{r}))),"
               f"OR('Job Search'!$C$5=\"All\",$D{r}='Job Search'!$C$5),OR('Job Search'!$C$6=\"All\",$B{r}='Job Search'!$C$6),"
               f"OR('Job Search'!$C$7=\"All\",${c['locgroup']}{r}='Job Search'!$C$7),OR('Job Search'!$C$8=\"All\",${c['status']}{r}='Job Search'!$C$8),"
               f"${c['match']}{r}>='Job Search'!$C$9,OR('Job Search'!$C$10=\"No\",${c['active']}{r}<>\"Expired/Closed\")),1,0))"),
     "srank": f'=IF(${c["sflag"]}{r}=0,"",SUMPRODUCT((${c["sflag"]}${M0}:${c["sflag"]}${M1}=1)*(${c["match"]}${M0}:${c["match"]}${M1}>${c["match"]}{r}))+SUMPRODUCT((${c["sflag"]}${M0}:${c["sflag"]}{r}=1)*(${c["match"]}${M0}:${c["match"]}{r}=${c["match"]}{r})))',
    }
    for k, fx in F.items():
        mt[f"{c[k]}{r}"] = fx
    mt[f"{c['missing']}{r}"] = ArrayFormula(f"{c['missing']}{r}",
        f'=IF({blank},"",_xlfn.TEXTJOIN(", ",TRUE,IF(ISNUMBER(SEARCH(", "&{SK}&",",", "&{req}&","))*({SK}<>"")*({SKL}<2),{SK},"")))')

# formatting master
for r in range(M0, M1 + 1):
    for i, (h, k, w, fm) in enumerate(MC, 1):
        cell = mt.cell(r, i)
        if k not in ("url", "website") or r >= M0 + len(jobs):
            cell.font = f()
        cell.border = BOX
        cell.alignment = Alignment(vertical="top", wrap_text=k in ("jd", "expdetail", "reqtype", "notes", "req", "missing", "title"))
        if fm: cell.fill = fill(GREY)
for k in ("deadline", "posted", "disc", "verified", "applied", "nextint", "fup", "firstint", "offer"):
    for r in range(M0, M1 + 1): mt[f"{CL[k]}{r}"].number_format = "dd-mmm-yyyy"
for k in ("s_tech", "s_exp", "s_edu", "s_loc", "s_pref", "s_cert", "match"):
    for r in range(M0, M1 + 1): mt[f"{CL[k]}{r}"].number_format = "0%"
for i, (h, k, w, fm) in enumerate(MC, 1): mt.column_dimensions[L(i)].width = w
mt.row_dimensions[4].height = 42
add_table(mt, "tblJobs", f"A4:{L(NC)}{M1}")
mt.freeze_panes = "D5"
for r in range(M0, M0 + len(jobs)): mt.row_dimensions[r].height = 45

# validations
R = lambda k: f"{CL[k]}{M0}:{CL[k]}{M1}"
dv_list(mt, R("pri"), LREF["Priority"]); dv_list(mt, R("cat"), LREF["Job Category"])
dv_list(mt, R("mode"), LREF["Work Mode"]); dv_list(mt, R("level"), LREF["Job Level"])
dv_list(mt, R("emp"), LREF["Employment Type"], strict=False); dv_list(mt, R("visa"), LREF["Visa Sponsorship"])
dv_list(mt, R("reloc"), LREF["Relocation"]); dv_list(mt, R("locgroup"), LREF["Location Group"])
dv_list(mt, R("locfit"), LREF["Location Fit"]); dv_list(mt, R("conf"), LREF["Data Confidence"])
dv_list(mt, R("lstatus"), LREF["Listing Status"]); dv_list(mt, R("status"), LREF["Application Status"])
dv_list(mt, R("edu_ok"), LREF["Yes/No/Unknown"]); dv_list(mt, R("cover"), LREF["Yes/No"])
for k in ("deadline", "posted", "disc", "verified", "applied", "fup", "offer"):
    dv = DataValidation(type="date", operator="greaterThan", formula1="DATE(2020,1,1)", allow_blank=True,
                        errorStyle="warning", error="Enter a valid date (e.g. 15-Nov-2026)")
    mt.add_data_validation(dv); dv.add(R(k))
dv = DataValidation(type="decimal", operator="between", formula1="0", formula2="30", allow_blank=True)
mt.add_data_validation(dv); dv.add(R("minexp"))

# conditional formatting - status colours
sc = CL["status"]; SR_ = R("status")
def cf_eq(rng, col_letter, values, color, font_color="000000"):
    cond = "OR(" + ",".join(f'${col_letter}{M0}="{v}"' for v in values) + ")"
    mt.conditional_formatting.add(rng, FormulaRule(formula=[cond], fill=fill(color), font=Font(name=FONT, color=font_color), stopIfTrue=True))
# orange first: follow-up due on an open application
fu = CL["fup"]
mt.conditional_formatting.add(SR_, FormulaRule(
    formula=[f'AND(${fu}{M0}<>"",${fu}{M0}<=TODAY(),OR(${sc}{M0}="Applied",${sc}{M0}="Assessment Pending",${sc}{M0}="Assessment Completed",${sc}{M0}="No Response",${sc}{M0}="On Hold"))'],
    fill=fill("F4B183"), font=Font(name=FONT, bold=True), stopIfTrue=True))
cf_eq(SR_, sc, ["Offer Received", "Accepted"], "C6EFCE", "006100")
cf_eq(SR_, sc, ["Rejected"], "FFC7CE", "9C0006")
cf_eq(SR_, sc, ["Interview Scheduled", "Interview In Progress", "Technical Round", "Managerial Round", "HR Round"], "BDD7EE", "1F3864")
cf_eq(SR_, sc, ["Applied", "Assessment Pending", "Assessment Completed"], "FFEB9C", "7F6000")
cf_eq(SR_, sc, ["No Response", "On Hold"], "F8CBAD")
cf_eq(SR_, sc, ["Not Applied", "Researching", "Interested", "Shortlisted"], "EDEDED", "404040")
cf_eq(SR_, sc, ["Job Closed", "Withdrawn"], "D9D9D9", "808080")
# follow-up date cell itself
mt.conditional_formatting.add(R("fup"), FormulaRule(formula=[f'AND(${fu}{M0}<>"",${fu}{M0}<=TODAY())'], fill=fill("F4B183")))
# expired deadline / closed rows: grey out title + red deadline
dl = CL["deadline"]; ac = CL["active"]
mt.conditional_formatting.add(R("deadline"), FormulaRule(formula=[f'AND(${dl}{M0}<>"",${dl}{M0}<TODAY())'], fill=fill("FFC7CE"), font=Font(name=FONT, color="9C0006", bold=True)))
mt.conditional_formatting.add(R("deadline"), FormulaRule(formula=[f'AND(${dl}{M0}<>"",${dl}{M0}>=TODAY(),${dl}{M0}-TODAY()<=7)'], fill=fill("FFEB9C")))
mt.conditional_formatting.add(f"C{M0}:C{M1}", FormulaRule(formula=[f'${ac}{M0}="Expired/Closed"'], font=Font(name=FONT, color="A6A6A6", strike=True)))
mt.conditional_formatting.add(R("active"), FormulaRule(formula=[f'${ac}{M0}="Expired/Closed"'], fill=fill("FFC7CE")))
mt.conditional_formatting.add(R("active"), FormulaRule(formula=[f'${ac}{M0}="Verify"'], fill=fill("FFEB9C")))
mt.conditional_formatting.add(R("active"), FormulaRule(formula=[f'${ac}{M0}="Active"'], fill=fill("C6EFCE")))
# match band
bd = CL["band"]
for txt, col_ in [("Strong", "63BE7B"), ("Good", "C6EFCE"), ("Moderate", "FFEB9C"), ("Low", "F8CBAD"), ("Not Eligible", "FF7C80")]:
    mt.conditional_formatting.add(R("band"), FormulaRule(formula=[f'LEFT(${bd}{M0},{len(txt)})="{txt}"'], fill=fill(col_)))
mt.conditional_formatting.add(R("match"), CellIsRule(operator="greaterThanOrEqual", formula=["0.8"], fill=fill("63BE7B")))
mt.conditional_formatting.add(R("match"), CellIsRule(operator="between", formula=["0.65", "0.7999"], fill=fill("C6EFCE")))
mt.conditional_formatting.add(R("match"), CellIsRule(operator="between", formula=["0.5", "0.6499"], fill=fill("FFEB9C")))
mt.conditional_formatting.add(R("match"), CellIsRule(operator="between", formula=["0.0001", "0.4999"], fill=fill("F8CBAD")))
# duplicates: Job ID + duplicate flag
mt.conditional_formatting.add(f"A{M0}:A{M1}", FormulaRule(formula=[f'AND($A{M0}<>"",COUNTIF($A${M0}:$A${M1},$A{M0})>1)'], fill=fill("FF0000"), font=Font(name=FONT, color="FFFFFF", bold=True)))
dp = CL["dup"]
mt.conditional_formatting.add(R("dup"), FormulaRule(formula=[f'${dp}{M0}="Possible Duplicate"'], fill=fill("FF7C80")))
mt.conditional_formatting.add(R("dup"), FormulaRule(formula=[f'${dp}{M0}="Shared Source URL"'], fill=fill("FFEB9C")))
cfc = CL["conf"]
for v, col_ in [("High", "C6EFCE"), ("Medium", "FFEB9C"), ("Low", "F8CBAD")]:
    mt.conditional_formatting.add(R("conf"), FormulaRule(formula=[f'${cfc}{M0}="{v}"'], fill=fill(col_)))
pc = "B"
for v, col_ in [("P1", "1F3864"), ("P2", "2E75B6"), ("P3", "7030A0"), ("P4", "548235"), ("P5", "C55A11")]:
    mt.conditional_formatting.add(R("pri"), FormulaRule(formula=[f'$B{M0}="{v}"'], fill=fill(col_), font=Font(name=FONT, color="FFFFFF", bold=True)))
mt.sheet_properties.tabColor = NAVY

# =====================================================================================  INTERVIEW TRACKER
it = sheet("Interview Tracker")
title(it, "Interview Tracker", "One row per interview round. Enter the Job ID - company and title fill in automatically. Interview ID auto-generates.")
IH = ["Interview ID", "Job ID", "Company", "Job Title", "Interview Round", "Interview Date", "Interview Time",
      "Interview Format", "Interviewer Name", "Interviewer Profile", "Topics Asked", "Technical Questions",
      "Coding Questions", "System Design Questions", "HR Questions", "My Performance Rating", "Weak Areas",
      "Feedback Received", "Result", "Next Round", "Next Interview Date", "Preparation Notes", "Upcoming Rank"]
IF_ = {"Interview ID", "Company", "Job Title", "Upcoming Rank"}
ex = ["EXAMPLE ->", "JOB-0003", "CME Group", "Site Reliability Engineer I - India", "Technical Round 1", "15-Dec-2026",
      "11:00 IST", "Video", "(name)", "(LinkedIn URL)", "Linux, networking, monitoring", "How does DNS resolution work?",
      "Parse a log file in Python", "-", "-", "3", "SLO maths", "Positive", "Passed", "Technical Round 2", "22-Dec-2026",
      "Revise Prometheus alert rules", ""]
for i, v in enumerate(ex, 1):
    cc = it.cell(3, i, v); cc.font = f(False, 8, "808080", True); cc.fill = fill("FAFAFA")
header(it, 4, IH, IF_)
for r in range(5, 1005):
    it[f"A{r}"] = f'=IF(B{r}="","","INT-"&TEXT(ROW()-4,"0000"))'
    it[f"C{r}"] = f'=IF(B{r}="","",IFERROR(INDEX(tblJobs[Company],MATCH(B{r},tblJobs[Job ID],0)),"Unknown Job ID"))'
    it[f"D{r}"] = f'=IF(B{r}="","",IFERROR(INDEX(tblJobs[Job Title],MATCH(B{r},tblJobs[Job ID],0)),""))'
    it[f"W{r}"] = (f'=IF(OR(F{r}="",F{r}<TODAY(),S{r}<>"Scheduled"),"",COUNTIFS($F$5:$F$1004,">="&TODAY(),$S$5:$S$1004,"Scheduled",$F$5:$F$1004,"<"&F{r})'
                   f'+COUNTIFS($F$5:F{r},F{r},$S$5:S{r},"Scheduled"))')
    for c in range(1, 24):
        cc = it.cell(r, c); cc.font = f(); cc.border = BOX; cc.alignment = Alignment(vertical="top", wrap_text=c in (11, 12, 13, 14, 15, 17, 18, 22))
        if IH[c - 1] in IF_: cc.fill = fill(GREY)
    it[f"F{r}"].number_format = "dd-mmm-yyyy"; it[f"U{r}"].number_format = "dd-mmm-yyyy"
add_table(it, "tblInterviews", "A4:W1004")
dv_list(it, "B5:B1004", f"{MT}$A${M0}:$A${M1}", strict=False)
dv_list(it, "E5:E1004", LREF["Interview Round"]); dv_list(it, "T5:T1004", LREF["Interview Round"])
dv_list(it, "H5:H1004", LREF["Interview Format"]); dv_list(it, "S5:S1004", LREF["Interview Result"])
dv_list(it, "P5:P1004", LREF["Rating"])
for v, col_ in [("Passed", "C6EFCE"), ("Failed", "FFC7CE"), ("Scheduled", "BDD7EE"), ("Awaiting Result", "FFEB9C"), ("Cancelled", "D9D9D9")]:
    it.conditional_formatting.add("S5:S1004", FormulaRule(formula=[f'$S5="{v}"'], fill=fill(col_)))
it.conditional_formatting.add("F5:F1004", FormulaRule(formula=['AND($F5<>"",$F5>=TODAY(),$F5-TODAY()<=3)'], fill=fill("F4B183"), font=Font(name=FONT, bold=True)))
for c, w in zip(range(1, 24), [11, 10, 20, 30, 18, 12, 10, 14, 16, 18, 26, 30, 26, 22, 22, 9, 22, 22, 13, 18, 12, 30, 9]):
    it.column_dimensions[L(c)].width = w
it.freeze_panes = "C5"
it.row_dimensions[4].height = 32

# =====================================================================================  SKILLS MATRIX
sm = sheet("Skills & Requirements Matrix")
title(sm, "Skills & Requirements Matrix",
      "Demand is counted live from the Required Skills column of every listing in the Master Job Tracker. Proficiency pulls from My Profile.")
SH = ["Skill", "Job Category", "Number of Job Listings Requiring It", "Percentage of Listings Requiring It",
      "Listings Preferring It", "All-Category Listings Requiring It", "Demand Level", "Beginner / Intermediate / Advanced",
      "My Current Proficiency", "Required Proficiency", "Skill Gap (levels)", "Learning Priority", "Related Courses",
      "Official Documentation", "Practice Resources", "Certification Options"]
SFm = {SH[i] for i in (2, 3, 4, 5, 6, 8, 10, 11)}
header(sm, 4, SH, SFm)
r = 5
for cat, rows in SM.items():
    for skill, diff, reqp in rows:
        res = RES.get(skill, ("-", "-", "-", "-"))
        sm[f"A{r}"], sm[f"B{r}"], sm[f"H{r}"], sm[f"J{r}"] = skill, cat, diff, reqp
        sm[f"C{r}"] = f'=SUMPRODUCT(ISNUMBER(SEARCH(", "&A{r}&",",", "&tblJobs[Required Skills]&","))*(tblJobs[Job Category]=B{r}))'
        sm[f"D{r}"] = f'=IFERROR(C{r}/COUNTIF(tblJobs[Job Category],B{r}),0)'
        sm[f"E{r}"] = f'=SUMPRODUCT(ISNUMBER(SEARCH(", "&A{r}&",",", "&tblJobs[Preferred Skills]&","))*(tblJobs[Job Category]=B{r}))'
        sm[f"F{r}"] = f'=SUMPRODUCT(--ISNUMBER(SEARCH(", "&A{r}&",",", "&tblJobs[Required Skills]&",")))'
        sm[f"G{r}"] = f'=IF(D{r}>=0.4,"Very High",IF(D{r}>=0.25,"High",IF(D{r}>=0.1,"Medium",IF(C{r}+E{r}>0,"Low","Not seen in sample"))))'
        sm[f"I{r}"] = f'=IFERROR(INDEX({P}$C${S0}:$C${S1},MATCH(A{r},{P}$A${S0}:$A${S1},0)),"None")'
        sm[f"K{r}"] = f'=MAX(0,MATCH(J{r},Lists!${L(4+list(LISTS).index("Proficiency"))}$2:${L(4+list(LISTS).index("Proficiency"))}$6,0)-MATCH(I{r},Lists!${L(4+list(LISTS).index("Proficiency"))}$2:${L(4+list(LISTS).index("Proficiency"))}$6,0))'
        sm[f"L{r}"] = f'=IF(K{r}=0,"Maintain",IF(AND(D{r}>=0.25,K{r}>=1),"High",IF(OR(D{r}>=0.1,AND(B{r}="Cloud & DevOps",C{r}+E{r}>=3)),"Medium","Low")))'
        sm[f"M{r}"], sm[f"N{r}"], sm[f"O{r}"], sm[f"P{r}"] = res
        if res[1].startswith("http"): sm[f"N{r}"].hyperlink = res[1]
        r += 1
SM1 = r - 1
for rr in range(5, SM1 + 1):
    for c in range(1, 17):
        cc = sm.cell(rr, c); cc.border = BOX; cc.alignment = Alignment(vertical="top", wrap_text=c >= 13)
        cc.font = f(color="0563C1") if c == 14 else f()
        if SH[c - 1] in SFm: cc.fill = fill(GREY)
    sm[f"D{rr}"].number_format = "0%"
add_table(sm, "tblSkills", f"A4:P{SM1}")
for v, col_ in [("High", "FF7C80"), ("Medium", "FFEB9C"), ("Low", "DDEBF7"), ("Maintain", "C6EFCE")]:
    sm.conditional_formatting.add(f"L5:L{SM1}", FormulaRule(formula=[f'$L5="{v}"'], fill=fill(col_)))
for v, col_ in [("Very High", "63BE7B"), ("High", "C6EFCE"), ("Medium", "FFEB9C")]:
    sm.conditional_formatting.add(f"G5:G{SM1}", FormulaRule(formula=[f'$G5="{v}"'], fill=fill(col_)))
from openpyxl.formatting.rule import DataBarRule
sm.conditional_formatting.add(f"D5:D{SM1}", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="5B9BD5"))
dv_list(sm, f"J5:J{SM1}", LREF["Proficiency"])
for c, w in zip("ABCDEFGHIJKLMNOP", [26, 24, 12, 12, 10, 12, 14, 14, 13, 13, 9, 11, 34, 36, 32, 28]):
    sm.column_dimensions[c].width = w
sm.row_dimensions[4].height = 45
sm.freeze_panes = "C5"

# =====================================================================================  COMPANY DATABASE
cd = sheet("Company Database")
title(cd, "Company Database", "Company intelligence. 'Jobs in Tracker' and 'Applications' count live from the Master Job Tracker using the Match Key.")
CH = ["Company Name", "Industry", "Company Website", "Careers Page", "Headquarters", "Major Hiring Locations",
      "Company Size", "Technology Stack", "Hiring Categories", "Fresher Hiring", "Internship Opportunities",
      "Remote Opportunities", "Visa Sponsorship", "Recruiter / Talent Acquisition Contact", "LinkedIn Company Page",
      "Current Hiring Status", "Notes", "Match Key", "Jobs in Tracker", "Active Jobs", "Applications", "Company Rank Helper"]
CF_ = {"Jobs in Tracker", "Active Jobs", "Applications", "Company Rank Helper"}
header(cd, 4, CH, CF_)
CD1 = 4 + len(CO) + 60
for i in range(len(CO) + 60):
    r = 5 + i
    if i < len(CO):
        row = CO[i]
        vals = list(row[:13]) + ["Not researched - find via LinkedIn 'People' tab"] + [row[13], row[14], row[15]]
        key = row[0].split(" /")[0].split(" (")[0]
        for c, v in enumerate(vals, 1):
            cd.cell(r, c, v)
        cd.cell(r, 18, key)
        for c in (3, 4, 15):
            v = cd.cell(r, c).value
            if isinstance(v, str) and v.startswith("http"): cd.cell(r, c).hyperlink = v
    cd.cell(r, 19, f'=IF(R{r}="","",COUNTIF(tblJobs[Company],"*"&R{r}&"*"))')
    cd.cell(r, 20, f'=IF(R{r}="","",COUNTIFS(tblJobs[Company],"*"&R{r}&"*",tblJobs[Active Flag],"Active"))')
    cd.cell(r, 21, f'=IF(R{r}="","",COUNTIFS(tblJobs[Company],"*"&R{r}&"*",tblJobs[Date Applied],">0"))')
    cd.cell(r, 22, f'=IF(R{r}="",-1,S{r}*100+U{r}*1000+({CD1}-ROW())/1000)')
    for c in range(1, 23):
        cc = cd.cell(r, c); cc.border = BOX; cc.alignment = Alignment(vertical="top", wrap_text=True)
        cc.font = f(color="0563C1") if c in (3, 4, 15) and i < len(CO) else f()
        if CH[c - 1] in CF_: cc.fill = fill(GREY)
add_table(cd, "tblCompanies", f"A4:V{CD1}")
for c, w in zip(range(1, 23), [22, 18, 24, 30, 18, 26, 14, 26, 26, 22, 12, 14, 18, 22, 30, 28, 32, 12, 9, 9, 9, 8]):
    cd.column_dimensions[L(c)].width = w
cd.freeze_panes = "B5"; cd.row_dimensions[4].height = 40
cd.conditional_formatting.add(f"J5:J{CD1}", FormulaRule(formula=['LEFT($J5,3)="Yes"'], fill=fill("C6EFCE")))
cd.conditional_formatting.add(f"M5:M{CD1}", FormulaRule(formula=['LEFT($M5,3)="Yes"'], fill=fill("C6EFCE")))

# =====================================================================================  APPLICATION PIPELINE
pp = sheet("Application Pipeline")
title(pp, "Application Pipeline (Kanban)", "Stages are derived automatically from Application Status. Change a job's status in the Master Job Tracker to move its card.")
pp["A4"] = "Stage"; pp["A5"] = "Jobs in stage"; pp["A6"] = "% of all jobs"
for c in ("A4", "A5", "A6"): pp[c].font = f(True)
STAGE_COL = {}
for i, s in enumerate(STAGES):
    c = L(2 + i); STAGE_COL[s] = c
    pp[f"{c}4"] = f"{i+1}. {s}" if s != "Inactive" else "12. Inactive (closed/withdrawn/on hold/no response)"
    pp[f"{c}4"].font = f(True, 10, "FFFFFF"); pp[f"{c}4"].fill = fill(NAVY if s not in ("Offer", "Accepted") else "548235")
    if s == "Rejected": pp[f"{c}4"].fill = fill("C00000")
    if s == "Inactive": pp[f"{c}4"].fill = fill("7F7F7F")
    pp[f"{c}4"].alignment = CENTER
    pp[f"{c}5"] = f'=COUNTIF(tblJobs[Pipeline Stage],"{s}")'
    pp[f"{c}5"].font = f(True, 16, NAVY); pp[f"{c}5"].alignment = CENTER
    pp[f"{c}6"] = f'=IFERROR({c}5/COUNTIF(tblJobs[Job Title],"?*"),0)'; pp[f"{c}6"].number_format = "0%"; pp[f"{c}6"].alignment = CENTER
    pp.column_dimensions[c].width = 26
    for n in range(1, 41):
        rr = 7 + n
        pp[f"{c}{rr}"] = (f'=IFERROR(INDEX(tblJobs[Job ID],MATCH("{s}#{n}",tblJobs[Pipeline Key],0))&" | "&INDEX(tblJobs[Company],MATCH("{s}#{n}",tblJobs[Pipeline Key],0))'
                          f'&" | "&INDEX(tblJobs[Job Title],MATCH("{s}#{n}",tblJobs[Pipeline Key],0)),"")')
        cc = pp[f"{c}{rr}"]; cc.font = f(size=8); cc.alignment = Alignment(wrap_text=True, vertical="top"); cc.border = BOX
        cc.fill = fill("F7F9FC")
pp["A8"] = "Cards (first 40 per stage)"; pp["A8"].font = f(True); pp["A8"].alignment = WRAP
pp.column_dimensions["A"].width = 16
pp.row_dimensions[4].height = 45
for rr in range(8, 48): pp.row_dimensions[rr].height = 36
pp.freeze_panes = "B7"
pp["A50"] = "Total jobs"; pp["B50"] = '=COUNTIF(tblJobs[Job Title],"?*")'; pp["A51"] = "Check (sum of stages)"; pp["B51"] = "=SUM(B5:M5)"
for c in ("A50", "A51", "B50", "B51"): pp[c].font = f(True)
ch = BarChart(); ch.type = "bar"; ch.title = "Jobs per pipeline stage"; ch.style = 10
ch.add_data(Reference(pp, min_col=2, max_col=13, min_row=5), from_rows=True, titles_from_data=False)
ch.set_categories(Reference(pp, min_col=2, max_col=13, min_row=4)); ch.legend = None
ch.height, ch.width = 9, 22
pp.add_chart(ch, "B53")

# =====================================================================================  DAILY LOG
dl_ = sheet("Daily Job Hunting Log")
title(dl_, "Daily Job Hunting Log", "Enter your daily numbers (blue). Weekly and monthly summaries on the right update automatically.")
DH = ["Date", "Jobs Discovered", "Jobs Reviewed", "Applications Submitted", "Recruiters Contacted", "Referrals Requested",
      "Assessments Completed", "Interviews Attended", "Follow-ups Sent", "Learning Hours", "Notes"]
ex = ["EXAMPLE ->", 12, 8, 3, 2, 1, 0, 0, 2, 2.5, "Applied to CME SRE I, MongoDB TSE"]
for i, v in enumerate(ex, 1):
    cc = dl_.cell(3, i, v); cc.font = f(False, 8, "808080", True)
header(dl_, 4, DH, {"Date"})
NDAYS = 400
for i in range(NDAYS):
    r = 5 + i
    dl_[f"A{r}"] = dt.date(2026, 11, 10) if i == 0 else f"=A{r-1}+1"
    dl_[f"A{r}"].number_format = "ddd dd-mmm-yy"
    for c in range(1, 12):
        cc = dl_.cell(r, c); cc.border = BOX; cc.font = f() if c == 1 else f(color="0000FF")
    dl_[f"A{r}"].fill = fill(GREY)
DL1 = 4 + NDAYS
add_table(dl_, "tblDaily", f"A4:K{DL1}")
dl_.conditional_formatting.add(f"A5:K{DL1}", FormulaRule(formula=["$A5=TODAY()"], fill=fill("FFF2CC"), font=Font(name=FONT, bold=True)))
for c, w in zip("ABCDEFGHIJK", [15, 10, 10, 11, 11, 10, 11, 10, 10, 9, 36]): dl_.column_dimensions[c].width = w
dl_.row_dimensions[4].height = 40
dl_.freeze_panes = "B5"
# summaries
metrics = DH[1:10]
dl_["M3"] = "WEEKLY SUMMARY (Mon-Sun)"; dl_["M3"].font = f(True, 11, NAVY)
header_w = ["Week Starting"] + metrics
for i, h in enumerate(header_w):
    cc = dl_.cell(4, 13 + i, h); cc.font = f(True, 9, "FFFFFF"); cc.fill = fill(TEAL); cc.alignment = CENTER
for w in range(56):
    r = 5 + w
    dl_.cell(r, 13, "=A5-WEEKDAY(A5,3)" if w == 0 else f"=M{r-1}+7").number_format = "dd-mmm-yy"
    for i in range(len(metrics)):
        src = L(2 + i)
        dl_.cell(r, 14 + i, f'=SUMIFS(${src}$5:${src}${DL1},$A$5:$A${DL1},">="&$M{r},$A$5:$A${DL1},"<"&$M{r}+7)')
    for c in range(13, 23): dl_.cell(r, c).font = f(size=9); dl_.cell(r, c).border = BOX
dl_.conditional_formatting.add("M5:V60", FormulaRule(formula=["AND(TODAY()>=$M5,TODAY()<$M5+7)"], fill=fill("FFF2CC")))
dl_["X3"] = "MONTHLY SUMMARY"; dl_["X3"].font = f(True, 11, NAVY)
for i, h in enumerate(["Month"] + metrics):
    cc = dl_.cell(4, 24 + i, h); cc.font = f(True, 9, "FFFFFF"); cc.fill = fill(TEAL); cc.alignment = CENTER
for m in range(14):
    r = 5 + m
    dl_.cell(r, 24, "=DATE(2026,11,1)" if m == 0 else f"=EDATE(X{r-1},1)").number_format = "mmm-yyyy"
    for i in range(len(metrics)):
        src = L(2 + i)
        dl_.cell(r, 25 + i, f'=SUMIFS(${src}$5:${src}${DL1},$A$5:$A${DL1},">="&$X{r},$A$5:$A${DL1},"<="&EOMONTH($X{r},0))')
    for c in range(24, 34): dl_.cell(r, c).font = f(size=9); dl_.cell(r, c).border = BOX
dl_["X20"] = "ALL-TIME TOTALS"; dl_["X20"].font = f(True)
for i in range(len(metrics)):
    src = L(2 + i)
    dl_.cell(20, 25 + i, f"=SUM({src}5:{src}{DL1})").font = f(True)
for c in range(13, 34): dl_.column_dimensions[L(c)].width = 10
dl_.column_dimensions["L"].width = 3

# =====================================================================================  JD ANALYSIS
ja = sheet("Job Description Analysis")
title(ja, "Job Description Analysis & Preparation Checklists",
      "'Stated' columns come from the listing text found in research. Teal columns are recommendations generated for your preparation. Missing skills update from My Profile.")
JH = ["Job ID", "Company", "Job Title", "Match %", "Required Qualifications (stated)", "Technical Requirements (stated)",
      "Soft Skills (stated)", "Years of Experience", "Mandatory Certifications", "Preferred Qualifications",
      "Responsibilities", "Interview Topics Likely to Be Tested", "ATS Keywords", "Resume Keywords",
      "Missing Skills (live)", "Recommended Preparation Topics", "Job-Specific Preparation Checklist", "Prep Status"]
JF = {"Company", "Job Title", "Match %", "Missing Skills (live)", "Interview Topics Likely to Be Tested",
      "ATS Keywords", "Resume Keywords", "Recommended Preparation Topics", "Job-Specific Preparation Checklist"}
header(ja, 4, JH, JF)
r = 5
for jid in JD_.SHORTLIST:
    d = JD[jid]
    ja[f"A{r}"] = jid
    ja[f"B{r}"] = f'=IFERROR(INDEX(tblJobs[Company],MATCH(A{r},tblJobs[Job ID],0)),"")'
    ja[f"C{r}"] = f'=IFERROR(INDEX(tblJobs[Job Title],MATCH(A{r},tblJobs[Job ID],0)),"")'
    ja[f"D{r}"] = f'=IFERROR(INDEX(tblJobs[Match Percentage],MATCH(A{r},tblJobs[Job ID],0)),"")'; ja[f"D{r}"].number_format = "0%"
    for c, k in zip("EFGHIJKLMN", ["q", "tech", "soft", "yrs", "cert", "pref", "resp", "topics", "ats", "resume"]):
        ja[f"{c}{r}"] = d[k]
    ja[f"O{r}"] = f'=IFERROR(INDEX(tblJobs[Missing Skills],MATCH(A{r},tblJobs[Job ID],0)),"")'
    ja[f"P{r}"] = f'=IF(O{r}="","Core skills covered - focus on interview practice and projects.","Close these gaps first: "&O{r})'
    topics = [t.strip() for t in d["topics"].split(";")]
    chk = ["Tailor resume with ATS keywords (col M)", "Map 2 projects to the responsibilities (col K)"] + \
          [f"Revise: {t}" for t in topics] + ["Prepare 3 STAR stories (ownership, failure, teamwork)",
           "Research company product & recent news", "Ask for a referral on LinkedIn", "Set follow-up date after applying"]
    ja[f"Q{r}"] = "\n".join("[ ] " + x for x in chk)
    ja[f"R{r}"] = "Not started"
    r += 1
JA1 = r - 1
for rr in range(5, JA1 + 1):
    ja.row_dimensions[rr].height = 190
    for c in range(1, 19):
        cc = ja.cell(rr, c); cc.font = f(size=9); cc.border = BOX; cc.alignment = WRAP
        if JH[c - 1] in JF: cc.fill = fill("EAF4F4")
add_table(ja, "tblJD", f"A4:R{JA1 + 30}")
dv_list(ja, f"A5:A{JA1+30}", f"{MT}$A${M0}:$A${M1}", strict=False)
dv = DataValidation(type="list", formula1='"Not started,In progress,Ready,Applied"', allow_blank=True)
ja.add_data_validation(dv); dv.add(f"R5:R{JA1+30}")
for rr in range(JA1 + 1, JA1 + 31):
    ja[f"B{rr}"] = f'=IF(A{rr}="","",IFERROR(INDEX(tblJobs[Company],MATCH(A{rr},tblJobs[Job ID],0)),""))'
    ja[f"C{rr}"] = f'=IF(A{rr}="","",IFERROR(INDEX(tblJobs[Job Title],MATCH(A{rr},tblJobs[Job ID],0)),""))'
    ja[f"D{rr}"] = f'=IF(A{rr}="","",IFERROR(INDEX(tblJobs[Match Percentage],MATCH(A{rr},tblJobs[Job ID],0)),""))'
    ja[f"D{rr}"].number_format = "0%"
    ja[f"O{rr}"] = f'=IF(A{rr}="","",IFERROR(INDEX(tblJobs[Missing Skills],MATCH(A{rr},tblJobs[Job ID],0)),""))'
    for c in range(1, 19): ja.cell(rr, c).font = f(size=9); ja.cell(rr, c).border = BOX
for c, w in zip(range(1, 19), [10, 16, 24, 8, 24, 28, 18, 10, 14, 18, 28, 32, 28, 28, 22, 26, 44, 12]):
    ja.column_dimensions[L(c)].width = w
ja.freeze_panes = "D5"; ja.row_dimensions[4].height = 45

# =====================================================================================  FOLLOW-UPS
fw = sheet("Follow-up & Reminders")
title(fw, "Follow-up & Reminders", "Enter a Job ID. Company, application date and recruiter fill in; next follow-up defaults to 7 days after the last contact (overwrite if needed). Overdue rows turn red.")
FH = ["Company", "Job ID", "Application Date", "Last Contact Date", "Next Follow-up Date", "Recruiter", "Contact Method",
      "Follow-up Status", "Days Overdue", "Follow-up Notes"]
ex = ["CME Group", "JOB-0003", "20-Nov-2026", "20-Nov-2026", "27-Nov-2026", "(recruiter)", "LinkedIn", "Pending", "", "Polite nudge + 1-line value add"]
for i, v in enumerate(["EXAMPLE -> " + ex[0]] + ex[1:], 1):
    cc = fw.cell(3, i, v); cc.font = f(False, 8, "808080", True)
header(fw, 4, FH, {"Company", "Application Date", "Next Follow-up Date", "Recruiter", "Days Overdue"})
FW1 = 304
for r in range(5, FW1 + 1):
    fw[f"A{r}"] = f'=IF(B{r}="","",IFERROR(INDEX(tblJobs[Company],MATCH(B{r},tblJobs[Job ID],0)),"Unknown Job ID"))'
    fw[f"C{r}"] = f'=IF(B{r}="","",IFERROR(1/(1/INDEX(tblJobs[Date Applied],MATCH(B{r},tblJobs[Job ID],0))),""))'
    fw[f"E{r}"] = f'=IF(B{r}="","",IF(D{r}<>"",D{r}+7,IF(C{r}<>"",C{r}+7,"")))'
    fw[f"F{r}"] = f'=IF(B{r}="","",IFERROR(INDEX(tblJobs[Recruiter Name],MATCH(B{r},tblJobs[Job ID],0))&"",""))'
    fw[f"I{r}"] = f'=IF(OR(E{r}="",H{r}="Replied",H{r}="Closed"),"",MAX(0,TODAY()-E{r}))'
    for c in range(1, 11):
        cc = fw.cell(r, c); cc.font = f(); cc.border = BOX
        if FH[c - 1] in ("Company", "Application Date", "Next Follow-up Date", "Recruiter", "Days Overdue"): cc.fill = fill(GREY)
    for c in "CDE": fw[f"{c}{r}"].number_format = "dd-mmm-yyyy"
add_table(fw, "tblFollowups", f"A4:J{FW1}")
dv_list(fw, f"B5:B{FW1}", f"{MT}$A${M0}:$A${M1}", strict=False)
dv_list(fw, f"G5:G{FW1}", LREF["Contact Method"]); dv_list(fw, f"H5:H{FW1}", LREF["Follow-up Status"])
fw.conditional_formatting.add(f"A5:J{FW1}", FormulaRule(formula=['AND($E5<>"",$E5<TODAY(),$H5<>"Replied",$H5<>"Closed")'], fill=fill("FFC7CE"), font=Font(name=FONT, color="9C0006", bold=True)))
fw.conditional_formatting.add(f"A5:J{FW1}", FormulaRule(formula=['AND($E5<>"",$E5=TODAY(),$H5<>"Replied",$H5<>"Closed")'], fill=fill("F4B183")))
for c, w in zip("ABCDEFGHIJ", [22, 10, 13, 13, 13, 18, 14, 14, 9, 40]): fw.column_dimensions[c].width = w
fw.freeze_panes = "C5"; fw.row_dimensions[4].height = 32

# =====================================================================================  JOB SEARCH
js = sheet("Job Search")
title(js, "Job Search", "Type a keyword and/or choose filters. Results are ranked by Match Percentage (best first). Up to 60 results shown.")
labels = ["Keyword (title, company, location, skills)", "Job Category", "Priority", "Location Group", "Application Status",
          "Minimum Match %", "Hide expired / closed? (Yes/No)"]
defaults = ["", "All", "All", "All", "All", 0, "Yes"]
for i, (lb, dv_) in enumerate(zip(labels, defaults)):
    r = 4 + i
    js[f"B{r}"] = lb; js[f"B{r}"].font = f(True)
    c = js[f"C{r}"]; c.value = dv_ if dv_ != "" else None; c.fill = fill("FFFF00"); c.font = f(color="0000FF"); c.border = BOX
js["C9"].number_format = "0%"
dv_list(js, "C5", LREF["Job Category F"]); dv_list(js, "C6", LREF["Priority F"]); dv_list(js, "C7", LREF["Location Group F"])
dv_list(js, "C8", LREF["Status F"]); dv_list(js, "C10", '"Yes,No"')
js["E4"] = "Matches found:"; js["E4"].font = f(True)
js["F4"] = "=SUM(tblJobs[Search Flag])"; js["F4"].font = f(True, 14, NAVY)
RH = ["#", "Job ID", "Priority", "Job Title", "Company", "Location", "Work Mode", "Job Level", "Match %", "Match Band",
      "Application Status", "Active Flag", "Job Application URL"]
for i, h in enumerate(RH, 1):
    cc = js.cell(12, i, h); cc.font = f(True, 10, "FFFFFF"); cc.fill = fill(TEAL); cc.alignment = CENTER
srcs = [None, "Job ID", "Priority", "Job Title", "Company", "Location", "Work Mode", "Job Level", "Match Percentage",
        "Match Band", "Application Status", "Active Flag", "Job Application URL"]
for n in range(1, 61):
    r = 12 + n
    js[f"A{r}"] = n
    for i, s in enumerate(srcs[1:], 2):
        js.cell(r, i, f'=IFERROR(INDEX(tblJobs[{s}],MATCH($A{r},tblJobs[Search Rank],0))&"","")' if s != "Match Percentage"
                else f'=IFERROR(INDEX(tblJobs[{s}],MATCH($A{r},tblJobs[Search Rank],0)),"")')
    js[f"I{r}"].number_format = "0%"
    for c in range(1, 14): js.cell(r, c).font = f(size=9); js.cell(r, c).border = BOX
for c, w in zip("ABCDEFGHIJKLM", [5, 10, 8, 40, 24, 24, 10, 18, 9, 16, 16, 12, 50]): js.column_dimensions[c].width = w
js.column_dimensions["B"].width = 34
js.freeze_panes = "A13"
js.sheet_properties.tabColor = "FFC000"

# =====================================================================================  DASHBOARD
db = sheet("Dashboard")
db.sheet_properties.tabColor = "C00000"
title(db, "Job Hunt Command Centre", None)
db["A2"] = '="Live dashboard - recalculates from every sheet. Today: "&TEXT(TODAY(),"dd-mmm-yyyy")'
db["A2"].font = f(False, 9, "595959", True)
def kpi(cell_lbl, cell_val, label, formula, fmt="0", color=NAVY):
    db[cell_lbl] = label; db[cell_lbl].font = f(True, 9, "595959"); db[cell_lbl].alignment = CENTER
    db[cell_val] = formula; db[cell_val].font = f(True, 18, color); db[cell_val].alignment = CENTER
    db[cell_val].number_format = fmt
    for c in (cell_lbl, cell_val): db[c].fill = fill("F2F6FC"); db[c].border = BOX
TOT = 'COUNTIF(tblJobs[Job Title],"?*")'
APPLIED = 'COUNTIF(tblJobs[Date Applied],">0")'
db["A4"] = "APPLICATION METRICS"; db["A4"].font = f(True, 11, TEAL)
app_metrics = [
    ("Total Jobs Discovered", f"={TOT}"),
    ("Active Openings (not expired)", '=COUNTIF(tblJobs[Active Flag],"Active")+COUNTIF(tblJobs[Active Flag],"Verify")'),
    ("Total Jobs Applied", f"={APPLIED}"),
    ("Applications Pending", '=SUM(COUNTIF(tblJobs[Application Status],{"Applied","Assessment Pending","Assessment Completed","On Hold","No Response"}))'),
    ("Rejections", '=COUNTIF(tblJobs[Application Status],"Rejected")'),
    ("Interviews Scheduled", '=COUNTIF(tblInterviews[Result],"Scheduled")'),
    ("Interviews Completed", '=SUM(COUNTIF(tblInterviews[Result],{"Passed","Failed","Awaiting Result"}))'),
    ("Offers Received", '=COUNTIF(tblJobs[Application Status],"Offer Received")+COUNTIF(tblJobs[Application Status],"Accepted")'),
    ("Offers Accepted", '=COUNTIF(tblJobs[Application Status],"Accepted")'),
    ("Jobs Not Yet Applied", '=SUM(COUNTIFS(tblJobs[Application Status],{"Not Applied","Researching","Interested","Shortlisted"},tblJobs[Active Flag],"<>Expired/Closed"))'),
]
for i, (lb, fx) in enumerate(app_metrics):
    c = L(1 + i)
    kpi(f"{c}5", f"{c}6", lb, fx)
db["A8"] = "PERFORMANCE METRICS"; db["A8"].font = f(True, 11, TEAL)
JWI = 'COUNTIF(tblJobs[First Interview Date],">0")'
perf = [
    ("Application-to-Interview Rate", f"=IFERROR({JWI}/{APPLIED},0)", "0%"),
    ("Interview-to-Offer Rate", f"=IFERROR(H6/{JWI},0)", "0%"),
    ("Overall Success Rate", f"=IFERROR(H6/{APPLIED},0)", "0%"),
    ("Rejection Rate", f"=IFERROR(E6/{APPLIED},0)", "0%"),
    ("Avg Days to First Interview", '=IFERROR(AVERAGE(tblJobs[Days to Interview]),"n/a")', "0.0"),
    ("Avg Days to Offer", '=IFERROR(AVERAGE(tblJobs[Days to Offer]),"n/a")', "0.0"),
    ("Overdue Follow-ups", '=COUNTIF(tblFollowups[Days Overdue],">0")', "0"),
    ("Strong + Good Matches (active)", '=COUNTIFS(tblJobs[Match Band],"Strong Match",tblJobs[Active Flag],"<>Expired/Closed")+COUNTIFS(tblJobs[Match Band],"Good Match",tblJobs[Active Flag],"<>Expired/Closed")', "0"),
    ("Fresher-Friendly Openings", '=SUM(COUNTIFS(tblJobs[Job Level],{"Internship","Apprenticeship","Graduate Program","Entry-Level"},tblJobs[Active Flag],"<>Expired/Closed"))', "0"),
    ("Avg Match % (active)", '=IFERROR(AVERAGEIFS(tblJobs[Match Percentage],tblJobs[Active Flag],"<>Expired/Closed",tblJobs[Job Title],"?*"),0)', "0%"),
]
for i, (lb, fx, fm) in enumerate(perf):
    c = L(1 + i)
    kpi(f"{c}9", f"{c}10", lb, fx, fm, TEAL)
for i in range(1, 13): db.column_dimensions[L(i)].width = 15
db.column_dimensions["A"].width = 27
db.row_dimensions[5].height = 30; db.row_dimensions[9].height = 30
db.row_dimensions[6].height = 30; db.row_dimensions[10].height = 30

# Category table
db["A12"] = "CATEGORY METRICS"; db["A12"].font = f(True, 11, TEAL)
cath = ["Category", "Total", "Active", "Fresher-Friendly", "Remote", "Applied", "Interviews", "Offers", "Avg Match"]
for i, h in enumerate(cath):
    cc = db.cell(13, 1 + i, h); cc.font = f(True, 9, "FFFFFF"); cc.fill = fill(NAVY); cc.alignment = CENTER
for k, cat in enumerate(CATS):
    r = 14 + k
    db[f"A{r}"] = cat
    db[f"B{r}"] = f'=COUNTIF(tblJobs[Job Category],A{r})'
    db[f"C{r}"] = f'=COUNTIFS(tblJobs[Job Category],A{r},tblJobs[Active Flag],"<>Expired/Closed")'
    db[f"D{r}"] = f'=SUM(COUNTIFS(tblJobs[Job Category],A{r},tblJobs[Job Level],{{"Internship","Apprenticeship","Graduate Program","Entry-Level"}},tblJobs[Active Flag],"<>Expired/Closed"))'
    db[f"E{r}"] = f'=COUNTIFS(tblJobs[Job Category],A{r},tblJobs[Work Mode],"Remote")'
    db[f"F{r}"] = f'=COUNTIFS(tblJobs[Job Category],A{r},tblJobs[Date Applied],">0")'
    db[f"G{r}"] = f'=COUNTIFS(tblJobs[Job Category],A{r},tblJobs[First Interview Date],">0")'
    db[f"H{r}"] = f'=SUM(COUNTIFS(tblJobs[Job Category],A{r},tblJobs[Application Status],{{"Offer Received","Accepted"}}))'
    db[f"I{r}"] = f'=IFERROR(AVERAGEIFS(tblJobs[Match Percentage],tblJobs[Job Category],A{r}),0)'; db[f"I{r}"].number_format = "0%"
    for c in range(1, 10): db.cell(r, c).font = f(size=9); db.cell(r, c).border = BOX
db["A19"] = "Total"; db["A19"].font = f(True, 9)
for c in "BCDEFGH": db[f"{c}19"] = f"=SUM({c}14:{c}18)"; db[f"{c}19"].font = f(True, 9); db[f"{c}19"].border = BOX
# Location table
db["K12"] = "LOCATION METRICS"; db["K12"].font = f(True, 11, TEAL)
for i, h in enumerate(["Location", "Total", "Active", "Applied"]):
    cc = db.cell(13, 11 + i, h); cc.font = f(True, 9, "FFFFFF"); cc.fill = fill(NAVY); cc.alignment = CENTER
locs = [("India (on-site/hybrid)", '"India"'), ("Germany", '"Germany"'), ("UAE", '"UAE"'),
        ("Other International", '"Other International"'), ("Remote - India Eligible", '"Remote - India Eligible"'),
        ("Remote - Restricted / Unclear", '"Remote - Restricted / Unclear"')]
for k, (lb, crit) in enumerate(locs):
    r = 14 + k
    db[f"K{r}"] = lb
    db[f"L{r}"] = f"=COUNTIF(tblJobs[Location Group],{crit})"
    db[f"M{r}"] = f'=COUNTIFS(tblJobs[Location Group],{crit},tblJobs[Active Flag],"<>Expired/Closed")'
    db[f"N{r}"] = f'=COUNTIFS(tblJobs[Location Group],{crit},tblJobs[Date Applied],">0")'
    for c in range(11, 15): db.cell(r, c).font = f(size=9); db.cell(r, c).border = BOX
db["K20"] = "All Remote (any)"; db["L20"] = '=COUNTIF(tblJobs[Work Mode],"Remote")'
db["K21"] = "All International (non-India)"; db["L21"] = '=L15+L16+L17+L19'
for c in ("K20", "L20", "K21", "L21"): db[c].font = f(True, 9)
db.column_dimensions["K"].width = 26

# ---- the five questions
db["A23"] = "1) WHICH JOBS SHOULD I APPLY FOR?  Top 10 by Apply Score (match + priority + data confidence; active & not yet applied)"
db["A23"].font = f(True, 11, "C00000")
for i, h in enumerate(["#", "Job ID", "Priority", "Job Title", "", "Company", "Location", "Match %", "Band", "Apply Score"]):
    cc = db.cell(24, 1 + i, h); cc.font = f(True, 9, "FFFFFF"); cc.fill = fill(NAVY)
for n in range(1, 11):
    r = 24 + n
    db[f"A{r}"] = n
    for c, s in zip("BCDFGHIJ", ["Job ID", "Priority", "Job Title", "Company", "Location", "Match Percentage", "Match Band", "Apply Score"]):
        db[f"{c}{r}"] = (f'=IFERROR(INDEX(tblJobs[{s}],MATCH($A{r},tblJobs[Apply Rank],0)),"")' if s in ("Match Percentage", "Apply Score")
                         else f'=IFERROR(INDEX(tblJobs[{s}],MATCH($A{r},tblJobs[Apply Rank],0))&"","")')
    db[f"H{r}"].number_format = "0%"
    db.merge_cells(f"D{r}:E{r}")
    for c in range(1, 11): db.cell(r, c).font = f(size=9); db.cell(r, c).border = BOX
db["L23"] = "2) WHAT SKILLS AM I MISSING?  Top gaps weighted by demand"
db["L23"].font = f(True, 11, "C00000")
for i, h in enumerate(["#", "Skill", "Listings Requiring", "My Level"]):
    cc = db.cell(24, 12 + i, h); cc.font = f(True, 9, "FFFFFF"); cc.fill = fill(NAVY)
for n in range(1, 11):
    r = 24 + n
    db[f"L{r}"] = n
    db[f"M{r}"] = f'=IFERROR(IF(LARGE({P}$J${S0}:$J${S1},L{r})<0,"",INDEX({P}$A${S0}:$A${S1},MATCH(LARGE({P}$J${S0}:$J${S1},L{r}),{P}$J${S0}:$J${S1},0))),"")'
    db[f"N{r}"] = f'=IF(M{r}="","",INDEX({P}$E${S0}:$E${S1},MATCH(M{r},{P}$A${S0}:$A${S1},0)))'
    db[f"O{r}"] = f'=IF(M{r}="","",INDEX({P}$C${S0}:$C${S1},MATCH(M{r},{P}$A${S0}:$A${S1},0)))'
    for c in range(12, 16): db.cell(r, c).font = f(size=9); db.cell(r, c).border = BOX
db.column_dimensions["M"].width = 26
db["A37"] = "3) WHAT SHOULD I PREPARE NEXT?  Upcoming interviews"
db["A37"].font = f(True, 11, "C00000")
for i, h in enumerate(["#", "Date", "Company", "Job Title", "", "Round", "Format"]):
    cc = db.cell(38, 1 + i, h); cc.font = f(True, 9, "FFFFFF"); cc.fill = fill(NAVY)
for n in range(1, 6):
    r = 38 + n
    db[f"A{r}"] = n
    for c, s in zip("BCDFG", ["Interview Date", "Company", "Job Title", "Interview Round", "Interview Format"]):
        db[f"{c}{r}"] = (f'=IFERROR(INDEX(tblInterviews[{s}],MATCH($A{r},tblInterviews[Upcoming Rank],0)),"")' if s == "Interview Date"
                         else f'=IFERROR(INDEX(tblInterviews[{s}],MATCH($A{r},tblInterviews[Upcoming Rank],0))&"","")')
    db[f"B{r}"].number_format = "dd-mmm-yyyy"
    db.merge_cells(f"D{r}:E{r}")
    for c in range(1, 8): db.cell(r, c).font = f(size=9); db.cell(r, c).border = BOX
db["A44"] = '=IF(B39="","No interviews scheduled yet - spend prep time on the top skill gaps (section 2) and DSA/Linux/networking fundamentals.","Prepare for the interview(s) above first, then the top skill gaps.")'
db["A44"].font = f(False, 9, "595959", True)
db["L37"] = "4) WHICH COMPANIES ARE HIRING?  Most openings in tracker"
db["L37"].font = f(True, 11, "C00000")
for i, h in enumerate(["#", "Company", "Jobs", "Applied"]):
    cc = db.cell(38, 12 + i, h); cc.font = f(True, 9, "FFFFFF"); cc.fill = fill(NAVY)
for n in range(1, 11):
    r = 38 + n
    db[f"L{r}"] = n
    db[f"M{r}"] = f'=IFERROR(INDEX(tblCompanies[Company Name],MATCH(LARGE(tblCompanies[Company Rank Helper],L{r}),tblCompanies[Company Rank Helper],0)),"")'
    db[f"N{r}"] = f'=IF(M{r}="","",INDEX(tblCompanies[Jobs in Tracker],MATCH(M{r},tblCompanies[Company Name],0)))'
    db[f"O{r}"] = f'=IF(M{r}="","",INDEX(tblCompanies[Applications],MATCH(M{r},tblCompanies[Company Name],0)))'
    for c in range(12, 16): db.cell(r, c).font = f(size=9); db.cell(r, c).border = BOX
db["A46"] = "5) WHERE AM I IN EACH PROCESS?  See pipeline chart below and the 'Application Pipeline' sheet."
db["A46"].font = f(True, 11, "C00000")

# ---- chart data (right side, column R onward)
db["R3"] = "CHART DATA (auto - do not edit)"; db["R3"].font = f(True, 9, "808080")
db["R4"], db["S4"] = "Status", "Jobs"
for i, s in enumerate(STATUSES):
    db[f"R{5+i}"] = s; db[f"S{5+i}"] = f'=COUNTIF(tblJobs[Application Status],R{5+i})'
SR1 = 4 + len(STATUSES)
db["U4"], db["V4"], db["W4"] = "Month", "Applications", "Daily-log submissions"
for m in range(12):
    r = 5 + m
    db[f"U{r}"] = "=DATE(2026,11,1)" if m == 0 else f"=EDATE(U{r-1},1)"; db[f"U{r}"].number_format = "mmm-yy"
    db[f"V{r}"] = f'=COUNTIFS(tblJobs[Date Applied],">="&U{r},tblJobs[Date Applied],"<="&EOMONTH(U{r},0))'
    db[f"W{r}"] = f'=SUMIFS(tblDaily[Applications Submitted],tblDaily[Date],">="&U{r},tblDaily[Date],"<="&EOMONTH(U{r},0))'
db["Y4"], db["Z4"] = "Funnel stage (reached)", "Jobs"
fun = [("Discovered", f"={TOT}"), ("Applied", f"={APPLIED}"), ("Interviewed", f"={JWI}"),
       ("HR / Final", '=SUMPRODUCT(--((ISNUMBER(MATCH(tblJobs[Interview Status],{"HR","Final Interview"},0))+ISNUMBER(MATCH(tblJobs[Application Status],{"HR Round","Offer Received","Accepted"},0)))>0))'),
       ("Offer", "=H6"), ("Accepted", "=I6")]
for i, (s, fx) in enumerate(fun):
    db[f"Y{5+i}"] = s; db[f"Z{5+i}"] = fx
db["AB4"], db["AC4"] = "Top skills in demand", "Listings"
for n in range(1, 16):
    r = 4 + n
    db[f"AB{r}"] = f'=IFERROR(INDEX({P}$A${S0}:$A${S1},MATCH(LARGE({P}$H${S0}:$H${S1},{n}),{P}$H${S0}:$H${S1},0)),"")'
    db[f"AC{r}"] = f'=IFERROR(INDEX({P}$E${S0}:$E${S1},MATCH(AB{r},{P}$A${S0}:$A${S1},0)),0)'
db["AE4"], db["AF4"], db["AG4"] = "Company", "Jobs tracked", "Applications"
for n in range(1, 11):
    r = 4 + n
    db[f"AE{r}"] = f"=M{38+n}"; db[f"AF{r}"] = f'=IF(AE{r}="",0,N{38+n})'; db[f"AG{r}"] = f'=IF(AE{r}="",0,O{38+n})'
db["AI4"], db["AJ4"] = "Category", "Jobs"
for k in range(5):
    db[f"AI{5+k}"] = f"=A{14+k}"; db[f"AJ{5+k}"] = f"=B{14+k}"
for c in range(18, 37):
    for r in range(4, 25): db.cell(r, c).font = f(size=8, color="808080")
    db.column_dimensions[L(c)].width = 13

def place(chart, anchor, w=16, h=8):
    chart.width, chart.height = w, h; db.add_chart(chart, anchor)
pie = PieChart(); pie.title = "Application Status"
pie.add_data(Reference(db, min_col=19, min_row=4, max_row=SR1), titles_from_data=True)
pie.set_categories(Reference(db, min_col=18, min_row=5, max_row=SR1))
pie.dataLabels = DataLabelList(); pie.dataLabels.showPercent = True
place(pie, "A48", 15, 9)
bc = BarChart(); bc.title = "Jobs by Category"; bc.legend = None
bc.add_data(Reference(db, min_col=36, min_row=4, max_row=9), titles_from_data=True)
bc.set_categories(Reference(db, min_col=35, min_row=5, max_row=9))
bc.dataLabels = DataLabelList(); bc.dataLabels.showVal = True
place(bc, "H48", 15, 9)
lc = LineChart(); lc.title = "Applications Over Time"
lc.add_data(Reference(db, min_col=22, max_col=23, min_row=4, max_row=16), titles_from_data=True)
lc.set_categories(Reference(db, min_col=21, min_row=5, max_row=16)); lc.y_axis.title = "Applications"
place(lc, "A67", 15, 9)
fc = BarChart(); fc.type = "bar"; fc.title = "Interview Conversion Funnel"; fc.legend = None
fc.add_data(Reference(db, min_col=26, min_row=4, max_row=10), titles_from_data=True)
fc.set_categories(Reference(db, min_col=25, min_row=5, max_row=10)); fc.y_axis.scaling.orientation = "minMax"
fc.x_axis.scaling.orientation = "maxMin"; fc.dataLabels = DataLabelList(); fc.dataLabels.showVal = True
place(fc, "H67", 15, 9)
sk = BarChart(); sk.type = "bar"; sk.title = "Skill Demand Ranking (Top 15)"; sk.legend = None
sk.add_data(Reference(db, min_col=29, min_row=4, max_row=19), titles_from_data=True)
sk.set_categories(Reference(db, min_col=28, min_row=5, max_row=19)); sk.x_axis.scaling.orientation = "maxMin"
place(sk, "A86", 15, 11)
cb = BarChart(); cb.title = "Company-wise Jobs & Applications"
cb.add_data(Reference(db, min_col=32, max_col=33, min_row=4, max_row=14), titles_from_data=True)
cb.set_categories(Reference(db, min_col=31, min_row=5, max_row=14))
place(cb, "H86", 15, 11)
db.freeze_panes = "A4"
db.print_area = "A1:O105"
db.page_setup.orientation = "landscape"
db.page_setup.fitToWidth = 1
db.page_setup.fitToHeight = 0
db.sheet_properties.pageSetUpPr.fitToPage = True

# =====================================================================================  RESEARCH SOURCES
rs = sheet("Research Sources")
title(rs, "Research Sources & Verification Log", "Per-listing provenance (linked live to the Master Job Tracker) plus the platforms searched and what happened.")
RSH = ["Job ID", "Company", "Job Title", "Job Source", "Source URL", "Date Verified", "Verification Method",
       "Data Confidence", "Listing Status", "Active Flag"]
header(rs, 4, RSH, set(RSH) - {"Verification Method"})
for i in range(len(jobs)):
    r = 5 + i; mr = M0 + i
    for c, k in zip("ABCDEFHIJ", ["id", "company", "title", "source", "url", "verified", "conf", "lstatus", "active"]):
        rs[f"{c}{r}"] = f"={MT}{CL[k]}{mr}&\"\"" if k not in ("verified",) else f"={MT}{CL[k]}{mr}"
    rs[f"G{r}"] = JD_.V_IDX
    rs[f"F{r}"].number_format = "dd-mmm-yyyy"
    for c in range(1, 11): rs.cell(r, c).font = f(size=9); rs.cell(r, c).border = BOX
RS1 = 4 + len(jobs)
add_table(rs, "tblSources", f"A4:J{RS1}")
for c, w in zip("ABCDEFGHIJ", [10, 22, 36, 24, 60, 12, 44, 11, 20, 12]): rs.column_dimensions[c].width = w
p0 = RS1 + 3
rs[f"A{p0}"] = "PLATFORMS & SOURCES SEARCHED (10-Nov-2026)"; rs[f"A{p0}"].font = f(True, 11, NAVY)
PL = [("Platform", "Access method", "Outcome", "Notes"),
 ("Greenhouse job-board API (Cloudflare, MongoDB, Databricks, Grafana Labs, Datadog, PhonePe, Postman, GitLab, Elastic, Zscaler, Groww)", "Direct API fetch", "BLOCKED", "Host not reachable from the research environment's network policy; no data used."),
 ("Lever API (Mindtickle, CRED, Meesho, Paytm, Zeta)", "Direct API fetch", "BLOCKED", "Same network restriction."),
 ("Ashby API (Sarvam, Supabase, Deel)", "Direct API fetch", "BLOCKED", "Same network restriction."),
 ("Arbeitnow, Remote OK, Himalayas, amazon.jobs, careers.microsoft.com", "Direct fetch", "BLOCKED", "Reached instead through web-search indexes where possible."),
 ("Company careers pages (Amazon, Cisco, SAP, Deloitte, Wipro, HCLTech, Checkmarx, Softwire, Singtel, Nutanix/Jobvite, CBTS/Rippling)", "Web search index", "Used", "Official-domain URLs captured; content from search snippets."),
 ("LinkedIn, Indeed, Glassdoor, Naukri/foundit, Wellfound, Cutshort, Instahyre, Hirist", "Web search index", "Partial", "Mostly search-result pages; several listings point to search pages, flagged 'Direct link not captured'."),
 ("Built In, AnitaB.org, General Catalyst, Index Ventures, b2venture boards", "Web search index", "Used", "Reputable mirrors of employer ATS postings."),
 ("Relocate.me, Arbeitnow, devjobs.de, ZipRecruiter DE, Bayt, GrabJobs", "Web search index", "Used", "International listings; sponsorship recorded only when explicit."),
 ("Remotive, Remote Rocketship, Arc, YC Work at a Startup", "Web search index", "Used", "Remote eligibility recorded per listing text."),
 ("Fresher-drive blogs & aggregators (freshershunt, offcampusjobs4u, testingsociety, cloudsoftsol, jobfound)", "Web search index", "Used with caution", "Marked Low confidence; confirm on employer site."),
 ("StepStone, Otta / Welcome to the Jungle, Dice, We Work Remotely, Startup.jobs, GermanTechJobs", "Web search index", "No usable entry-level results", "Searched; no qualifying listings surfaced in results."),
]
for i, row in enumerate(PL):
    for c, v in enumerate(row, 1):
        cc = rs.cell(p0 + 1 + i, c, v); cc.border = BOX; cc.alignment = WRAP
        cc.font = f(True, 9, "FFFFFF") if i == 0 else f(size=9)
        if i == 0: cc.fill = fill(NAVY)
q0 = p0 + len(PL) + 3
rs[f"A{q0}"] = "CONFIDENCE DEFINITIONS"; rs[f"A{q0}"].font = f(True, 11, NAVY)
for i, (k, v) in enumerate([("High", "Verified by opening the official company careers page (none yet - the research environment could not open pages; upgrade to High after you open the link)."),
                            ("Medium", "Listing found on an official careers domain, employer ATS, or reputable platform (Built In, LinkedIn, Wellfound, Bayt, Greenhouse, AnitaB) via search index."),
                            ("Low", "Found on an aggregator/blog or only on a search-results page; not independently verified.")]):
    rs.cell(q0 + 1 + i, 1, k).font = f(True, 9); rs.cell(q0 + 1 + i, 2, v).font = f(size=9)

# =====================================================================================  RESEARCH SUMMARY
su = sheet("Research Summary")
title(su, "Research Summary", "Live counts recalculate from the tracker; narrative findings reflect the 10-Nov-2026 research pass.")
rows = [
 ("RESEARCH VOLUME", None),
 ("Jobs discovered (in tracker)", f"={TOT}"),
 ("Active jobs (not expired / closed)", '=COUNTIF(tblJobs[Active Flag],"Active")+COUNTIF(tblJobs[Active Flag],"Verify")'),
 ("  of which 'Active' (no age concerns)", '=COUNTIF(tblJobs[Active Flag],"Active")'),
 ("  of which 'Verify' (possibly closed - older posting)", '=COUNTIF(tblJobs[Active Flag],"Verify")'),
 ("Expired / closed (excluded from active counts)", '=COUNTIF(tblJobs[Active Flag],"Expired/Closed")'),
 ("Medium-confidence listings", '=COUNTIF(tblJobs[Data Confidence],"Medium")'),
 ("Low-confidence listings", '=COUNTIF(tblJobs[Data Confidence],"Low")'),
 ("JOBS BY CATEGORY", None),
] + [(c, f'=COUNTIF(tblJobs[Job Category],"{c}")') for c in CATS] + [
 ("OPPORTUNITY TYPES", None),
 ("Fresher-friendly (internship / apprenticeship / graduate / entry-level), active", "=Dashboard!I10"),
 ("Remote opportunities (any)", '=COUNTIF(tblJobs[Work Mode],"Remote")'),
 ("Remote open to India-based applicants", '=COUNTIF(tblJobs[Location Group],"Remote - India Eligible")'),
 ("International (Germany, UAE, other countries)", '=COUNTIF(tblJobs[Location Group],"Germany")+COUNTIF(tblJobs[Location Group],"UAE")+COUNTIF(tblJobs[Location Group],"Other International")'),
 ("Explicit visa sponsorship (employer-stated)", '=COUNTIF(tblJobs[Visa Sponsorship],"Yes")'),
 ("Hard-ineligible (location restricted)", '=COUNTIF(tblJobs[Match Band],"Not Eligible*")'),
 ("MOST DEMANDED SKILLS (live, all categories)", None),
] + [(f"#{n}", f"=Dashboard!AB{4+n}&\"  (\"&Dashboard!AC{4+n}&\" listings)\"") for n in range(1, 11)] + [
 ("TOP HIRING COMPANIES (live)", None),
] + [(f"#{n}", f'=Dashboard!M{38+n}&"  ("&Dashboard!N{38+n}&" listings)"') for n in range(1, 8)] + [
 ("MAJOR SKILL GAPS (live, demand-weighted vs. My Profile)", None),
] + [(f"#{n}", f'=IF(Dashboard!M{24+n}="","",Dashboard!M{24+n}&"  - you: "&Dashboard!O{24+n}&", needed by "&Dashboard!N{24+n}&" listings")') for n in range(1, 9)]
r = 4
for k, v in rows:
    if v is None:
        su[f"A{r}"] = k; su[f"A{r}"].font = f(True, 11, "FFFFFF"); su[f"A{r}"].fill = fill(NAVY)
        su[f"B{r}"].fill = fill(NAVY)
    else:
        su[f"A{r}"] = k; su[f"A{r}"].font = f(size=10); su[f"B{r}"] = v; su[f"B{r}"].font = f(True, 10)
        su[f"A{r}"].border = BOX; su[f"B{r}"].border = BOX
    r += 1
r += 1
NARR = [
 ("KEY FINDINGS", None),
 ("Market shape", "Entry-level P1 (Cloud/DevOps/SRE) roles exist but are fewer than SDE roles; the most fresher-accessible P1 entry points are cloud/technical support (AWS Cloud Support Associate, MongoDB Associate TSE, Microsoft support), NOC, and a small number of SRE I / Associate DevOps reqs (CME Group, Nutanix)."),
 ("Strongest P1 targets now", "JOB-0003 CME Group SRE I (0-1 yrs, 2025/26 grads); JOB-0002 Nutanix Associate DevOps & Cloud (0-1 yrs, closes 23-Nov-2026); JOB-0001 AWS Cloud Support Associate; JOB-0022 MongoDB Associate TSE I; JOB-0009 Ecolibrium Junior Platform Engineer (0-2 yrs)."),
 ("Bridge roles (P1 x P3/P5)", "JOB-0055 Together AI inference infra (remote India, junior band); JOB-0076 Checkmarx Junior DevSecOps; JOB-0078 Orange Health SE-I DevSecOps. These reward your combined DevOps + AI/security exposure."),
 ("International reality", "Explicit sponsorship for junior roles is rare. Confirmed: HomeToGo Berlin (listing says full visa + relocation, but a mirror shows it filled) and Softwire UK graduate scheme (company states Skilled Worker sponsorship). Germany Blue Card IT threshold ~EUR 45.9k (2026) blocks many junior offers; consider the Chancenkarte. Relocation leads mostly target 3+ yrs."),
 ("Remote reality", "'Worldwide' remote listings often carry hidden country limits (e.g. NEORIS = Spain only). Only rows marked 'Remote - India Eligible' are counted as open to you."),
 ("Mass-hiring windows", "TCS NQT (Feb-Mar), Infosys SP (to May) and Wipro Elite (Jul-Sep) 2026 windows have passed; IBM off-campus typically runs Sep-Dec - check now. Watch for 2027 cycles."),
 ("Major skill gaps (narrative)", "Against the listings sampled, your profile is strongest in Python, Docker, Terraform, CI/CD, Linux and LLM tooling. Gaps that recur in P1 entry roles: Kubernetes depth, monitoring/observability practice (Prometheus/Grafana beyond basics), SQL, DSA for product-company screens, and Azure (for support roles). See the live gap list above."),
 ("RECOMMENDED APPLICATION PRIORITIES", None),
 ("This week", "1) Nutanix JOB-0002 (deadline 23-Nov). 2) CME SRE I JOB-0003. 3) AWS Cloud Support Associate JOB-0001 (pick a req matching your shift tolerance). 4) MongoDB Associate TSE I JOB-0022. 5) Evnek GenAI JOB-0050 and Together AI JOB-0055 as P3 bridges."),
 ("Next 2 weeks", "CBTS NOC JOB-0007, Credera NOC JOB-0006, Ecolibrium JOB-0009, Checkmarx JOB-0076, Cisco new-grad JOB-0059, Softwire UK 2027 grad JOB-0071 (sponsorship), Seven Senders Berlin JOB-0030 (ask about visa first)."),
 ("Preparation focus", "Linux + networking fundamentals (every P1 screen), Kubernetes (CKA-level basics), one observability project (Prometheus + Grafana + alerting on a FastAPI app), SQL practice, and DSA (easy-medium) for SDE/SRE screens. Consider AWS SAA-C03 or CKA as the single highest-leverage certification."),
 ("LIMITATIONS (read before applying)", None),
 ("Verification", "The research environment's network policy blocked direct access to job boards and careers sites, so listings were captured from search-engine indexes. No listing is marked High confidence. Open each link, confirm it is live, then set Listing Status to 'Active (page verified)' and Data Confidence to 'High'."),
 ("No fabrication", "Salaries, experience, and visa status are recorded only as the source stated them; otherwise 'Not disclosed' / 'Unknown'. Aggregator salary claims are labelled as such. A few skill tags on thin listings are flagged in Notes as inferred."),
 ("Coverage", "This is a curated starting set, not exhaustive internet coverage. Keep adding roles - the workbook supports 600 rows (extendable)."),
]
for k, v in NARR:
    if v is None:
        su[f"A{r}"] = k; su[f"A{r}"].font = f(True, 11, "FFFFFF"); su[f"A{r}"].fill = fill(NAVY); su[f"B{r}"].fill = fill(NAVY)
    else:
        su[f"A{r}"] = k; su[f"A{r}"].font = f(True, 10); su[f"A{r}"].alignment = WRAP
        su[f"B{r}"] = v; su[f"B{r}"].font = f(size=10); su[f"B{r}"].alignment = WRAP
        su.row_dimensions[r].height = max(30, 15 * (len(v) // 95 + 1))
    r += 1
su.column_dimensions["A"].width = 52; su.column_dimensions["B"].width = 110

# =====================================================================================  README
rd = sheet("README")
rd.sheet_properties.tabColor = "548235"
title(rd, "Global Job Hunting, Recruitment & Interview Tracker - README",
      "A personal recruitment CRM + career-intelligence dashboard. Built 10-Nov-2026. All metrics are live formulas.")
GUIDE = [
 ("START HERE", None),
 ("1. Check your profile", "Open 'My Profile'. Correct the yellow cells (experience, degree, certifications) and your proficiency for each skill. Every Match % in the workbook recalculates instantly."),
 ("2. Pick jobs to apply for", "Dashboard section 1 lists the top 10 by Apply Score. Or use 'Job Search' to filter by keyword, category, priority, location and minimum match."),
 ("3. Verify, then apply", "Open the Job Application URL. If it is live, set Listing Status = 'Active (page verified)' and Data Confidence = 'High'. Then set Application Status = 'Applied' and enter Date Applied."),
 ("4. Track the process", "Log each interview round in 'Interview Tracker' (enter Job ID only - company/title auto-fill). Add follow-ups in 'Follow-up & Reminders'. Log daily effort in 'Daily Job Hunting Log'."),
 ("5. Review weekly", "Dashboard + Research Summary + Skills Matrix show conversion rates, where you are in each pipeline, and which skills to learn next."),
 ("SHEET GUIDE", None),
 ("Dashboard", "KPIs, performance rates, category & location breakdowns, the five key questions, and 6 charts (status pie, category bar, applications over time, funnel, skill demand ranking, company-wise)."),
 ("Master Job Tracker", "Primary table (tblJobs). 84 researched listings + capacity to 600 rows. Navy headers = input; teal headers = formulas. Dropdowns on status, priority, category, location, visa, confidence etc."),
 ("Interview Tracker", "One row per round; result dropdown; interviews within 3 days highlight orange; feeds Interview Status / Next Interview Date / First Interview Date in the master."),
 ("Skills & Requirements Matrix", "Skill x category demand counted from real listings (Required Skills column), % of listings, demand level, your proficiency, required proficiency, gap, learning priority and resources."),
 ("Company Database", "40 companies with careers pages, hiring locations, fresher/intern/remote/visa notes and live counts of jobs and applications."),
 ("Application Pipeline", "Kanban: 11 requested stages + 'Inactive'. Counts and job cards update from Application Status."),
 ("Daily Job Hunting Log", "Daily inputs with automatic weekly (Mon-Sun) and monthly summaries."),
 ("Job Description Analysis", "15 shortlisted roles: stated requirements, likely interview topics, ATS/resume keywords, live missing skills and a job-specific checklist. Add more rows by entering a Job ID."),
 ("Follow-up & Reminders", "Auto next-follow-up (last contact + 7 days); overdue rows turn red, due-today orange."),
 ("Job Search", "Searchable view of the master table, ranked by Match %."),
 ("Research Sources / Summary", "Provenance per listing, platforms searched, confidence definitions, findings and recommended priorities."),
 ("My Profile", "Your skills, proficiency, scoring weights and location-fit scores. 'Lists' holds dropdown values (stage mapping is editable there)."),
 ("MATCH PERCENTAGE (Section 6 of the brief)", None),
 ("Weights", "Technical skills 40% | Experience 20% | Education 10% | Location/work authorization 15% | Preferred skills 10% | Certifications 5% (editable on My Profile)."),
 ("Technical / preferred skills", "Share of the listing's recognised skills you hold at Intermediate+ (Beginner counts half). Listings with no recognised skills score a neutral 50% instead of 0, so thin listings neither win nor lose on skills."),
 ("Experience", "Min Experience Yrs vs your years: meets = 100%, 1 yr short = 75%, 2 yrs = 45%, 3 yrs = 20%, more = 0%. Unknown = 50%."),
 ("Education", "Set 'Education Eligible' per job (Yes/No). 'Unknown' uses your profile answer (90% if you hold a CS/IT degree, else 60%)."),
 ("Location / auth", "From 'Location Work Auth Fit': India-based or India-eligible remote 100%, sponsorship offered 85%, sponsorship unknown 40%, restricted 0%."),
 ("Bands", "80-100% Strong | 65-79% Good | 50-64% Moderate | <50% Low. A location restriction shows 'Not Eligible - Hard Restriction' regardless of score."),
 ("Requirement types", "'Requirement Types' column separates Mandatory, Preferred, Trainable and Hard restrictions. A missing preferred skill never disqualifies a job - it only lowers the 10% preferred component."),
 ("COLOUR LEGEND", None),
 ("Application Status", "Green = Offer/Accepted | Red = Rejected | Blue = Interview stages | Yellow = Applied/Assessment | Orange = follow-up due or No Response/On Hold | Grey = Not applied | Dark grey = Closed/Withdrawn."),
 ("Other", "Deadline passed = red; deadline within 7 days = yellow. Expired rows: title struck through. Duplicate Job IDs = red. 'Possible Duplicate' = same company + title + location."),
 ("Input cells", "Yellow fill + blue text = settings you should edit. Grey cells = formulas (do not type over them)."),
 ("ADDING JOBS & SCALING", None),
 ("Add a job", "Type in the first empty row of the Master Job Tracker. Job ID auto-generates from the row (the 'Next free Job ID' cell shows it). Use skill names exactly as listed on My Profile, separated by comma + space, so matching works. Add new skills to My Profile first."),
 ("Sorting", "Filter freely. Before sorting the master table, copy the Job ID column and Paste Values, so auto IDs do not change and interview/follow-up links stay intact."),
 ("Beyond 600 rows", "Select the last table row and drag the table's resize handle down; formulas extend with it."),
 ("PivotTables & slicers", "Not included: the file was generated programmatically and validated in LibreOffice, which cannot author them. Every metric uses live formulas instead. To add slicers in Excel: click inside tblJobs -> Table Design -> Insert Slicer (Category, Company, Location Group, Status)."),
 ("DATA QUALITY", None),
 ("Confidence", "High = verified on official careers page | Medium = official domain / reputable platform via search index | Low = aggregator / not independently verified. No row is High yet - see Research Summary > Limitations."),
 ("Unknowns", "Salary, visa, relocation and experience are never guessed: 'Unknown' / 'Not disclosed' unless the source stated them."),
]
r = 4
for k, v in GUIDE:
    if v is None:
        rd[f"A{r}"] = k; rd[f"A{r}"].font = f(True, 11, "FFFFFF"); rd[f"A{r}"].fill = fill(TEAL); rd[f"B{r}"].fill = fill(TEAL)
    else:
        rd[f"A{r}"] = k; rd[f"A{r}"].font = f(True, 10); rd[f"A{r}"].alignment = WRAP
        rd[f"B{r}"] = v; rd[f"B{r}"].font = f(size=10); rd[f"B{r}"].alignment = WRAP
        rd.row_dimensions[r].height = max(18, 15 * (len(v) // 100 + 1))
    r += 1
rd.column_dimensions["A"].width = 34; rd.column_dimensions["B"].width = 120

# =====================================================================================  ORDER & SAVE
order = ["README", "Dashboard", "Master Job Tracker", "Job Search", "Interview Tracker", "Skills & Requirements Matrix",
         "Company Database", "Application Pipeline", "Daily Job Hunting Log", "Job Description Analysis",
         "Follow-up & Reminders", "Research Sources", "Research Summary", "My Profile", "Lists"]
wb._sheets = [wb[n] for n in order]
wb.active = 0
for ws in wb.worksheets:
    ws.sheet_view.zoomScale = 90
wb.calculation.fullCalcOnLoad = True
wb.save(OUT)
print("saved", OUT, "| jobs:", len(jobs), "| unknown skill tokens:", sorted(unknown_tokens))
