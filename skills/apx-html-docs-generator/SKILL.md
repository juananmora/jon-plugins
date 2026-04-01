---
name: apx-html-docs-generator
description: Generación determinista de documentación HTML APX a partir de Markdown en `docs/` con estructura BBVA homogénea y saneamiento de bloques Mermaid para evitar errores por caracteres conflictivos. Usar cuando Codex necesite (1) regenerar `html/` completo o por categoría desde `docs/functional`, `docs/api` o `docs/architecture`, (2) estandarizar navegación/plantilla visual en todas las páginas, o (3) corregir fallos de renderizado Mermaid durante la publicación de documentación.
---

# APX HTML Docs Generator

Regenerar HTML APX desde Markdown usando el script del skill. Editar siempre los `.md` en `docs/` y volver a generar; evitar edición manual de `html/`.

## Recursos
- Script principal: `scripts/generate-html-docs.py`
- Referencia de categorías y navegación: `references/structure-and-nav.md`

## Inputs esperados
- Fuentes Markdown: `docs/functional`, `docs/api`, `docs/architecture`
- ADRs opcionales: `docs/architecture/decisions/*.md` (agregadas en una sola página HTML)
- CSS corporativo existente en proyecto: `html/css/bbva-styles.css`

## Outputs
- Archivos HTML en `html/functional`, `html/api`, `html/architecture`.
- Página consolidada de ADRs: `html/architecture/decisions.html`.
- Índice raíz `html/index.html`.
- Hoja de estilos `html/css/bbva-styles.css`.
- Salida por consola con conteo de archivos generados.
- Footer con sello determinista (basado en última modificación de Markdown fuente).

## Commands

### Regenerar todo
```bash
python3 .agents/skills/apx-html-docs-generator/scripts/generate-html-docs.py --verbose
```

### Elegir densidad visual
```bash
# Más aire y lectura cómoda (default)
python3 .agents/skills/apx-html-docs-generator/scripts/generate-html-docs.py --density comfortable --verbose

# Más compacto para páginas largas
python3 .agents/skills/apx-html-docs-generator/scripts/generate-html-docs.py --density compact --verbose
```

### Regenerar una categoría
```bash
python3 .agents/skills/apx-html-docs-generator/scripts/generate-html-docs.py --category functional --verbose
python3 .agents/skills/apx-html-docs-generator/scripts/generate-html-docs.py --category api --verbose
python3 .agents/skills/apx-html-docs-generator/scripts/generate-html-docs.py --category architecture --verbose
```

## Garantías del script
- Misma estructura HTML base en todas las páginas.
- Menú de navegación homogéneo.
- CSS base corporativo generado automáticamente si no existe (o actualizado en regeneración).
- Landing principal `html/index.html` generada automáticamente con accesos por categoría.
- Soporte de listas no ordenadas (`- item`) y ordenadas (`1. item`).
- Conversión de tablas Markdown tipo pipe (`| col |`) a `<table>`.
- Limpieza Mermaid en bloques ` ```mermaid `:
  - elimina `¿`
  - reemplaza `€` por `EUR`
  - transforma `++` en incremento explícito
  - normaliza emojis compuestos conflictivos

## Edge Cases / Gotchas
- Si no existen `docs/` y `html/` en la raíz, el script falla explícitamente.
- La limpieza de caracteres se aplica solo dentro de Mermaid; el texto normal se conserva.
- No editar HTML a mano: se sobrescribe en la siguiente regeneración.
- No hay `assets/` en este skill porque no requiere plantillas binarias ni ficheros de salida reutilizables.

## Quick Validation
```bash
python3 .agents/skills/apx-html-docs-generator/scripts/validate-skill.py .agents/skills/apx-html-docs-generator
python3 .agents/skills/apx-html-docs-generator/scripts/generate-html-docs.py --verbose
test -f html/index.html && test -f html/css/bbva-styles.css
find html -type f -name '*.html' | wc -l
```

## Skill Folder Layout
```text
.agents/skills/apx-html-docs-generator/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── structure-and-nav.md
└── scripts/
    └── generate-html-docs.py
```
