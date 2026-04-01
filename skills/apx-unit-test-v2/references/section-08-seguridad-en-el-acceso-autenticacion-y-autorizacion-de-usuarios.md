## Seguridad en el Acceso: Autenticación y Autorización de Usuarios

Como desarrollador de APX necesitarás comprender el flujo de autenticación y autorización para conseguir una integración segura y efectiva con los servicios multicanal ASO.

Cuando se ejecutan servicios ASO primero se produce la autenticación, donde se verifica la identidad del usuario para asegurar que la persona que intenta acceder al sistema es quien dice ser. Después, se produce la autorización para determinar a qué recursos, funciones y datos puede acceder el usuario.

Pongamos un ejemplo: primero se produce la autenticación cuando al entrar a un edificio enseñamos nuestro DNI al guardia de seguridad y después, el guardia nos otorga una tarjeta para acceder solo a las áreas del edificio para las cuales tenemos permiso.

### Autenticación y autorización

La autenticación permite verificar la identidad del usuario, mientras que, la autorización revisa si ese usuario ya autenticado, tiene permiso para realizar una acción específica o acceder a un recurso determinado. Son procesos fundamentales para garantizar la seguridad y la confianza cuando lanzamos una petición:

- Protege los datos y recursos del servicio de accesos no autorizados.
- Asegura que solo los usuarios legítimos puedan realizar acciones sensibles, como transacciones financieras.
- Ayuda a prevenir fraudes y actividades maliciosas.

En nuestros desarrollos debemos tener la integridad de nuestro código para que solo el código autorizado y validado se ejecuta para ellos dos puntos claves:

- **Uso Estricto de Scripts .sh para Utilidades de BBDD**: "Los archivos .sh que se liberan en la plataforma Batch son exclusivamente para lanzar las utilidades de BBDD. NO pueden incluir código script diferente al necesario para lanzar la utilidad DE. Los procesos batch deben implementarse con el APX Batch Runtime y NO en shell script, para evitar la ejecución de código arbitrario y mantener la lógica de negocio controlada por la arquitectura APX."
- **No Código Funcional en la Interfaz de Librería**: "No debe incluirse ningún código funcional en la interfaz de la Librería. El código funcional debe ir siempre en la implementación de la Librería, manteniendo una clara separación de responsabilidades y facilitando la revisión de seguridad."

### Flujo del proceso de acceso

Cuando un cliente interactúa con los frontales se inicia un diálogo con la plataforma de servicios:

1. El cliente introduce sus credenciales en el frontal y se realiza una petición de autenticación.
2. GrantingTickets realiza la validación de:
   - Credenciales del usuario
   - AAP (Access Point - consumerId, por ejemplo Banca Móvil Android)
   - Tipo de proceso de autenticación
3. Obtención del TSEC e inicialización del contexto para próximas peticiones
4. Usar el TSEC para consumir varios SMCs (Servicios Multicanal). Enviado como cabecera
5. La arquitectura de servicios intercepta la solicitud para realizar el control de autorización:
   - Aceptar la solicitud -> El servicio continúa con su ejecución
   - Rechazar la solicitud -> La ejecución del servicio se detiene y el control de autorización devuelve al canal un error HTTP

    En una primera etapa, la Arquitectura de Seguridad ASO se encarga de determinar si la petición supera el control de fraude y el control de canal, lo que significa que el cliente puede operar sobre los contratos, porque efectivamente son suyos y no hay restricciones aplicadas.
    El siguiente diagrama muestra la segunda etapa, representando cómo actúa el proceso de la arquitectura de Seguridad en la capa APX, tras haber superado la interacción con el servicio. En esta capa ya no hay información del TSEC, si no del usuario transaccional que se necesita validar.

    ... (contenido restante del bloque proporcionado por el usuario se mantiene íntegro) ...

```bash
mvn clean test
```

La salida debe mantener (o mejorar) el número de pruebas pasadas. No se aceptan regresiones funcionales.

#### Renombrado de clase y paquete

1. Crear paquete `impl` si aplica.
2. Renombrar `QWAIR001Test` → `QWAIR001ImplTest`.
3. Mover la clase al paquete final `com.bbva.qwai.lib.r001.impl`.
4. Reejecutar:

```bash
mvn clean install
```

#### Eliminación de artefactos antiguos

Repetir verificación:

```bash
apx check --test
```

Si lista archivos obsoletos (factories, mocks Spring, XML de contexto), eliminarlos manualmente o vía:

```bash
apx check --test --repair
```

#### Limpieza de dependencias en `pom.xml`

Cuando la verificación sugiera remover dependencias (spring-context, spring-test, elara-test, etc.), aceptar y confirmar que el POM se actualizó. Revisar que las pruebas siguen pasando tras la limpieza.

#### Validación final

La verificación debe mostrar:

- Clase de test con nomenclatura actual: Found.
- Uso de Spring Context: NO.
- Archivos antiguos: eliminados.
- Dependencias sobrantes: removidas.

#### Criterio de aceptación del estándar

- Tiempo de ejecución de las pruebas reducido (indicador cualitativo aceptado si no hay métrica previa).
- 0 dependencias de contexto Spring en scope test (excepto si algún módulo lo requiere explícitamente para integración — documentar excepción).
- Consistencia de resultados frente a la versión previa.

#### Notas

- Si alguna funcionalidad depende de proxies de Spring, evaluar mover esa validación a pruebas de integración separadas.
- Mantener los mocks simples; evitar sobre-mockear lógica interna.

(Indica si este es el último estándar o continuamos añadiendo más.)

### Cómo desarrollar un test JUnit para transacciones en APX

En la forma "tradicional" de hacer las pruebas se utiliza el contexto de Spring, que incluye múltiples mocks de arquitectura. Esto provoca:

- Fragilidad (si cambia la interfaz de módulos simulados fallan todas las pruebas)
- Exceso de burla (mocking) que impide pruebas realmente unitarias
- Lentitud (~3 segundos por prueba al inicializar el contexto)

