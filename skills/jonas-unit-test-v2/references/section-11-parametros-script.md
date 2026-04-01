# Parámetros del Script de Informe

Referencia completa de parámetros para `scripts/generate_test_report.py`.

## Requeridos

| Parámetro | Descripción |
|-----------|-------------|
| `--project` | Nombre del proyecto |
| `--total` | Total de tests ejecutados |
| `--passed` | Tests exitosos |
| `--failed` | Tests fallidos |
| `--errors` | Tests con errores |
| `--cov-classes` | Cobertura por clases (%) |
| `--cov-methods` | Cobertura por métodos (%) |
| `--cov-lines` | Cobertura por líneas (%) |
| `--output` | Ruta del archivo de salida (.md) |

## Opcionales - Metadatos

| Parámetro | Descripción |
|-----------|-------------|
| `--date` | Fecha de ejecución (default: hoy) |
| `--env` | Entorno (default: VSCODE) |
| `--iteration` | Número de iteración (default: 1) |
| `--status` | Estado del análisis (default: COMPLETADO) |

## Opcionales - Desglose por módulo

| Parámetro | Descripción |
|-----------|-------------|
| `--modules` | Tabla de módulos `Módulo:tests:passed:failed:errors;...` |

## Opcionales - Cobertura detallada

| Parámetro | Descripción |
|-----------|-------------|
| `--cov-instructions` | Cobertura por instrucciones (%) |
| `--cov-branches` | Cobertura por ramas (%) |
| `--cov-instructions-ratio` | Ratio instrucciones `cubierto/total` |
| `--cov-lines-ratio` | Ratio líneas `cubierto/total` |
| `--cov-branches-ratio` | Ratio ramas `cubierto/total` |
| `--cov-methods-ratio` | Ratio métodos `cubierto/total` |
| `--module-coverage` | Cobertura por módulo `Módulo:pct:covered:total;...` |
| `--classes-analyzed` | Clases analizadas `Clase:pct:estado;...` |
| `--low-coverage` | Clases con baja cobertura `Clase:pct,Clase:pct` |
| `--full-coverage` | Clases con cobertura completa `Clase1,Clase2` |

## Opcionales - JUnit

| Parámetro | Descripción |
|-----------|-------------|
| `--junit-total` | Total tests JUnit (default: --total) |
| `--junit-version` | Etiqueta versión JUnit (default: JUnit) |
| `--junit-classes` | Clases de test `Clase (N tests),Clase2 (M tests)` |
| `--junit-cases` | Casos validados `caso1,caso2` |

## Opcionales - Mockito

| Parámetro | Descripción |
|-----------|-------------|
| `--mock-total` | Total de mocks utilizados |
| `--mock-components` | Componentes mockeados (simple) `Comp1,Comp2` |
| `--mock-descriptions` | Componentes con descripción `Comp:desc;Comp2:desc2` |
| `--mock-behaviors` | Comportamientos verificados `beh1,beh2` |

## Opcionales - Escenarios de test

| Parámetro | Descripción |
|-----------|-------------|
| `--test-scenarios` | Escenarios detallados `Sección\|método\|escenario\|resultado;...` |

## Opcionales - HTTP y otros

| Parámetro | Descripción |
|-----------|-------------|
| `--http-endpoints` | Endpoints HTTP `VERB /path:status:validaciones;...` |
| `--http-tool` | Herramienta HTTP (default: MockMvc) |
| `--incidents` | Incidencias `desc:clase:metodo:solucion;...` |

## Opcionales - Conclusión

| Parámetro | Descripción |
|-----------|-------------|
| `--conclusion-coverage` | Cobertura para conclusión (default: --cov-lines) |
| `--conclusion-criteria` | Tabla de criterios `Criterio:Objetivo:Resultado:Estado;...` |
| `--verdict` | Veredicto final: APROBADO / NO APROBADO (default: auto) |

## Opcionales - Archivos y comandos

| Parámetro | Descripción |
|-----------|-------------|
| `--test-files` | Rutas de archivos de test `path1,path2,...` |
| `--exec-commands` | Comandos de ejecución `cmd1;cmd2;...` |
