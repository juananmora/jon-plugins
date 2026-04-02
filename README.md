# jon-plugins

Colección de **plugins y activos reutilizables para GitHub Copilot** ✨

Este repositorio agrupa agentes, skills, comandos, instrucciones y hooks para estandarizar tareas de ingeniería (documentación, calidad, testing, automatizaciones) en proyectos de desarrollo.

## 🎯 Objetivo

- Acelerar tareas repetibles (documentación, revisiones, tests) con flujos guiados y consistentes.
- Centralizar estándares corporativos (plantillas, instrucciones, guías) para que se apliquen de forma homogénea.
- Proveer componentes listos para reutilizar como “building blocks” en nuevos repos.

## 📦 Estructura del plugin

```
jon-plugins/
├── .claude-plugin/
│   ├── marketplace.json          # Registro local/legacy del plugin
│   └── plugin.json               # Metadatos del plugin
├── .github/
│   └── plugin/
│       └── marketplace.json      # Registro autoritativo del plugin
├── agents/                       # Agentes IA especializados
│   ├── agent-orchestrator-parallel.agent.md
│   ├── apx_code_generator-local.agent.md
│   ├── apx_doc_generator.agent.md
│   └── quality-sonar.agent.md
├── commands/                     # Slash commands reutilizables
│   ├── code-reviewed.md
│   ├── hello.md
│   └── review-pr.md
├── hooks/                        # Hooks del ciclo de vida de Copilot
│   ├── copilot-hooks.json
│   ├── collect_and_report.py
│   ├── log-subagent.sh
│   ├── log-subagent-end.sh
│   └── save-before-compact.sh
├── instructions/                 # Instrucciones aplicables a repos consumidores
│   ├── apx_documentation.instructions.md
│   ├── apx_html_documentation.instructions.md
│   └── quality-sonar.instructions.md
├── skills/                       # Skills autocontenidos (conocimiento + scripts)
│   ├── jonas-html-docs-generator/
│   │   ├── SKILL.md              # Punto de entrada
│   │   ├── agents/
│   │   │   └── openai.yaml
│   │   ├── references/
│   │   │   └── structure-and-nav.md
│   │   └── scripts/
│   │       ├── generate-html-docs.py
│   │       └── validate-skill.py
│   └── jonas-unit-test-v2/
│       ├── SKILL.md              # Punto de entrada
│       ├── agents/
│       │   └── openai.yaml
│       ├── references/
│       │   ├── section-01-estandares-de-estilo.md
│       │   ├── section-02-introduccion.md
│       │   ├── section-03-patrones.md
│       │   ├── section-04-antipatrones.md
│       │   ├── section-05-directrices-generales.md
│       │   ├── section-06-reglas-de-sonda.md
│       │   ├── section-07-mejores-practicas-de-seguridad.md
│       │   ├── section-08-seguridad-en-el-acceso-autenticacion-y-autorizacion-de-usuarios.md
│       │   ├── section-09-enlaces-de-interes.md
│       │   ├── section-10-ejemplos-de-test.md
│       │   └── section-11-parametros-script.md
│       └── scripts/
│           └── generate_test_report.py
├── CLAUDE.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE
├── README.md
├── SECURITY.md
└── SUPPORT.md
```

## 🤖 Agentes

Agentes IA con frontmatter YAML (`name`, `description`, `tools`) y comportamiento definido en Markdown.

| Agente | Descripción |
|--------|-------------|
| `agent-orchestrator-parallel` | Orquesta el ciclo de vida completo: Plan → Docs → Código → (SonarQube + Tests en **paralelo**) → Finalizar. Incluye pausas obligatorias antes de commit. |
| `apx_code_generator-local` | Genera código Java/Spring Boot siguiendo patrones del framework. Lee guías de estilo y seguridad antes de codificar. |
| `apx_doc_generator` | Genera documentación funcional y de arquitectura completa para proyectos. |
| `quality-sonar` | Análisis de calidad con SonarQube: evalúa, genera informes y recomienda mejoras. Nunca modifica código. |

