#!/usr/bin/env python3
"""
Generador de Documentación HTML APX
====================================

Convierte archivos Markdown a HTML con estilos BBVA corporativos,
manejo robusto de diagramas Mermaid y navegación consistente.

Uso:
    python3 generate-html-docs.py [--category CATEGORIA] [--verbose]

Ejemplos:
    # Generar toda la documentación
    python3 generate-html-docs.py

    # Solo documentación funcional
    python3 generate-html-docs.py --category functional

    # Modo verbose
    python3 generate-html-docs.py --verbose
"""

import re
import sys
import os
import argparse
import html
from pathlib import Path
from typing import Dict, List
from datetime import datetime, timezone

# Configuración de categorías
CATEGORIES = {
    'functional': {
        'source': 'docs/functional',
        'target': 'html/functional',
        'nav_label': '📋 Funcional',
        'color': '#5BBEFF'
    },
    'api': {
        'source': 'docs/api',
        'target': 'html/api',
        'nav_label': '🔌 API',
        'color': '#004481'
    },
    'architecture': {
        'source': 'docs/architecture',
        'target': 'html/architecture',
        'nav_label': '🏗️ Arquitectura',
        'color': '#F8CD51'
    }
}

# Configuración de navegación
NAV_ITEMS = [
    ('index.html', '🏠 Inicio'),
    ('functional/README.html', '📋 Funcional'),
    ('functional/requirements.html', '📊 Requisitos'),
    ('functional/user-stories.html', '👥 User Stories'),
    ('functional/use-cases.html', '🎯 Casos de Uso'),
    ('architecture/README.html', '🏗️ Arquitectura'),
    ('architecture/data-model.html', '🗃️ Modelo Datos'),
    ('architecture/decisions.html', '📝 ADRs'),
    ('api/README.html', '🔌 API'),
    ('api/endpoints.html', '📡 Endpoints'),
]

