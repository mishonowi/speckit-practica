# Lista de Verificación de Experiencia de Usuario y Validación de Datos: Organizador de Tareas Académicas

**Propósito**: Comprobar la calidad (completitud, claridad, consistencia y medibilidad) de los requisitos de experiencia de usuario y de validación de datos antes de generar las tareas e implementar.
**Creado**: 2026-10-26
**Funcionalidad**: [spec.md](../spec.md) · [plan.md](../plan.md) · [data-model.md](../data-model.md) · [contracts/api.md](../contracts/api.md)

**Nota**: Esta lista personalizada fue generada por el comando `/speckit-checklist` a partir del contexto de la funcionalidad. Evalúa la **redacción de los requisitos**, no el funcionamiento del código.
**Responsabilidad de revisión**: Esta lista es un artefacto de revisión de calidad de requisitos que pertenece a quien revisa. Marca un ítem con `[x]` solo cuando la persona revisora determine que el criterio se cumple.
**Significado de las marcas**: `[x]` significa que el criterio de calidad del requisito fue revisado y se cumple. No significa que el trabajo de implementación esté terminado.

**Supuestos de generación** (no hubo preguntas previas): profundidad estándar; audiencia: quien revisa la especificación y el plan antes de `/speckit-tasks`; foco: experiencia de usuario (listado, indicadores, formularios, estados vacíos y de error, accesibilidad) y validación de datos (campos, límites, duplicados, fechas).

## Completitud de Requisitos de Experiencia de Usuario

- [ ] CHK001 ¿Están definidos los estados de carga y de error de comunicación (por ejemplo, el servidor no responde) para el listado y para cada acción de guardar, completar o borrar? [Completitud, Brecha]
- [ ] CHK002 ¿Se especifica qué ve el estudiante cuando todavía no tiene materias, y cómo se le guía a registrar la primera antes de crear una tarea? [Cobertura, Spec §Casos Límite]
- [ ] CHK003 ¿Se define el estado vacío del listado cuando no hay tareas y cuando un filtro no da resultados, con un mensaje distinto para cada caso? [Completitud, Spec §HU5 escenario 4]
- [ ] CHK004 ¿Están descritos los flujos de interfaz para editar una materia y editar una tarea (qué se puede cambiar y cómo se confirma), y no solo la existencia de la operación? [Brecha, Spec §RF-003, RF-006]
- [ ] CHK005 ¿Se especifica si borrar una tarea individual requiere confirmación, igual que borrar una materia? [Brecha, Spec §RF-006]
- [ ] CHK006 ¿Se define cómo se presenta al estudiante la confirmación de borrado de materia (contenido del mensaje y acciones disponibles), más allá de "indicar cuántas tareas se perderán"? [Claridad, Spec §RF-003]
- [ ] CHK007 ¿Se define el estado inicial de los filtros al abrir la aplicación y si se conservan al recargar la página? [Brecha, Spec §RF-012]
- [ ] CHK008 ¿Se especifica la información mínima que muestra cada elemento del listado (título, materia, fecha, estado, descripción) y si la descripción es visible en el listado o solo al abrir la tarea? [Completitud, Spec §RF-007]

## Claridad de los Indicadores y la Presentación

- [ ] CHK009 ¿Está cuantificado o descrito de forma verificable qué significa "destacar" una tarea vencida (por ejemplo, color, ícono y texto) en lugar de un adjetivo subjetivo? [Ambigüedad, Spec §RF-008]
- [ ] CHK010 ¿Se exige que "vencida" y "urgente" se distingan también por texto o ícono y no solo por color, coherente con el principio de accesibilidad de la constitución? [Consistencia, Spec §RF-016]
- [ ] CHK011 ¿Se define cómo se distingue visualmente una tarea completada de una pendiente y qué ocurre con su posición en el orden del listado? [Claridad, Spec §HU4]
- [ ] CHK012 ¿Se define el formato de presentación de la fecha y hora de entrega (idioma, 12/24 horas, año) y si se muestra el tiempo restante en tareas urgentes? [Brecha, Spec §RF-007]
- [ ] CHK013 ¿Está listada en la especificación la paleta de colores disponible o, al menos, la cantidad de colores, en lugar de dejarla solo en el plan? [Brecha, Spec §Supuestos]
- [ ] CHK014 ¿Es medible el criterio "identificar en menos de 5 segundos la tarea pendiente más próxima" (¿con cuántas tareas en pantalla y en qué dispositivo?)? [Medibilidad, Spec §CE-003]
- [ ] CHK015 ¿Se define la población y el método de medición del "90 % de estudiantes de prueba" (cuántos estudiantes, qué se considera primer intento)? [Medibilidad, Spec §CE-006]

## Calidad de los Requisitos de Validación de Datos

