## Antipatrones

Un antipatrón de diseño es un patrón de diseño que invariablemente conduce a una mala solución a un problema. Entre los antipatrones que hemos detectado dentro de APX, citamos los siguientes, así como el enlace a su detalle:

- Blob en librerías.
- Contenedor mágico en librerías. Este mismo antipatrón es aplicable a transacciones, por lo que no se debe utilizar un campo de entrada para que la transacción haga cosas funcionalmente diferentes (por ejemplo, un campo de acción con valores "A", "B" o "M" para hacer Alta, Borrar o Modificar.