BASE_CSS = """/* ============================================================
   BBVA APX Documentation Theme
   Extracted from bbva.com computed styles - Feb 2026
   Tokens: BentonBook/BentonMedium/BentonBold, #070e46, #001391,
           #004481, #f7f8f8, border-radius 16px
   ============================================================ */

/* --- Google Fonts fallback for Benton family --- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    /* BBVA Brand – extracted from bbva.com */
    --bbva-core:      #001391;   /* primary blue - sub-nav, footer, accents */
    --bbva-navy:      #070e46;   /* body text, headings */
    --bbva-blue:      #004481;   /* links, secondary accents */
    --bbva-sky:       #5bbeff;   /* highlight blue */
    --bbva-aqua:      #1973b8;   /* mid-blue */
    --bbva-green:     #04e26a;   /* CTA green from bbva.com */

    /* Surfaces */
    --bg:             #f7f8f8;   /* page background */
    --surface:        #ffffff;
    --surface-alt:    #f4f4f4;

    /* Text */
    --text:           #070e46;
    --text-secondary: #595959;
    --text-muted:     #666666;

    /* Borders & Shadows */
    --line:           #e1e1e1;
    --radius:         16px;      /* BBVA signature radius */
    --radius-sm:      8px;
    --shadow-card:    0 2px 12px rgba(7, 14, 70, 0.08);
    --shadow-hover:   0 8px 32px rgba(0, 19, 145, 0.14);

    /* Semantic */
    --ok:    #048a38;
    --warn:  #d97706;
    --danger:#d63031;
}

/* === RESET === */
*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }

/* === BODY === */
body {
    font-family: "BentonBook", Inter, "Segoe UI", Helvetica, Arial, sans-serif;
    color: var(--text);
    font-size: 15px;
    line-height: 1.6;
    background: var(--bg);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* === HEADER – Matches bbva.com header zone === */
header {
    background: var(--surface);
    color: var(--text);
    padding: 24px 32px 20px;
    border-bottom: 1px solid var(--line);
    text-align: left;
}

header h1 {
    margin: 0;
    font-family: "BentonBold", Inter, sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: var(--bbva-navy);
    letter-spacing: -0.25px;
    line-height: 1.2;
}

header p {
    margin: 6px 0 0;
    color: var(--text-secondary);
    font-size: 14px;
    font-weight: 400;
}

/* === LOGO BAR (BBVA blue top bar) === */
header::before {
    content: "BBVA";
    display: block;
    font-family: "BentonBold", Inter, sans-serif;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: var(--surface);
    background: var(--bbva-navy);
    margin: -24px -32px 16px -32px;
    padding: 12px 32px;
}

/* === NAV – BBVA pill-shaped sub-nav bar === */
nav {
    position: sticky;
    top: 0;
    z-index: 100;
    background: var(--bbva-core);
    border-radius: 0 0 var(--radius) var(--radius);
    margin: 0 16px;
    box-shadow: 0 4px 20px rgba(0, 19, 145, 0.25);
}

nav ul {
    margin: 0;
    padding: 10px 16px;
    list-style: none;
    display: flex;
    justify-content: center;
    gap: 4px;
    flex-wrap: wrap;
}

nav a {
    display: inline-block;
    text-decoration: none;
    color: rgba(255, 255, 255, 0.85);
    font-family: "BentonMedium", Inter, sans-serif;
    font-weight: 500;
    font-size: 13px;
    padding: 8px 16px;
    border-radius: 999px;
    border: 1px solid transparent;
    transition: all 0.2s ease;
}

nav a:hover {
    color: #ffffff;
    background: rgba(255, 255, 255, 0.15);
}

nav a.active {
    color: var(--bbva-core);
    background: var(--surface);
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
}

/* === MAIN CONTENT === */
main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 32px 24px 48px;
}

/* === SECTION CARDS – bbva.com card style with 16px radius === */
main > section {
    margin: 0 0 20px;
    padding: 24px;
    border-radius: var(--radius);
    background: var(--surface);
    box-shadow: var(--shadow-card);
    border: none;
    transition: box-shadow 0.25s ease;
}

main > section:hover {
    box-shadow: var(--shadow-hover);
}

/* === TYPOGRAPHY – BBVA heading hierarchy === */
h1, h2, h3, h4 {
    font-family: "BentonBold", Inter, sans-serif;
    color: var(--bbva-navy);
    line-height: 1.25;
    letter-spacing: -0.25px;
}

h1 {
    font-size: 32px;
    font-weight: 700;
    margin: 0 0 16px;
}

h2 {
    font-size: 22px;
    font-weight: 700;
    margin: 28px 0 12px;
    padding-bottom: 8px;
    border-bottom: 2px solid var(--bbva-core);
}

h3 {
    font-size: 17px;
    font-weight: 600;
    margin: 20px 0 8px;
    color: var(--bbva-blue);
}

h4 {
    font-size: 15px;
    font-weight: 600;
    margin: 16px 0 6px;
}

p {
    margin: 8px 0;
    color: var(--text);
    line-height: 1.6;
}

/* === LINKS – bbva.com style: blue, no underline === */
a {
    color: var(--bbva-blue);
    text-decoration: none;
    transition: color 0.15s ease;
}

a:hover {
    color: var(--bbva-core);
    text-decoration: underline;
}

/* === LISTS – Clean BBVA style === */
main ul,
main ol {
    margin: 8px 0 16px;
    padding-left: 24px;
}

main ul {
    list-style: none;
    padding-left: 0;
}

main ul li {
    position: relative;
    padding: 6px 8px 6px 24px;
    margin: 4px 0;
    border-radius: var(--radius-sm);
    transition: background 0.15s ease;
}

main ul li:hover {
    background: rgba(0, 19, 145, 0.04);
}

main ul li::before {
    content: "";
    position: absolute;
    left: 8px;
    top: 14px;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--bbva-core);
}

main ol {
    list-style: none;
    counter-reset: bbva-ol;
    padding-left: 0;
}

main ol li {
    counter-increment: bbva-ol;
    position: relative;
    padding: 6px 8px 6px 36px;
    margin: 4px 0;
    border-radius: var(--radius-sm);
    transition: background 0.15s ease;
}

main ol li:hover {
    background: rgba(0, 19, 145, 0.04);
}

main ol li::before {
    content: counter(bbva-ol);
    position: absolute;
    left: 6px;
    top: 6px;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: var(--bbva-core);
    color: #fff;
    font-size: 12px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* === TABLES – BBVA clean style === */
table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    margin: 16px 0 24px;
    background: var(--surface);
    border-radius: var(--radius);
    overflow: hidden;
    box-shadow: var(--shadow-card);
    border: 1px solid var(--line);
}

th, td {
    padding: 10px 14px;
    text-align: left;
    vertical-align: top;
    border-bottom: 1px solid var(--line);
}

th {
    background: var(--bbva-core);
    color: #fff;
    font-family: "BentonMedium", Inter, sans-serif;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

td {
    font-size: 14px;
    color: var(--text);
}

tbody tr:hover {
    background: rgba(0, 19, 145, 0.03);
}

tbody tr:nth-child(even) {
    background: var(--surface-alt);
}

tbody tr:nth-child(even):hover {
    background: rgba(0, 19, 145, 0.05);
}

/* === CODE BLOCKS === */
pre {
    margin: 12px 0 16px;
    padding: 16px 20px;
    overflow-x: auto;
    border-radius: var(--radius);
    background: #1e1e2e;
    color: #cdd6f4;
    font-size: 13px;
    line-height: 1.5;
    border: 1px solid #313244;
}

pre code {
    color: inherit;
    background: transparent;
    padding: 0;
    font-size: inherit;
}

code {
    font-family: "JetBrains Mono", "Fira Code", "SF Mono", Consolas, monospace;
    padding: 2px 6px;
    border-radius: 4px;
    background: rgba(0, 19, 145, 0.08);
    color: var(--bbva-core);
    font-size: 0.88em;
}

/* === MERMAID DIAGRAMS === */
.mermaid {
    margin: 16px 0 24px;
    padding: 24px;
    border-radius: var(--radius);
    background: var(--surface);
    border: 1px solid var(--line);
    box-shadow: var(--shadow-card);
    text-align: center;
    overflow-x: auto;
}

.mermaid svg {
    max-width: 100%;
    height: auto;
}

/* === KPI GRID === */
.apx-kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin: 16px 0 24px;
}

.apx-kpi {
    padding: 20px;
    border-radius: var(--radius);
    background: var(--surface);
    border: 1px solid var(--line);
    box-shadow: var(--shadow-card);
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.apx-kpi:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-hover);
}

.apx-kpi strong {
    display: block;
    font-size: 28px;
    font-weight: 700;
    color: var(--bbva-core);
    font-family: "BentonBold", Inter, sans-serif;
    letter-spacing: -0.5px;
}

.apx-kpi span {
    color: var(--text-muted);
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

/* === CARDS GRID === */
.apx-cards {
    display: grid;
    gap: 16px;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    margin: 12px 0 24px;
}

.apx-card {
    border-radius: var(--radius);
    padding: 24px;
    background: var(--surface);
    border: 1px solid var(--line);
    box-shadow: var(--shadow-card);
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}

.apx-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--bbva-core), var(--bbva-sky));
    opacity: 0;
    transition: opacity 0.25s ease;
}

.apx-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-hover);
}

.apx-card:hover::before {
    opacity: 1;
}

.apx-card h3 {
    margin: 0 0 8px;
    font-size: 16px;
    color: var(--bbva-navy);
}

.apx-card p {
    margin: 0;
    color: var(--text-muted);
    font-size: 14px;
}

/* === BADGES === */
.badge {
    display: inline-block;
    border-radius: 999px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.3px;
    text-transform: uppercase;
    margin-left: 6px;
}

.badge--ok {
    background: rgba(4, 226, 106, 0.15);
    color: var(--ok);
}

/* === INFO BOXES === */
.info-box {
    margin: 12px 0 16px;
    padding: 16px 20px;
    border-radius: var(--radius);
    border-left: 4px solid var(--bbva-core);
    background: rgba(0, 19, 145, 0.04);
}

.info-box.warning {
    border-left-color: var(--warn);
    background: rgba(217, 119, 6, 0.06);
}

.info-box.danger {
    border-left-color: var(--danger);
    background: rgba(214, 48, 49, 0.05);
}

.info-box.success {
    border-left-color: var(--ok);
    background: rgba(4, 138, 56, 0.05);
}

/* === BLOCKQUOTE === */
blockquote {
    margin: 12px 0 16px;
    padding: 12px 20px;
    border-left: 4px solid var(--bbva-core);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    color: var(--text-secondary);
    background: rgba(0, 19, 145, 0.03);
    font-style: italic;
}

/* === FOOTER – BBVA-style dark footer === */
footer {
    margin-top: 40px;
    text-align: center;
    color: var(--surface);
    font-size: 13px;
    padding: 24px;
    background: var(--bbva-navy);
    border-radius: var(--radius) var(--radius) 0 0;
    margin-left: 16px;
    margin-right: 16px;
}

footer p {
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
}

/* === RESPONSIVE === */
@media (max-width: 768px) {
    header { padding: 20px 16px 16px; }
    header::before { margin: -20px -16px 12px -16px; padding: 10px 16px; }
    nav { margin: 0 8px; }
    nav ul {
        justify-content: flex-start;
        overflow-x: auto;
        flex-wrap: nowrap;
        padding: 8px 12px;
        -webkit-overflow-scrolling: touch;
    }
    nav a { white-space: nowrap; font-size: 12px; padding: 6px 12px; }
    main { padding: 20px 12px 32px; }
    main > section { padding: 16px; border-radius: 12px; }
    footer { margin-left: 8px; margin-right: 8px; }
}

/* === PRINT === */
@media print {
    nav { display: none; }
    header::before { background: #000; -webkit-print-color-adjust: exact; }
    main > section { box-shadow: none; border: 1px solid #ddd; }
    footer { background: #eee; color: #333; }
}
"""