- [ ] CHK016 ¿Están los límites de longitud (50, 100 y 500) expresados en el contrato de la API y en los requisitos con el mismo criterio de conteo (caracteres tras recortar espacios)? [Consistencia, Spec §RF-005, Aclaraciones]
- [ ] CHK017 ¿Se aclara si los espacios al inicio y al final se recortan antes de validar y de guardar, y qué pasa con espacios múltiples internos? [Claridad, Spec §RF-005]
- [ ] CHK018 ¿Está definido qué se considera nombre duplicado (mayúsculas, minúsculas y letras acentuadas, por ejemplo "Álgebra" y "algebra") de forma que dos personas obtengan la misma conclusión? [Ambigüedad, Spec §RF-002]
- [ ] CHK019 ¿Se especifica si el estudiante puede escribir cualquier carácter (emojis, saltos de línea en la descripción, signos) o existe un conjunto restringido? [Brecha, Spec §RF-005]
- [ ] CHK020 ¿Se define si la fecha de entrega se captura con hora (y cuál es la hora por defecto si el estudiante solo elige el día), ya que la regla de 48 horas depende de ella? [Brecha, Spec §Supuestos, RF-009]
- [ ] CHK021 ¿Se define un rango válido de fechas (por ejemplo, un máximo hacia el futuro) además de permitir fechas pasadas? [Brecha, Spec §Casos Límite]
- [ ] CHK022 ¿Se especifica si, al guardar una tarea con fecha pasada, se avisa al estudiante o se permite sin ningún aviso? [Claridad, Spec §Casos Límite]
- [ ] CHK023 ¿Se define el comportamiento cuando se intenta crear o editar una tarea con una materia que fue borrada mientras el formulario estaba abierto? [Cobertura, Caso de Excepción, Brecha]
- [ ] CHK024 ¿Se define qué ocurre cuando el estudiante guarda una descripción vacía o solo con espacios (se trata como "sin descripción")? [Claridad, Spec §RF-004]
- [ ] CHK025 ¿Existe un límite máximo de materias o de tareas, o se declara explícitamente que no hay límite? [Brecha, Spec §Supuestos]

## Mensajes de Error y Retroalimentación

- [ ] CHK026 ¿Están definidos los textos o criterios de redacción de los mensajes de error para cada regla de validación (campo vacío, demasiado largo, duplicado, fecha inválida)? [Completitud, Spec §RF-005]
- [ ] CHK027 ¿Se especifica dónde y cuándo aparece el mensaje de error (junto al campo, al enviar o mientras se escribe) y que se anuncia a tecnologías de apoyo? [Brecha, Spec §RF-016]
- [ ] CHK028 ¿Se define que, ante un error de validación, los datos que el estudiante ya escribió se conservan en el formulario? [Brecha, Caso de Excepción]
- [ ] CHK029 ¿Se especifica qué confirmación o retroalimentación recibe el estudiante tras crear, completar o borrar algo (por ejemplo, aviso breve o actualización inmediata del listado)? [Brecha, Spec §CE-004]
- [ ] CHK030 ¿Se indica el límite de caracteres al estudiante antes de que lo supere (contador o texto de ayuda), o solo después del rechazo? [Claridad, Spec §Casos Límite]

## Cobertura de Escenarios y Casos Límite

- [ ] CHK031 ¿Se definen los requisitos de recuperación cuando falla el guardado (por ejemplo, error al escribir en el almacenamiento local): se informa y se conservan los datos del formulario? [Cobertura, Recuperación, Brecha]
- [ ] CHK032 ¿Se aborda el uso de la aplicación en dos pestañas o ventanas a la vez, y qué estado ve el estudiante tras un cambio hecho en la otra? [Cobertura, Brecha]
- [ ] CHK033 ¿Se define qué ocurre con un filtro por materia cuando esa materia es borrada o renombrada? [Cobertura, Caso Límite, Spec §RF-012]
- [ ] CHK034 ¿Es consistente la regla de "urgente" entre la Historia 3, RF-009 y CE-002 (que aún dice "dentro de las próximas 48 horas" sin precisar el cálculo por horas exactas)? [Consistencia, Spec §HU3, RF-009, CE-002]
- [ ] CHK035 ¿Se define el orden de tareas con la misma fecha y hora de entrega (desempate) a nivel de requisitos y no solo en el modelo de datos? [Claridad, Spec §RF-007]

## Accesibilidad y Diseño Adaptable

- [ ] CHK036 ¿Están definidos los requisitos de uso con teclado para todas las acciones (crear, editar, completar, borrar, filtrar, confirmar) y el orden de foco en formularios y diálogos? [Cobertura, Spec §RF-016]
- [ ] CHK037 ¿Se cuantifica el "contraste suficiente" con un criterio verificable (por ejemplo, una razón mínima de contraste) y se aplica a los colores de las materias? [Medibilidad, Spec §RF-016, Supuestos]
- [ ] CHK038 ¿Se definen los anchos de pantalla mínimos soportados en celular y el comportamiento del listado y los formularios en pantallas pequeñas? [Claridad, Spec §RF-016]
- [ ] CHK039 ¿Se especifica que las etiquetas de los campos del formulario y los controles de completar/borrar tienen nombres descriptivos para lectores de pantalla? [Cobertura, Spec §RF-016]

## Dependencias y Supuestos

- [ ] CHK040 ¿Está validado o documentado el supuesto de que la hora del dispositivo es correcta, dado que de ella depende el cálculo de "vencida" y "urgente"? [Supuesto, Spec §Supuestos]
- [ ] CHK041 ¿Se aclara cómo se ejecuta la aplicación en el dispositivo del estudiante (quién la inicia) y cómo se relaciona eso con el requisito "un solo usuario por dispositivo" y con la persistencia de datos? [Supuesto, Spec §RF-013, RF-014]

## Notas

- Marca los ítems con `[x]` solo después de que la revisión confirme que se cumple el criterio de calidad del requisito
- Deja los ítems sin marcar cuando todavía requieran aclaración, corrección o evaluación de quien revisa
- `/speckit-implement` lee el estado de las casillas de esta lista como una puerta de calidad y no debe modificar las marcas
- `checklists/requirements.md` tiene un ciclo de vida independiente, mantenido por `/speckit-specify` y `/speckit-clarify`
- Los ítems con la etiqueta [Brecha] suelen resolverse con una nueva ronda de `/speckit-clarify` o con un ajuste directo a la especificación
- Agrega comentarios o hallazgos en línea debajo de cada ítem
- Los ítems están numerados de forma secuencial para facilitar su referencia
