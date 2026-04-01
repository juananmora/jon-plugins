---
description: "Estándares y reglas para documentación de proyectos APX"
applyTo: "**/docs/**/*.md, **/README.md, **/CHANGELOG.md"
---

# Instrucciones de Documentación APX

Estas instrucciones definen los estándares obligatorios para generar documentación funcional y de arquitectura en proyectos APX (BBVA Application eXperience Platform).

## Reglas

### Estructura de documentación
- Crear carpeta `/docs` en la raíz del proyecto para toda la documentación
- Organizar en subcarpetas: `functional/`, `architecture/`, `api/`
- Incluir siempre `docs/README.md` como índice principal
- Versionar documentación junto con el código fuente

### Formato y estilo
- Usar **Markdown** exclusivamente para documentación textual
- Seguir [GitHub Flavored Markdown](https://github.github.com/gfm/)
- Incluir tabla de contenidos en documentos largos (>500 líneas)
- Usar código de bloque con lenguaje específico (```java, ```yaml, etc.)
- Incluir emojis para mejorar legibilidad: 📚 🎯 ⚠️ ✅ ❌

### Diagramas
- Usar **Mermaid** para diagramas simples (embebidos en Markdown)
- Usar **PlantUML** para diagramas complejos (archivos `.puml` separados)
- Incluir diagrama de arquitectura C4 nivel 1 (Context) obligatorio
- Incluir diagrama de arquitectura C4 nivel 2 (Container) obligatorio
- Guardar diagramas en `docs/architecture/diagrams/`

### Documentación funcional
- Describir funcionalidades desde perspectiva de negocio, no técnica
- Incluir casos de uso principales con flujos alternativos
- Documentar requisitos funcionales numerados (RF-001, RF-002...)
- Usar formato Gherkin (Given-When-Then) para escenarios si aplica

### Documentación de arquitectura
- Incluir decisiones arquitectónicas (ADR) en `docs/architecture/decisions/`
- Documentar patrones arquitectónicos usados (Hexagonal, CQRS, etc.)
- Listar dependencias externas y APIs consumidas
- Incluir modelo de datos con entidades y relaciones

### Documentación de API
- Generar especificación **OpenAPI 3.0+** válida
- Incluir ejemplos de request/response para cada endpoint
- Documentar códigos de error HTTP con descripciones
- Usar Swagger UI para validación visual

### README.md del proyecto
- Incluir sección "Descripción" con propósito del microservicio
- Incluir sección "Arquitectura" con diagrama de alto nivel
- Incluir sección "Getting Started" con instrucciones de construcción
- Incluir sección "API" con enlace a especificación OpenAPI
- Incluir sección "Documentación" con enlaces a `/docs`

## Estándares de estilo

### Títulos y secciones
```markdown
# Título principal (H1) - Solo uno por archivo
## Sección principal (H2)
### Subsección (H3)
#### Detalle (H4)
```

### Código inline y bloques
```markdown
Usa `backticks` para código inline.

Usa bloques con lenguaje específico:
```java
@RestController
public class PaymentController {
    // ...
}
```
```

### Listas
```markdown
- Usar listas con guiones
  - Subítems indentados con 2 espacios
- No mezclar guiones y asteriscos

1. Listas numeradas para pasos secuenciales
2. Usar numeración automática
3. Mantener coherencia
```

### Enlaces
```markdown
[Texto del enlace](ruta/relativa/archivo.md)
[Enlace externo](https://ejemplo.com)
[Enlace con título](archivo.md "Tooltip")
```

### Tablas
```markdown
| Columna 1 | Columna 2 | Columna 3 |
|-----------|-----------|-----------|
| Dato 1    | Dato 2    | Dato 3    |
| Dato 4    | Dato 5    | Dato 6    |
```

### Notas y advertencias
```markdown
> **Nota:** Información adicional importante

> ⚠️ **Advertencia:** Precaución necesaria

> ✅ **Buena práctica:** Recomendación
```

## Buenas prácticas

### Sincronización con código
- Actualizar documentación en cada Pull Request que modifique funcionalidad
- Incluir validación de documentación en pipeline CI/CD
- Revisar documentación en code reviews
- Usar plugins Maven para generación automática (springdoc, maven-site)

### Mantenibilidad
- Preferir "documentación como código" (diagramas en PlantUML/Mermaid)
- Evitar duplicar información (enlazar en lugar de copiar)
- Mantener documentación cerca del código que describe
- Usar includes/referencias para reutilizar contenido común

### Accesibilidad
- Usar lenguaje claro y directo
- Evitar jerga innecesaria
- Incluir glosario de términos técnicos si es necesario
- Proporcionar contexto suficiente para nuevos desarrolladores

### Versionado
- Incluir fecha de última actualización en documentos importantes
- Mantener CHANGELOG.md actualizado con cambios significativos
- Archivar documentación obsoleta en `/docs/archive` con fecha

## Dependencias y herramientas

### Generación automática
```xml
<!-- Maven plugin para OpenAPI -->
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
</dependency>

<!-- Maven site plugin -->
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-site-plugin</artifactId>
</plugin>
```

### Validación
```bash
# Validar Markdown
npx markdownlint-cli docs/**/*.md

# Validar OpenAPI
npx @apidevtools/swagger-cli validate docs/api/openapi.yaml

# Generar site Maven
mvn site
```

### Visualización de diagramas
- [Mermaid Live Editor](https://mermaid.live/)
- [PlantUML Online](https://www.plantuml.com/plantuml/)
- [Swagger Editor](https://editor.swagger.io/)

## Referencias relacionadas

- [C4 Model Documentation](https://c4model.com/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Architecture Decision Records](https://adr.github.io/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Mermaid Syntax](https://mermaid.js.org/intro/)
- [PlantUML Guide](https://plantuml.com/guide)

## Plantillas recomendadas

### Template ADR
```markdown
# ADR-XXX: [Título]

**Estado:** [Propuesto | Aceptado | Rechazado | Obsoleto]
**Fecha:** YYYY-MM-DD
**Autores:** [Nombres]

## Contexto
[Descripción del problema o decisión a tomar]

## Decisión
[Qué se decidió y por qué]

## Alternativas consideradas
- Opción A: [Descripción y razón de descarte]
- Opción B: [Descripción y razón de descarte]

## Consecuencias
**Positivas:**
- ✅ Consecuencia 1
- ✅ Consecuencia 2

**Negativas:**
- ⚠️ Consecuencia 1
- ⚠️ Consecuencia 2

## Referencias
- [Link 1]
- [Link 2]
```

### Template Caso de Uso
```markdown
# UC-XXX: [Nombre del caso de uso]

**Actor principal:** [Usuario/Sistema]
**Nivel:** [Objetivo del usuario | Subfunción]
**Precondiciones:** [Qué debe ser cierto antes]
**Postcondiciones:** [Qué será cierto después]

## Flujo principal
1. Paso 1
2. Paso 2
3. ...

## Flujos alternativos
**3a. [Condición alternativa]**
1. Paso alternativo 1
2. ...

## Flujos de excepción
**2a. [Condición de error]**
1. Sistema muestra error
2. Caso de uso termina
```

## Notas

- Esta guía se actualiza regularmente - revisa versión más reciente
- Para consultas, contacta al equipo de Copilot Full Capacity
- Contribuciones bienvenidas vía Pull Request

---

**Versión:** 1.0  
**Última actualización:** 2026-01-13  
**Aplica a:** Proyectos APX en BBVA