#!/usr/bin/env python3
"""
Validación ligera de SKILL.md sin dependencias externas.
"""

import re
import sys
from pathlib import Path

MAX_NAME_LEN = 64
MAX_DESCRIPTION_LEN = 1024


def parse_frontmatter(content: str):
    match = re.match(r'^---\n(.*?)\n---', content, flags=re.DOTALL)
    if not match:
        return None, "No se encontró frontmatter YAML válido"

    frontmatter_text = match.group(1)
    data = {}
    for raw_line in frontmatter_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#'):
            continue
        m = re.match(r'^([a-zA-Z0-9_-]+)\s*:\s*(.*)$', line)
        if not m:
            return None, f"Línea inválida en frontmatter: {raw_line}"
        key, value = m.group(1), m.group(2).strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        if value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        data[key] = value
    return data, None


def validate(skill_path: Path):
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md no existe"

    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return False, "SKILL.md debe empezar por frontmatter YAML"

    frontmatter, error = parse_frontmatter(content)
    if error:
        return False, error

    allowed = {"name", "description"}
    extra = set(frontmatter.keys()) - allowed
    if extra:
        return False, f"Frontmatter contiene claves no permitidas: {', '.join(sorted(extra))}"

    for required in ("name", "description"):
        if required not in frontmatter or not str(frontmatter[required]).strip():
            return False, f"Falta campo obligatorio '{required}' en frontmatter"

    name = frontmatter["name"].strip()
    if len(name) > MAX_NAME_LEN:
        return False, f"name excede {MAX_NAME_LEN} caracteres"
    if not re.match(r"^[a-z0-9-]+$", name):
        return False, "name debe estar en hyphen-case (a-z, 0-9, -)"
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return False, "name no puede empezar/terminar en '-' ni contener '--'"

    description = frontmatter["description"].strip()
    if len(description) > MAX_DESCRIPTION_LEN:
        return False, f"description excede {MAX_DESCRIPTION_LEN} caracteres"
    if "<" in description or ">" in description:
        return False, "description no puede contener '<' ni '>'"

    return True, "Validación OK"


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 validate-skill.py <path-skill>")
        return 1

    ok, message = validate(Path(sys.argv[1]))
    print(message)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