Con las transacciones, los datos se reciben en la superclase (`AbstractTransaction`), lo que complica el mocking completo. Se propone una transacción de prueba controlada donde se reemplazan los puntos de extensión mediante estructuras internas simples (Map para parámetros y librerías) y se inyectan mocks con Mockito.

#### Clase de transacción concreta

```java
package com.bbva.qwai;

import com.bbva.elara.domain.transaction.RequestHeaderParamsName;
import com.bbva.qwai.lib.r001.QWAIR001;
import com.bbva.elara.domain.transaction.Severity;
import com.bbva.qwai.dto.customers.CustomerDTO;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;

public class QWAIT00101ESTransaction extends AbstractQWAIT00101ESTransaction {

    private static final Logger LOGGER = LoggerFactory.getLogger(QWAIT00101ESTransaction.class);

    @Override
    public void execute() {
        QWAIR001 qwaiR001 = this.getServiceLibrary(QWAIR001.class);
        LOGGER.info("Execution of QWAIT00101ESTransaction");
        CustomerDTO customerIn = getCustomerin();
        CustomerDTO customerOut;
        String option = getOption();
        List<CustomerDTO> listCustomerOut = null;
        switch (option) {
            case "insert":
                customerOut = qwaiR001.executeInsert(customerIn, getUserCode(), getBranchCode());
                setCustomerOut(customerOut);
                break;
            case "update":
                customerOut = qwaiR001.executeUpdate(customerIn, getUserCode(), getBranchCode());
                setCustomerOut(customerOut);
                break;
            case "delete":
                qwaiR001.executeDelete(customerIn.getCustomerId());
                setCustomerOut(customerIn);
                break;
            case "selectById":
                listCustomerOut = qwaiR001.executeFindById(customerIn.getCustomerId());
                setCustomerOutList(listCustomerOut);
                break;
            case "selectByDocument":
                String documentType = customerIn.getDocumentType();
                String documentNumber = customerIn.getDocumentNumber();
                listCustomerOut = qwaiR001.executeFindByDocument(documentType, documentNumber);
                setCustomerOutList(listCustomerOut);
                break;
            case "selectAll":
                listCustomerOut = qwaiR001.executeFindAll();
                setCustomerOutList(listCustomerOut);
                break;
            default:
                LOGGER.warn("Error: option not entered");
                setSeverity(Severity.EWR);
                break;
        }
    }

    private void setCustomerOut(CustomerDTO customerOut) {
        if (this.getAdvice() != null) {
            LOGGER.warn("Error performing the operation");
            setSeverity(Severity.EWR);
        } else {
            LOGGER.debug("Successful operation");
            List<CustomerDTO> listDTO = new ArrayList<>();
            listDTO.add(customerOut);
            this.setCustomerlist(listDTO);
        }
    }

    private void setCustomerOutList(List<CustomerDTO> listCustomerOut) {
        if (this.getAdvice() != null) {
            if(this.getAdvice().getCode().equals("QWAI00841000")){
                LOGGER.warn("Customer not found");
                setSeverity(Severity.WARN);
            } else {
                LOGGER.error("Error when searching for clients");
                setSeverity(Severity.EWR);
            }
        } else {
            LOGGER.debug("Search completed successfully");
            this.setCustomerlist(listCustomerOut);
        }
    }

    private String getUserCode() {
        return (String) this.getRequestHeader().getHeaderParameter(RequestHeaderParamsName.USERCODE);
    }

    private String getBranchCode() {
        return (String) this.getRequestHeader().getHeaderParameter(RequestHeaderParamsName.BRANCHCODE);
    }
}
```

#### Resumen de la clase abstracta

```java
package com.bbva.qwai;

import com.bbva.elara.transaction.AbstractTransaction;
import com.bbva.qwai.dto.customers.CustomerDTO;
import java.util.List;

public abstract class AbstractQWAIT00101ESTransaction extends AbstractTransaction {

    public AbstractQWAIT00101ESTransaction(){ }

    protected String getOption(){
        return (String)this.getParameter("option");
    }

    protected CustomerDTO getCustomerin(){
        return (CustomerDTO)this.getParameter("customerIn");
    }

    protected void setCustomerlist(final List<CustomerDTO> field){
        this.addParameter("customerList", field);
    }
}
```

#### Clase de test (estructura final)

Se construye una instancia anónima de la transacción sobrescribiendo métodos para redirigir parámetros y librerías a Maps internos.

```java
public class QWAIT00101ESTransactionTest {

    private Map<String, Object> parameters;
    private Map<Class<?>, Object> serviceLibraries;

    @Mock private ApplicationConfigurationService applicationConfigurationService;
    @Mock private CommonRequestHeader commonRequestHeader;
    @Mock private QWAIR001 qwaiR001;

    private final QWAIT00101ESTransaction transaction = new QWAIT00101ESTransaction() {
        @Override protected void addParameter(String field, Object obj) { if (parameters != null) parameters.put(field, obj); }
        @Override protected Object getParameter(String field) { return parameters.get(field); }
        @Override protected <T> T getServiceLibrary(Class<T> serviceInterface) { return (T) serviceLibraries.get(serviceInterface); }
        @Override public String getProperty(String keyProperty) { return applicationConfigurationService.getProperty(keyProperty); }
        @Override protected CommonRequestHeader getRequestHeader() { return commonRequestHeader; }
    };

    private void setServiceLibrary(Class<?> clasz, Object mockObject) { serviceLibraries.put(clasz, mockObject); }
    private void setParameterToTransaction(String parameter, Object value) { parameters.put(parameter, value); }
    private Object getParameterFromTransaction(String parameter) { return parameters.get(parameter); }

    @Before
    public void setUp() throws Exception {
        MockitoAnnotations.initMocks(this);
        initializeTransaction();
        setServiceLibrary(QWAIR001.class, qwaiR001);
    }

    private void initializeTransaction() {
        this.transaction.setContext(new Context());
        parameters = new HashMap<>();
        serviceLibraries = new HashMap<>();
    }
}
```

