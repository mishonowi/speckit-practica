---

description: "Lista de tareas para implementar el Organizador de Tareas Académicas"
---

# Tareas: Organizador de Tareas Académicas

**Entrada**: Documentos de diseño en `/specs/001-organizador-tareas-academicas/`

**Prerrequisitos**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/api.md](contracts/api.md), [quickstart.md](quickstart.md)

**Pruebas**: OBLIGATORIAS según la constitución (principio II): cada historia incluye pruebas del caso principal y de al menos un caso de error o borde. Escribirlas primero y comprobar que fallan antes de implementar.

**Organización**: Las tareas se agrupan por historia de usuario para poder implementar y probar cada una de forma independiente.

## Formato: `[ID] [P?] [Historia] Descripción`

- **[P]**: Se puede ejecutar en paralelo (archivos distintos, sin dependencias pendientes)
- **[HUx]**: Historia de usuario a la que pertenece la tarea
- Todas las descripciones incluyen la ruta exacta del archivo

## Convenciones de rutas

Proyecto único (ver [plan.md](plan.md)): código en `app/`, pruebas en `tests/` y frontend estático en `app/static/`, todo en la raíz del repositorio.

---

## Fase 1: Preparación (infraestructura compartida)

**Propósito**: Inicializar el proyecto y su estructura básica

- [X] T001 Crear la estructura de carpetas del plan: `app/`, `app/static/`, `tests/unit/`, `tests/integration/`, y archivos vacíos `app/__init__.py`, `tests/__init__.py`
- [X] T002 Crear `requirements.txt` con `fastapi`, `uvicorn`, `pytest` y `httpx`, y un `.gitignore` en la raíz que excluya `.venv/`, `__pycache__/`, `.pytest_cache/` y `datos/`
- [X] T003 [P] Crear `README.md` en español con requisitos (Python 3.12+), instalación, comando de ejecución (`uvicorn app.main:app --host 127.0.0.1 --port 8000`) y comando de pruebas (`pytest`)
- [X] T004 [P] Crear `pytest.ini` en la raíz con `testpaths = tests`

---

## Fase 2: Fundamentos (prerrequisitos bloqueantes)

**Propósito**: Infraestructura que DEBE estar completa antes de cualquier historia de usuario

**⚠️ CRÍTICO**: Ninguna historia puede empezar hasta terminar esta fase

- [X] T005 Implementar `app/db.py`: ruta del archivo (`datos/tareas.db`, configurable por variable de entorno `TAREAS_DB` para las pruebas), función de conexión con `PRAGMA foreign_keys = ON` y `sqlite3.Row`, y creación de tablas `materia(id PK, nombre TEXT UNIQUE NOT NULL, color TEXT NOT NULL)` y `tarea(id PK, materia_id FK→materia ON DELETE CASCADE, titulo TEXT NOT NULL, descripcion TEXT NULL, fecha_entrega TEXT NOT NULL (ISO 8601 UTC), completada INTEGER NOT NULL DEFAULT 0)` con índice sobre `tarea(fecha_entrega)`; crear la carpeta `datos/` si no existe
- [X] T006 [P] Implementar en `app/esquemas.py` la paleta fija `COLORES_PERMITIDOS` (`#E53935`, `#FB8C00`, `#FDD835`, `#43A047`, `#00897B`, `#1E88E5`, `#8E24AA`, `#6D4C41`) y una utilidad para recortar espacios en textos
- [X] T007 Implementar en `app/main.py` la aplicación FastAPI: evento de arranque que llama a la creación de tablas, manejador de errores de validación que devuelva `{"detalle": "Hay datos inválidos.", "campos": {campo: mensaje}}` con mensajes en español y estado 422, formato de error `{"detalle": "..."}` para 404 y 409, y montaje de `app/static/` en `/` con `StaticFiles(html=True)` al final (después de los routers bajo `/api`)
- [X] T008 [P] Crear `tests/integration/conftest.py` con un fixture `cliente` que use una base SQLite temporal por prueba (variable `TAREAS_DB` apuntando a `tmp_path`) y devuelva un `TestClient` de FastAPI
- [X] T009 [P] Crear la base del frontend: `app/static/index.html` (HTML semántico en español, `lang="es"`, meta viewport, enlaces a `estilos.css` y `app.js`, regiones para materias, formulario de tarea y listado), `app/static/estilos.css` (diseño adaptable de móvil primero, variables de color con contraste suficiente, estilo de foco visible) y `app/static/app.js` con una función `api(metodo, ruta, cuerpo)` que use `fetch` y lance un error con el mensaje en español devuelto por la API

