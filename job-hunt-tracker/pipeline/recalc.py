"""Recalculate every formula with headless LibreOffice so the saved file carries computed values
(phones, previewers and Google Drive viewers then show numbers instead of blanks). Excel recalculates on open anyway.

Usage: python recalc.py workbook.xlsx
Exit code 0 = recalculated with no formula errors; 1 = LibreOffice failed; 2 = formula errors found.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from openpyxl import load_workbook

MACRO = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE script:module PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "module.dtd">
<script:module xmlns:script="http://openoffice.org/2000/script" script:name="Module1" script:language="StarBasic">
Sub Recalc
  ThisComponent.calculateAll()
  ThisComponent.store()
  ThisComponent.close(True)
End Sub
</script:module>
"""


def soffice():
    for name in ("soffice", "libreoffice"):
        p = shutil.which(name)
        if p:
            return p
    sys.exit("LibreOffice (soffice) not found")


def recalc(path: Path, timeout=600):
    exe = soffice()
    with tempfile.TemporaryDirectory() as prof:
        url = Path(prof).as_uri()
        subprocess.run([exe, f"-env:UserInstallation={url}", "--headless", "--terminate_after_init"],
                       timeout=180, capture_output=True)
        mdir = Path(prof) / "user" / "basic" / "Standard"
        mdir.mkdir(parents=True, exist_ok=True)
        (mdir / "Module1.xba").write_text(MACRO, encoding="utf-8")
        if not (mdir / "script.xlb").exists():
            (mdir / "script.xlb").write_text(
                '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE library:library PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "library.dtd">\n'
                '<library:library xmlns:library="http://openoffice.org/2000/library" library:name="Standard" library:readonly="false" library:passwordprotected="false">\n'
                ' <library:element library:name="Module1"/>\n</library:library>\n', encoding="utf-8")
        r = subprocess.run([exe, f"-env:UserInstallation={url}", "--headless", "--norestore",
                            "vnd.sun.star.script:Standard.Module1.Recalc?language=Basic&location=application",
                            str(path.resolve())], timeout=timeout, capture_output=True, text=True)
        return r.returncode, r.stderr[-500:]


def count_errors(path: Path):
    wb = load_workbook(path, data_only=True)
    errs = []
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if isinstance(v, str) and v[:4] in ("#REF", "#VAL", "#N/A", "#NAM", "#DIV", "#NUM", "#NUL"):
                    errs.append(f"{ws.title}!{c.coordinate}={v}")
    return errs


if __name__ == "__main__":
    p = Path(sys.argv[1])
    code, err = recalc(p)
    if code != 0:
        print("LibreOffice failed:", err)
        sys.exit(1)
    errs = count_errors(p)
    print(f"recalculated {p}; formula errors: {len(errs)}", errs[:10])
    sys.exit(2 if errs else 0)
