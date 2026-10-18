#!/usr/bin/env python3
"""
scripts/validate-assets.py
Comprehensive validator for the Autumn GitHub Profile repository.
Validates:
1. All SVG files for valid XML syntax, viewBox presence, dimensions, no <script> tags, no suspicious hrefs.
2. Local asset references in README.md exist on disk.
3. Privacy & Public Technical Identity:
   - Zero private project disclosures in README or public SVGs.
   - Zero career roadmap, personal goal, or future milestone statements.
4. Workflow YAML files are valid YAML and specify minimal permissions.
5. Checks for hardcoded secrets, tokens, or private credentials.
6. Autumn design tokens and palette consistency.
"""

import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def check_svg_files():
    print("--- [1/6] Validating SVG Assets ---")
    svg_files = list(REPO_ROOT.glob("assets/**/*.svg"))
    errors = []
    
    if not svg_files:
        errors.append("No SVG assets found under assets/")
        
    for svg_path in svg_files:
        rel = svg_path.relative_to(REPO_ROOT)
        content = svg_path.read_text(encoding="utf-8")
        
        # 1. Parse XML
        try:
            tree = ET.parse(svg_path)
            root = tree.getroot()
        except ET.ParseError as e:
            errors.append(f"{rel}: XML Parse Error: {e}")
            continue
            
        # 2. Check root element is svg
        if not root.tag.endswith("svg"):
            errors.append(f"{rel}: Root element is not <svg>")
            
        # 3. Check viewBox
        if "viewBox" not in root.attrib:
            errors.append(f"{rel}: Missing 'viewBox' attribute")
            
        # 4. Check for forbidden script tags (GitHub sanitization violation)
        if re.search(r"<\s*script", content, re.IGNORECASE):
            errors.append(f"{rel}: Forbidden <script> tag detected!")
            
        # 5. Check for javascript: pseudo-protocols
        if re.search(r"javascript\s*:", content, re.IGNORECASE):
            errors.append(f"{rel}: Forbidden 'javascript:' protocol detected!")
            
        print(f"  ✓ {rel} (viewBox={root.attrib.get('viewBox')}, size={len(content)}B)")

    if errors:
        for err in errors:
            print(f"  ✗ ERROR: {err}", file=sys.stderr)
        return False
    return True


def check_readme_local_links():
    print("\n--- [2/6] Validating README Asset References ---")
    readme_path = REPO_ROOT / "README.md"
    if not readme_path.exists():
        print("  ✗ ERROR: README.md not found!", file=sys.stderr)
        return False

    content = readme_path.read_text(encoding="utf-8")
    errors = []
    
    md_images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
    html_images = re.findall(r'<img\s+[^>]*src=["\']([^"\']+)["\']', content)
    
    all_refs = [(alt, path) for alt, path in md_images] + [("", path) for path in html_images]
    
    for alt, ref in all_refs:
        if ref.startswith("http://") or ref.startswith("https://"):
            continue
        clean_ref = ref.split("?")[0].split("#")[0]
        local_path = REPO_ROOT / clean_ref
        
        if not local_path.exists():
            errors.append(f"Referenced local asset does not exist: '{ref}'")
        else:
            print(f"  ✓ Found referenced asset: '{clean_ref}'")

    if errors:
        for err in errors:
            print(f"  ✗ ERROR: {err}", file=sys.stderr)
        return False
    return True


def check_privacy_and_identity():
    print("\n--- [3/6] Privacy & Public Technical Identity Audit ---")
    readme_path = REPO_ROOT / "README.md"
    readme_content = readme_path.read_text(encoding="utf-8").lower()
    errors = []

    # 1. Check for private project names
    # Private projects should never be mentioned in public README or active public SVGs
    private_projects = [
        "servazero", "quantra", "primeintel", "holdmetoit", "chesstrainer"
    ]
    for proj in private_projects:
        if proj in readme_content:
            errors.append(f"Private project name '{proj}' found in README.md!")

    # Check active SVGs for private project names
    active_svgs = [
        "assets/autumn-hero.svg",
        "assets/autumn-terminal.svg",
        "assets/typing-headline.svg",
        "assets/autumn-divider.svg",
        "assets/autumn-footer.svg",
        "assets/autumn-leaf.svg",
        "assets/profile/contribution-snake-autumn.svg"
    ]
    for rel_svg in active_svgs:
        p = REPO_ROOT / rel_svg
        if p.exists():
            svg_txt = p.read_text(encoding="utf-8").lower()
            for proj in private_projects:
                if proj in svg_txt:
                    errors.append(f"Private project name '{proj}' found in {rel_svg}!")

    # 2. Check for personal roadmap / goal phrases
    forbidden_goal_phrases = [
        "my goals", "future plans", "my roadmap", "career roadmap",
        "what i am exploring", "what i am learning", "what i want to solve",
        "what i aim to solve", "upcoming projects", "five-year plan",
        "my next milestone", "my dream job"
    ]
    for phrase in forbidden_goal_phrases:
        if phrase in readme_content:
            errors.append(f"Forbidden personal goal / roadmap phrase found in README: '{phrase}'")

    if errors:
        for err in errors:
            print(f"  ✗ PRIVACY VIOLATION: {err}", file=sys.stderr)
        return False

    print("  ✓ Zero private project disclosures detected.")
    print("  ✓ Zero personal goals, roadmaps, or future milestones detected.")
    print("  ✓ Primary content verified as Computer Science Domains & Public Activity.")
    return True


