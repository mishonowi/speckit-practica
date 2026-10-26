# Especificación de Funcionalidad: Organizador de Tareas Académicas

**Rama de la funcionalidad**: `001-organizador-tareas-academicas`

**Creado**: 2026-10-26

**Estado**: Borrador

**Entrada**: Descripción del usuario: "Quiero una aplicación para estudiantes de la UPB que les ayude a organizar sus tareas académicas. El estudiante puede registrar sus materias (nombre y color). Puede crear tareas asociadas a una materia, con título, descripción opcional y fecha de entrega. Ve un listado de tareas ordenado por fecha de entrega, donde las tareas vencidas se destacan y las próximas 48 horas aparecen como "urgentes". Puede marcar tareas como completadas y filtrarlas por materia o por estado. En esta primera versión no hay inicio de sesión: es un solo usuario por dispositivo."

## Aclaraciones

### Sesión 2026-10-26

- Q: ¿Qué pasa con las tareas al borrar una materia? → A: Se borran también todas sus tareas, tras una confirmación que indica cuántas tareas se perderán.
- Q: ¿Cuántos caracteres máximo acepta cada campo? → A: Nombre de materia 50, título de tarea 100 y descripción 500.
- Q: ¿Cómo se calcula "urgente"? → A: Por horas exactas: es urgente si faltan 48 horas o menos (y aún no venció) entre el momento actual y la fecha y hora de entrega.

## Escenarios de Usuario y Pruebas *(obligatorio)*

### Historia de Usuario 1 - Registrar materias (Prioridad: P1)

El estudiante registra las materias que cursa, indicando un nombre y eligiendo un color para cada una. El color le permite reconocer rápidamente a qué materia pertenece cada tarea.

**Por qué esta prioridad**: Las tareas siempre pertenecen a una materia; sin materias no se puede crear ninguna tarea. Es la base de toda la aplicación.

**Prueba independiente**: Se puede probar creando una materia con nombre y color y verificando que aparece en la lista de materias; entrega valor al permitir al estudiante armar su catálogo de materias del semestre.

**Escenarios de aceptación**:

1. **Dado** que el estudiante no tiene materias registradas, **cuando** ingresa el nombre "Cálculo II" y elige un color, **entonces** la materia aparece en su lista con ese nombre y color.
2. **Dado** que el estudiante intenta guardar una materia sin nombre, **cuando** confirma el formulario, **entonces** se muestra un mensaje de error claro en español y la materia no se crea.
3. **Dado** que ya existe una materia llamada "Física I", **cuando** el estudiante intenta registrar otra con el mismo nombre, **entonces** se le informa que ya existe y no se crea un duplicado.

---

### Historia de Usuario 2 - Crear tareas y verlas ordenadas por fecha (Prioridad: P1)

El estudiante crea tareas asociadas a una materia, con título, descripción opcional y fecha de entrega, y las ve en un único listado ordenado por fecha de entrega (primero las más cercanas).

**Por qué esta prioridad**: Es el valor central de la aplicación: saber qué hay que entregar y en qué orden.

**Prueba independiente**: Con al menos una materia creada, se crean varias tareas con distintas fechas y se verifica que el listado las muestra de la más próxima a la más lejana, con su materia y color.

**Escenarios de aceptación**:

1. **Dado** que existe la materia "Cálculo II", **cuando** el estudiante crea una tarea con título "Taller 3" y una fecha de entrega, **entonces** la tarea aparece en el listado asociada a esa materia y con su color.
2. **Dado** que existen tareas con fechas de entrega distintas, **cuando** el estudiante abre el listado, **entonces** las tareas aparecen ordenadas por fecha de entrega de la más próxima a la más lejana.
3. **Dado** que el estudiante crea una tarea sin descripción, **cuando** la guarda, **entonces** la tarea se crea correctamente (la descripción es opcional).
4. **Dado** que el estudiante intenta guardar una tarea sin título, sin materia o sin fecha de entrega, **cuando** confirma, **entonces** se muestra un mensaje de error claro en español indicando el campo faltante y la tarea no se crea.

---

### Historia de Usuario 3 - Identificar tareas vencidas y urgentes (Prioridad: P2)

En el listado, las tareas cuya fecha de entrega ya pasó se destacan visualmente como "vencidas", y las que vencen dentro de las próximas 48 horas se muestran como "urgentes".

**Por qué esta prioridad**: Ayuda a priorizar, pero depende de que ya existan tareas y listado.

**Prueba independiente**: Se crean tareas con fecha pasada, con fecha dentro de 48 horas y con fecha posterior, y se verifica que cada una muestra el indicador correspondiente (o ninguno).

