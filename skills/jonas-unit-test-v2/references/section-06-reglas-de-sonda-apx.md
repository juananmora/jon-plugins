## Reglas de sonda APX

Por favor, haga clic en el siguiente enlace del equipo de Devops para conocer las reglas de Quality Gate y Sonar que están definidas para los diferentes Runtimes y específicamente para APX:

Sonar: tiempos de ejecución de Ether

### Cobertura de DTO

Excepcionalmente, en proyectos DTO se puede excluir la cobertura. Para ello se debe incorporar la propiedad ' sonar.coverage.exclusions ' indicando las clases que serán excluidas.

Ejemplo de uso:

```xml
<properties>
    <sonar.coverage.exclusions>
        /src/main/java/com/bbva/uuaa/dto/**/*.java
    </sonar.coverage.exclusions>
</properties>
```
