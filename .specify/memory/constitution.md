<!--
Informe de Impacto de Sincronización
- Cambio de versión: 1.0.0 → 1.1.0 (MENOR: se agrega una sección nueva; no cambia ningún principio)
- Principios modificados: ninguno
- Secciones añadidas: Trabajo en Equipo y Control de Versiones
- Secciones modificadas: Flujo de Desarrollo y Puertas de Calidad (nueva condición 5 de "terminada")
- Secciones eliminadas: ninguna
- Artefactos alineados: specs/001-organizador-tareas-academicas/plan.md (verificación de la
  constitución) y tasks.md (ramas, responsables y archivos compartidos de las fases pendientes)
- Archivos añadidos: `.gitattributes` (finales de línea LF, exigido por la nueva sección)
- TODO pendientes: ninguno
-->

# Constitución de Speckit Práctica (UPB)

## Principios Fundamentales

### I. Simplicidad Primero

- Cada funcionalidad DEBE implementarse con la solución mínima que cumpla sus requisitos.
- NO se DEBE agregar código, capas, dependencias ni configuraciones "por si acaso" (YAGNI).
- Toda abstracción o dependencia nueva DEBE justificarse en el plan por una necesidad actual.
- Ante dos soluciones que cumplen el requisito, se DEBE elegir la más sencilla.

**Justificación**: en un proyecto académico el tiempo es limitado; lo simple se entrega,
se explica y se mantiene con menos errores.

### II. Pruebas Obligatorias (NO NEGOCIABLE)

- Toda funcionalidad DEBE tener pruebas automatizadas antes de darse por terminada.
- Las pruebas DEBEN cubrir el caso principal y al menos un caso de error o borde.
- Todas las pruebas DEBEN pasar antes de integrar o entregar un cambio.
- Una tarea sin pruebas que la verifiquen NO se considera completada.

**Justificación**: las pruebas demuestran que el sistema hace lo que la especificación pide
y evitan regresiones al agregar funcionalidades.

### III. Código Legible

- Variables, funciones, clases y archivos DEBEN tener nombres claros que expresen su propósito.
- Las funciones DEBEN ser pequeñas y hacer una sola cosa; si una función crece demasiado,
  se DEBE dividir.
- Se DEBE documentar con comentarios todo lo que no sea obvio (decisiones, reglas de negocio,
  casos especiales); no se comenta lo evidente.
- El estilo de código DEBE ser consistente en todo el proyecto.

**Justificación**: el código lo leen docentes y compañeros; si no se entiende, no se puede
evaluar ni mantener.

### IV. Validación de Entradas

- Todo dato proveniente del usuario (formularios, parámetros, archivos, peticiones) DEBE
  validarse antes de procesarse o almacenarse.
- La validación DEBE comprobar tipo, formato, longitud y rango según corresponda.
- Los datos inválidos DEBEN rechazarse con un mensaje de error claro y en español.
- Si existe backend, la validación DEBE hacerse también en el servidor, no solo en la interfaz.

**Justificación**: validar las entradas previene errores, datos corruptos y vulnerabilidades
de seguridad.

### V. Accesible y Responsivo

- La interfaz DEBE funcionar correctamente en celular y en computadora.
- Los elementos interactivos DEBEN poder usarse con teclado y tener etiquetas descriptivas.
- El texto DEBE tener contraste suficiente para leerse con facilidad.
- Las imágenes con información DEBEN tener texto alternativo.

**Justificación**: los usuarios acceden desde distintos dispositivos y capacidades; una
interfaz que solo funciona en un tamaño de pantalla excluye a parte de ellos.

## Restricciones del Proyecto Académico

- Todo el contenido de los documentos (especificaciones, planes, tareas, README y mensajes
  al usuario) DEBE estar en español.
- El proyecto se desarrolla en el marco de una materia de la Universidad Privada Boliviana
  (UPB) y DEBE poder ejecutarse y explicarse en una presentación académica.
- Las tecnologías elegidas DEBEN ser las mínimas necesarias y justificarse en el plan.

## Flujo de Desarrollo y Puertas de Calidad

- El trabajo sigue el flujo de Spec Kit: constitución → especificación → plan → tareas →
  implementación.