**Punto de control**: Fundamentos listos; las historias pueden comenzar

---

## Fase 3: Historia de Usuario 1 - Registrar materias (Prioridad: P1) 🎯 MVP

**Meta**: El estudiante crea, edita, ve y borra materias con nombre y color.

**Prueba independiente**: Crear una materia con nombre y color y verla en la lista; intentar crear una sin nombre o repetida y ver el mensaje de error (escenarios 1 y 2 de [quickstart.md](quickstart.md)).

### Pruebas de la Historia 1 (escribir primero; deben fallar)

- [X] T010 [P] [HU1] Prueba de integración en `tests/integration/test_materias.py`: crear materia válida devuelve 201 con `id`, `nombre`, `color` y `total_tareas` igual a 0; `GET /api/materias` la lista ordenada por nombre
- [X] T011 [P] [HU1] Pruebas de error en `tests/integration/test_materias.py`: nombre vacío o solo espacios → 422; nombre de 51 caracteres → 422; color fuera de la paleta → 422; nombre repetido ("Física I" y "física i", y "Álgebra" y "álgebra") → 409 con mensaje en español
- [X] T012 [P] [HU1] Pruebas en `tests/integration/test_materias.py` de edición (`PUT`, incluido el caso de renombrar a un nombre ya existente → 409 y el de guardar la misma materia con su propio nombre → 200), borrado (`DELETE` → 204) y materia inexistente → 404

### Implementación de la Historia 1

- [X] T013 [HU1] En `app/esquemas.py`, crear los modelos `MateriaEntrada` (`nombre`: obligatorio, se recortan espacios, no vacío, máximo 50 caracteres; `color`: obligatorio, debe pertenecer a `COLORES_PERMITIDOS`) y `MateriaSalida` (`id`, `nombre`, `color`, `total_tareas`), con mensajes de error en español
- [X] T014 [HU1] En `app/db.py`, añadir funciones de materias con SQL parametrizado: listar con `total_tareas` (ordenadas por nombre), obtener por id, crear, actualizar, borrar y buscar duplicado comparando con `casefold()` en Python (excluyendo el propio id al editar), con restricción `UNIQUE` como respaldo
- [X] T015 [HU1] Crear `app/rutas_materias.py` con el router `/api/materias` (`GET`, `POST`, `PUT /{id}`, `DELETE /{id}`) según [contracts/api.md](contracts/api.md), devolviendo 409 «Ya existe una materia con ese nombre.» y 404 «La materia no existe.»; registrar el router en `app/main.py`
- [X] T016 [HU1] En `app/static/index.html` y `app/static/app.js`, implementar la sección de materias: formulario con etiqueta, selector de los 8 colores de la paleta (accesible con teclado y con nombre descriptivo del color), lista de materias con su color, botones editar y borrar, y mensajes de error junto al campo; incluir el contador o texto de ayuda con el límite de 50 caracteres
- [X] T017 [HU1] En `app/static/app.js`, implementar el borrado de materia con confirmación que indique cuántas tareas se perderán según `total_tareas` («Se borrarán N tareas.»); si se cancela, no se llama a la API

**Punto de control**: La Historia 1 funciona sola y sus pruebas pasan

---

## Fase 4: Historia de Usuario 2 - Crear tareas y verlas ordenadas por fecha (Prioridad: P1)

**Meta**: El estudiante crea, edita y borra tareas asociadas a una materia y las ve ordenadas por fecha de entrega.

**Prueba independiente**: Con una materia creada, crear tareas con distintas fechas y comprobar el orden y el color de materia (escenarios 3 y 4 de [quickstart.md](quickstart.md)).

### Pruebas de la Historia 2 (escribir primero; deben fallar)

- [X] T018 [P] [HU2] Prueba de integración en `tests/integration/test_tareas.py`: crear tarea válida (con y sin descripción) devuelve 201 con `materia_nombre` y `materia_color`; la descripción vacía se guarda como `null`
- [X] T019 [P] [HU2] Prueba en `tests/integration/test_tareas.py`: `GET /api/tareas` devuelve las tareas ordenadas por `fecha_entrega` ascendente, con desempate por `id` ascendente
- [X] T020 [P] [HU2] Pruebas de error en `tests/integration/test_tareas.py`: título vacío/solo espacios → 422; título de 101 caracteres → 422; descripción de 501 caracteres → 422; fecha de entrega sin zona horaria → 422; materia inexistente → 422; falta de título, materia o fecha → 422 con el campo indicado; fecha pasada → 201 (se permite)
- [X] T021 [P] [HU2] Pruebas en `tests/integration/test_tareas.py` de edición (`PUT`), borrado (`DELETE` → 204), tarea inexistente → 404, y borrado en cascada: al borrar una materia con 2 tareas se eliminan también sus tareas