CSS_DENSITY_OVERRIDES = {
    'comfortable': """
/* Density: comfortable */
main { max-width: 1280px; padding: 36px 32px 56px; }
main > section { padding: 28px; }
nav a { padding: 10px 18px; font-size: 14px; }
""",
    'compact': """
/* Density: compact */
body { font-size: 14px; }
header { padding: 16px 24px 14px; }
header::before { margin: -16px -24px 10px -24px; padding: 8px 24px; font-size: 16px; }
nav ul { padding: 6px 12px; gap: 2px; }
nav a { font-size: 11px; padding: 5px 10px; }
main { max-width: 1000px; padding: 20px 16px 32px; }
main > section { padding: 16px; margin-bottom: 12px; }
h2 { margin: 20px 0 8px; font-size: 19px; }
h3 { margin: 14px 0 6px; font-size: 15px; }
.apx-kpi { padding: 14px; }
.apx-card { padding: 16px; }
"""
}


def clean_mermaid_syntax(content: str) -> str:
    """
    Limpia sintaxis de Mermaid para evitar errores de renderizado.
    
    Args:
        content: Contenido con bloques Mermaid
        
    Returns:
        Contenido limpio
    """
    mermaid_fence_pattern = re.compile(
        r'(?m)^[ \t]*```mermaid[ \t]*\n(.*?)(?:\n[ \t]*```[ \t]*(?=\n|$))',
        flags=re.DOTALL
    )

    def clean_mermaid_block(match):
        # Extraer el contenido del bloque (sin los ```)
        mermaid_code = match.group(1)
        
        # Eliminar signos de interrogación invertidos
        mermaid_code = mermaid_code.replace('¿', '')
        
        # Reemplazar símbolo de euro
        mermaid_code = mermaid_code.replace('100€', '100 EUR')
        mermaid_code = mermaid_code.replace('€', ' EUR')
        
        # Normalizar operadores
        mermaid_code = mermaid_code.replace(' >=', '>=').replace('>= ', '>=')
        mermaid_code = mermaid_code.replace(' <=', '<=').replace('<= ', '<=')
        mermaid_code = mermaid_code.replace(' !=', '!=').replace('!= ', '!=')
        
        # Reemplazar ++ por incremento explícito para evitar errores de parser
        mermaid_code = re.sub(r'([A-Za-z_][A-Za-z0-9_]*)\+\+', r'\1 + 1', mermaid_code)
        
        # Reemplazar emojis compuestos problemáticos
        mermaid_code = mermaid_code.replace('👨‍💼', '👤')
        mermaid_code = mermaid_code.replace('👩‍💼', '👤')
        
        # Asegurar que <br> esté cerrado
        mermaid_code = re.sub(r'<br>(?!/)', '<br/>', mermaid_code)

        # Normalizar tokens <...> conflictivos sin romper flechas Mermaid (--> / ->> / etc.)
        # Conserva explícitamente <br/> y reemplaza placeholders tipo <token> por (token).
        mermaid_code = re.sub(
            r'<(?!br/?\s*>)([^>\n]{1,80})>',
            r'(\1)',
            mermaid_code
        )
        
        # Retornar con los backticks
        return f'```mermaid\n{mermaid_code}\n```'
    
    # Aplicar limpieza solo a bloques mermaid
    content = mermaid_fence_pattern.sub(clean_mermaid_block, content)
    
    return content