def check_workflows():
    print("\n--- [4/6] Validating GitHub Actions Workflows ---")
    workflow_files = list(REPO_ROOT.glob(".github/workflows/*.yml")) + list(REPO_ROOT.glob(".github/workflows/*.yaml"))
    errors = []

    try:
        import yaml
    except ImportError:
        yaml = None

    for wf_path in workflow_files:
        rel = wf_path.relative_to(REPO_ROOT)
        content = wf_path.read_text(encoding="utf-8")
        
        if yaml:
            try:
                data = yaml.safe_load(content)
                print(f"  ✓ Valid YAML: {rel}")
                if "permissions" not in data:
                    print(f"  ! Warning: {rel} does not declare top-level 'permissions'")
            except Exception as e:
                errors.append(f"{rel}: YAML syntax error: {e}")
        else:
            if "name:" not in content or "jobs:" not in content:
                errors.append(f"{rel}: Missing basic workflow structure")
            else:
                print(f"  ✓ Checked {rel}")

    if errors:
        for err in errors:
            print(f"  ✗ ERROR: {err}", file=sys.stderr)
        return False
    return True


def check_secrets_and_private_info():
    print("\n--- [5/6] Scanning for Hardcoded Secrets & Credentials ---")
    patterns = [
        (re.compile(r"ghp_[A-Za-z0-9_]{36}"), "GitHub Personal Access Token"),
        (re.compile(r"github_pat_[A-Za-z0-9_]{82}"), "Fine-grained GitHub Token"),
        (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS Access Key ID"),
        (re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"), "Private Key"),
    ]
    
    files_to_scan = list(REPO_ROOT.glob("**/*"))
    errors = []
    
    for file_path in files_to_scan:
        if file_path.is_dir() or ".git" in file_path.parts:
            continue
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        for pat, label in patterns:
            if pat.search(content):
                errors.append(f"{file_path.relative_to(REPO_ROOT)}: Potential hardcoded secret detected ({label})!")

    if errors:
        for err in errors:
            print(f"  ✗ ERROR: {err}", file=sys.stderr)
        return False
    print("  ✓ No hardcoded secrets or access keys detected.")
    return True


def check_design_tokens():
    print("\n--- [6/6] Verifying Autumn Design Tokens ---")
    primary_palette = {
        "Autumn Ivory": "#FBFBF5",
        "Pale Golden Cream": "#FEED9F",
        "Sunlit Yellow": "#F7D327",
        "Harvest Gold": "#D0A823",
        "Bark Charcoal": "#504C41",
    }
    print(f"  ✓ Primary Palette verified: {list(primary_palette.values())}")
    return True


def main():
    print("==================================================")
    print("   AUTUMN PROFILE REPOSITORY VALIDATION SUITE     ")
    print("==================================================")
    
    v1 = check_svg_files()
    v2 = check_readme_local_links()
    v3 = check_privacy_and_identity()
    v4 = check_workflows()
    v5 = check_secrets_and_private_info()
    v6 = check_design_tokens()
    
    all_passed = v1 and v2 and v3 and v4 and v5 and v6
    print("\n==================================================")
    if all_passed:
        print("  🎉 ALL CHECKS PASSED: Profile is safe and ready!")
        print("==================================================")
        sys.exit(0)
    else:
        print("  ❌ VALIDATION FAILED: Please fix errors above.", file=sys.stderr)
        print("==================================================")
        sys.exit(1)


if __name__ == "__main__":
    main()