### Implementación de la Historia 2

- [X] T022 [HU2] En `app/esquemas.py`, crear `TareaEntrada` (`materia_id`: obligatorio; `titulo`: obligatorio, se recortan espacios, no vacío, máximo 100 caracteres; `descripcion`: opcional, máximo 500 caracteres, vacía → nula; `fecha_entrega`: obligatoria, ISO 8601 con zona horaria, se convierte a UTC) y `TareaSalida` (`id`, `materia_id`, `materia_nombre`, `materia_color`, `titulo`, `descripcion`, `fecha_entrega` en UTC con sufijo `Z`, `completada`), con mensajes de error en español
- [X] T023 [HU2] En `app/db.py`, añadir funciones de tareas con SQL parametrizado: listar con JOIN a materia ordenando por `fecha_entrega` ASC y `id` ASC, obtener por id, crear (verificando que la materia exista), actualizar y borrar
- [X] T024 [HU2] Crear `app/rutas_tareas.py` con el router `/api/tareas` (`GET`, `POST`, `PUT /{id}`, `DELETE /{id}`) según [contracts/api.md](contracts/api.md); registrar el router en `app/main.py`
- [X] T025 [HU2] En `app/static/index.html` y `app/static/app.js`, implementar el formulario de tarea (materia, título, descripción opcional, fecha y hora de entrega; la fecha se envía con el desplazamiento horario del dispositivo; si solo se elige el día, usar las 23:59 locales) con etiquetas accesibles, contadores de 100 y 500 caracteres, conservación de lo escrito ante errores y mensaje que guía a registrar una materia si no existe ninguna
- [X] T026 [HU2] En `app/static/app.js` y `app/static/estilos.css`, implementar el listado de tareas: título, materia con su color, fecha y hora en hora local y formato en español; estado vacío «Aún no tienes tareas…»; botones editar y borrar tarea (con confirmación al borrar); y actualización inmediata del listado tras crear, editar o borrar
- [X] T027 [HU2] En `app/static/app.js`, mostrar un mensaje claro cuando la API no responda o falle el guardado, sin perder los datos del formulario

**Punto de control**: Las Historias 1 y 2 funcionan juntas (MVP completo)

---

## Fase 5: Historia de Usuario 3 - Identificar tareas vencidas y urgentes (Prioridad: P2)

**Meta**: El listado destaca las tareas vencidas y marca como urgentes las que vencen en 48 horas o menos.

**Prueba independiente**: Crear tareas con fecha pasada, en 24 horas y en 10 días y comprobar su indicador (escenario 5 de [quickstart.md](quickstart.md)).

### Pruebas de la Historia 3 (escribir primero; deben fallar)

- [ ] T028 [P] [HU3] Pruebas unitarias en `tests/unit/test_plazo.py` de `calcular_estado_plazo(fecha_entrega, completada, ahora)`: fecha pasada → `vencida`; fecha igual a `ahora` → `vencida`; 47 h → `urgente`; exactamente 48 h → `urgente`; 48 h y 1 segundo → `normal`; completada (con fecha pasada o próxima) → `ninguno`
- [ ] T029 [P] [HU3] Prueba de integración en `tests/integration/test_tareas.py`: `GET /api/tareas` incluye `estado_plazo` correcto para tareas vencida, urgente y normal creadas con fechas relativas al momento actual

### Implementación de la Historia 3

- [ ] T030 [HU3] Crear `app/plazo.py` con la función pura `calcular_estado_plazo(fecha_entrega, completada, ahora)` según la regla de [data-model.md](data-model.md): completada → `ninguno`; `fecha_entrega <= ahora` → `vencida`; `fecha_entrega - ahora <= 48 horas` → `urgente`; en otro caso → `normal`; con comentario en español que explique que el cálculo es por horas exactas
- [ ] T031 [HU3] Añadir `estado_plazo` a `TareaSalida` en `app/esquemas.py` y calcularlo con `datetime.now(timezone.utc)` en `app/rutas_tareas.py` para cada tarea devuelta
- [ ] T032 [HU3] En `app/static/app.js` y `app/static/estilos.css`, mostrar los indicadores «Vencida» y «Urgente» con texto e ícono además del color (accesibilidad), y volver a pedir el listado cada 60 segundos y al recuperar el foco de la pestaña para que las tareas cambien de estado con la aplicación abierta