def stash_blocks(content: str, pattern: str, token_prefix: str):
    """
    Reemplaza bloques completos por tokens temporales para protegerlos
    de transformaciones regex posteriores.
    """
    blocks = []

    def replacer(match):
        blocks.append(match.group(0))
        return f'__{token_prefix}_{len(blocks) - 1}__'

    protected = re.sub(pattern, replacer, content, flags=re.DOTALL)
    return protected, blocks


def restore_blocks(content: str, token_prefix: str, blocks):
    """Restaura bloques previamente protegidos con stash_blocks."""
    for idx, block in enumerate(blocks):
        content = content.replace(f'__{token_prefix}_{idx}__', block)
    return content


def convert_markdown_tables(content: str) -> str:
    """Convierte tablas Markdown (pipe tables) a HTML."""
    table_block_pattern = re.compile(r'((?:^\|.*\|\s*$\n?){2,})', flags=re.MULTILINE)
    separator_pattern = re.compile(
        r'^\|\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$'
    )

    def render_table(block_match):
        block = block_match.group(1)
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if len(lines) < 2 or not separator_pattern.match(lines[1]):
            return block

        header_cells = [cell.strip() for cell in lines[0].strip('|').split('|')]
        body_lines = lines[2:]
        body_rows = [[cell.strip() for cell in line.strip('|').split('|')] for line in body_lines]

        thead = ''.join(f'<th>{cell}</th>' for cell in header_cells)
        tbody = ''
        for row in body_rows:
            padded = row + [''] * (len(header_cells) - len(row))
            cells = ''.join(f'<td>{cell}</td>' for cell in padded[:len(header_cells)])
            tbody += f'<tr>{cells}</tr>\n'

        return (
            '<table>\n'
            f'<thead><tr>{thead}</tr></thead>\n'
            '<tbody>\n'
            f'{tbody}'
            '</tbody>\n'
            '</table>\n'
        )

    return table_block_pattern.sub(render_table, content)


