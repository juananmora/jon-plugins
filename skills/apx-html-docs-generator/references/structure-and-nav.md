# Estructura y navegación

## Categorías soportadas

- `functional`: `docs/functional` -> `html/functional`
- `api`: `docs/api` -> `html/api`
- `architecture`: `docs/architecture` -> `html/architecture`

## Reglas de procesamiento

- Convertir solo archivos `*.md` del primer nivel de cada categoría.
- Resolver automáticamente la raíz del proyecto buscando `docs/` y `html/`.
- Aplicar limpieza Mermaid solo dentro de bloques ` ```mermaid `.
- Conservar el resto del Markdown sin limpieza específica de caracteres.
- Inyectar en cada `README.html` de categoría una sección de enlaces automáticos a todas las páginas HTML generadas de esa categoría (excepto el propio README), para evitar páginas huérfanas.

## Menú de navegación actual

- `index.html`
- `functional/README.html`
- `functional/requirements.html`
- `functional/user-stories.html`
- `functional/use-cases.html`
- `architecture/README.html`
- `architecture/data-model.html`
- `architecture/decisions.html`
- `api/README.html`
- `api/endpoints.html`

## Mantenimiento

- Actualizar este archivo si cambia el mapa de categorías o los ítems de navegación.
- Mantener el contenido sincronizado con las constantes `CATEGORIES` y `NAV_ITEMS` del script.