**Punto de control**: Las Historias 1 a 3 funcionan de forma independiente

---

## Fase 6: Historia de Usuario 4 - Marcar tareas como completadas (Prioridad: P2)

**Meta**: El estudiante marca y desmarca tareas como completadas.

**Prueba independiente**: Marcar una tarea, ver el cambio y comprobar que se conserva al recargar (escenario 6 de [quickstart.md](quickstart.md)).

### Pruebas de la Historia 4 (escribir primero; deben fallar)

- [ ] T033 [P] [HU4] Pruebas de integración en `tests/integration/test_tareas.py`: `PATCH /api/tareas/{id}/completada` con `{"completada": true}` marca la tarea y con `false` la revierte; el cambio persiste en una nueva consulta
- [ ] T034 [P] [HU4] Pruebas de error en `tests/integration/test_tareas.py`: tarea inexistente → 404; cuerpo sin `completada` o con un valor no booleano → 422; una tarea vencida marcada como completada pasa a `estado_plazo` `ninguno` y al desmarcarla vuelve a `vencida`

### Implementación de la Historia 4

- [ ] T035 [HU4] En `app/db.py`, añadir la función que actualiza `completada` de una tarea y, en `app/esquemas.py`, el modelo de entrada `{completada: bool}`
- [ ] T036 [HU4] En `app/rutas_tareas.py`, añadir `PATCH /api/tareas/{id}/completada` según [contracts/api.md](contracts/api.md), devolviendo la tarea con su `estado_plazo` recalculado
- [ ] T037 [HU4] En `app/static/app.js` y `app/static/estilos.css`, añadir a cada tarea una casilla accesible «Marcar como completada» (operable con teclado y con etiqueta descriptiva) y el estilo visual de tarea completada (tachado y texto «Completada», sin depender solo del color)

**Punto de control**: Las Historias 1 a 4 funcionan de forma independiente

---

## Fase 7: Historia de Usuario 5 - Filtrar tareas por materia o estado (Prioridad: P3)

**Meta**: El estudiante filtra el listado por materia y/o por estado.

**Prueba independiente**: Aplicar cada filtro y su combinación y comprobar los resultados y el mensaje de lista vacía (escenario 7 de [quickstart.md](quickstart.md)).

### Pruebas de la Historia 5 (escribir primero; deben fallar)

- [ ] T038 [P] [HU5] Pruebas de integración en `tests/integration/test_tareas.py`: `GET /api/tareas?materia_id=` devuelve solo las tareas de esa materia; `?estado=pendiente` y `?estado=completada` filtran por estado; ambos filtros combinados aplican AND; el orden por fecha se mantiene
- [ ] T039 [P] [HU5] Pruebas de borde y error en `tests/integration/test_tareas.py`: un filtro sin coincidencias devuelve 200 con lista vacía; `estado` desconocido (por ejemplo `?estado=otro`) → 422 con mensaje en español; `materia_id` no numérico → 422

### Implementación de la Historia 5

- [ ] T040 [HU5] En `app/db.py` y `app/rutas_tareas.py`, añadir los parámetros opcionales `materia_id` (entero) y `estado` (`pendiente` | `completada`) a `GET /api/tareas`, con consulta parametrizada y validación del valor de `estado`
- [ ] T041 [HU5] En `app/static/index.html` y `app/static/app.js`, añadir los controles de filtro por materia (con la opción «Todas») y por estado (Todas, Pendientes, Completadas), con etiquetas accesibles, estado inicial «Todas / Todas», que se combinen y se conserven al recargar el listado
- [ ] T042 [HU5] En `app/static/app.js`, mostrar el mensaje «No hay tareas que coincidan con el filtro.» cuando el filtro no devuelva resultados (distinto del estado vacío sin tareas) y reiniciar el filtro por materia si esa materia se borra

**Punto de control**: Las cinco historias funcionan de forma independiente

---

## Fase 8: Pulido y aspectos transversales

**Propósito**: Mejoras que afectan a varias historias