- Antes de implementar, el plan DEBE verificar el cumplimiento de los cinco principios.
- Una funcionalidad se considera terminada solo si:
  1. cumple su especificación,
  2. tiene pruebas automatizadas que pasan,
  3. valida las entradas del usuario,
  4. funciona en celular y en computadora,
  5. está integrada en `main` mediante una solicitud de integración (pull request) sin
     conflictos pendientes y con todas las pruebas pasando.

## Trabajo en Equipo y Control de Versiones

El proyecto lo desarrollan varias personas sobre el mismo repositorio. Estas reglas existen
para evitar conflictos de fusión (merge conflicts) y para que cada cambio se pueda revisar.

- **Una rama por historia**: cada historia de usuario (o tarea transversal) DEBE desarrollarse
  en su propia rama creada desde `main` actualizado, con el nombre
  `<número de funcionalidad>-hu<N>-<descripción-corta>` (por ejemplo `001-hu3-plazos`).
  Nadie DEBE trabajar directamente sobre `main`.
- **Un responsable por historia**: cada historia DEBE tener una sola persona responsable a la
  vez, registrada en la sección "Responsables" de `tasks.md` antes de empezar. Dos personas NO
  DEBEN implementar a la vez historias que modifiquen las mismas funciones o secciones.
- **Sincronizar seguido**: antes de empezar a trabajar y antes de abrir la solicitud de
  integración, se DEBE incorporar el último `main` a la rama propia y ejecutar `pytest`.
  Las ramas DEBEN integrarse pronto: una historia por solicitud de integración, sin acumular
  varias.
- **Commits pequeños**: un commit por tarea o grupo lógico, con el identificador de la tarea en
  el mensaje (por ejemplo `T030: función calcular_estado_plazo`).
- **Integración por revisión**: los cambios llegan a `main` solo mediante una solicitud de
  integración revisada por otra persona del equipo. NO se DEBE usar `push --force` sobre `main`
  ni reescribir historia ya compartida.
- **Archivos compartidos**: en los archivos que tocan varias historias (`app/main.py`,
  `app/esquemas.py`, `app/db.py`, `app/static/app.js`, `app/static/index.html`,
  `app/static/estilos.css` y `tasks.md`), cada persona DEBE agregar su código en la sección
  de su historia (o al final del archivo) y NO DEBE reordenar, renombrar ni reformatear código
  ajeno. Los cambios de formato masivos o de reorganización DEBEN acordarse y hacerse en una
  solicitud de integración propia, sin mezclarse con funcionalidad.
- **`tasks.md`**: cada persona marca `[X]` solo en las tareas de su historia, dentro de su rama.
  No se DEBEN reescribir ni renumerar tareas existentes; las tareas nuevas se agregan al final
  de la fase correspondiente con el siguiente número libre.
- **Documentos de especificación**: los cambios a la constitución, `spec.md`, `plan.md` y demás
  documentos de diseño DEBEN ir en su propia solicitud de integración, separados del código.
- **Archivos generados y finales de línea**: NO se DEBEN subir archivos generados (`.venv/`,
  `datos/`, `__pycache__/`). El repositorio DEBE fijar finales de línea LF con
  `.gitattributes`, para que Windows, macOS y Linux no generen diferencias falsas.
- **Resolución de conflictos**: si aparece un conflicto, lo resuelve quien integra su rama,
  conservando los cambios de ambas partes cuando correspondan, y DEBE volver a ejecutar
  `pytest` antes de terminar la integración.

**Justificación**: en un equipo académico los conflictos de fusión consumen tiempo y pueden
borrar trabajo ajeno sin que nadie lo note; ramas cortas, responsables claros y cambios
acotados los hacen raros y fáciles de resolver.

## Gobernanza

- Esta constitución prevalece sobre cualquier otra práctica del proyecto.
- Toda enmienda DEBE documentarse en este archivo, con su justificación y la nueva versión.
- Versionado semántico de la constitución:
  - MAYOR: se elimina o redefine un principio.
  - MENOR: se agrega un principio o sección, o se amplía de forma significativa.
  - PARCHE: aclaraciones de redacción sin cambio de significado.
- Cada revisión de especificaciones, planes y código DEBE verificar el cumplimiento de estos
  principios; cualquier complejidad adicional DEBE justificarse por escrito.

**Version**: 1.1.0 | **Ratified**: 2026-10-26 | **Last Amended**: 2026-10-26
