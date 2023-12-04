# Projecto 2 - Bases de Datos 2

## Requerimientos
1. Implementar las rutas de "obtener uno" ( GET /{book_id} ) y "actualizar" para libros.
2. En el código entregado, las rutas que usan id entregan un error genérico cuando el id no existe en la base de datos. Implementar un mensaje de error que envíe un código 404 e indique "El no existe".
3. Implementar una ruta que permita buscar libros mediante su título. Para esto se puede utilizar "LIKE", cuyo uso en SQLAlchemy se detalla en esta sección de la documentación.
4. Implementar un modelo para "clientes" de la biblioteca, con su gestión a través de la API.
5. Implementar un mecanismo en la API que permita ingresar préstamos de libros. Para esto será necesario agregar las
entidades necesarias e implementar su gestión a través de la API. Recordar que pueden existir múltiples copias de cada libro, y
al momento de ingresar el préstamo se debe verificar si existen copias disponibles para préstamo
##