def markdown_to_html_content(md_content: str) -> str:
    """
    Convierte contenido Markdown a HTML.
    
    Args:
        md_content: Contenido en formato Markdown
        
    Returns:
        Contenido HTML
    """
    # Limpiar sintaxis de Mermaid primero
    md_content = clean_mermaid_syntax(md_content)
    
    mermaid_fence_pattern = re.compile(
        r'(?m)^[ \t]*```mermaid[ \t]*\n(.*?)(?:\n[ \t]*```[ \t]*(?=\n|$))',
        flags=re.DOTALL
    )
    code_fence_pattern = re.compile(
        r'(?m)^[ \t]*```([A-Za-z0-9_-]+)?[ \t]*\n(.*?)(?:\n[ \t]*```[ \t]*(?=\n|$))',
        flags=re.DOTALL
    )

    # Convertir bloques de código mermaid a divs
    def mermaid_to_div(match):
        mermaid_code = match.group(1)
        return f'<div class="mermaid">\n{mermaid_code}\n</div>'
    
    html_content = mermaid_fence_pattern.sub(mermaid_to_div, md_content)
    
    # Convertir otros bloques de código
    html_content = code_fence_pattern.sub(
        lambda m: (
            f'<pre><code class="language-{m.group(1) or "text"}">'
            f'{html.escape(m.group(2))}'
            f'</code></pre>'
        ),
        html_content
    )

    # Proteger bloques para no alterarlos en sustituciones de listas/párrafos/tablas
    html_content, pre_blocks = stash_blocks(
        html_content,
        r'<pre><code class="language-[^"]+">.*?</code></pre>',
        'PRE_BLOCK'
    )
    html_content, mermaid_blocks = stash_blocks(
        html_content,
        r'<div class="mermaid">\n.*?\n</div>',
        'MERMAID_BLOCK'
    )
    
    # Headers (h1-h6)
    html_content = re.sub(r'^###### (.*?)$', r'<h6>\1</h6>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^##### (.*?)$', r'<h5>\1</h5>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)

    # Horizontal rules
    html_content = re.sub(r'(?m)^[ \t]*---[ \t]*$', '<hr>', html_content)
    
    # Tablas Markdown
    html_content = convert_markdown_tables(html_content)

    # Listas
    html_content = re.sub(r'^\- (.*?)$', r'<li data-list="ul">\1</li>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^\d+\. (.*?)$', r'<li data-list="ol">\1</li>', html_content, flags=re.MULTILINE)
    html_content = re.sub(
        r'((?:<li data-list="ul">.*?</li>\n?)+)',
        lambda m: f'<ul>\n{m.group(1)}</ul>\n',
        html_content
    )
    html_content = re.sub(
        r'((?:<li data-list="ol">.*?</li>\n?)+)',
        lambda m: f'<ol>\n{m.group(1)}</ol>\n',
        html_content
    )
    html_content = re.sub(r' data-list="(?:ul|ol)"', '', html_content)
    
    # Negrita y cursiva
    html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
    html_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html_content)
    
    # Inline code
    html_content = re.sub(
        r'`([^`\n]*)`',
        lambda m: f'<code>{html.escape(m.group(1))}</code>',
        html_content
    )
    
    # Links
    html_content = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html_content)
    
    # Párrafos
    html_content = re.sub(r'\n\n', '</p>\n<p>', html_content)
    html_content = f'<p>{html_content}</p>'
    
    # Limpiar párrafos vacíos y mal formados
    html_content = re.sub(r'<p>\s*</p>', '', html_content)
    html_content = re.sub(r'<p>\s*(<h[1-6]>)', r'\1', html_content)
    html_content = re.sub(r'(</h[1-6]>)\s*</p>', r'\1', html_content)
    html_content = re.sub(r'<p>\s*(<(?:ul|ol|pre|table|div|hr)[^>]*>)', r'\1', html_content)
    html_content = re.sub(r'(</(?:ul|ol|pre|table|div)>)\s*</p>', r'\1', html_content)
    html_content = re.sub(r'<p>\s*<hr>\s*</p>', '<hr>', html_content)
    html_content = re.sub(r'<hr>\s*</p>', '<hr>', html_content)

    # Restaurar bloques protegidos
    html_content = restore_blocks(html_content, 'MERMAID_BLOCK', mermaid_blocks)
    html_content = restore_blocks(html_content, 'PRE_BLOCK', pre_blocks)
    
    # Post-restore: limpiar <p> que envuelven bloques restaurados (mermaid, pre, div)
    html_content = re.sub(r'<p>\s*(<div\b[^>]*>)', r'\1', html_content)
    html_content = re.sub(r'(</div>)\s*</p>', r'\1', html_content)
    html_content = re.sub(r'<p>\s*(<pre\b[^>]*>)', r'\1', html_content)
    html_content = re.sub(r'(</pre>)\s*</p>', r'\1', html_content)
    
    return html_content


def normalize_generated_links(
    html_content: str,
    category: str,
    base_path: Path,
    source_file: Path,
    target_file: Path
) -> str:
    """Normaliza href locales para que apunten a recursos generados en html/."""
    href_pattern = re.compile(r'href="([^"]+)"')
    docs_root = (base_path / 'docs').resolve()
    html_root = (base_path / 'html').resolve()

    def map_docs_to_html_target(resolved_source: Path):
        try:
            docs_rel = resolved_source.relative_to(docs_root)
        except ValueError:
            return None

        if resolved_source.suffix.lower() == '.md':
            if len(docs_rel.parts) >= 2 and docs_rel.parts[0] == 'architecture' and docs_rel.parts[1] == 'decisions':
                return html_root / 'architecture' / 'decisions.html'
            return (html_root / docs_rel).with_suffix('.html')

        if resolved_source.suffix.lower() in ('.yaml', '.yml') and docs_rel.as_posix() == 'api/openapi.yaml':
            return html_root / 'api' / 'openapi.yaml'

        return None

    def replace_href(match):
        href = match.group(1)

        if href.startswith(('http://', 'https://', '#', 'mailto:', 'javascript:')):
            return match.group(0)

        resolved_source = (source_file.parent / href).resolve()
        mapped_target = map_docs_to_html_target(resolved_source)

        if mapped_target is not None:
            normalized = os.path.relpath(mapped_target, start=target_file.parent.resolve()).replace('\\', '/')
            return f'href="{normalized}"'

        normalized = href
        if normalized.endswith('.md'):
            normalized = normalized[:-3] + '.html'

        if category == 'api' and normalized.endswith('openapi.yaml'):
            normalized = 'openapi.yaml'

        final_target = (target_file.parent / normalized).resolve()
        if final_target.exists():
            return f'href="{normalized}"'

        return 'href="#"'

    return href_pattern.sub(replace_href, html_content)


def generate_navigation(current_path: str) -> str:
    """
    Genera HTML de navegación.
    
    Args:
        current_path: Ruta del archivo actual
        
    Returns:
        HTML de navegación
    """
    nav_html = '<nav>\n<ul>\n'
    
    for path, label in NAV_ITEMS:
        # Calcular ruta relativa
        if current_path.startswith('functional/'):
            rel_path = f'../{path}'
        elif current_path.startswith('api/'):
            rel_path = f'../{path}'
        elif current_path.startswith('architecture/'):
            rel_path = f'../{path}'
        else:
            rel_path = path
        
        # Marcar elemento actual
        is_current = current_path in path or path in current_path
        active_class = ' class="active"' if is_current else ''
        
        nav_html += f'<li><a href="{rel_path}"{active_class}>{label}</a></li>\n'
    
    nav_html += '</ul>\n</nav>\n'
    return nav_html


