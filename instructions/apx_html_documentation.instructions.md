---
description: "Estándares y reglas para generación de documentación HTML con estilos BBVA para proyectos APX"
applyTo: "**/html/**/*.html, **/docs/**/*.html"
---

# Instrucciones de Documentación HTML APX

Estas instrucciones definen los estándares obligatorios para generar documentación en formato **HTML** con estilos corporativos BBVA para proyectos APX (BBVA Application eXperience Platform).

## Reglas Generales

### Estructura de carpetas
- Crear carpeta `/html` en la raíz del proyecto para documentación HTML
- Organizar en subcarpetas que reflejen la estructura de `/docs`:
  - `html/index.html` - Página principal
  - `html/functional/` - Documentación funcional
  - `html/architecture/` - Documentación de arquitectura
  - `html/api/` - Documentación de API
  - `html/css/` - Hojas de estilo (copiar desde template)

### CSS Corporativo BBVA

> 📁 **Template CSS**: `.github/templates/bbva-styles.css`

- **OBLIGATORIO**: Copiar el CSS template a `html/css/bbva-styles.css`
- Referenciar el CSS en cada archivo HTML según su ubicación:

```html
<!-- Desde html/index.html -->
<link rel="stylesheet" href="css/bbva-styles.css">

<!-- Desde html/functional/*.html, html/architecture/*.html, html/api/*.html -->
<link rel="stylesheet" href="../css/bbva-styles.css">
```

**Comando para copiar el CSS:**
```bash
mkdir -p html/css
cp .github/templates/bbva-styles.css html/css/
```

> ⚠️ **IMPORTANTE**: Consulta el archivo `.github/templates/bbva-styles.css` para ver todas las variables CSS, clases y componentes disponibles (badges, cards, tablas, info-boxes, etc.)

## Estructura HTML Base

### Template de página HTML

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Título] - [Nombre Proyecto] | BBVA APX</title>
    <link rel="stylesheet" href="[ruta-relativa]/css/bbva-styles.css">
    <!-- Mermaid.js para diagramas -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
</head>
<body>
    <header>
        <h1>🏦 [Nombre del Proyecto]</h1>
        <p>[Descripción breve]</p>
    </header>

    <nav>
        <ul>
            <!-- Menú de navegación unificado -->
            <li><a href="[ruta]/index.html">🏠 Inicio</a></li>
            <li><a href="[ruta]/functional/README.html">📋 Funcional</a></li>
            <li><a href="[ruta]/functional/requirements.html">📝 Requisitos</a></li>
            <li><a href="[ruta]/functional/user-stories.html">👤 User Stories</a></li>
            <li><a href="[ruta]/functional/use-cases.html">🎯 Casos de Uso</a></li>
            <li><a href="[ruta]/architecture/README.html">🏗️ Arquitectura</a></li>
            <li><a href="[ruta]/architecture/data-model.html">📊 Modelo Datos</a></li>
            <li><a href="[ruta]/architecture/decisions.html">📋 ADRs</a></li>
            <li><a href="[ruta]/api/README.html">🔌 API</a></li>
            <li><a href="[ruta]/api/endpoints.html">📡 Endpoints</a></li>
        </ul>
    </nav>

    <main>
        <!-- Contenido principal aquí -->
    </main>

    <footer>
        <p>© 2026 BBVA - APX Documentation</p>
        <p>Generado automáticamente | Última actualización: [fecha]</p>
    </footer>

    <!-- Configuración Mermaid -->
    <script>
        mermaid.initialize({
            startOnLoad: true,
            theme: 'default',
            themeVariables: {
                primaryColor: '#5BBEFF',
                primaryBorderColor: '#004481',
                lineColor: '#1973B8',
                actorBkg: '#F7F8F8',
                actorBorder: '#004481',
                actorTextColor: '#072146',
                signalColor: '#1973B8',
                signalTextColor: '#072146',
                noteBkgColor: '#FFF3CD',
                noteTextColor: '#072146',
                fontFamily: 'BentonSans, Helvetica Neue, Helvetica, Arial, sans-serif'
            }
        });
    </script>
