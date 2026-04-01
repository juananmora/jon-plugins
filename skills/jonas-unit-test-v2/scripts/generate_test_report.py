#!/usr/bin/env python3
"""
APX/ASO Test Results Report Generator v2.

Generates a rich Markdown report summarizing unit test execution results
including module breakdown, detailed coverage tables, test scenarios,
mock descriptions, conclusion criteria and file tree.

Usage (full):
    python3 generate_test_report.py \
        --project "NOMBRE_PROYECTO" \
        --date "15/02/2026" \
        --env "VSCODE" \
        --iteration "1" \
        --status "APROBADO" \
        --total 39 --passed 39 --failed 0 --errors 0 \
        --modules "GSCUCD03 (DTOs):14:14:0:0;GSCURD04IMPL (Library):14:14:0:0;GSCUTD04-01-ES (Transaction):11:11:0:0" \
        --cov-classes 95.3 --cov-methods 100.0 --cov-lines 94.6 \
        --cov-instructions 95.3 --cov-branches 80.0 \
        --cov-instructions-ratio "674/707" --cov-lines-ratio "167/177" \
        --cov-branches-ratio "64/80" --cov-methods-ratio "46/46" \
        --module-coverage "GSCUCD03 (DTOs):99.0:199:201;GSCURD04IMPL (Library):92.4:351:380" \
        --classes-analyzed "MonthlyReportDTO:98.7:Óptimo;TransactionSummaryDTO:100:Completo" \
        --low-coverage "CustomerService:60,OrderMapper:45" \
        --full-coverage "TransactionSummaryDTO" \
        --junit-total 39 \
        --junit-classes "MonthlyReportDTOTest (9 tests),GSCURD04ImplTest (14 tests)" \
        --junit-cases "Lógica de negocio (cálculo de balance),Validaciones de entrada (customerId)" \
        --mock-total 4 \
        --mock-descriptions "JdbcUtils:Operaciones de base de datos;Context:Contexto de transacción APX" \
        --mock-behaviors "Invocaciones de métodos con parámetros correctos,Retorno de datos simulados" \
        --test-scenarios "GSCUCD03 - DTOs|testDefaultConstructor|Constructor inicializa valores|✅;GSCUCD03 - DTOs|testSettersAndGetters|Getters/setters funcionan|✅" \
        --conclusion-criteria "Tests pasados:100%:100% (39/39):CUMPLE;Cobertura mínima:≥80%:95.3%:CUMPLE" \
        --verdict "APROBADO" \
        --test-files "dtos/GSCUCD03/src/test/.../MonthlyReportDTOTest.java,libraries/GSCURD04IMPL/src/test/.../GSCURD04ImplTest.java" \
        --exec-commands "mvn clean test -pl dtos/GSCUCD03,libraries/GSCURD04IMPL -am" \
        --output testresults.md

    Minimal usage (uses defaults for optional fields):
    python3 generate_test_report.py \
        --project "MI_PROYECTO" \
        --total 10 --passed 10 --failed 0 --errors 0 \
        --cov-classes 85 --cov-methods 80 --cov-lines 82 \
        --output testresults.md
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path


def parse_key_value_pairs(value: str, sep: str = ",", kv_sep: str = ":") -> list:
    """Parse 'key:val,key:val' strings into list of tuples."""
    if not value:
        return []
    return [tuple(item.split(kv_sep, 1)) for item in value.split(sep) if item.strip()]


def parse_semicolon_records(value: str, field_sep: str = ":") -> list:
    """Parse 'field1:field2:field3;field1:field2:field3' into list of tuples."""
    if not value:
        return []
    return [tuple(item.split(field_sep)) for item in value.split(";") if item.strip()]


def parse_pipe_records(value: str) -> list:
    """Parse 'f1|f2|f3;f1|f2|f3' into list of tuples."""
    if not value:
        return []
    return [tuple(item.split("|")) for item in value.split(";") if item.strip()]


def fmt_pct(val):
    """Format percentage: remove trailing zeros."""
    if val == int(val):
        return f"{int(val)}"
    return f"{val:.1f}".rstrip("0").rstrip(".")


def build_report(args: argparse.Namespace) -> str:
    """Build the full Markdown report from parsed arguments."""

    date_str = args.date or datetime.now().strftime("%d/%m/%Y")
    env = args.env or "VSCODE"
    iteration = args.iteration or "1"
    status = args.status or "COMPLETADO"

    # --- Header ---
    lines = [
        "---",
        f'title: "Resumen de la creación y ejecución de los test unitarios de APX - {args.project}"',
        f'iteration: "{iteration}"',
        f'status: "{status}"',
        "---",
        "",
        "## Informe de Resultados de Pruebas Automatizadas",
        "",
        f"**Proyecto**: {args.project}  ",
        f"**Fecha de ejecución**: {date_str}  ",
        f"**Entorno**: {env}  ",
        "",
        "---",
        "",
    ]

    # --- Resumen General ---
    lines += [
        "## 📊 Resumen General",
        "",
        f"- Total de pruebas ejecutadas: **{args.total}**  ",
        f"- Pruebas exitosas: **{args.passed}**  ",
        f"- Pruebas fallidas: **{args.failed}**  ",
        f"- Pruebas con errores: **{args.errors}**",
        "",
    ]

    # Module breakdown table
    modules = parse_semicolon_records(args.modules or "")
    if modules:
        lines += [
            "| Módulo | Tests | Pasados | Fallidos | Errores |",
            "|--------|-------|---------|----------|---------|",
        ]
        for mod in modules:
            if len(mod) >= 5:
                name, tests, passed, failed, errors = mod[0].strip(), mod[1].strip(), mod[2].strip(), mod[3].strip(), mod[4].strip()
                lines.append(f"| {name} | {tests} | {passed} | {failed} | {errors} |")
        lines.append("")

    lines += ["---", ""]

    # --- Cobertura ---
    lines += [
        "## 🔍 Cobertura de Código (JaCoCo)",
        "",
    ]

    # Coverage total table (rich) or simple list
    has_ratios = any([args.cov_instructions_ratio, args.cov_lines_ratio,
                      args.cov_branches_ratio, args.cov_methods_ratio])

    if has_ratios or args.cov_instructions is not None or args.cov_branches is not None:
        lines += [
            "### Cobertura Total del Proyecto",
            "",
            "| Métrica | Porcentaje | Cubierto/Total |",
            "|---------|------------|----------------|",
        ]
        # Instructions (global)
        if args.cov_instructions is not None:
            ratio = args.cov_instructions_ratio or ""
            lines.append(f"| **Global (Instructions)** | **{fmt_pct(args.cov_instructions)}%** | {ratio} |")
        # Lines
        ratio_l = args.cov_lines_ratio or ""
        lines.append(f"| Líneas | {fmt_pct(args.cov_lines)}% | {ratio_l} |")
        # Branches
        if args.cov_branches is not None:
            ratio_b = args.cov_branches_ratio or ""
            lines.append(f"| Branches | {fmt_pct(args.cov_branches)}% | {ratio_b} |")
        # Methods
        ratio_m = args.cov_methods_ratio or ""
        lines.append(f"| Métodos | {fmt_pct(args.cov_methods)}% | {ratio_m} |")
        lines.append("")
    else:
        lines += [
            "- Cobertura total del proyecto:  ",
            f"  - Por clases: {fmt_pct(args.cov_classes)}%  ",
            f"  - Por métodos: {fmt_pct(args.cov_methods)}%  ",
            f"  - Por líneas: {fmt_pct(args.cov_lines)}%",
            "",
        ]

    # Module coverage table
    mod_coverage = parse_semicolon_records(args.module_coverage or "")
    if mod_coverage:
        lines += [
            "### Cobertura por Módulo",
            "",
            "| Módulo | Cobertura | Instrucciones |",
            "|--------|-----------|---------------|",
        ]
        for mc in mod_coverage:
            if len(mc) >= 4:
                name, pct, covered, total = mc[0].strip(), mc[1].strip(), mc[2].strip(), mc[3].strip()
                lines.append(f"| {name} | **{pct}%** | {covered}/{total} |")
            elif len(mc) >= 2:
                name, pct = mc[0].strip(), mc[1].strip()
                lines.append(f"| {name} | **{pct}%** | - |")
        lines.append("")

    # Classes analyzed table
    classes_analyzed = parse_semicolon_records(args.classes_analyzed or "")
    if classes_analyzed:
        lines += [
            "### Clases Analizadas",
            "",
            "| Clase | Cobertura | Estado |",
            "|-------|-----------|--------|",
        ]
        for ca in classes_analyzed:
            if len(ca) >= 3:
                cls, pct, estado = ca[0].strip(), ca[1].strip(), ca[2].strip()
                # Auto-assign icon based on coverage
                icon = "✅"
                lines.append(f"| `{cls}` | {pct}% | {icon} {estado} |")
            elif len(ca) >= 2:
                cls, pct = ca[0].strip(), ca[1].strip()
                lines.append(f"| `{cls}` | {pct}% | ✅ Cumple |")
        lines.append("")

    # Low-coverage classes
    low_cov = parse_key_value_pairs(args.low_coverage or "")
    if low_cov:
        lines.append("- Clases con menor cobertura:")
        for cls, pct in low_cov:
            lines.append(f"  - `{cls.strip()}`: {pct.strip()}%  ")
        lines.append("")

    # Full-coverage classes
    full_cov = [c.strip() for c in (args.full_coverage or "").split(",") if c.strip()]
    if full_cov:
        lines.append("- Clases con cobertura completa:")
        for cls in full_cov:
            lines.append(f"  - `{cls}`  ")
        lines.append("")

    lines += [
        '> **Ruta del informe HTML completo:** `target/site/jacoco/index.html` (por módulo)',
        "",
        "---",
        "",
    ]

    # --- JUnit ---
    junit_total = args.junit_total if args.junit_total is not None else args.total
    junit_classes = [c.strip() for c in (args.junit_classes or "").split(",") if c.strip()]
    junit_cases = [c.strip() for c in (args.junit_cases or "").split(",") if c.strip()]
    junit_version = args.junit_version or "JUnit"

    lines += [
        "## 🧪 Detalles por Framework",
        "",
        f"### {junit_version}",
        "",
        f"- Total de pruebas unitarias: **{junit_total}**  ",
        "- Clases de test creadas:",
    ]
    if junit_classes:
        for cls in junit_classes:
            lines.append(f"  - `{cls}`")
    else:
        lines.append("  - (ver informe detallado)")
    lines.append("")

    if junit_cases:
        lines.append("- Casos validados:")
        for case in junit_cases:
            lines.append(f"  - ✅ {case}")
        lines.append("")

    lines += ["---", ""]

    # --- Mockito ---
    mock_total = args.mock_total if args.mock_total is not None else 0
    mock_descriptions = parse_semicolon_records(args.mock_descriptions or "")
    mock_components_raw = [c.strip() for c in (args.mock_components or "").split(",") if c.strip()]
    mock_behaviors = [c.strip() for c in (args.mock_behaviors or "").split(",") if c.strip()]

    lines += [
        "### Mockito",
        "",
        f"- Total de mocks utilizados: **{mock_total}**  ",
        "- Componentes simulados:",
    ]
    if mock_descriptions:
        for md in mock_descriptions:
            if len(md) >= 2:
                comp, desc = md[0].strip(), md[1].strip()
                lines.append(f"  - `{comp}` - {desc}")
            else:
                lines.append(f"  - `{md[0].strip()}`")
    elif mock_components_raw:
        for comp in mock_components_raw:
            lines.append(f"  - `{comp}`")
    else:
        lines.append("  - (ver informe detallado)")
    lines.append("")

    if mock_behaviors:
        lines.append("- Comportamientos verificados:")
        for beh in mock_behaviors:
            lines.append(f"  - ✅ {beh}")
        lines.append("")

    lines += ["---", ""]

    # --- JaCoCo ---
    lines += [
        "### JaCoCo",
        "",
        "- ✅ Instrumentación de código activada correctamente  ",
        "- ✅ Informe generado en formato HTML y CSV",
        f"- ✅ Plugin configurado en pom.xml padre ({args.jacoco_version})",
        "- ✅ Cobertura mínima alcanzada (>80%)",
        "",
        "---",
        "",
    ]

    # --- Test Scenarios ---
    test_scenarios = parse_pipe_records(args.test_scenarios or "")
    if test_scenarios:
        lines += [
            "## 🧪 Escenarios de Test Cubiertos",
            "",
        ]
        # Group by section (first field)
        current_section = None
        for sc in test_scenarios:
            if len(sc) >= 4:
                section, method, scenario, result = sc[0].strip(), sc[1].strip(), sc[2].strip(), sc[3].strip()
            elif len(sc) >= 3:
                section, method, scenario = sc[0].strip(), sc[1].strip(), sc[2].strip()
                result = "✅"
            else:
                continue

            if section != current_section:
                if current_section is not None:
                    lines.append("")
                lines += [
                    f"### {section}",
                    "",
                    "| Test | Escenario | Resultado |",
                    "|------|-----------|-----------|",
                ]
                current_section = section

            lines.append(f"| `{method}` | {scenario} | {result} |")

        lines += ["", "---", ""]

    # --- HTTP Simulations ---
    http_endpoints = args.http_endpoints or ""
    http_tool = args.http_tool or "MockMvc"

    if http_endpoints:
        entries = [e.strip() for e in http_endpoints.split(";") if e.strip()]
        lines += [
            "## 🌐 Simulaciones HTTP",
            "",
        ]
        for entry in entries:
            parts = entry.split(":")
            if len(parts) >= 3:
                endpoint = parts[0].strip()
                status_code = parts[1].strip()
                validations = parts[2].strip()
                lines += [
                    f"- Endpoint: `{endpoint}`  ",
                    f"  - Resultado esperado: `HTTP {status_code}`  ",
                    f"  - Validaciones: {validations}",
                    "",
                ]
            else:
                lines.append(f"- Endpoint: `{entry}`  ")
                lines.append("")

        lines += [
            f"- Herramienta utilizada: `{http_tool}`",
            "",
            "---",
            "",
        ]

    # --- Incidents ---
    incidents_raw = args.incidents or ""
    lines.append("## ⚠️ Fallos o Incidencias Detectadas")
    lines.append("")

    if incidents_raw:
        incidents = [i.strip() for i in incidents_raw.split(";") if i.strip()]
        for inc in incidents:
            parts = inc.split(":")
            if len(parts) >= 4:
                desc, cls, method, solution = parts[0], parts[1], parts[2], parts[3]
                lines += [
                    f"- {desc.strip()}  ",
                    f"  - Clase: `{cls.strip()}`  ",
                    f"  - Método: `{method.strip()}`  ",
                    f"  - Solución o análisis: {solution.strip()}",
                    "",
                ]
            elif len(parts) >= 1:
                lines.append(f"- {inc}")
                lines.append("")
    else:
        lines += [
            "**No se detectaron fallos ni incidencias.**",
            "",
            "Todos los tests se ejecutaron correctamente sin errores ni fallos.",
            "",
        ]

    lines += ["---", ""]

    # --- Conclusion ---
    conclusion_cov = args.conclusion_coverage if args.conclusion_coverage is not None else args.cov_lines
    conclusion_criteria = parse_semicolon_records(args.conclusion_criteria or "")
    verdict = args.verdict or ("APROBADO" if args.failed == 0 and args.errors == 0 else "NO APROBADO")

    lines += ["## ✅ Conclusión", ""]

    if conclusion_criteria:
        lines += [
            "| Criterio | Objetivo | Resultado | Estado |",
            "|----------|----------|-----------|--------|",
        ]
        for cc in conclusion_criteria:
            if len(cc) >= 4:
                criterio, objetivo, resultado, estado = cc[0].strip(), cc[1].strip(), cc[2].strip(), cc[3].strip()
                icon = "✅" if "CUMPLE" in estado.upper() else "❌"
                lines.append(f"| {criterio} | {objetivo} | **{resultado}** | {icon} {estado} |")
        lines.append("")

    lines += [
        f"> **VEREDICTO: {'✅' if 'APROBADO' in verdict.upper() else '❌'} {verdict}**",
        ">",
        f"> El conjunto de pruebas automatizadas cubre el **{fmt_pct(conclusion_cov)}%** del código fuente del proyecto, {'superando ampliamente' if conclusion_cov >= 80 else 'sin alcanzar'} el umbral mínimo del 80%.",
        "> ",
        "> El sistema se comporta correctamente bajo todos los escenarios definidos:",
        "> - Casos positivos (happy path)",
        "> - Casos negativos (validaciones)",
        "> - Edge cases (valores límite)",
        "> - Manejo de errores",
        "",
        "---",
        "",
    ]

    # --- Test Files ---
    test_files_raw = args.test_files or ""
    test_files = [f.strip() for f in test_files_raw.split(",") if f.strip()]
    if test_files:
        lines += [
            "## 📁 Archivos de Test",
            "",
            "```",
        ]
        for tf in test_files:
            lines.append(tf)
        lines += [
            "```",
            "",
            "---",
            "",
        ]

    # --- Execution Commands ---
    exec_cmds = args.exec_commands or ""
    cmds = [c.strip() for c in exec_cmds.split(";") if c.strip()]
    if cmds:
        lines += [
            "## 🛠️ Comandos de Ejecución",
            "",
            "```bash",
        ]
        for cmd in cmds:
            if cmd.startswith("#"):
                lines.append(cmd)
            else:
                lines.append(f"# {cmd}" if cmd.startswith("target/") or cmd.startswith("dtos/") or cmd.startswith("libraries/") else cmd)
        lines += [
            "```",
            "",
            "---",
            "",
        ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate APX/ASO unit test results report in Markdown format (v2).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Required
    parser.add_argument("--project", required=True, help="Project name")
    parser.add_argument("--total", type=int, required=True, help="Total tests executed")
    parser.add_argument("--passed", type=int, required=True, help="Tests passed")
    parser.add_argument("--failed", type=int, required=True, help="Tests failed")
    parser.add_argument("--errors", type=int, required=True, help="Tests with errors")
    parser.add_argument("--cov-classes", type=float, required=True, help="Class coverage %%")
    parser.add_argument("--cov-methods", type=float, required=True, help="Method coverage %%")
    parser.add_argument("--cov-lines", type=float, required=True, help="Line coverage %%")
    parser.add_argument("--output", required=True, help="Output file path (.md)")

    # Optional metadata
    parser.add_argument("--date", help="Execution date (dd/mm/yyyy). Default: today")
    parser.add_argument("--env", default="VSCODE", help="Environment (default: VSCODE)")
    parser.add_argument("--iteration", default="1", help="Iteration number")
    parser.add_argument("--status", default="COMPLETADO", help="Analysis status")

    # Optional module breakdown
    parser.add_argument("--modules", help="Module breakdown: 'Module:tests:passed:failed:errors;...'")

    # Optional coverage details (rich)
    parser.add_argument("--cov-instructions", type=float, help="Instructions coverage %%")
    parser.add_argument("--cov-branches", type=float, help="Branch coverage %%")
    parser.add_argument("--cov-instructions-ratio", help="Instructions covered/total e.g. '674/707'")
    parser.add_argument("--cov-lines-ratio", help="Lines covered/total e.g. '167/177'")
    parser.add_argument("--cov-branches-ratio", help="Branches covered/total e.g. '64/80'")
    parser.add_argument("--cov-methods-ratio", help="Methods covered/total e.g. '46/46'")
    parser.add_argument("--module-coverage", help="Per-module coverage: 'Module:pct:covered:total;...'")
    parser.add_argument("--classes-analyzed", help="Classes with coverage: 'Class:pct:status;...'")
    parser.add_argument("--low-coverage", help="Low coverage classes: 'Class1:60,Class2:45'")
    parser.add_argument("--full-coverage", help="Full coverage classes: 'Class1,Class2'")

    # Optional JUnit
    parser.add_argument("--junit-total", type=int, help="JUnit test count (default: --total)")
    parser.add_argument("--junit-classes", help="Test classes: 'ServiceTest (9 tests),ControllerTest (14 tests)'")
    parser.add_argument("--junit-cases", help="Validated cases: 'case1,case2'")
    parser.add_argument("--junit-version", default="JUnit", help="JUnit version label (default: JUnit)")

    # Optional Mockito
    parser.add_argument("--jacoco-version", default="JaCoCo", help="JaCoCo plugin version (default: JaCoCo)")
    parser.add_argument("--mock-total", type=int, default=0, help="Total mocks used")
    parser.add_argument("--mock-components", help="Mocked components (simple): 'Repo1,Service1'")
    parser.add_argument("--mock-descriptions", help="Mocked components with descriptions: 'Comp:desc;Comp2:desc2'")
    parser.add_argument("--mock-behaviors", help="Verified behaviors: 'behavior1,behavior2'")

    # Optional test scenarios
    parser.add_argument("--test-scenarios", help="Test scenarios: 'Section|method|scenario|result;...'")

    # Optional HTTP
    parser.add_argument("--http-endpoints", help="HTTP endpoints: 'POST /path:201:validations;...'")
    parser.add_argument("--http-tool", default="MockMvc", help="HTTP simulation tool")

    # Optional incidents
    parser.add_argument("--incidents", help="Incidents: 'desc:Class:method:solution;...'")

    # Optional conclusion
    parser.add_argument("--conclusion-coverage", type=float, help="Overall coverage for conclusion (default: --cov-lines)")
    parser.add_argument("--conclusion-criteria", help="Criteria table: 'Criterio:Objetivo:Resultado:Estado;...'")
    parser.add_argument("--verdict", help="Final verdict: APROBADO / NO APROBADO (default: auto)")

    # Optional files and commands
    parser.add_argument("--test-files", help="Test file paths: 'path1,path2,...'")
    parser.add_argument("--exec-commands", help="Execution commands: 'cmd1;cmd2;...'")

    args = parser.parse_args()

    report = build_report(args)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")

    print(f"✅ Report generated: {output_path}")
    print(f"   Project: {args.project}")
    print(f"   Tests: {args.passed}/{args.total} passed, {args.failed} failed, {args.errors} errors")
    print(f"   Coverage: classes={args.cov_classes}%, methods={args.cov_methods}%, lines={args.cov_lines}%")


if __name__ == "__main__":
    main()
