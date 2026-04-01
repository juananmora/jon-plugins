#!/usr/bin/env python3
"""
Collects Maven Surefire + JaCoCo results from the workspace and calls
generate_test_report.py to produce an up-to-date Markdown report.

Only generates a report when test results were produced during the
subagent execution (--since timestamp). Called from SubagentStop hook.
"""

import argparse
import csv
import glob
import os
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

WORKSPACE = "/workspaces/demo-sesion"
REPORT_SCRIPT = os.path.join(
    WORKSPACE,
    ".agents/skills/apx-unit-test-v2/scripts/generate_test_report.py",
)
OUTPUT_FILE = os.path.join(WORKSPACE, "testresults.md")


def parse_since(since_str):
    """Convert --since value to epoch seconds."""
    if not since_str:
        return 0
    try:
        dt = datetime.strptime(since_str, "%Y-%m-%d %H:%M:%S")
        return dt.timestamp()
    except ValueError:
        return 0


# ---------------------------------------------------------------------------
# 1. Discover surefire XML reports
# ---------------------------------------------------------------------------
def find_surefire_xmls(since_epoch):
    """Return list of TEST-*.xml paths modified after since_epoch."""
    pattern = os.path.join(WORKSPACE, "**/target/surefire-reports/TEST-*.xml")
    recent = []
    for path in glob.glob(pattern, recursive=True):
        if os.path.getmtime(path) >= since_epoch:
            recent.append(path)
    return recent


# ---------------------------------------------------------------------------
# 2. Parse surefire XML → aggregate counts
# ---------------------------------------------------------------------------
def parse_surefire(xml_paths):
    """Return (total, passed, failed, errors, skipped, modules_dict, scenarios)."""
    total = passed = failed = errors = skipped = 0
    modules = {}  # module_label → {tests, passed, failed, errors}
    scenarios = []  # list of (module, test_name, description, result)

    for path in xml_paths:
        try:
            tree = ET.parse(path)
        except ET.ParseError:
            continue
        root = tree.getroot()
        t = int(root.attrib.get("tests", 0))
        f = int(root.attrib.get("failures", 0))
        e = int(root.attrib.get("errors", 0))
        s = int(root.attrib.get("skipped", 0))
        p = t - f - e - s

        total += t
        failed += f
        errors += e
        skipped += s
        passed += p

        # Derive module label from path
        # e.g. .../dtos/GSCUCD13/target/... → GSCUCD13
        parts = Path(path).parts
        try:
            idx = parts.index("target")
            module_dir = parts[idx - 1]
            category = parts[idx - 2]  # dtos / libraries / transactions
        except (ValueError, IndexError):
            module_dir = "unknown"
            category = ""

        label_map = {
            "dtos": "DTOs",
            "libraries": "Library",
            "transactions": "Transaction",
        }
        cat_label = label_map.get(category, category)
        mod_label = f"{module_dir} ({cat_label})"

        if mod_label not in modules:
            modules[mod_label] = {"tests": 0, "passed": 0, "failed": 0, "errors": 0}
        modules[mod_label]["tests"] += t
        modules[mod_label]["passed"] += p
        modules[mod_label]["failed"] += f
        modules[mod_label]["errors"] += e

        # Collect individual test cases for scenarios
        suite_name = root.attrib.get("name", module_dir)
        for tc in root.findall("testcase"):
            tc_name = tc.attrib.get("name", "?")
            has_failure = tc.find("failure") is not None
            has_error = tc.find("error") is not None
            status = "❌" if (has_failure or has_error) else "✅"
            scenarios.append((mod_label, tc_name, tc_name, status))

    return total, passed, failed, errors, skipped, modules, scenarios


# ---------------------------------------------------------------------------
# 3. Discover and parse JaCoCo CSV reports
# ---------------------------------------------------------------------------
def find_jacoco_csvs(since_epoch):
    """Return list of jacoco.csv paths modified after since_epoch."""
    pattern = os.path.join(WORKSPACE, "**/target/site/jacoco/jacoco.csv")
    recent = []
    for path in glob.glob(pattern, recursive=True):
        if os.path.getmtime(path) >= since_epoch:
            recent.append(path)
    return recent