#### Ejemplos de métodos de prueba

Inserción correcta:

```java
@Test
public void executeInsertTest() {
    CustomerDTO customerIn = new CustomerDTO();
    setParameterToTransaction("customerIn", customerIn);
    setParameterToTransaction("option", "insert");
    when(commonRequestHeader.getHeaderParameter(RequestHeaderParamsName.USERCODE)).thenReturn("userCode");
    when(commonRequestHeader.getHeaderParameter(RequestHeaderParamsName.BRANCHCODE)).thenReturn("0182");
    when(qwaiR001.executeInsert(customerIn, "userCode", "0182")).thenReturn(customerIn);
    transaction.execute();
    verify(qwaiR001, times(1)).executeInsert(customerIn, "userCode", "0182");
    Assert.assertEquals(0, transaction.getAdviceList().size());
}
```

Inserción con error:

```java
@Test
public void executeInsertErrorTest() {
    CustomerDTO customerIn = new CustomerDTO();
    setParameterToTransaction("customerIn", customerIn);
    setParameterToTransaction("option", "insert");
    when(commonRequestHeader.getHeaderParameter(RequestHeaderParamsName.USERCODE)).thenReturn("userCode");
    when(commonRequestHeader.getHeaderParameter(RequestHeaderParamsName.BRANCHCODE)).thenReturn("0182");
    when(qwaiR001.executeInsert(customerIn, "userCode", "0182")).thenAnswer(answerCustomerDTO());
    transaction.execute();
    verify(qwaiR001, times(1)).executeInsert(customerIn, "userCode", "0182");
    Assert.assertEquals(1, transaction.getAdviceList().size());
}
```

Listado completo (selectAll) correcto y con error (mostrar sólo uno en detalle aquí; el otro se mantiene en el código final del ejemplo original):

```java
@Test
public void executeSelectAllTest() {
    setParameterToTransaction("option", "selectAll");
    List<CustomerDTO> listCustomerDTO = customerDtoList();
    when(qwaiR001.executeFindAll()).thenReturn(listCustomerDTO);
    this.transaction.execute();
    verify(qwaiR001, times(1)).executeFindAll();
    List<CustomerDTO> resultCustomerDTO = (List<CustomerDTO>) getParameterFromTransaction("customerList");
    Assert.assertEquals(listCustomerDTO.size(), resultCustomerDTO.size());
    Assert.assertEquals(0, transaction.getAdviceList().size());
}
```

#### Criterios de aceptación específicos (Transacciones)

- Control total de parámetros vía Maps internos.
- Sin carga de contexto Spring.
- Verificación de cada rama del switch `option` mediante pruebas dedicadas.
- Advice list validada (0 en éxito, >=1 en error).

---

### Cómo desarrollar un test JUnit para bibliotecas en APX

Cuando se crea una biblioteca en APX se genera un paquete de prueba (`src/test/java/.../impl/`) con una clase `<UUAA>R001ImplTest`. Tradicionalmente se usaba Spring context con múltiples XML y factories compartidas que centralizan los mocks (por ejemplo JDBC factory). Esto ocasiona acoplamiento y pérdida de control fino en cada test.

Se reemplaza el enfoque por Mockito puro aprovechando:

- `@InjectMocks` para la clase concreta (`QWAIR001Impl`).
- `@Mock` para cada dependencia (`JdbcUtils`, `APIConnector`, `InterBackendConnectionUtils`, `QWAIR002`, etc.).
- Evitar cargar contextos globales, usando sólo inicialización liviana (`MockitoAnnotations.initMocks`).

#### Clase bajo prueba (fragmento)

```java
public class QWAIR001Impl extends QWAIR001Abstract {
    // ... métodos executeInsert, executeUpdate, executeDelete, executeFindById, executeFindByDocument, executeFindAll
}
```

#### Clase abstracta generada automáticamente (fragmento)

```java
public abstract class QWAIR001Abstract extends AbstractLibrary implements QWAIR001 {
    protected ApplicationConfigurationService applicationConfigurationService;
    protected JdbcUtils jdbcUtils;
    protected APIConnector internalApiConnector;
    protected APIConnectorBuilder apiConnectorBuilder;
    protected InterBackendConnectionUtils interBackendConnectionUtils;
    protected QWAIR002 qwaiR002;
    // setters...
}
```

#### Clase de test (estructura simplificada)

```java
public class QWAIR001ImplTest {
    public static final String USER_CODE = "userCode";
    public static final String BRANCH_CODE = "0182";
    public static final String CUSTOMER_ID_NEW = "1";
    public static final String DOCUMENT_TYPE_NIE = "NIE";
    public static final String DOCUMENT_NUMBER_CUSTOMER = "12341234N";
    public static final String DOCUMENT_TYPE_NIE_CODE = "1";
    public static final String QUERY_CODE_SELECT_CUSTOMER_ID_MAX = "customer.select.id.max";
    public static final String QUERY_CODE_CUSTOMER_INSERT = "customer.insert";

    @Captor private ArgumentCaptor<Map<String, Object>> mapCaptor;
    @Mock private ApplicationConfigurationService applicationConfigurationService;
    @Mock private JdbcUtils jdbcUtils;
    @Mock private APIConnector internalApiConnector;
    @Mock private InterBackendConnectionUtils interBackendConnectionUtils;
    @Mock private QWAIR002 qwaiR002;
    @InjectMocks private QWAIR001Impl qwaiR001;

    @Before
    public void setUp() throws Exception {
        MockitoAnnotations.initMocks(this);
        ThreadContext.set(new Context());
        when(qwaiR002.executeDocumentGetCode(DOCUMENT_TYPE_NIE)).thenReturn(DOCUMENT_TYPE_NIE_CODE);
    }
}
```

#### Ejemplos de pruebas

Inserción correcta:

```java
@Test public void executeInsertTest() {
    Date date = new Date();
    CustomerDTO customerDTO = createCustomerDTO(date);
    when(jdbcUtils.queryForString(QUERY_CODE_SELECT_CUSTOMER_ID_MAX)).thenReturn(CUSTOMER_ID_NEW);
    when(jdbcUtils.queryForMap("customer.select.by.document", getMapParamsJdbc(DOCUMENT_TYPE_NIE_CODE, DOCUMENT_NUMBER_CUSTOMER))).thenThrow(NoResultException.class);
    qwaiR001.executeInsert(customerDTO, USER_CODE, BRANCH_CODE);
    verify(jdbcUtils, times(1)).queryForString(QUERY_CODE_SELECT_CUSTOMER_ID_MAX);
    verify(jdbcUtils, times(1)).update(eq(QUERY_CODE_CUSTOMER_INSERT), mapCaptor.capture());
    Map<String, Object> customerMapCaptorValue = mapCaptor.getValue();
    Assert.assertEquals("userCode", customerMapCaptorValue.get("audUser"));
    Assert.assertEquals(0, qwaiR001.getAdviceList().size());
}
```

Inserción duplicada:

```java
@Test public void executeInsertErrorDuplicateTest() {
    Date date = new Date();
    CustomerDTO customerDTO = createCustomerDTO(date);
    when(jdbcUtils.queryForString(QUERY_CODE_SELECT_CUSTOMER_ID_MAX)).thenReturn(CUSTOMER_ID_NEW);
    when(jdbcUtils.queryForMap("customer.select.by.document", getMapParamsJdbc(DOCUMENT_TYPE_NIE_CODE, DOCUMENT_NUMBER_CUSTOMER))).thenThrow(NoResultException.class);
    when(jdbcUtils.update(eq(QUERY_CODE_CUSTOMER_INSERT), anyMap())).thenThrow(DuplicateKeyException.class);
    qwaiR001.executeInsert(customerDTO, USER_CODE, BRANCH_CODE);
    verify(jdbcUtils, times(1)).queryForString(QUERY_CODE_SELECT_CUSTOMER_ID_MAX);
    Assert.assertEquals(1, qwaiR001.getAdviceList().size());
}
```

Encontrar por documento (modo JDBC):

```java
@Test public void executeFindByDocumentJDBCTest(){
    Map<String, Object> mapParams = getMapParamsJdbc(DOCUMENT_TYPE_NIE_CODE, DOCUMENT_NUMBER_CUSTOMER);
    when(applicationConfigurationService.getDefaultProperty("type.find", "hardcode")).thenReturn("jdbc");
    CustomerDTO customerDTO = createCustomerDTO(new Date());
    Map<String, Object> customerMap = getCustomerMapJdbc(customerDTO, CUSTOMER_ID_NEW, DOCUMENT_TYPE_NIE_CODE);
    when(jdbcUtils.queryForMap("customer.select.by.document", mapParams)).thenReturn(customerMap);
    List<CustomerDTO> listCustomer = qwaiR001.executeFindByDocument(DOCUMENT_TYPE_NIE, DOCUMENT_NUMBER_CUSTOMER);
    Assert.assertEquals(1, listCustomer.size());
    Assert.assertEquals(CUSTOMER_ID_NEW, listCustomer.get(0).getCustomerId());
}
```

API Connector:

```java
@Test public void executeFindByDocumentIntApiConnectorTest(){
    when(applicationConfigurationService.getDefaultProperty("type.find", "hardcode")).thenReturn("intapiconnector");
    ResponseEntity responseEntity = mock(ResponseEntity.class);
    CustomerDTO customerDTO = createCustomerDtoWithId();
    when(responseEntity.getBody()).thenReturn(customerDTO);
    when(internalApiConnector.getForEntity("customer", CustomerDTO.class, getMapParamsApi(DOCUMENT_TYPE_NIE, DOCUMENT_NUMBER_CUSTOMER))).thenReturn(responseEntity);
    List<CustomerDTO> listCustomer = qwaiR001.executeFindByDocument(DOCUMENT_TYPE_NIE, DOCUMENT_NUMBER_CUSTOMER);
    Assert.assertEquals(1, listCustomer.size());
}
```

Interbackend:

```java
@Test public void executeFindByDocumentImsBackendTest(){
    when(applicationConfigurationService.getDefaultProperty("type.find", "hardcode")).thenReturn("intback");
    when(interBackendConnectionUtils.invoke("UUAAT001010101", getMapParamsApi(DOCUMENT_TYPE_NIE, DOCUMENT_NUMBER_CUSTOMER))).thenReturn(getCustomerDtoMap());
    List<CustomerDTO> listCustomer = qwaiR001.executeFindByDocument(DOCUMENT_TYPE_NIE, DOCUMENT_NUMBER_CUSTOMER);
    Assert.assertEquals(1, listCustomer.size());
}
```

Parámetros vacíos:

```java
@Test public void executeFindByDocumentParamsEmptyTest(){
    List<CustomerDTO> listCustomer = qwaiR001.executeFindByDocument("", "");
    Assert.assertEquals(0, listCustomer.size());
    Assert.assertEquals(1, qwaiR001.getAdviceList().size());
}
```

#### Criterios de aceptación específicos (Bibliotecas)

- Cada dependencia externa mockeada individualmente.
- Cobertura de caminos: inserción OK, inserción duplicada, búsqueda por documento (jdbc, api, intback, parámetros vacíos), validaciones de advice.
- Sin carga de contexto Spring.
- Uso consistente de constantes para códigos y parámetros.

#### Notas finales

Anotaciones clave de Mockito:

```text
@InjectMocks  -> Crea instancia real e inyecta mocks.
@Mock         -> Crea mocks de dependencias.
@Spy          -> Instancia real parcialmente mockeable (no usada en los ejemplos anteriores).
```

---

(Indica si añadiremos más estándares o pasamos a la sección Reglas.)

### Cambio estructural de pruebas unitarias (APX CLI ≥ 1.15)