def generate_html_template(
    title: str,
    content: str,
    current_path: str,
    category: str = 'general',
    generated_at: str = 'estable'
) -> str:
    """
    Genera plantilla HTML completa.
    
    Args:
        title: Título de la página
        content: Contenido HTML
        current_path: Ruta del archivo actual
        category: Categoría de la documentación
        
    Returns:
        HTML completo
    """
    navigation = generate_navigation(current_path)
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - APX Customer Data Service</title>
    <link rel="stylesheet" href="../css/bbva-styles.css">
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.0/dist/mermaid.min.js"></script>
</head>
<body>
    <header>
        <h1>{title}</h1>
        <p>APX Customer Data Service - Documentación Técnica</p>
    </header>

    {navigation}

    <main>
        {content}
    </main>

    <footer>
        <p>© 2026 BBVA - APX Framework 8.0.11</p>
        <p>Generado automáticamente el {generated_at}</p>
    </footer>

    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'base',
            securityLevel: 'loose',
            logLevel: 'error',
            themeVariables: {{
                primaryColor: '#e8eeff',
                primaryBorderColor: '#001391',
                primaryTextColor: '#070e46',
                secondaryColor: '#f7f8f8',
                secondaryBorderColor: '#e1e1e1',
                tertiaryColor: '#f4f4f4',
                lineColor: '#004481',
                textColor: '#070e46',
                mainBkg: '#e8eeff',
                nodeBorder: '#001391',
                clusterBkg: '#f7f8f8',
                clusterBorder: '#001391',
                titleColor: '#070e46',
                edgeLabelBackground: '#ffffff',
                actorBkg: '#e8eeff',
                actorBorder: '#001391',
                actorTextColor: '#070e46',
                actorLineColor: '#004481',
                signalColor: '#004481',
                signalTextColor: '#070e46',
                noteBkgColor: '#fff9eb',
                noteTextColor: '#070e46',
                noteBorderColor: '#d97706',
                activationBorderColor: '#001391',
                activationBkgColor: '#e8eeff',
                fontFamily: 'Inter, BentonBook, Helvetica, Arial, sans-serif',
                fontSize: '13px'
            }}
        }});

        // Retry mermaid rendering for blocks that fail on first pass
        window.addEventListener('load', function() {{
            setTimeout(function() {{
                const diagrams = document.querySelectorAll('.mermaid');
                diagrams.forEach(function(el, i) {{
                    if (!el.querySelector('svg') && el.textContent.trim()) {{
                        try {{
                            mermaid.render('mermaid-retry-' + i, el.textContent.trim()).then(function(result) {{
                                el.innerHTML = result.svg;
                            }});
                        }} catch(e) {{
                            el.innerHTML = '<div style="padding:16px;border-radius:8px;background:#fff2f1;border:1px solid #d63031;color:#d63031;font-size:13px;">' +
                                '<strong>⚠ Error rendering diagram</strong><pre style="margin:8px 0 0;color:#666;background:transparent;border:none;padding:0;">' +
                                e.message + '</pre></div>';
                        }}
                    }}
                }});
            }}, 500);
        }});
    </script>
</body>
</html>'''
    
    return html


def write_base_css(base_path: Path, density: str = 'comfortable') -> Path:
    """Escribe el CSS base en html/css con la densidad seleccionada."""
    css_path = base_path / 'html' / 'css' / 'bbva-styles.css'
    css_path.parent.mkdir(parents=True, exist_ok=True)
    css_content = BASE_CSS + "\n" + CSS_DENSITY_OVERRIDES.get(density, CSS_DENSITY_OVERRIDES['comfortable'])
    css_path.write_text(css_content, encoding='utf-8')
    return css_path


def build_index_cards(base_path: Path) -> str:
    """Construye tarjetas de acceso rápido por categoría."""
    card_chunks: List[str] = []
    for category_name, cfg in CATEGORIES.items():
        target_dir = base_path / cfg['target']
        files = sorted(target_dir.glob('*.html'))
        readme = target_dir / 'README.html'
        entry_rel = (
            str(readme.relative_to(base_path / 'html'))
            if readme.exists()
            else (str(files[0].relative_to(base_path / 'html')) if files else '#')
        )
        disabled = ' style="opacity:.65"' if not files else ''
        card_chunks.append(
            '<article class="apx-card">'
            f'<h3>{cfg["nav_label"]}</h3>'
            f'<p>{len(files)} archivo(s) HTML generado(s).</p>'
            f'<p><a href="{entry_rel}"{disabled}>Abrir sección</a></p>'
            '</article>'
        )
    return ''.join(card_chunks)


def generate_root_index(base_path: Path, generated_at: str) -> Path:
    """Genera html/index.html como landing de documentación."""
    html_root = base_path / 'html'
    html_root.mkdir(parents=True, exist_ok=True)
    index_path = html_root / 'index.html'
    nav = generate_navigation('index.html')
    cards = build_index_cards(base_path)
    total_docs = sum(len(list((base_path / cfg['target']).glob('*.html'))) for cfg in CATEGORIES.values())

    index_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APX Customer Data Service - Documentación</title>
    <link rel="stylesheet" href="css/bbva-styles.css">
</head>
<body>
    <header>
        <h1>APX Customer Data Service</h1>
        <p>Portal de documentación técnica y funcional</p>
    </header>

    {nav}

    <main>
        <h2>Resumen</h2>
        <div class="apx-kpi-grid">
            <article class="apx-kpi">
                <strong>{total_docs}</strong>
                <span>páginas HTML disponibles</span>
            </article>
            <article class="apx-kpi">
                <strong>{len(CATEGORIES)}</strong>
                <span>categorías documentales</span>
            </article>
            <article class="apx-kpi">
                <strong>Mermaid</strong>
                <span>diagramas soportados con saneamiento</span>
            </article>
        </div>

        <h2>Accesos por categoría</h2>
        <section class="apx-cards">
            {cards}
        </section>
    </main>

    <footer>
        <p>© 2026 BBVA - APX Framework 8.0.11</p>
        <p>Generado automáticamente el {generated_at}</p>
    </footer>
</body>
</html>'''

    index_path.write_text(index_html, encoding='utf-8')
    return index_path


