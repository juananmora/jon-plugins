## Mejores prácticas de seguridad de APX

### Introducción: Pilares de Seguridad en APX

Esta sección te dará una visión general de la seguridad en APX y las herramientas que te ayudarán a construir servicios seguros.

### APX y la seguridad en el desarrollo

En esta guía queremos abordar los aspectos de la seguridad que nos ofrece APX y cómo enfocarlos para reducir el número de vulnerabilidades en código. APX nos ofrece para la gestión de la seguridad:

- Autenticación del usuario
- Registro seguro de datos sensibles
- Librerías de criptografía personalizadas
    Trazabilidad y seguimiento de incidencias

    Con ello es importante que nos apoyemos en los elementos de seguridad que aporta la arquitectura y que veremos en los próximos capítulos.
    Herramientas de seguridad

    Al igual que otras áreas, en seguridad disponemos de herramientas automatizables que nos permiten analizar nuestro código para detectar vulnerabilidades para ser resueltas. En BBVA disponemos de la siguiente herramienta que nos permitirá reducir el riesgo de nuestros servicios APX:
    Chimera (SAST & SCA)
    Se trata de una herramienta interna del banco que orquesta los análisis de nuestros repositorios y permite revisar dos puntos cruciales:
- **SAST (Static Analysis Security Testing)**: análisis del código estático de nuestros repositorios que evalúa si existen vulnerabilidades de seguridad en código. Con ello obtenemos un informe de las vulnerabilidades detectadas en las líneas de código y separadas por criticidad (high, medium or low). Ejemplos de vulnerabilidades que podemos encontrarnos: SQL Inyection, Log inyection, uso de algoritmos criptográficos vulnerables, etc. Para más información puedes consultar el siguiente enlace: <https://owasp.org/www-community/Source_Code_Analysis_Tools>
- **SCA (Software Component Analysis)**: análisis de las librerías o dependencias referenciadas en nuestro proyecto con el objetivo de detectar vulnerabilidades de seguridad conocidas que puedan comprometer la integridad o seguridad del software.

    El resultado del análisis de Chimera permite visualizar la presencia o ausencia de vulnerabilidades de seguridad, además de sincronizarse con Samuel para bloquear el despliegue en caso de presencia de vulnerabilidades.

    En el siguiente enlace podrás encontrar la wiki de Chimera donde localizar más detalles o FAQ's que consultar:
    Link Chimera documentación

    Para el acceso de nuestros proyectos en análisis podemos hacerlo en la siguiente URL:
    Link Chimera

    ¿Dónde puedo localizar el estado de seguridad de mis proyectos/repositorios?

    Para facilitar el estado de nuestros proyectos respecto a las vulnerabilidades en SAST o SCA podemos acceder al Dashboard SSDLC donde podemos encontrar el detalle por país, UUAA's, aplicaciones, repositorios o subáreas. Está disponible en:
    Link Dashboard SSDLC
    ¿Qué puedo obtener de esta guía?

    El objetivo de esta guía es poder acercar la seguridad al desarrollador y hacer que sea parte de su ADN. Para ello abordamos temas que afectan a la seguridad de nuestros servicios con ejemplos de problemas y soluciones que nos ofrece APX o técnicas de seguridad para evitar que nuestros servicios sean comprometidos en un ataque.

    Tras revisar la guía esperamos que ganes conciencia en la gestión de datos sensibles de clientes/empresas, entiendas los procesos de autorización sobre las funcionalidades del banco, o sepas qué procesos/métodos/herramientas tienes a tu disposición para conseguir implementar un desarrollo seguro.