Desde la versión 1.15 de APX CLI se modificó la generación y estructura de pruebas unitarias para bibliotecas y transacciones con los objetivos de:

- Eliminar uso de Spring Context y XML de configuración de prueba.
- Reducir el acoplamiento con clases de arquitectura (evolución continua).
- Disminuir tiempos de compilación y ejecución (no descarga dependencias Spring ni inicializa contexto).
- Aumentar intensidad de uso de Mockito (mocking explícito y localizado).

| Característica               | Estructura actual   | Estructura anterior   |
| ---------------------------- | ------------------- | --------------------- |
| Uso de Spring context        | No                  | Sí                    |
| Acoplamiento arquitectura    | Bajo                | Alto                  |
| Dependencia spring-framework | No                  | Sí                    |
| Dependencia elara-test       | No                  | Sí                    |
| Uso Mockito                  | Alto                | Medio                 |
| XML beans test               | No                  | Sí                    |

#### Cambios en bibliotecas

Ejemplo (comparativo simplificado):

```text
Current structure                       Previous structure
=========================================================  ==================================================
src/main/java                            src/main/java
- ...UUAAR000Abstract                    - ...UUAAR000Abstract
- ...UUAAR000Impl                        - ...UUAAR000Impl
src/main/resources                       src/main/resources
- META-INF/spring/UUAAR000-app.xml       - META-INF/spring/UUAAR000-app.xml
- META-INF/spring/UUAAR000-app-osgi.xml  - META-INF/spring/UUAAR000-app-osgi.xml
- META-INF/spring/UUAAR000-arc.xml       - META-INF/spring/UUAAR000-arc.xml
- META-INF/spring/UUAAR000-arc-osgi.xml  - META-INF/spring/UUAAR000-arc-osgi.xml
- multilanguage-ES.properties            - multilanguage-ES.properties
src/test/java                            src/test/java
- ...impl.UUAAR000ImplTest               - ...UUAAR000Test
                                         - ...mock.ConfigurationFactoryMock
                                         - ...mock.LibraryMonitorizationAspectMock
                                         - ...mock.MockBundleContext
src/test/resources                       src/test/resources
- log4j.xml                              - log4j.xml
                                         - META-INF/spring/UUAAR000-app-test.xml
                                         - META-INF/spring/UUAAR000-arc-test.xml
                                         - properties-uuaa.properties
```

Claves:

- El test ahora reside en el mismo paquete `impl` → nombre estándar: `UUAAR000ImplTest`.
- Eliminadas clases mock de infraestructura y XML de test.
- No se generan factories globales; se mockean dependencias directas con Mockito.

#### Cambios en transacciones

```text
Current structure                       Previous structure
=========================================================  ==================================================
src/main/java                            src/main/java
- AbstractTESTT50001ESTransaction        - AbstractTESTT50001ESTransaction
- TESTT50001ESTransaction                - TESTT50001ESTransaction
src/main/resources                       src/main/resources
- multilanguage-ES.properties            - multilanguage-ES.properties
- TESTT500-01-ES.xml                     - TESTT500-01-ES.xml
src/test/java                            src/test/java
- TESTT50001ESTransactionTest            - TESTT50001ESTransactionTest
src/test/resources                       src/test/resources
                                          - META-INF/spring/TESTT50001ESTest.xml
                                          - common-env.properties
- log4j.xml                               - log4j.xml
                                          - TEST.properties
```

Claves:

- Mismo nombre de clase de test (ya seguía la convención).
- Eliminados XML de test y properties auxiliares.
- Menos dependencias test en `pom.xml` (Spring y elara-test retiradas).

#### Archivos/clases que dejan de generarse

Bibliotecas:

- `ConfigurationFactoryMock`, `LibraryMonitorizationAspectMock`, `MockBundleContext`.
- XML: `*-app-test.xml`, `*-arc-test.xml`, `properties-uuaa.properties`.

Transacciones:

- XML: `*Test.xml`, `common-env.properties`, `TEST.properties`.

#### Estándar de nombres

- Clase bajo prueba: mismo paquete.
- Test: `<NombreClase>Test` (biblioteca impl: `UUAAR000ImplTest`).
- No usar sufijos alternativos (`Prueba`, etc.).

#### Beneficios cuantitativos (qualitativos si no hay métrica previa)

- Menor tiempo de arranque de cada test (sin contexto → milisegundos vs segundos).
- Menos fallos masivos ante cambios en arquitectura.
- Mocking explícito focalizado.

#### Criterios de aceptación (Cambio estructural)

- Ningún test unitario carga Spring Context.
- Eliminadas dependencias `spring-test`, `spring-beans`, `elara-test` del `pom.xml` (salvo justificación documentada en Notas).
- Clases de test colocadas en el mismo paquete que la clase que prueban.
- Limpieza de archivos heredados confirmada por `apx check --test` (sin advertencias de archivos obsoletos).

### Proceso para actualizar una transacción a la nueva estructura de pruebas

Este estándar guía la migración de una clase de prueba de transacción que aún usa Spring Context hacia el modelo ligero basado en Mockito.

#### Paso 0: Verificar necesidad de migración

Ejecutar:

```bash
apx check --test -y
```

Si el reporte indica: `Does the unit testing class use Spring Context?: YES` → proceder con migración.

#### Paso 1: Asegurar línea base

```bash
mvn clean test
```

Confirmar que todas las pruebas actuales pasan (sirve como referencia).

#### Paso 2: Obtener skeleton sugerido

```bash
apx check --test --repair
```

Elegir ver el contenido del skeleton para compararlo con la clase existente.

#### Paso 3: Refactor clave en la clase de prueba

Eliminar:

- `@RunWith(SpringJUnit4ClassRunner.class)`
- `@ContextConfiguration(...)`
- `@Resource(name = "...")`
- `@Autowired`
- `DummyBundleContext` y usos asociados
- Método `getObjectIntrospection()` (si existe)

Añadir/invertir:

- Sustituir cada `@Resource` por `@Mock`.
- Incluir `@InjectMocks` (si la transacción no se instancia anónimamente) o mantener instancia anónima con overrides de parámetros/libs.
- Inicializar mocks en `@Before` con `MockitoAnnotations.initMocks(this);`.
- Maps internos para parámetros y librerías si se usa instancia anónima.

#### Paso 4: Validar refactor incremental

```bash
mvn clean test
```

Resultados deben mantenerse o mejorar (mismas pruebas pasan, menos tiempo).

#### Paso 5: Eliminar artefactos obsoletos

Reejecutar:

```bash
apx check --test
```

Si lista XML/propiedades antiguos, eliminarlos manualmente o:

```bash
apx check --test --repair
```

#### Paso 6: Limpieza de dependencias

Revisión interactiva:

```bash
apx check --test --repair
```

Cuando solicite borrar dependencias `elara-test`, `spring-test`, `spring-beans` (scope test), aceptar.

#### Paso 7: Confirmación final

Reejecutar verificación (esperado):

```text
Does the unit testing class use Spring Context?: NO
```

Sin archivos previos listados para eliminación y sin dependencias sobrantes.

#### Ejemplo de fragmento post-migración (simplificado)

```java
@Before
public void setUp() throws Exception {
    MockitoAnnotations.initMocks(this);
    initializeTransaction();
    setServiceLibrary(QWAIR001.class, qwaiR001);
}
```

#### Criterios de aceptación (Actualización transacción)

- Informe `apx check --test` sin advertencias de Spring Context.
- Dependencias de Spring de prueba eliminadas del `pom.xml`.
- Pruebas existentes siguen pasando (o mejoran cobertura / tiempo).
- Código de prueba sin anotaciones Spring (@RunWith, @ContextConfiguration, @Autowired, @Resource).

#### Notas de rollback

Si algo falla, utilizar git para revertir (`git checkout -- <ruta/clase>` o revert commit) antes de seguir iterando.

#### Métricas sugeridas (optativo)

- Tiempo antes vs después (ejecución surefire). Si no se capturó antes, documentar mejora cualitativa.

### Componente LOCAL-TEST para pruebas locales

El componente `local-test` permite probar en entorno local bibliotecas de terceros y transacciones de prueba que no se desplegarán en producción.

#### Características

- Se crea dentro de la Unidad de Implementación de la biblioteca o unidad online.
- No se añade como módulo al proyecto principal (compilación separada).
- Los cambios persisten en el repositorio del proyecto.
- Contiene dos submódulos: `mock-libraries` y `transactions`.

#### Estructura base

```text
local-test/
├── pom.xml
├── mock-libraries/
│   └── pom.xml
└── transactions/
    └── pom.xml
```

#### Bibliotecas simuladas

Simulan comportamiento esperado de dependencias usadas por componentes APX. Se generan como dependencias declaradas en POM.

Comandos para crear mock libraries:

```bash
apx add mock-lib --scan -y
apx add mock-lib -a="TESTR001" -v="0.0.0" -y
```

#### Transacciones de prueba

Permiten probar bibliotecas sin transacciones propias.

```bash
apx add mock-trx -y --code=MOC --trx-country=ES --trx-version=01 --description=Test --project-path=./TESTR001-parent
```

#### Despliegue incluyendo local-test

```bash
apx deploy local -y --runtime=online --country=ESP --local-test
```

#### Flujo de ejemplo (resumen)

1. `apx init du-lib ...`
2. Añadir dependencia real: `apx add dep -a="QWYPRX80" -v="1.0.4" -y --project-path=.../TESTR001IMPL`
3. Escanear para mock libs: `apx add mock-lib --scan -y --project-path=./TESTR001-parent`
4. Crear transacción de prueba: `apx add mock-trx ...`
5. Añadir dependencia a transacción mock: `apx add dep -a="TESTR001" -v="0.0.0" --force -y --project-path=.../local-test/transactions/TESTTMOC-01-ES/`
6. Crear request: `apx add req -n="test" -y --project-path=.../TESTTMOC-01-ES/`
7. Implementar mock library (`QWYPRX80Impl.java`).
8. Modificar implementación real para invocar la mock library.
9. Ajustar transacción de prueba para llamar a la biblioteca.
10. Desplegar: `apx deploy local ... --local-test` y luego `apx start online`.
11. Enviar request: `apx send req -n="TESTTMOC-01-ES-test.json" -y --project-path=.../TESTTMOC-01-ES/`.

#### Código ejemplo MockLibrary (QWYPRX80Impl)

```java
public class QWYPRX80Impl extends AbstractLibrary implements QWYPRX80 {
    private static final Logger LOGGER = LoggerFactory.getLogger(QWYPRX80Impl.class);
    public List<String[]> execute(Long p1, Long p2, String s1, String s2, String s3, String s4, String s5, String s6, Long p3, Long p4) {
        LOGGER.info("QWYPRX80Impl.execute - MockLibrary is Ok :)");
        List<String[]> list = new ArrayList<>();
        list.add(new String[]{"code1","description1"});
        list.add(new String[]{"code2","description2"});
        return list;
    }
    public List<String[]> execute(Long p1, Long p2, String s1, String s2, String s3, String s4, String s5, String s6, Long p3, Long p4, String s7) {
        LOGGER.info("QWYPRX80Impl.execute - MockLibrary is Ok  :)");
        List<String[]> list = new ArrayList<>();
        list.add(new String[]{"code10","description10"});
        list.add(new String[]{"code20","description20"});
        return list;
    }
}
```

#### Flujo resumido de creación

1. Crear `local-test` (si no existe) y submódulo `mock-libraries`.
2. Agregar mock library (scan o manual).
3. Implementar métodos de la interfaz con datos controlados.
4. Referenciar la biblioteca simulada en la implementación real o transacción mock.
5. Desplegar entorno local y validar invocación.

#### Criterios de aceptación (LOCAL-TEST)