**Escenarios de aceptación**:

1. **Dado** una tarea pendiente con fecha de entrega anterior al momento actual, **cuando** el estudiante ve el listado, **entonces** la tarea aparece destacada como vencida.
2. **Dado** una tarea pendiente cuya entrega es dentro de 48 horas o menos (por ejemplo, mañana a las 23:00 estando hoy a las 10:00), **cuando** el estudiante ve el listado, **entonces** la tarea aparece marcada como "urgente".
3. **Dado** una tarea pendiente cuya fecha de entrega es posterior a 48 horas, **cuando** el estudiante ve el listado, **entonces** no se muestra ningún indicador especial.
4. **Dado** una tarea completada con fecha de entrega pasada o próxima, **cuando** el estudiante ve el listado, **entonces** no se muestra como vencida ni como urgente.

---

### Historia de Usuario 4 - Marcar tareas como completadas (Prioridad: P2)

El estudiante marca una tarea como completada cuando la termina (y puede revertirlo si se equivocó).

**Por qué esta prioridad**: Permite llevar el control del avance; sin ello el listado se llena de tareas ya resueltas.

**Prueba independiente**: Se marca una tarea como completada y se verifica que su estado cambia y que el cambio se conserva al volver a abrir la aplicación.

**Escenarios de aceptación**:

1. **Dado** una tarea pendiente, **cuando** el estudiante la marca como completada, **entonces** su estado cambia a completada y se distingue visualmente de las pendientes.
2. **Dado** una tarea completada, **cuando** el estudiante la desmarca, **entonces** vuelve a estado pendiente.

---

### Historia de Usuario 5 - Filtrar tareas por materia o estado (Prioridad: P3)

El estudiante filtra el listado por una materia específica y/o por estado (pendientes, completadas), para concentrarse en lo que le interesa.

**Por qué esta prioridad**: Mejora la comodidad cuando hay muchas tareas, pero la aplicación ya es útil sin ello.

**Prueba independiente**: Con tareas de varias materias y estados, se aplica cada filtro y se verifica que solo se muestran las tareas que cumplen el criterio.

**Escenarios de aceptación**:

1. **Dado** tareas de distintas materias, **cuando** el estudiante filtra por "Cálculo II", **entonces** solo se muestran las tareas de esa materia, manteniendo el orden por fecha.
2. **Dado** tareas pendientes y completadas, **cuando** el estudiante filtra por "Completadas", **entonces** solo se muestran las completadas.
3. **Dado** que se combinan filtro por materia y por estado, **cuando** se aplican ambos, **entonces** se muestran solo las tareas que cumplen los dos criterios.
4. **Dado** un filtro que no coincide con ninguna tarea, **cuando** se aplica, **entonces** se muestra un mensaje indicando que no hay tareas para ese filtro.

---

### Casos Límite

- ¿Qué pasa cuando el estudiante todavía no tiene materias y quiere crear una tarea? Se le indica que debe registrar primero una materia.
- ¿Qué pasa si no hay ninguna tarea registrada? El listado muestra un mensaje de estado vacío que invita a crear la primera tarea.
- ¿Qué ocurre con una tarea cuya fecha de entrega es exactamente dentro de 48 horas? Se considera urgente (el límite es inclusivo). ¿Y con una tarea cuya hora de entrega es exactamente el momento actual? Se considera vencida.
- ¿Qué pasa si una tarea pasa de "urgente" a "vencida" mientras la aplicación está abierta? El estado visual debe actualizarse sin perder el orden del listado.
- ¿Qué pasa con textos muy largos en nombre de materia, título o descripción? Se rechazan los textos que superen 50 caracteres (nombre de materia), 100 (título) o 500 (descripción), indicando el límite en un mensaje claro.
- ¿Qué pasa si el estudiante intenta eliminar una materia que tiene tareas? Se le advierte de cuántas tareas también se eliminarán y debe confirmar la acción; si cancela, la materia y sus tareas se conservan.
- ¿Qué pasa si se ingresa una fecha de entrega ya pasada al crear una tarea? Se permite (por ejemplo, para registrar una tarea atrasada) y se muestra como vencida.

## Requisitos *(obligatorio)*

### Requisitos Funcionales

