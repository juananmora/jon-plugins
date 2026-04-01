## Directrices generales

### Estandarización del código

De acuerdo con la nueva forma de trabajo colaborativo, se requiere que todo el desarrollo (clases, métodos, variables y comentarios) en APX esté definido en inglés, ya que los componentes pueden ser reutilizados en todo el Grupo BBVA.

### Reutilización de Code

El modelo de reutilización pasa por el empaquetamiento del código reutilizable en librerías APX, por lo tanto, cualquier lógica reutilizable o acceso a datos debe ser empaquetado de dicha manera.

### Escritura de registros y seguimiento de errores de la aplicación

La escritura debe realizarse siempre a través de las utilidades que proporciona la Arquitectura.

No se permite generar archivos propios para la escritura de logs. La Arquitectura, a través de su utilidad, debe ser la encargada de la generación de estos archivos de log . Tampoco se permite la escritura por sysout, debe ser la Arquitectura la que escriba dichos scripts.

Debes preguntar antes de generar el seguimiento que deseas escribir el nivel de seguimiento para optimizar la creación de objetos innecesarios.

Por último, las aplicaciones deben utilizar adecuadamente los [niveles de log](https://www.slf4j.org/apidocs/org/apache/commons/logging/Log.html).

### Mejores prácticas en el registro de aplicaciones

La información registrada en el registro debe ser relevante y completa. Para decidir qué información incluir, se pueden tener en cuenta los siguientes aspectos:

#### Qué

- ¿Qué evento o acción ha ocurrido?
- ¿Qué entidades han estado involucradas?
- Si hay un cambio de estado ¿cuál era el anterior? ¿Cuál es el nuevo estado?

#### Dónde

En qué punto del código ha ocurrido: componente, clase, archivo de código, método o bloque de ejecución, línea de código... Cuanto más detallada sea esta información, mejor.

Los niveles más comunes son DEBUG, INFO, WARNING y ERROR . La clasificación de los diferentes eventos en cada nivel es parte del ejercicio de análisis, y debe estar orientada a la traza legible y útil:

- **DEBUG** , para información de muy bajo nivel sólo útil para depurar la aplicación, tanto en el desarrollo como en el análisis de incidencias:
  - Llamadas a funciones y procedimientos y otros componentes, con parámetros y respuestas.
  - Flujos de ejecución.
  - Desarrollo de algoritmos y procedimientos que permitan identificar y seguir su ejecución en el desarrollo.
- **INFO** , información de nivel superior que permite monitorizar la normal ejecución:
  - Paradas y arranques de servicios y sistemas.
  - Parámetros críticos o relevantes de configuración.
  - Inicio y fin de transacciones y operaciones completadas.
  - Cambios del estado de operaciones.
- **AVISO** , información de situaciones , que aun sin ser de error, si son anómalas o no previstas , aunque la aplicación tiene alternativas para solucionar:
  - Parámetros no definidos y cuyo valor se toma por defecto.
  - Situaciones anómalas, pero que son solucionadas por la aplicación, dejando el funcionamiento en un estado correcto.
  - Funciones no esenciales o imprescindibles, que no se pueden solucionar, pero dejan el funcionamiento en un estado correcto.
- **ERROR** , información de situaciones que son error y que impiden la correcta ejecución de una operación o transacción, pero sin afectar a otras operaciones o transacciones (error aislado o de contenido):
  - No se pudo realizar una operación o transacción, pero no afecta otras solicitudes ni consultas erróneas (almacenando los parámetros de entrada).
  - Funciones Aspectos generales de la aplicación, que aun afectando al funcionamiento general de la misma, no se consideran esenciales ni imprescindibles.

Recordamos que es una mala práctica capturar excepciones genéricas y está totalmente prohibido su tratamiento.

### Invariabilidad del código generado

En tiempo de desarrollo no se pueden modificar aquellos componentes que son generados por la Arquitectura en el IDE de forma automática (Por ejemplo, clase abstracta de la Transacción). Estos componentes contienen información necesaria para la ejecución de la Transacción en APX y cualquier modificación al respecto podría alterar su comportamiento.

Además, ante modificaciones realizadas con asistentes IDE, hay objetos que se regeneran, por lo que cualquier adaptación no autorizada se perderá.

La aplicación solo debe modificar los archivos spring que tengan el sufijo "-app" así como la clase generada para la librería de transacciones o de aplicaciones, que contengan los métodos de ejecución. En los apartados de desarrollo de transacciones y librerías se encuentra más detalle al respecto.

### Información o modificaciones de variables de entorno o de la JVM

No se permite que la aplicación modifique o informe una variable de entorno de la JVM. No se permiten sentencias del tipo "System.setProperty" o "Locale.setDefault" ya que afectan a todas las aplicaciones que se ejecutan en Runtime Online o Batch.

### Uso de anotaciones de Spring Bean

Como regla general, no se recomienda utilizar anotaciones de Spring en las clases de la biblioteca APX porque provoca un acoplamiento con el marco de Spring y causaría problemas en caso de que queramos cambiar el marco de inyección de dependencias en el futuro.

Está prohibido colocar las siguientes anotaciones de spring en las clases de implementación de las bibliotecas APX: @Component, @Service, @Controller y @Repository, porque estas anotaciones causan conflictos en la resolución de la ruta de clase del paquete de la biblioteca y tienen el efecto de que la biblioteca no expone su servicio OSGi.

Ejemplo de Code no conforme:

```java
@Component("uuaaR001")
public class UUAAR001Impl extends UUAAR001Abstract { ... }
```

Solución compatible:

```java
public class UUAAR001Impl extends UUAAR001Abstract { ... }
```

#### Mejores prácticas generales

Respecto a las buenas prácticas de cada tecnología, nos remitiremos a las páginas de cada tecnología, tal y como las presuponen los desarrolladores de aplicaciones, siempre que no entren en conflicto con las directrices anteriormente indicadas.

- [Java](http://docs.oracle.com/cd/A97688_16/generic.903/bp/java.htm)
- [Framework de Spring](http://springframework.net/overview/)
- [OSGI](https://docs.osgi.org/)

### Mejores prácticas: Transacciones en línea

#### Elaboración de perfiles de transacciones

Todas las transacciones deben estar correctamente perfiladas para garantizar un uso conveniente.

#### Invocación entre transacciones

No se permite la invocación síncrona. Si una transacción debe invocar a otra, solo se puede hacer de forma asíncrona, previa indicación del arquitecto APX asignado al proyecto.

La invocación asíncrona entre transacciones sólo debe aplicarse en casos de transacciones no críticas, en las que el estado de finalización de la transacción asíncrona puede ignorarse, y por tanto no es necesario esperar a la finalización de dicha transacción para continuar con el flujo operativo.

Una transacción asincrónica no puede ser invocada nuevamente desde otra transacción asincrónica.

#### Orquestación del flujo de ejecución en línea

La orquestación del flujo de ejecución en APX debe realizarse en una transacción. Esta transacción debe ser autocontenida, pudiendo invocar bibliotecas de la propia UUAA y de aquellas bibliotecas de infraestructura que otras UUAA hayan definido como públicas.

#### Anidación e invocación finita de bibliotecas

El árbol de dependencias en la invocación de bibliotecas debe ser finito. Esta recomendación se basa no solo en razones de legibilidad y trazabilidad del código, sino también en minimizar el impacto de que una biblioteca mostrada incorrectamente pueda tener otras bibliotecas o transacciones. Una biblioteca que no se implementa correctamente impide que los componentes que la consumen se instalen y activen correctamente. Cuanto mayor sea el número de módulos dependientes, mayor será la probabilidad de fallo.

#### Transacciones y librerías sin estado

Las transacciones y bibliotecas no pueden tener variables miembro, más allá de las generadas por la propia Arquitectura APX en los asistentes provistos, ya que estos módulos se instancian como singleton y por lo tanto las variables miembro son compartidas entre todas las invocaciones a una transacción o biblioteca.

Esto implica que confiar en variables miembro implica una posible mezcla de datos, lo que genera incidencias en el momento de la ejecución.

La información utilizada en la lógica de negocio de la transacción debe estar incluida en los parámetros de entrada nunca en variables globales o archivos locales ya que no se puede garantizar que el nodo de ejecución de esta lógica tenga estos recursos disponibles.

Cualquier dato común que deba compartirse entre bibliotecas o transacciones de una UUAA debe almacenarse en una base de datos. En el caso de una configuración, debe incluirse como variable de configuración a través de la consola de configuración.

El intercambio de datos entre métodos de una biblioteca, u otras clases auxiliares, debe realizarse pasando estos datos como parámetro entre los diferentes métodos.

### Gestión de la transaccionalidad

Para garantizar el comportamiento transaccional de APX, la arquitectura se basa en el estándar JTA, por lo que los recursos gestionados dentro de la transacción deben ser de tipo XA.

En ningún caso, la aplicación puede invocar comandos o métodos que realicen la confirmación o persistencia de las sentencias ejecutadas en su lógica de negocio. La arquitectura se encarga de gestionar esta confirmación para garantizar la transaccionalidad.

### Gestión de errores

La gestión de errores debe seguir el modelo definido por la Arquitectura.

No se permite ningún modelo alternativo. Este modelo permite que las bibliotecas y las transacciones agreguen errores a la pila de ejecución y a la transacción para establecer la gravedad final de los errores.

Para más detalles a nivel de desarrollo consultar aquí .

### Lanzamiento de excepciones en bibliotecas

No se permite el uso de excepciones que las aplicaciones ejecuten desde los métodos de ejecución de las bibliotecas. El modo de notificación de errores de una biblioteca a su consumidor debe basarse en el modelo de Gestión de Errores mencionado en la sección anterior.
    Manejo de excepciones
    El código de la aplicación no puede manejar las excepciones lanzadas por los conectores proporcionados por APX, por los productos invocados por terceros, ni ninguna excepción que herede de RuntimeException.
    Por lo tanto, intente... el código catch (Exception exc) no está permitido.
    Si ocurre una excepción, la Arquitectura la capturará y habilitará la gestión de errores. También será responsable de deshacer los accesos transaccionales (accesos a bases de datos, etc.).
    Las únicas excepciones que pueden ser capturadas y gestionadas por las aplicaciones son las siguientes, típicas de APX:
    com.bbva.apx.exception.business.BusinessException
    com.bbva.apx.exception.io.network.TimeoutException
    Acceso a utilidades y bibliotecas de JAVA
    Desde librerías y Transacciones se deben utilizar únicamente las piezas de Arquitectura que se proporcionan desde las clases abstractas (que heredan de las librerías y transacciones), así como las utilidades que el IDE pone a disposición de las librerías.
    El uso de otro tipo de utilidades y/o librerías de terceros puede crear colisiones con las proporcionadas por la Arquitectura, por lo que cualquier necesidad deberá ser comunicada al equipo de Arquitectura para que este equipo decida cómo cubrir dicha necesidad.
    La existencia en Repositorio Binario (Nexus o Artifactory) de una librería no implica que la misma pueda ser utilizada libremente, y por tanto su uso dentro de la Arquitectura APX está sujeto a su autorización por parte del grupo de Arquitectura así como a su aprobación por parte del Dpto. de Calidad.
    Reutilización de utilidades y conectores APX
    Desde librerías y Transacciones, la arquitectura APX proporciona a las aplicaciones las utilidades necesarias para establecer la conexión con las consultas bbdd y ejecutar las utilidades, como jdbcUtils. Estos objetos son de uso exclusivo para la implementación para la que la arquitectura ha inyectado estas referencias. En ningún caso, estos objetos deben cruzar la referencia entre diferentes componentes.
    Control de versiones de transacciones
    La arquitectura APX permite la implementación y ejecución de varias versiones de una transacción al mismo tiempo.
    Un cambio en una transacción puede o no implicar el versionado. La transacción no requiere versionado cuando el cambio realizado es retrocompatible o cuando no se ha implementado en ningún entorno. Los cambios que se consideran retrocompatibles se especifican a continuación:
    Agregue un campo de entrada opcional.
    Modificar un campo de entrada obligatorio y configúrelo como opcional.
    Modificar un campo de salida opcional y hacerlo obligatorio.
    Lógica interna.
    Consideramos cambios No retrocompatibles, y por tanto implican la necesidad de versionar la transacción, los siguientes:
    Añade un campo de entrada obligatorio.
    Añadir un campo de salida (ya sea opcional u obligatorio), ya que aún siendo opcional, el consumidor podría no poder gestionarlo al recibirlo.
    Modificar un campo de entrada a opcional y ponerlo como obligatorio.
    Modificar un campo de salida obligatorio y ponerlo como opcional.
    Modificar el tipo de un campo de entrada o salida existente.
    El control de versiones implica que los consumidores que necesitan utilizar la nueva versión de la transacción deciden modificar sus invocaciones para llamar a la nueva versión.
    El número de versión de la transacción se especifica tanto en el nombre del componente como en la versión de la etiqueta pom.xml. El asistente de creación de transacciones es responsable de mantener esta coherencia en las transacciones que crea.
    Uso de DTO
    El uso de este patrón es obligatorio cuando:
    Se necesita una agrupación simple de datos en función de una funcionalidad asociada.
    Desea intercambiar información entre diferentes componentes en APX de forma coherente, organizada y agrupada.
    Es aplicable para las siguientes combinaciones: Transacción ← → Librería Librería ← → LibreríaTrabajo ← → Librería
    Puede generar jerarquías de clases DTO.
    Para más información, puedes consultar la descripción completa del patrón DTO aplicado a APX en este enlace .
    Dependencias técnicas
Las dependencias específicas del desarrollo de una transacción o biblioteca, que requieren modificaciones de parámetros o de la versión de la JVM, bibliotecas del sistema operativo, JBOSS, etc., no pueden solicitarse ni ejecutarse unilateralmente, ya que pueden desestabilizar toda la arquitectura. Este tipo de solicitudes siempre deben pasar por el grupo de Arquitectura APX.

No se pueden incluir etiquetas @SuppressWarnings ni similares. Estas anotaciones no generan errores ni advertencias en el compilador durante la compilación. Un claro ejemplo de su uso es evitar que, al compilar, se envíe una advertencia indicando que se están utilizando clases obsoletas.

### MonoHilo

La creación de hilos ni su gestión por parte de las aplicaciones no está permitida en ningún caso.