def generate_decisions_page(base_path: Path, generated_at: str, verbose: bool = False) -> bool:
    """
    Genera html/architecture/decisions.html agregando ADRs desde
    docs/architecture/decisions/*.md.
    """
    decisions_dir = base_path / 'docs' / 'architecture' / 'decisions'
    target_file = base_path / 'html' / 'architecture' / 'decisions.html'

    md_files = sorted(decisions_dir.glob('*.md')) if decisions_dir.exists() else []
    if not md_files:
        content = (
            '<h1>ADRs de Arquitectura</h1>'
            '<p>No se encontraron archivos en <code>docs/architecture/decisions/</code>.</p>'
        )
        full_html = generate_html_template(
            'ADRs de Arquitectura',
            content,
            'architecture/decisions.html',
            'architecture',
            generated_at
        )
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(full_html, encoding='utf-8')
        if verbose:
            print("  ℹ️ No hay ADRs fuente; se generó página informativa decisions.html")
        return True

    toc_items = ''.join(
        f'<li><a href="#adr-{idx + 1}">{html.escape(md_file.stem)}</a></li>'
        for idx, md_file in enumerate(md_files)
    )
    sections = []
    for idx, md_file in enumerate(md_files):
        md_content = md_file.read_text(encoding='utf-8')
        section_html = markdown_to_html_content(md_content)
        section_html = normalize_generated_links(
            section_html,
            'architecture',
            base_path,
            md_file,
            target_file
        )
        sections.append(
            f'<section id="adr-{idx + 1}">'
            f'<h2>{html.escape(md_file.stem)}</h2>'
            f'{section_html}'
            '</section>'
        )

    content = (
        '<h1>ADRs de Arquitectura</h1>'
        f'<p>Se encontraron <strong>{len(md_files)}</strong> ADR(s) en '
        '<code>docs/architecture/decisions/</code>.</p>'
        '<h2>Índice de decisiones</h2>'
        f'<ol>{toc_items}</ol>'
        + ''.join(sections)
    )

    full_html = generate_html_template(
        'ADRs de Arquitectura',
        content,
        'architecture/decisions.html',
        'architecture',
        generated_at
    )
    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.write_text(full_html, encoding='utf-8')

    if verbose:
        print(f"  ✅ decisions/*.md → {target_file.name} ({len(md_files)} ADRs)")
    return True