- [ ] T043 [P] Revisar accesibilidad y diseño adaptable en `app/static/index.html` y `app/static/estilos.css`: orden de foco, contraste suficiente en los 8 colores de materia (elegir texto blanco o negro según el color), sin desplazamiento horizontal en celular, etiquetas de todos los controles (escenario 11 de [quickstart.md](quickstart.md))
- [ ] T044 [P] Revisar que todos los textos visibles y mensajes de error de `app/` y `app/static/` estén en español y que las reglas de negocio no obvias tengan comentarios en español
- [ ] T045 Ejecutar `pytest` completo y corregir fallos; confirmar que cada historia tiene pruebas del caso principal y de un caso de error o borde
- [ ] T046 Recorrer los 11 escenarios manuales de [quickstart.md](quickstart.md) con la aplicación en ejecución (incluida la persistencia al reiniciar el servidor) y anotar cualquier desviación
- [ ] T047 [P] Completar `README.md` con una descripción breve de la aplicación y de la estructura de carpetas

---

## Dependencias y orden de ejecución

### Dependencias entre fases

- **Preparación (Fase 1)**: sin dependencias; puede empezar de inmediato.
- **Fundamentos (Fase 2)**: depende de la Fase 1; BLOQUEA todas las historias.
- **Historias (Fases 3 a 7)**: dependen de la Fase 2.
- **Pulido (Fase 8)**: depende de las historias que se vayan a entregar.

### Dependencias entre historias

- **HU1 (P1)**: puede empezar tras la Fase 2; no depende de otras historias.
- **HU2 (P1)**: necesita materias (usa `app/db.py` y `app/rutas_materias.py` de HU1) para crear tareas; en las pruebas puede crear la materia mediante la API.
- **HU3 (P2)**: depende de HU2 (añade `estado_plazo` a las tareas listadas).
- **HU4 (P2)**: depende de HU2; se integra con HU3 (una tarea completada pasa a `ninguno`).
- **HU5 (P3)**: depende de HU2; es independiente de HU3 y HU4.

### Dentro de cada historia

- Escribir las pruebas primero y comprobar que fallan.
- Orden: esquemas → funciones de base de datos → rutas → frontend.
- Terminar la historia antes de pasar a la siguiente prioridad.

### Oportunidades de paralelismo

- Fase 1: T003 y T004 en paralelo.
- Fase 2: T006, T008 y T009 en paralelo tras T005 (T007 depende de T005).
- Dentro de cada historia: todas las pruebas marcadas [P] pueden escribirse a la vez (archivos o secciones distintas).
- Tras HU2, HU3, HU4 y HU5 pueden avanzar en paralelo en lo que no comparta archivos (`app/rutas_tareas.py`, `app/static/app.js`), coordinando los cambios.

### Ejemplo de paralelismo: Historia 1

```text
Tarea: "Prueba de creación y listado de materias en tests/integration/test_materias.py"   (T010)
Tarea: "Pruebas de error de materias en tests/integration/test_materias.py"               (T011)
Tarea: "Pruebas de edición y borrado de materias en tests/integration/test_materias.py"   (T012)
```

---

## Estrategia de implementación

### Primero el MVP (HU1 + HU2)

1. Completar Preparación y Fundamentos.
2. Completar HU1 (materias) y HU2 (tareas con listado ordenado).
3. **DETENERSE Y VALIDAR**: pasar `pytest` y los escenarios 1 a 4 de [quickstart.md](quickstart.md).
4. Mostrar o entregar el MVP.

### Entrega incremental

1. Preparación + Fundamentos → base lista.
2. HU1 y HU2 → MVP (organizador básico).
3. HU3 → prioridad visual (vencidas y urgentes).
4. HU4 → control de avance.
5. HU5 → filtros.
6. Cada historia añade valor sin romper las anteriores.

### Resumen

- **Total de tareas**: 47 (HU1: 8, HU2: 10, HU3: 5, HU4: 5, HU5: 5; Preparación: 4, Fundamentos: 5, Pulido: 5).

## Notas

- [P] = archivos distintos, sin dependencias pendientes.
- La etiqueta [HUx] enlaza la tarea con su historia para trazabilidad.
- Cada historia debe poder completarse y probarse por separado.
- Verificar que las pruebas fallan antes de implementar.
- Hacer commit tras cada tarea o grupo lógico.
- Evitar: tareas vagas, conflictos en el mismo archivo, dependencias entre historias que rompan su independencia.
