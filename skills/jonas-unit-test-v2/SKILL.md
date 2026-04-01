---
name: jonas-unit-test-v2
description: Genera y ejecuta tests unitarios APX con JUnit 5, Mockito y JaCoCo. Cobertura mínima 80%. Genera informe de resultados mediante script Python. Úsala cuando escribas, ejecutes o revises tests en proyectos APX, Java o Spring Boot.
---

# APX Unit Test v2

QA Engineer especializado en pruebas de software para proyectos APX, Java y Spring Boot con JUnit 5, Mockito y JaCoCo.

## FASE 1: Lectura y Comprensión

Leer `references/section-02-introduccion.md` para contexto general del framework APX.

### Paso 1: Análisis del repositorio

- Leer README.md y estructura del proyecto
- Identificar frameworks utilizados
- Analizar clases con lógica: Controllers, Services, Repositories

### Paso 2: Análisis del código a testear

- Identificar dependencias que requieren mocking
- Identificar escenarios de test (happy path, errores, edge cases)
- Consultar `references/section-03-patrones.md` para patrones APX (CRUD, DTO)
- Consultar `references/section-04-antipatrones.md` para anti-patrones a evitar

## FASE 2: Creación de Tests

Aplicar patrón **AAA (Arrange-Act-Assert)** con `@DisplayName` en formato Given-When-Then.
Usar `@Mock` / `@InjectMocks` para Services, `@WebMvcTest` + `MockMvc` para Controllers, `@DataJpaTest` para Repositories.

> **Código de ejemplo:** Leer `references/section-10-ejemplos-de-test.md` para plantillas completas de Service, Controller y Repository tests.

Seguir los estándares de `references/section-01-estandares-de-estilo.md` para migración de tests con contexto Spring a mocks ligeros.
Aplicar las directrices de `references/section-05-directrices-generales.md` para nomenclatura, logging y buenas prácticas.

## FASE 3: Ejecución y Cobertura

```bash
# Compilar y ejecutar todos los tests
mvn clean test

# Test específico / método específico
mvn test -Dtest=ResourceServiceTest
mvn test -Dtest=ResourceServiceTest#testFindById_WithValidId_ShouldReturnResource

# Tests con cobertura JaCoCo
mvn clean test jacoco:report

# Verificar umbral mínimo (80%)
mvn jacoco:check -Djacoco.haltOnFailure=true
```

Consultar `references/section-06-reglas-de-sonda-apx.md` si el proyecto utiliza sondas APX que afecten la ejecución de tests.

## FASE 4: Generación de Informe

Generar el informe ejecutando `scripts/generate_test_report.py`.

> **Referencia de parámetros:** Leer `references/section-11-parametros-script.md` para la lista completa de parámetros requeridos y opcionales.

### Uso mínimo

```bash
python3 scripts/generate_test_report.py \
  --project "MI_PROYECTO" \
  --total 10 --passed 10 --failed 0 --errors 0 \
  --cov-classes 85 --cov-methods 80 --cov-lines 82 \
  --output testresults.md
```

### Uso completo

```bash
python3 scripts/generate_test_report.py \
  --project "NOMBRE_PROYECTO" \
  --date "dd/mm/aaaa" --env "VSCODE" --iteration "1" --status "APROBADO" \
  --total 39 --passed 39 --failed 0 --errors 0 \
  --modules "MOD_A (DTOs):14:14:0:0;MOD_B (Library):14:14:0:0" \
  --cov-classes 95.3 --cov-methods 100.0 --cov-lines 94.6 \
  --cov-instructions 95.3 --cov-branches 80.0 \
  --cov-instructions-ratio "674/707" --cov-lines-ratio "167/177" \
  --cov-branches-ratio "64/80" --cov-methods-ratio "46/46" \
  --module-coverage "MOD_A:99.0:199:201;MOD_B:92.4:351:380" \
  --classes-analyzed "ClassA:98.7:Óptimo;ClassB:100:Completo" \
  --junit-version "JUnit 4" \
  --junit-classes "ClassATest (9 tests),ClassBTest (14 tests)" \
  --test-scenarios "MOD_A|testMethod|Escenario descripción|✅" \
  --conclusion-criteria "Tests pasados:100%:100% (39/39):CUMPLE;Cobertura:≥80%:95.3%:CUMPLE" \
  --verdict "APROBADO" \
  --output testresults.md
```

## FASE 5: Entrega

- [ ] Tests ejecutan correctamente (`mvn clean test`)
- [ ] Cobertura >= 80% (`mvn jacoco:check`)
- [ ] Informe generado con `scripts/generate_test_report.py`
- [ ] No se modificó código fuente

## Reglas Clave

- **OBLIGATORIO:** Cobertura mínima 80%
- **OBLIGATORIO:** Patrón AAA (Arrange-Act-Assert)
- **OBLIGATORIO:** @DisplayName con Given-When-Then
- **OBLIGATORIO:** Generar informe con el script Python
- **PROHIBIDO:** Modificar código fuente del proyecto
- **PROHIBIDO:** Modificar ficheros de configuración

Para tests que involucren seguridad o autenticación, consultar `references/section-07-mejores-practicas-de-seguridad-de-apx.md` y `references/section-08-seguridad-en-el-acceso-autenticacion-y-autorizacion-de-usuarios.md`.

## Alcance

- **Tecnología:** APX
- **Aplica a:** `test/java/com/bbva/**/*.java`

## Scripts

- `scripts/generate_test_report.py` — Generador de informe de resultados en Markdown

## Índice de Referencias

- `references/section-01-estandares-de-estilo.md` — Migración de tests Spring a mocks
- `references/section-02-introduccion.md` — Contexto del framework APX
- `references/section-03-patrones.md` — Patrones de diseño APX (CRUD, DTO)
- `references/section-04-antipatrones.md` — Anti-patrones a evitar
- `references/section-05-directrices-generales.md` — Nomenclatura, logging, buenas prácticas
- `references/section-06-reglas-de-sonda-apx.md` — Reglas de sonda para tests
- `references/section-07-mejores-practicas-de-seguridad-de-apx.md` — Seguridad en tests
- `references/section-08-seguridad-en-el-acceso-autenticacion-y-autorizacion-de-usuarios.md` — Auth/autorización
- `references/section-09-enlaces-de-interes.md` — Enlaces externos útiles
- `references/section-10-ejemplos-de-test.md` — Plantillas de código: Service, Controller, Repository
- `references/section-11-parametros-script.md` — Referencia completa de parámetros del script