</body>
</html>
```

## Diagramas Mermaid

### Configuración de colores para nodos

**IMPORTANTE**: Los nodos deben tener colores de texto apropiados según su fondo:

```html
<!-- Fondos OSCUROS → Texto BLANCO (#fff) -->
style NodeName fill:#004481,color:#fff,stroke:#072146
style NodeName fill:#1973B8,color:#fff,stroke:#004481
style NodeName fill:#48AE64,color:#fff,stroke:#2D8B4E
style NodeName fill:#CC3333,color:#fff,stroke:#A02929

<!-- Fondos CLAROS → Texto OSCURO (#072146) -->
style NodeName fill:#5BBEFF,color:#072146,stroke:#004481
style NodeName fill:#F8CD51,color:#072146,stroke:#C9A441
style NodeName fill:#F7F8F8,color:#072146,stroke:#D3D8DE
```

### Diagrama de Flujo (flowchart)

```html
<div class="mermaid">
flowchart TB
    subgraph Cliente["🖥️ Cliente"]
        A[Aplicación]
    end
    
    subgraph APX["🏦 APX Service"]
        B[Transaction]
        C[Library]
        D[DTO]
    end
    
    A --> B
    B --> C
    C --> D
    
    style A fill:#5BBEFF,color:#072146,stroke:#004481
    style B fill:#004481,color:#fff,stroke:#072146
    style C fill:#1973B8,color:#fff,stroke:#004481
    style D fill:#48AE64,color:#fff,stroke:#2D8B4E
</div>
```

### Diagrama de Secuencia

```html
<div class="mermaid">
sequenceDiagram
    participant C as 🖥️ Cliente
    participant T as 📦 Transaction
    participant L as 📚 Library
    participant DB as 🗄️ Database
    
    C->>T: Request
    T->>L: Process
    L->>DB: Query
    DB-->>L: Data
    L-->>T: Result
    T-->>C: Response
</div>
```

### Diagrama ER

```html
<div class="mermaid">
erDiagram
    CUSTOMER ||--o{ ORDER : places
    CUSTOMER {
        string id PK
        string name
        string email
    }
    ORDER {
        string id PK
        string customerId FK
        date createdAt
    }
</div>
```

### Diagrama C4

```html
<div class="mermaid">
C4Context
    title Sistema de Contexto - [Nombre Proyecto]
    
    Person(user, "Usuario", "Usuario del sistema")
    System(system, "APX Service", "Microservicio APX")
    System_Ext(external, "Sistema Externo", "API externa")
    
    Rel(user, system, "Usa")
    Rel(system, external, "Consume")
</div>
```

## Componentes HTML Disponibles

> 📁 **Referencia completa de clases CSS**: Ver `.github/templates/bbva-styles.css`

Las siguientes clases están disponibles en el CSS template:

| Clase | Uso |
|-------|-----|
| `.status-implemented`, `.status-pending`, `.status-high` | Estados de requisitos |
| `.badge-java`, `.badge-apx`, `.badge-maven`, `.badge-spring` | Tecnologías |
| `.method-get`, `.method-post`, `.method-put`, `.method-delete` | Métodos HTTP |
| `.info-box.note`, `.info-box.warning`, `.info-box.success`, `.info-box.danger` | Cajas informativas |
| `.cards-grid`, `.card` | Grid de tarjetas |
| `.doc-link` | Enlaces destacados |

### Ejemplos de uso

```html
<!-- Secciones -->
<section>
    <h2>📋 Título de Sección</h2>
    <p>Contenido...</p>
</section>

<!-- Badges -->
<span class="status status-implemented">Implementado</span>
<span class="badge badge-java">Java 11</span>
<span class="method-badge method-get">GET</span>

<!-- Info boxes -->
<div class="info-box warning">
    <strong>⚠️ Advertencia:</strong> Precaución necesaria.
</div>

<!-- Cards -->
<div class="cards-grid">
    <div class="card">
        <h4>📚 Título</h4>
        <p>Descripción...</p>
        <a href="link.html">Ver más →</a>
    </div>
</div>
```

## Archivos a Generar

### Estructura obligatoria

```
html/
├── index.html                    # ✅ OBLIGATORIO - Página principal
├── css/
│   └── bbva-styles.css          # ✅ OBLIGATORIO - Copiar desde template
├── functional/
│   ├── README.html              # ✅ OBLIGATORIO - Overview funcional
│   ├── requirements.html        # ✅ OBLIGATORIO - Con diagramas
│   ├── user-stories.html        # ✅ OBLIGATORIO - Formato Gherkin
│   └── use-cases.html           # ✅ OBLIGATORIO - Con diagramas
├── architecture/
│   ├── README.html              # ✅ OBLIGATORIO - Diagramas C4
│   ├── data-model.html          # ✅ OBLIGATORIO - Diagrama ER
│   └── decisions.html           # ✅ OBLIGATORIO - ADRs compilados
└── api/
    ├── README.html              # ✅ OBLIGATORIO - Referencia API
    └── endpoints.html           # ✅ OBLIGATORIO - Con ejemplos
```

### Checklist de validación

Antes de completar la generación, verificar:

- [ ] CSS copiado desde `.github/templates/bbva-styles.css` a `html/css/`
- [ ] Todos los archivos HTML usan el template base
- [ ] Navegación unificada en todos los archivos (10 enlaces)
- [ ] Rutas relativas correctas según ubicación del archivo
- [ ] Diagramas Mermaid renderizan correctamente
- [ ] Colores de nodos apropiados (texto blanco en fondos oscuros)
- [ ] Footer con año y fecha de generación
- [ ] Responsive design funciona en móvil
- [ ] Impresión limpia sin elementos de navegación

## Conversión desde Markdown

### Proceso recomendado

1. **Leer** el archivo `.md` fuente desde `/docs`
2. **Extraer** secciones, tablas y código
3. **Convertir** Markdown a HTML semántico
4. **Transformar** diagramas Mermaid a `<div class="mermaid">`
5. **Aplicar** clases CSS según tipo de contenido
6. **Añadir** navegación y estructura de página
7. **Validar** renderizado de diagramas

### Mapeo de elementos

| Markdown | HTML |
|----------|------|
| `# Título` | `<h1>Título</h1>` en header |
| `## Sección` | `<section><h2>Sección</h2>...</section>` |
| `### Subsección` | `<h3>Subsección</h3>` |
| `` ```mermaid `` | `<div class="mermaid">...</div>` |
| `` ```java `` | `<pre><code class="language-java">...</code></pre>` |
| `| tabla |` | `<table>...</table>` |
| `- lista` | `<ul><li>...</li></ul>` |
| `> nota` | `<div class="info-box note">...</div>` |

## Referencias

- [CSS Template](.github/templates/bbva-styles.css) - Estilos BBVA oficiales
- [Mermaid.js Documentation](https://mermaid.js.org/)
- [BBVA Brand Guidelines](https://www.bbva.com)
- [APX Documentation Instructions](apx_documentation.instructions.md)

---

**Versión:** 1.0  
**Última actualización:** 2026-01-22  
**Aplica a:** Proyectos APX con documentación HTML
