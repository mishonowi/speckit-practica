# Investigación (Fase 0): Organizador de Tareas Académicas

No quedaban marcadores "NEEDS CLARIFICATION" en el contexto técnico; este documento registra las decisiones de diseño y su justificación.

## D1. Acceso a datos con `sqlite3` estándar, sin ORM

- **Decisión**: usar el módulo `sqlite3` de la biblioteca estándar con consultas SQL parametrizadas.
- **Justificación**: son solo dos tablas; un ORM añadiría una dependencia y conceptos extra (principio de Simplicidad). Las consultas parametrizadas evitan inyección SQL.
- **Alternativas**: SQLAlchemy / SQLModel (más potentes, pero innecesarios para este tamaño).

## D2. Dónde se calcula "urgente" y "vencida"

- **Decisión**: el servidor calcula `estado_plazo` (`vencida`, `urgente`, `normal`, o `ninguno` si está completada) con una función pura `calcular_estado_plazo(fecha_entrega, completada, ahora)`. El frontend vuelve a pedir el listado cada 60 segundos y al volver a enfocar la pestaña.
- **Regla (según aclaraciones)**: tarea pendiente; si `fecha_entrega <= ahora` → `vencida`; si `fecha_entrega - ahora <= 48 horas` → `urgente`; en otro caso → `normal`. Las completadas siempre → `ninguno`.
- **Justificación**: una única implementación, probada con pytest pasando `ahora` como parámetro (sin depender del reloj real). La actualización periódica cubre el caso límite de que una tarea cambie de estado con la aplicación abierta.
- **Alternativas**: calcularlo en JavaScript (duplicaría la lógica y dificultaría las pruebas con pytest).

## D3. Representación de fechas y zona horaria

- **Decisión**: el frontend envía la fecha de entrega en formato ISO 8601 **con desplazamiento horario** (por ejemplo `2026-11-03T18:00:00-04:00`, tomado de la zona del dispositivo). El servidor la convierte y almacena en UTC y la devuelve en UTC (`...Z`); el navegador la muestra en hora local.
- **Justificación**: el cálculo de 48 horas exactas no depende de la zona; mostrar en hora local cumple el supuesto de la especificación. Se rechazan fechas sin zona horaria con mensaje en español.
- **Alternativas**: guardar hora local sin zona (ambiguo si cambia la zona del dispositivo).

## D4. Un usuario por dispositivo

- **Decisión**: la aplicación se ejecuta localmente en el dispositivo del estudiante y escucha solo en `127.0.0.1`; el archivo SQLite local es su almacenamiento. No hay autenticación ni identificador de usuario.
- **Justificación**: cumple RF-014 con la solución mínima. Los datos de un dispositivo no se comparten con otros porque el servidor no se expone a la red.
- **Alternativas**: servidor compartido con almacenamiento en el navegador (`localStorage`); descartada porque el usuario pidió SQLite como almacenamiento.

## D5. Validación y mensajes de error en español

- **Decisión**: validar con Pydantic (longitudes 50/100/500, texto no vacío tras recortar espacios, color dentro de la paleta, fecha con zona horaria). Un manejador de errores traduce los errores de validación a mensajes en español con el formato `{"detalle": "...", "campos": {...}}`.
- **Justificación**: cumple el principio IV (validación en el servidor) y el requisito de idioma. El frontend muestra el mensaje junto al campo.
- **Alternativas**: validar solo en el navegador (incumple la constitución).

## D6. Unicidad de materia sin distinguir mayúsculas

- **Decisión**: columna `nombre` con colación `NOCASE` y restricción `UNIQUE`; además se recorta el texto antes de guardar. Un duplicado devuelve 409 con mensaje en español.
- **Justificación**: la restricción en la base de datos es la fuente de verdad y evita condiciones de carrera.
- **Nota**: `NOCASE` de SQLite solo iguala mayúsculas ASCII (no acentuadas, por ejemplo "Álgebra" y "álgebra"). Se compara en Python con `casefold()` antes de insertar para cubrir ese caso, y se mantiene la restricción como respaldo.

## D7. Borrado de materia en cascada

- **Decisión**: clave foránea de `tarea.materia_id` con `ON DELETE CASCADE` (y `PRAGMA foreign_keys = ON` en cada conexión). La API devuelve `total_tareas` en cada materia para que la interfaz muestre "Se borrarán N tareas" antes de confirmar. El borrado es una única petición `DELETE` y la confirmación ocurre en el frontend.
- **Justificación**: refleja la aclaración de la especificación y mantiene la consistencia en una sola operación atómica.

## D8. Paleta de colores

- **Decisión**: paleta fija de 8 colores en formato `#RRGGBB`, elegidos con contraste suficiente sobre texto blanco o negro; el servidor valida que el color pertenezca a la paleta. El frontend elige el color de texto adecuado.
- **Justificación**: coherente con el supuesto de la especificación y con el principio V (contraste).

## D9. Servir el frontend desde FastAPI

- **Decisión**: `StaticFiles` montado en `/` con `html=True`, y las rutas de la API bajo `/api`.
- **Justificación**: un solo proceso y un solo comando de arranque (`uvicorn app.main:app`), sin CORS ni paso de compilación.

## D10. Estrategia de pruebas

- **Decisión**: pruebas unitarias de `plazo.py` (límites: exactamente 48 h, exactamente la hora actual, completada, fecha pasada) y pruebas de integración con `TestClient` de FastAPI sobre una base de datos SQLite temporal por prueba. Casos de borde y error: nombre vacío/duplicado/largo, tarea sin materia, borrado en cascada, filtros combinados.
- **Justificación**: cumple el principio II (caso principal y al menos un caso de error o borde por funcionalidad). El frontend se valida manualmente con el guion de [quickstart.md](quickstart.md), sin añadir herramientas de pruebas de navegador (Simplicidad).
