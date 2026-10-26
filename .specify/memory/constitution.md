<!--
Informe de Impacto de Sincronización
- Cambio de versión: plantilla (sin versión) → 1.0.0
- Principios definidos (nuevos):
  - I. Simplicidad Primero
  - II. Pruebas Obligatorias (NO NEGOCIABLE)
  - III. Código Legible
  - IV. Validación de Entradas
  - V. Accesible y Responsivo
- Secciones añadidas: Restricciones del Proyecto Académico, Flujo de Desarrollo y Puertas de Calidad
- Secciones eliminadas: ninguna
- Plantillas dependientes: no se modifican (leen la constitución en tiempo de ejecución)
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
  4. funciona en celular y en computadora.

## Gobernanza

- Esta constitución prevalece sobre cualquier otra práctica del proyecto.
- Toda enmienda DEBE documentarse en este archivo, con su justificación y la nueva versión.
- Versionado semántico de la constitución:
  - MAYOR: se elimina o redefine un principio.
  - MENOR: se agrega un principio o sección, o se amplía de forma significativa.
  - PARCHE: aclaraciones de redacción sin cambio de significado.
- Cada revisión de especificaciones, planes y código DEBE verificar el cumplimiento de estos
  principios; cualquier complejidad adicional DEBE justificarse por escrito.

**Version**: 1.0.0 | **Ratified**: 2026-10-26 | **Last Amended**: 2026-10-26