## 🛠️ Skills

Módulos de conocimiento autocontenidos con `SKILL.md` como punto de entrada, `references/` para conocimiento estático y `scripts/` para utilidades Python.

| Skill | Descripción |
|-------|-------------|
| `jonas-html-docs-generator` | Convierte documentación Markdown en `docs/` a HTML con estilos corporativos. Incluye saneamiento de bloques Mermaid. |
| `jonas-unit-test-v2` | Generación y ejecución de tests unitarios con JUnit 5 + Mockito + JaCoCo. Cobertura mínima 80%. Patrón AAA + `@DisplayName` Given-When-Then. |

## ⚡ Comandos

Slash commands invocables vía `/jon-plugins:<comando>`.

| Comando | Descripción |
|---------|-------------|
| `hello` | Saludo personalizado al usuario. |
| `code-reviewed` | Code review de un pull request. |
| `review-pr` | Revisión comprehensiva de PR usando agentes especializados. |

## 📋 Instrucciones

Reglas aplicables a ficheros en repos consumidores. Definen convenciones de nombrado, plantillas y quality gates.

| Instrucción | Descripción |
|-------------|-------------|
| `apx_documentation` | Estándares y reglas para documentación de proyectos. |
| `apx_html_documentation` | Estándares para generación de documentación HTML con estilos corporativos. |
| `quality-sonar` | Procedimientos detallados para análisis de calidad con SonarQube. |

## 🪝 Hooks

Eventos del ciclo de vida de Copilot configurados en `hooks/copilot-hooks.json`:

| Evento | Script | Descripción |
|--------|--------|-------------|
| `PreCompact` | `save-before-compact.sh` | Guarda contexto antes de compactar. |
| `SubagentStart` | `log-subagent.sh` | Registra inicio de subagente. |
| `SubagentStop` | `log-subagent-end.sh` | Registra fin de subagente. |

## 🔧 Registro del plugin

- **Autoritativo**: `.github/plugin/marketplace.json` — catálogo oficial referenciado por GitHub.
- **Legacy/local**: `.claude-plugin/marketplace.json` — copia local para compatibilidad.

## ▶️ Validación

```bash
# Validar estructura de un skill
python3 skills/jonas-html-docs-generator/scripts/validate-skill.py skills/jonas-html-docs-generator

# Generar documentación HTML (desde un repo consumidor)
python3 .agents/skills/jonas-html-docs-generator/scripts/generate-html-docs.py --verbose

# Generar informe de tests unitarios (desde un repo consumidor)
python3 .agents/skills/jonas-unit-test-v2/scripts/generate_test_report.py \
  --project "PROJECT" --total 10 --passed 10 --failed 0 --errors 0 \
  --cov-classes 85 --cov-methods 80 --cov-lines 82 --output testresults.md
```

## 🤝 Contribuir

Lee la guía en [CONTRIBUTING.md](CONTRIBUTING.md) y el [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) antes de enviar cambios.

### Añadir un nuevo agente

1. Crear `agents/<nombre>.agent.md`
2. Añadir frontmatter YAML con `name`, `description` y `tools`
3. Escribir instrucciones de comportamiento en el cuerpo Markdown
4. Agentes de solo lectura deben incluir reglas de parada explícitas

### Añadir un nuevo skill

1. Crear `skills/<nombre-skill>/SKILL.md` — punto de entrada
2. Añadir `references/` para conocimiento estático, `scripts/` para utilidades Python
3. Opcionalmente añadir `agents/openai.yaml` para definición compatible con OpenAI
4. Validar: `python3 scripts/validate-skill.py skills/<nombre-skill>`

### Estilo de commits

```text
fix/feat/chore/test/refactor: Descripción corta (max 50 chars)

- Bullet conciso 1
- Bullet conciso 2
```

## 📄 Licencia

MIT: ver [LICENSE](LICENSE).
