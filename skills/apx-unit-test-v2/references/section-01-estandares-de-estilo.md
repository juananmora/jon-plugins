# Instrucciones_apx_unittest

## Estándares de estilo

### Cómo actualizar una biblioteca a la nueva forma de pruebas unitarias

Este estándar describe el proceso para migrar pruebas unitarias que usan contexto de Spring a un enfoque ligero basado en mocks (Mockito) evitando cargar el contenedor de Spring. Sigue los pasos exactamente. No modifica el comportamiento funcional de la biblioteca; solo la estructura de los tests.

#### Ejemplo original con contexto Spring

```java
// Fragmento resumido de la clase original QWAIR001Test (con @RunWith y @ContextConfiguration)
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {
    "classpath:/META-INF/spring/QWAIR001-app.xml",
    "classpath:/META-INF/spring/QWAIR001-app-test.xml",
    "classpath:/META-INF/spring/QWAIR001-arc.xml",
    "classpath:/META-INF/spring/QWAIR001-arc-test.xml" })
public class QWAIR001Test {
    // ... uso de @Resource y contexto
}
```

#### Objetivo de la migración

Eliminar dependencias de Spring en tests unitarios para:

- Reducir tiempo de ejecución.
- Aislar dependencias mediante @Mock.
- Facilitar mantenimiento y claridad.

#### Comprobación inicial

1. Ejecutar pruebas actuales y asegurar que pasan:

```bash
mvn clean test
```

1. Ejecutar verificación APX CLI:

   ```bash
   apx check --test -y
   ```

2. Revisar advertencias: uso de contexto Spring, nomenclatura antigua, sugerencia de skeleton.

#### Generar skeleton de referencia (opcional)

```bash
apx check --test --repair
```

Si se solicita, aceptar mostrar la clase recomendada (skeleton) para comparar dependencias/mocks.

#### Cambios obligatorios en la clase de prueba

- Eliminar `@RunWith(SpringJUnit4ClassRunner.class)`.
- Eliminar `@ContextConfiguration(...)`.
- Sustituir cada `@Resource(name = "...")` por `@Mock` adecuado.
- Añadir `@InjectMocks` a la clase principal bajo prueba (ej: `QWAIR001Impl`).
- Eliminar métodos auxiliares para introspección (`getObjectIntrospection()`).
- Limpiar imports redundantes (Spring, Advised, etc.).

#### Estructura resultante (extracto simplificado)

```java
public class QWAIR001ImplTest {
 @Mock private ApplicationConfigurationService applicationConfigurationService;
 @Mock private JdbcUtils jdbcUtils;
 @Mock private APIConnector internalApiConnector;
 @Mock private InterBackendConnectionUtils interBackendConnectionUtils;
 @Mock private QWAIR002 qwaiR002;
 @InjectMocks private QWAIR001Impl qwaiR001;

 @Before
 public void setUp() {
  MockitoAnnotations.initMocks(this);
  ThreadContext.set(new Context());
  when(qwaiR002.executeDocumentGetCode("NIE")).thenReturn("1");
 }
}
```

#### Verificaciones tras refactor