def process_markdown_file(
    source_file: Path,
    target_file: Path,
    category: str,
    generated_at: str,
    base_path: Path,
    category_md_files: List[Path] = None,
    verbose: bool = False
) -> bool:
    """
    Procesa un archivo Markdown y genera HTML.
    
    Args:
        source_file: Archivo Markdown fuente
        target_file: Archivo HTML destino
        category: Categoría de la documentación
        verbose: Modo verbose
        
    Returns:
        True si se procesó exitosamente
    """
    try:
        # Leer contenido Markdown
        with open(source_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convertir a HTML
        html_content = markdown_to_html_content(md_content)
        html_content = normalize_generated_links(
            html_content,
            category,
            base_path,
            source_file,
            target_file
        )
        
        # Inyectar índice automático de páginas de la categoría en README
        if source_file.stem.lower() == 'readme' and category_md_files:
            def extract_title(md_file: Path) -> str:
                if md_file.stem.lower() == 'readme':
                    return 'README'
                try:
                    text = md_file.read_text(encoding='utf-8')
                    for line in text.splitlines():
                        stripped = line.strip()
                        if stripped.startswith('# '):
                            return stripped[2:].strip()
                except Exception:
                    pass
                return md_file.stem.replace('-', ' ').replace('_', ' ').title()

            items = []
            for md in sorted(category_md_files, key=lambda p: p.name.lower()):
                if md.stem.lower() == 'readme':
                    continue
                label = html.escape(extract_title(md))
                href = f"{md.stem}.html"
                items.append(f'<li><a href="{href}">{label}</a></li>')

            if items:
                auto_section = (
                    '<section class="apx-card">'
                    '<h2>🔗 Accesos automáticos de la categoría</h2>'
                    '<p>Sección generada automáticamente por el script para asegurar navegabilidad completa.</p>'
                    '<ul>' + ''.join(items) + '</ul>'
                    '</section>'
                )
                html_content += auto_section

        # Extraer título del primer h1 o usar nombre de archivo
        title_match = re.search(r'<h1>(.*?)</h1>', html_content)
        title = title_match.group(1) if title_match else source_file.stem.replace('-', ' ').title()
        
        # Calcular ruta relativa para navegación
        relative_path = str(target_file.relative_to(target_file.parent.parent))
        
        # Generar HTML completo
        full_html = generate_html_template(
            title,
            html_content,
            relative_path,
            category,
            generated_at
        )
        
        # Crear directorio destino si no existe
        target_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Escribir HTML
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        if verbose:
            print(f"  ✅ {source_file.name} → {target_file.name}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error procesando {source_file.name}: {e}")
        return False


def process_category(
    category_name: str,
    config: Dict,
    base_path: Path,
    generated_at: str,
    verbose: bool = False
) -> int:
    """
    Procesa todos los archivos de una categoría.
    
    Args:
        category_name: Nombre de la categoría
        config: Configuración de la categoría
        base_path: Ruta base del proyecto
        verbose: Modo verbose
        
    Returns:
        Número de archivos procesados
    """
    source_dir = base_path / config['source']
    target_dir = base_path / config['target']
    
    if not source_dir.exists():
        if verbose:
            print(f"  ⚠️ Directorio {source_dir} no existe, omitiendo")
        return 0
    
    # Obtener todos los archivos .md
    md_files = list(source_dir.glob('*.md'))
    
    if not md_files:
        if verbose:
            print(f"  ℹ️ No se encontraron archivos .md en {source_dir}")
        return 0
    
    processed = 0
    for md_file in md_files:
        html_file = target_dir / f"{md_file.stem}.html"
        if process_markdown_file(
            md_file,
            html_file,
            category_name,
            generated_at,
            base_path,
            md_files,
            verbose
        ):
            processed += 1
    
    return processed


def deterministic_build_stamp(base_path: Path) -> str:
    """
    Calcula un sello de build determinista basado en la última modificación
    de cualquier Markdown fuente.
    """
    newest_mtime = 0.0
    for category_cfg in CATEGORIES.values():
        source_dir = base_path / category_cfg['source']
        if source_dir.exists():
            for md_file in source_dir.glob('*.md'):
                newest_mtime = max(newest_mtime, md_file.stat().st_mtime)

    if newest_mtime == 0.0:
        return "estable"

    dt = datetime.fromtimestamp(newest_mtime, tz=timezone.utc)
    return dt.strftime('%Y-%m-%d %H:%M:%S UTC')


def copy_openapi_artifact(base_path: Path, verbose: bool = False) -> bool:
    """Copia docs/api/openapi.yaml a html/api/openapi.yaml para evitar enlaces rotos."""
    source = base_path / 'docs' / 'api' / 'openapi.yaml'
    target = base_path / 'html' / 'api' / 'openapi.yaml'

    if not source.exists():
        if verbose:
            print("  ⚠️ No existe docs/api/openapi.yaml, se omite copia del artefacto OpenAPI")
        return False

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source.read_text(encoding='utf-8'), encoding='utf-8')

    if verbose:
        print(f"  ✅ {source.relative_to(base_path)} → {target.relative_to(base_path)}")

    return True


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description='Genera documentación HTML APX desde archivos Markdown'
    )
    parser.add_argument(
        '--category',
        choices=list(CATEGORIES.keys()),
        help='Procesar solo una categoría específica'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Modo verbose'
    )
    parser.add_argument(
        '--density',
        choices=['compact', 'comfortable'],
        default='comfortable',
        help='Densidad visual del layout HTML (default: comfortable)'
    )
    
    args = parser.parse_args()
    
    # Determinar ruta base del proyecto (funciona aunque el script viva dentro de .agents/skills/...)
    current = Path(__file__).resolve()
    base_path = None
    for candidate in [current.parent] + list(current.parents):
        if (candidate / 'docs').exists() and (candidate / 'html').exists():
            base_path = candidate
            break

    if base_path is None:
        print("❌ No se pudo localizar la raíz del proyecto (se esperan carpetas 'docs/' y 'html/').")
        return 1
    
    print("🔄 Generando documentación HTML APX...\n")
    generated_at = deterministic_build_stamp(base_path)
    write_base_css(base_path, args.density)
    
    # Determinar qué categorías procesar
    categories_to_process = (
        {args.category: CATEGORIES[args.category]}
        if args.category
        else CATEGORIES
    )
    
    total_files = 0
    
    # Procesar cada categoría
    for category_name, config in categories_to_process.items():
        print(f"📁 Procesando {category_name}/")
        
        files_processed = process_category(
            category_name,
            config,
            base_path,
            generated_at,
            args.verbose
        )
        
        total_files += files_processed
        print(f"  📊 {files_processed} archivo(s) generado(s)\n")

    if args.category is None or args.category == 'api':
        copy_openapi_artifact(base_path, args.verbose)

    if (args.category is None or args.category == 'architecture') and generate_decisions_page(
        base_path,
        generated_at,
        args.verbose
    ):
        total_files += 1

    index_path = generate_root_index(base_path, generated_at)
    if args.verbose:
        print(f"🏠 Índice raíz generado: {index_path}")
    
    # Resumen final
    print(f"🎉 Documentación HTML generada exitosamente")
    print(f"🎨 Densidad aplicada: {args.density}")
    print(f"📍 Total: {total_files} archivos HTML creados")
    print(f"📂 Ubicación: {base_path / 'html'}/")
    
    return 0 if total_files > 0 else 1


if __name__ == '__main__':
    sys.exit(main())
