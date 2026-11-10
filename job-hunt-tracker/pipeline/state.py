"""Read the current workbook: master rows, the user's profile, and every hand-entered cell on input sheets."""
from __future__ import annotations

import datetime as dt
import os
import sys

from openpyxl import load_workbook

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "build"))
from schema import MC  # noqa: E402

from enrich import Profile, PROF, LOC_SCORE_DEFAULT  # noqa: E402

MASTER = "Master Job Tracker"
INPUT_KEYS = [k for _, k, _, fm in MC if not fm]
HEADER_TO_KEY = {h: k for h, k, _, _ in MC}

# (sheet, first_row, last_row or None, first_col, last_col): non-formula cells here are user data to preserve
CAPTURE = [
    ("Interview Tracker", 5, None, 1, 23),
    ("Follow-up & Reminders", 5, None, 1, 10),
    ("Daily Job Hunting Log", 5, None, 1, 11),
    ("Job Description Analysis", 5, None, 1, 18),
    ("My Profile", 4, 10, 1, 11),
    ("My Profile", 13, None, 1, 3),
    ("Job Search", 4, 10, 3, 3),
    ("Company Database", 5, None, 1, 18),
    ("Skills & Requirements Matrix", 5, None, 1, 16),
]


def _is_formula(v):
    return (isinstance(v, str) and v.startswith("=")) or type(v).__name__ in ("ArrayFormula", "DataTableFormula")


def _plain(v):
    if isinstance(v, dt.datetime):
        return v.date() if v.time() == dt.time(0) else v
    return v


def read_master(wb):
    ws = wb[MASTER]
    hdr = {}
    for c in range(1, ws.max_column + 1):
        h = ws.cell(4, c).value
        if h in HEADER_TO_KEY:
            hdr[HEADER_TO_KEY[h]] = c
    rows = []
    for r in range(5, ws.max_row + 1):
        title = ws.cell(r, hdr["title"]).value
        if title in (None, "") or _is_formula(title):
            continue
        row = {}
        for k in INPUT_KEYS:
            if k not in hdr:
                continue
            v = ws.cell(r, hdr[k]).value
            if _is_formula(v):
                v = f"JOB-{r - 4:04d}" if k == "id" else None   # auto-ID formula -> freeze the ID it showed
            row[k] = _plain(v)
        if not row.get("id"):
            row["id"] = f"JOB-{r - 4:04d}"
        rows.append(row)
    return rows


def capture_cells(wb):
    cells = {}
    for sname, r0, r1, c0, c1 in CAPTURE:
        if sname not in wb.sheetnames:
            continue
        ws = wb[sname]
        last = r1 or ws.max_row
        out = cells.setdefault(sname, {})
        for row in ws.iter_rows(min_row=r0, max_row=last, min_col=c0, max_col=c1):
            for c in row:
                v = c.value
                if v is None or v == "" or _is_formula(v):
                    continue
                if isinstance(v, (dt.datetime, dt.date)):
                    if not isinstance(v, dt.datetime):
                        v = dt.datetime.combine(v, dt.time(0))
                    out[c.coordinate] = ["date", v.isoformat()]
                else:
                    out[c.coordinate] = ["v", v]
    return cells


def read_profile(wb):
    ws = wb["My Profile"]
    skills = {}
    for r in range(13, ws.max_row + 1):
        s = ws.cell(r, 1).value
        if s and not _is_formula(s):
            skills[str(s).strip()] = PROF.get(str(ws.cell(r, 3).value or "None").strip(), 0)

    def num(v, d):
        try:
            return float(v)
        except (TypeError, ValueError):
            return d
    weights = tuple(num(ws.cell(r, 5).value, d) for r, d in zip(range(4, 10), (40, 20, 10, 15, 10, 5)))
    loc = dict(LOC_SCORE_DEFAULT)
    for r in range(4, 9):
        k = ws.cell(r, 7).value
        if k in loc:
            loc[k] = num(ws.cell(r, 8).value, loc[k])
    return Profile(skills=skills, years=num(ws["B4"].value, 0), has_degree=str(ws["B5"].value or "Yes").lower().startswith("y"),
                   certs=str(ws["B6"].value or ""), weights=weights if sum(weights) > 0 else (40, 20, 10, 15, 10, 5), loc_scores=loc)


def read_workbook(path):
    wb = load_workbook(path)          # formulas, not cached values: we only want what the user typed
    last_run = None
    if "Pipeline Runs" in wb.sheetnames:
        v = wb["Pipeline Runs"]["A5"].value          # newest run is written first
        if isinstance(v, str) and len(v) >= 16 and v[:4].isdigit():
            last_run = v[:16]
    return {"rows": read_master(wb), "cells": capture_cells(wb), "profile": read_profile(wb), "last_run": last_run}