- **RF-001**: El sistema DEBE permitir al estudiante registrar una materia con un nombre y un color.
- **RF-002**: El sistema DEBE rechazar materias sin nombre o con nombre repetido (sin distinguir mayúsculas/minúsculas), mostrando un mensaje de error en español.
- **RF-003**: El sistema DEBE permitir editar y eliminar materias; al eliminar una materia con tareas, DEBE pedir confirmación indicando cuántas tareas se perderán y, si el estudiante confirma, eliminar la materia junto con todas sus tareas. Si el estudiante cancela, no se elimina nada.
- **RF-004**: El sistema DEBE permitir crear una tarea asociada a una materia existente, con título obligatorio, descripción opcional y fecha de entrega obligatoria.
- **RF-005**: El sistema DEBE validar los datos de tareas y materias (obligatoriedad, fecha válida y longitud máxima: nombre de materia 50 caracteres, título de tarea 100 y descripción 500; se rechazan los textos que solo contienen espacios) y mostrar mensajes de error claros en español.
- **RF-006**: El sistema DEBE permitir editar y eliminar tareas.
- **RF-007**: El sistema DEBE mostrar un listado de tareas ordenado por fecha de entrega, de la más próxima a la más lejana, mostrando para cada una su título, materia (con su color) y fecha de entrega.
- **RF-008**: El sistema DEBE destacar visualmente como "vencidas" las tareas pendientes cuya fecha de entrega ya pasó.
- **RF-009**: El sistema DEBE mostrar como "urgentes" las tareas pendientes cuya fecha y hora de entrega no ha llegado y faltan 48 horas o menos desde el momento actual (cálculo por horas exactas, no por días de calendario). Al llegar la hora de entrega, la tarea pasa de "urgente" a "vencida".
- **RF-010**: El sistema NO DEBE mostrar como vencidas ni urgentes las tareas completadas.
- **RF-011**: El sistema DEBE permitir marcar una tarea como completada y revertirla a pendiente.
- **RF-012**: El sistema DEBE permitir filtrar el listado por materia y por estado (todas, pendientes, completadas), y combinar ambos filtros.
- **RF-013**: El sistema DEBE conservar las materias y tareas del estudiante entre sesiones en el mismo dispositivo.
- **RF-014**: El sistema DEBE funcionar sin inicio de sesión, tratando a cada dispositivo como un único usuario; los datos de un dispositivo no se comparten con otros.
- **RF-015**: Toda la interfaz y todos los mensajes al usuario DEBEN estar en español.
- **RF-016**: La interfaz DEBE ser usable en celular y en computadora, operable con teclado y con contraste de texto suficiente.

### Entidades Clave

- **Materia**: Asignatura que cursa el estudiante. Atributos: nombre (único) y color. Una materia tiene cero o más tareas.
- **Tarea**: Actividad académica por entregar. Atributos: título, descripción (opcional), fecha de entrega, estado (pendiente o completada) y la materia a la que pertenece. Toda tarea pertenece a exactamente una materia.

## Criterios de Éxito *(obligatorio)*

### Resultados Medibles

- **CE-001**: Un estudiante nuevo puede registrar una materia y crear su primera tarea en menos de 2 minutos, sin ayuda ni instrucciones.
- **CE-002**: El 100 % de las tareas pendientes con fecha de entrega vencida o dentro de las próximas 48 horas se muestran con su indicador correcto ("vencida" o "urgente").
- **CE-003**: El estudiante puede identificar en menos de 5 segundos cuál es su tarea pendiente más próxima al abrir la aplicación.
- **CE-004**: Marcar una tarea como completada o aplicar un filtro requiere como máximo 2 interacciones y el resultado se ve de inmediato.
- **CE-005**: Los datos registrados siguen disponibles al cerrar y volver a abrir la aplicación en el mismo dispositivo.
- **CE-006**: El 90 % de los estudiantes de prueba completa las acciones principales (crear materia, crear tarea, completarla, filtrar) en el primer intento.

## Supuestos

- Los usuarios son estudiantes de la UPB que usan la aplicación de forma personal; no hay roles ni colaboración entre usuarios.
- Cada dispositivo representa a un único usuario; no existe inicio de sesión, ni sincronización entre dispositivos, ni recuperación de datos si se pierde el dispositivo o se borran sus datos locales.
- Las fechas y horas se interpretan en la zona horaria del dispositivo del estudiante.
- La fecha de entrega incluye día y hora, necesarias para calcular la ventana de 48 horas.
- El color de una materia se elige de una paleta predefinida de colores, con suficiente contraste para el texto.
- Fuera del alcance de esta versión: inicio de sesión, recordatorios o notificaciones, tareas recurrentes, adjuntos, compartir tareas y sincronización entre dispositivos.
- Los datos se guardan en el propio dispositivo; no se requiere conexión a internet para usar la aplicación una vez cargada.