def parse_jacoco(csv_paths):
    """Aggregate JaCoCo coverage across all modules.
    Returns dict with instruction, line, branch, method, class coverage %.
    Also returns per-module coverage and class details.
    """
    totals = {
        "instr_missed": 0, "instr_covered": 0,
        "branch_missed": 0, "branch_covered": 0,
        "line_missed": 0, "line_covered": 0,
        "method_missed": 0, "method_covered": 0,
    }
    module_cov = []   # list of (module_label, cov%, covered, total)
    class_details = []  # list of (class_name, cov%, status)

    for path in csv_paths:
        mod_instr_m = mod_instr_c = 0
        try:
            with open(path, newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    im = int(row.get("INSTRUCTION_MISSED", 0))
                    ic = int(row.get("INSTRUCTION_COVERED", 0))
                    bm = int(row.get("BRANCH_MISSED", 0))
                    bc = int(row.get("BRANCH_COVERED", 0))
                    lm = int(row.get("LINE_MISSED", 0))
                    lc = int(row.get("LINE_COVERED", 0))
                    mm = int(row.get("METHOD_MISSED", 0))
                    mc = int(row.get("METHOD_COVERED", 0))

                    totals["instr_missed"] += im
                    totals["instr_covered"] += ic
                    totals["branch_missed"] += bm
                    totals["branch_covered"] += bc
                    totals["line_missed"] += lm
                    totals["line_covered"] += lc
                    totals["method_missed"] += mm
                    totals["method_covered"] += mc

                    mod_instr_m += im
                    mod_instr_c += ic

                    cls_name = row.get("CLASS", "?")
                    cls_total = im + ic
                    cls_pct = round(ic / cls_total * 100, 1) if cls_total > 0 else 0
                    status = "Óptimo" if cls_pct >= 90 else ("Aceptable" if cls_pct >= 80 else "Bajo")
                    class_details.append((cls_name, cls_pct, status))
        except Exception:
            continue

        # Module-level coverage
        parts = Path(path).parts
        try:
            idx = parts.index("target")
            mod_name = parts[idx - 1]
        except (ValueError, IndexError):
            mod_name = "unknown"
        mod_total = mod_instr_m + mod_instr_c
        mod_pct = round(mod_instr_c / mod_total * 100, 1) if mod_total > 0 else 0
        module_cov.append((mod_name, mod_pct, mod_instr_c, mod_total))

    def pct(covered_key, missed_key):
        c = totals[covered_key]
        m = totals[missed_key]
        t = c + m
        return round(c / t * 100, 1) if t > 0 else 0.0

    def ratio(covered_key, missed_key):
        c = totals[covered_key]
        m = totals[missed_key]
        return f"{c}/{c + m}"

    coverage = {
        "instructions": pct("instr_covered", "instr_missed"),
        "lines": pct("line_covered", "line_missed"),
        "branches": pct("branch_covered", "branch_missed"),
        "methods": pct("method_covered", "method_missed"),
        "instr_ratio": ratio("instr_covered", "instr_missed"),
        "lines_ratio": ratio("line_covered", "line_missed"),
        "branches_ratio": ratio("branch_covered", "branch_missed"),
        "methods_ratio": ratio("method_covered", "method_missed"),
    }

    return coverage, module_cov, class_details


# ---------------------------------------------------------------------------
# 4. Build command and call generate_test_report.py
# ---------------------------------------------------------------------------
def build_and_run(
    total, passed, failed, errors, modules, scenarios, coverage, module_cov, class_details
):
    # Determine project name from modules
    project = "APX-Customer-Service"

    # --modules format: "label:total:passed:failed:errors;..."
    mod_str = ";".join(
        f"{k}:{v['tests']}:{v['passed']}:{v['failed']}:{v['errors']}"
        for k, v in modules.items()
    )

    # --test-scenarios format: "module|name|desc|status;..."
    scen_str = ";".join(f"{s[0]}|{s[1]}|{s[2]}|{s[3]}" for s in scenarios[:60])

    # --module-coverage: "label:pct:covered:total;..."
    mcov_str = ";".join(f"{m[0]}:{m[1]}:{m[2]}:{m[3]}" for m in module_cov)

    # --classes-analyzed: "name:pct:status;..."
    cls_str = ";".join(f"{c[0]}:{c[1]}:{c[2]}" for c in class_details)

    # --conclusion-criteria
    test_pass_pct = round(passed / total * 100, 1) if total > 0 else 0
    verdict = "APROBADO" if (failed == 0 and errors == 0 and coverage["lines"] >= 80) else "NO APROBADO"
    conclusion = (
        f"Tests pasados:100%:{test_pass_pct}% ({passed}/{total}):"
        f"{'CUMPLE' if test_pass_pct == 100 else 'NO CUMPLE'};"
        f"Cobertura líneas:≥80%:{coverage['lines']}%:"
        f"{'CUMPLE' if coverage['lines'] >= 80 else 'NO CUMPLE'};"
        f"Cobertura ramas:≥70%:{coverage['branches']}%:"
        f"{'CUMPLE' if coverage['branches'] >= 70 else 'NO CUMPLE'}"
    )

    cmd = [
        sys.executable, REPORT_SCRIPT,
        "--project", project,
        "--total", str(total),
        "--passed", str(passed),
        "--failed", str(failed),
        "--errors", str(errors),
        "--cov-classes", str(coverage["instructions"]),
        "--cov-methods", str(coverage["methods"]),
        "--cov-lines", str(coverage["lines"]),
        "--cov-instructions", str(coverage["instructions"]),
        "--cov-branches", str(coverage["branches"]),
        "--cov-instructions-ratio", coverage["instr_ratio"],
        "--cov-lines-ratio", coverage["lines_ratio"],
        "--cov-branches-ratio", coverage["branches_ratio"],
        "--cov-methods-ratio", coverage["methods_ratio"],
        "--verdict", verdict,
        "--conclusion-criteria", conclusion,
        "--output", OUTPUT_FILE,
    ]

    if mod_str:
        cmd.extend(["--modules", mod_str])
    if scen_str:
        cmd.extend(["--test-scenarios", scen_str])
    if mcov_str:
        cmd.extend(["--module-coverage", mcov_str])
    if cls_str:
        cmd.extend(["--classes-analyzed", cls_str])

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--since", default="",
                        help="Only process files modified after this timestamp (YYYY-MM-DD HH:MM:SS)")
    args = parser.parse_args()

    debug_log = os.path.join(WORKSPACE, ".github/hooks/subagent-debug.log")
    since_epoch = parse_since(args.since)

    if not since_epoch:
        with open(debug_log, "a") as f:
            f.write("[collect_and_report] No --since provided — skipping (subagent did not run tests).\n")
        return

    surefire_files = find_surefire_xmls(since_epoch)
    if not surefire_files:
        with open(debug_log, "a") as f:
            f.write(f"[collect_and_report] No surefire results modified since {args.since} — subagent did not run tests.\n")
        return

    total, passed, failed, errors, skipped, modules, scenarios = parse_surefire(surefire_files)
    jacoco_files = find_jacoco_csvs(since_epoch)
    coverage, module_cov, class_details = parse_jacoco(jacoco_files)

    rc, stdout, stderr = build_and_run(
        total, passed, failed, errors, modules, scenarios,
        coverage, module_cov, class_details,
    )

    with open(debug_log, "a") as f:
        f.write(
            f"[collect_and_report] Generated report: {OUTPUT_FILE} "
            f"(tests={total}, passed={passed}, lines_cov={coverage['lines']}%, rc={rc})\n"
        )
        if stderr:
            f.write(f"[collect_and_report] stderr: {stderr}\n")


if __name__ == "__main__":
    main()