- Estructura `local-test` con submódulos presente.
- Mock libraries creadas o escaneadas según necesidad.
- Transacción mock desplegable y ejecutable en entorno local.
- Comandos de flujo ejecutables sin errores.

### Librería simulada (Mock Library)

Componente usado para simular comportamiento de una biblioteca externa en entorno local cuando la dependencia real no forma parte de la unidad de implementación.

#### Estructura

```text
├── pom.xml
└── src
        └── main
                ├── java/com/bbva/qwyp/lib/rx80/impl/QWYPRX80Impl.java
                └── resources/META-INF/spring/QWYPRX80-arc-osgi.xml
```

#### Archivos obligatorios

- `pom.xml` (declara dependencias base y plugins de empaquetado OSGi / copia artefactos)
- Clase Java de implementación mock (`QWYPRX80Impl`)
- XML Spring/OSGi que registra la implementación como servicio (no modificar)

#### POM (fragmento relevante)

```xml
<dependencies>
    <dependency>
        <groupId>com.bbva.elara</groupId>
        <artifactId>elara-library</artifactId>
        <version>${apx.core.online.version}</version>
    </dependency>
    <dependency>
        <groupId>com.bbva.qwyp</groupId>
        <artifactId>QWYPRX80</artifactId>
        <version>1.0.4</version>
    </dependency>
</dependencies>
```

Plugins clave:

- `maven-bundle-plugin` (empaquetado OSGi)
- `maven-antrun-plugin` (copia JAR a ruta destino)
- `maven-dependency-plugin` (descarga interfaz y DTOs para despliegue local)

#### XML OSGi (fragmento)

```xml
<osgi:service id="qwypRX80Osgi" ref="qwypRX80" interface="com.bbva.qwyp.lib.rx80.QWYPRX80"/>
<bean id="qwypRX80" class="com.bbva.qwyp.lib.rx80.impl.QWYPRX80Impl"/>
```

#### Implementación mock (estado inicial generado)

```java
public class QWYPRX80Impl extends AbstractLibrary implements QWYPRX80 {
        private static final Logger LOGGER = LoggerFactory.getLogger(QWYPRX80Impl.class);
        // Métodos de la interfaz deben ser implementados manualmente
}
```

#### Ejemplo de implementación con comportamiento simulado

```java
public List<String[]> execute(Long p1, Long p2, String a1, String a2, String a3, String a4, String a5, String a6, Long p3, Long p4) {
        LOGGER.info("QWYPRX80Impl.execute - MockLibrary is Ok :)");
        List<String[]> list = new ArrayList<>();
        list.add(new String[]{"code1","description1"});
        list.add(new String[]{"code2","description2"});
        return list;
}
```

#### Flujo resumido de creación de mock libraries

1. Crear `local-test` y submódulo `mock-libraries` (si no existen).
2. Agregar mock library (scan o manual).
3. Implementar métodos de la interfaz con datos controlados.
4. Desplegar entorno local y validar invocación.

#### Criterios de aceptación (Librería simulada)

- POM contiene dependencias mínimas y plugins listados.
- XML OSGi expone servicio con interfaz correcta.
- Métodos de la interfaz implementados retornando datos simulados coherentes.
- Despliegue local permite invocación sin errores.

### Buenas prácticas

#### Mejores prácticas: librerías APX

##### Acceso a datos en APX

- El acceso a los datos se realiza exclusivamente desde las bibliotecas APX en el caso de Internet.
- Una UUAA sólo podrá acceder a los datos que posea, y a los datos de terceros a través de las bibliotecas APX que el titular de los datos proporcione.
- Uso obligatorio de las utilidades provistas por la Arquitectura; para relacionales: JDBC (JPA en desuso desde 2018 y su caché no permitida).
- No manejar directamente `Datasource` (no crear, abrir o cerrar conexiones explícitamente).
- Incluir SIEMPRE el nombre de esquema en las tablas consultadas.
- Usar variables BIND en todas las consultas.
- Consultas dinámicas: restringidas y validadas por Arquitectura (y Calidad si procede).
- Evitar SQL específico de un gestor (compatibilidad Oracle/PostgreSQL requerida).
- Para Mongo usar `DocumentWrapper` y utilidades del conector Datio (evitar BSON/Document directos).

##### Anidación e invocación finita de bibliotecas en desarrollo

El árbol de dependencias debe ser finito para minimizar impacto de fallos y mejorar trazabilidad.

##### Bibliotecas sin estado

- No definir variables miembro (singleton compartido) salvo las generadas por la Arquitectura.
- No almacenar datos de negocio en variables globales o archivos locales.
- Datos compartidos: base de datos o configuración.
- Paso de datos entre métodos siempre vía parámetros.

##### Gestión de errores y excepciones

- Seguir exclusivamente el modelo de Gestión de Errores de la Arquitectura.
- Notificación de errores en bibliotecas mediante acumulación en la pila (no excepciones propias en métodos de ejecución).
- Prohibido capturar genéricamente `Exception`.
- Excepciones permitidas (ejemplos APX):
  - `com.bbva.apx.exception.business.BusinessException`
  - `com.bbva.apx.exception.io.network.TimeoutException`
  - `com.bbva.apx.exception.db.DuplicateKeyException`
  - `com.bbva.apx.exception.db.NoResultException` (etc. según listado original)
- Excepciones Java: formateo numérico (`NumberFormatException`) aceptada cuando corresponda.
- Spring: sólo `RestClientException`, `HttpStatusCodeException` en capas que lo justifiquen.

##### Acceso a utilidades y librerías

- Usar únicamente las utilidades inyectadas/abstractas provistas por la Arquitectura (p.ej. `jdbcUtils`).
- Evitar librerías de terceros sin validación de Arquitectura y Calidad.
- Objetos inyectados no deben compartirse entre componentes.

##### Exportación de funcionalidad

- Exportar sólo paquetes de la interfaz y DTOs usados como parámetros o retorno.
- Implementaciones permanecen ocultas.

##### Versionado de bibliotecas

- Sólo una versión desplegada simultáneamente; todos los cambios deben ser retrocompatibles.
- Cambios retrocompatibles: nuevos métodos, cambios internos, sobrecarga para nuevas firmas.

##### Uso de DTO

- Obligatorio para agrupar datos y para intercambio entre: Transacción ↔ Librería, Librería ↔ Librería, Trabajo ↔ Librería.
- Se permiten jerarquías DTO.
- Evitar dependencias circulares entre librerías y DTO (LIB1→LIB2→LIB3→LIB1 prohibido).

##### Dependencias técnicas

- Cambios que afecten JVM, SO, JBOSS u otros requieren aprobación Arquitectura.
- Prohibido `@SuppressWarnings` para ocultar usos obsoletos.

##### Monohilo

No crear ni gestionar hilos manualmente.

##### Publicación de servicios OSGi

Sólo mediante el asistente de bibliotecas (modelo estándar); no publicar servicios adicionales.

##### Comunicación hacia sistemas NO APX

Usar exclusivamente `APIConnector`. Requiere validación del Arquitecto de Solución y gestión de certificados por Seguridad Lógica/Criptografía.

##### Código en la interfaz de la Librería

No incluir lógica funcional en la interfaz; sólo en la implementación.

##### Invocaciones a transacciones de MainFrame

- Evitar invocaciones encadenadas; máximo dos llamadas salvo validación explícita.
- Preferir replicar datos de lectura en BD APX.

#### Mejores prácticas del modelo de dependencia

> El cumplimiento se valida (Samuel / APX CLI). APX CLI ofrece reparación automática.

##### Dependencias en Runtime (Import-Package)

- Generadas en `MANIFEST.MF` via `maven-bundle-plugin`.
- Instrucción comodín obligatoria: `*;version="${osgi.version.manifest}"` (resuelve a `0.0`).
- No editar/eliminar el comodín.
- Declarar explícitamente sólo DTOs de terceros no referenciados directamente.
- Orden: paquetes específicos primero, comodín al final.
- Prohibido `resolution:="optional"`.
- No modificar paquetes de Arquitectura (ej. `org.osgi.framework`, `com.bbva.elara.aspect`, etc.).
- Prohibido exportar transacciones, trabajos, DTOs e implementación. Usar en transacciones/trabajos:

```xml
<Export-Package>
    !*;version="${arc.osgi.version}"
</Export-Package>
```

Ejemplo correcto (sin paquetes explícitos adicionales):

```xml
<Import-Package>
    *;version="${osgi.version.manifest}"
</Import-Package>
```

Ejemplo con DTO indirecto:

```xml
<Import-Package>
    com.bbva.uuaa.dto.secondDTO;version="${osgi.version.manifest}",
    *;version="${osgi.version.manifest}"
</Import-Package>
```

Incorrecto (orden invertido):

```xml
<Import-Package>
    *;version="${osgi.version.manifest}",
    com.bbva.uuaa.dto.secondDTO;version="${osgi.version.manifest}"
</Import-Package>
```

Incorrecto (uso opcional):

```xml
<Import-Package>
    com.bbva.uuaa.lib.r002.*;version="${osgi.version.manifest}";resolution:="optional",
    *;version="${osgi.version.manifest}"
</Import-Package>
```

##### Dependencias de compilación (sección dependencies)

- Prohibido marcar dependencias como opcionales (`<optional>true</optional>`).
- En interfaz o DTO: sólo dependencias a DTO (no librerías).
- POM padre: no debe declarar dependencias de ejecución de componentes.
- Declarar dependencias únicamente en el módulo que las usa.

Ejemplo correcto:

```xml
<dependencies>
    <dependency>
        <groupId>com.bbva.qwpu</groupId>
        <artifactId>QWPUR001</artifactId>
        <version>0.1.0</version>
    </dependency>
</dependencies>
```

Incorrecto (opcional):

```xml
<dependencies>
    <dependency>
        <groupId>com.bbva.qwpu</groupId>
        <artifactId>QWPUR001</artifactId>
        <version>0.1.0</version>
        <optional>true</optional>
    </dependency>
</dependencies>
```

##### Interfaz de biblioteca (ejemplos)

Correcto:

```java
package com.bbva.test.lib.r001;
import com.bbva.test.dto.example.ExampleDTO;
import java.util.Map;

public interface TESTR001 {
    ExampleDTO executeFindOneBy(Map<String, Object> filters);
}
```

Incorrecto (uso de tipo no DTO externo):

```java
package com.bbva.test.lib.r001;
import org.json.JSONObject;
import java.util.Map;

public interface TESTR001 {
    JSONObject executeFindOneBy(Map<String, Object> filters);
}
```

##### POM padre (módulos únicamente)

Correcto:

```xml
<project>
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>com.bbva.qwpu</groupId>
        <artifactId>uuaa-test</artifactId>
        <version>0.1.0</version>
        <relativePath>../../</relativePath>
    </parent>
    <groupId>com.bbva.uuaa</groupId>
    <artifactId>TRANSACTIONS-uuaa-test</artifactId>
    <version>0.1.0</version>
    <packaging>pom</packaging>
    <modules>
        <module>UUAAT000-01-ZZ</module>
    </modules>
</project>
```

Incorrecto (declara dependencias):

```xml
<project>
    ...
    <dependencies>
        <dependency>
            <groupId>com.bbva.uuaa</groupId>
            <artifactId>UUAAR000</artifactId>
            <version>0.1.0</version>
        </dependency>
    </dependencies>
</project>
```

##### Otras consideraciones

- Nueva versión de una dependencia: gracias a versión `0.0` en `Import-Package` se acopla automáticamente a la disponible (retrocompatible si no elimina firmas previas).
- Eliminar dependencias no usadas siempre vía APX CLI (evitar edición manual).
- Paquete comodín debe ir al final y mantenerse.

Ejemplo comodín final:

```xml
<Import-Package>
    ...
    *;version="${arc.osgi.version}"
</Import-Package>
```
