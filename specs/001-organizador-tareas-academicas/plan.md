# Plan de Implementación: Organizador de Tareas Académicas

**Rama**: `001-organizador-tareas-academicas` | **Fecha**: 2026-10-26 | **Especificación**: [spec.md](spec.md)

**Entrada**: Especificación de la funcionalidad en `/specs/001-organizador-tareas-academicas/spec.md`

## Resumen

Aplicación web local para que estudiantes de la UPB gestionen materias (nombre y color) y tareas (título, descripción opcional, fecha de entrega), con listado ordenado por fecha, indicadores "vencida" y "urgente" (≤ 48 horas exactas), completado de tareas y filtros por materia y estado.

Enfoque técnico: un único proyecto Python con **FastAPI** que expone una API JSON y sirve también el frontend estático (HTML, CSS y JavaScript sin frameworks). Los datos se guardan en **SQLite** mediante el módulo estándar `sqlite3` (sin ORM). El estado de plazo ("vencida", "urgente", "normal") se calcula en el servidor con una función pura, fácil de probar. Las pruebas usan **pytest**.

## Contexto Técnico

**Lenguaje/Versión**: Python 3.12 (el equipo de desarrollo usa 3.14; el código no debe usar nada posterior a 3.12)

**Dependencias principales**: FastAPI (incluye Pydantic para validación), Uvicorn (servidor); para pruebas: pytest y httpx (requerido por el cliente de pruebas de FastAPI)

**Almacenamiento**: SQLite, un único archivo local (`datos/tareas.db`) con módulo estándar `sqlite3`

**Pruebas**: pytest (unitarias de la regla de plazo, y de integración de la API con base de datos temporal)

**Plataforma objetivo**: Se ejecuta en el propio dispositivo del estudiante (Windows/macOS/Linux); la interfaz se usa desde el navegador, en celular y en computadora

**Tipo de proyecto**: Aplicación web de un solo proyecto (backend + frontend estático servido por el mismo proceso)

**Metas de rendimiento**: Cada acción (crear, completar, filtrar) se refleja en pantalla en menos de 1 segundo con hasta 500 tareas

**Restricciones**: Sin inicio de sesión; un usuario por dispositivo; sin Docker, microservicios ni frameworks de frontend; todo texto visible y mensajes en español; fechas en la zona horaria del dispositivo

**Escala/Alcance**: Un usuario, decenas de materias y cientos de tareas como máximo; 1 pantalla principal con formularios en diálogos o secciones

## Verificación de la Constitución

*PUERTA: debe pasar antes de la investigación de la Fase 0. Se vuelve a verificar tras el diseño de la Fase 1.*

| Principio | Cumplimiento | Evidencia |
|-----------|--------------|-----------|
| I. Simplicidad Primero | ✅ Pasa | Un solo proyecto; `sqlite3` estándar sin ORM; frontend sin frameworks ni paso de compilación; sin capas de repositorio. Las dependencias nuevas (FastAPI, Uvicorn, pytest, httpx) las exige el usuario o son estrictamente necesarias (ver [research.md](research.md)). |
| II. Pruebas Obligatorias | ✅ Pasa | pytest con pruebas del caso principal y de borde/error para cada historia de usuario (ver [quickstart.md](quickstart.md)). |
| III. Código Legible | ✅ Pasa | Módulos pequeños con una responsabilidad (`plazo`, `validacion`, `db`, `rutas`); reglas de negocio comentadas en español. |
| IV. Validación de Entradas | ✅ Pasa | Validación en el servidor con Pydantic (tipo, longitud, rango, formato de color y fecha) con mensajes en español; el frontend repite las comprobaciones solo para dar respuesta inmediata. |
| V. Accesible y Responsivo | ✅ Pasa | HTML semántico, etiquetas en todos los campos, uso con teclado, contraste suficiente y diseño adaptable de móvil primero. Los estados "vencida"/"urgente" se indican con texto además de color. |

**Restricciones académicas**: documentos y mensajes en español ✅; ejecutable y explicable en una presentación (un solo comando para arrancar) ✅.

**Resultado de la puerta**: sin violaciones; la tabla de Seguimiento de Complejidad no aplica. La verificación posterior al diseño (Fase 1) también pasa: el diseño no añadió capas ni dependencias.

## Estructura del Proyecto

### Documentación (esta funcionalidad)

```text
specs/001-organizador-tareas-academicas/
├── plan.md              # Este archivo
├── research.md          # Salida de la Fase 0
├── data-model.md        # Salida de la Fase 1
├── quickstart.md        # Salida de la Fase 1
├── contracts/
│   └── api.md           # Contrato de la API REST (Fase 1)
└── tasks.md             # Salida de /speckit-tasks (NO la crea /speckit-plan)
```

### Código fuente (raíz del repositorio)

```text
app/
├── main.py              # Crea la aplicación FastAPI, monta la API y sirve el frontend
├── db.py                # Conexión SQLite y creación de tablas
├── esquemas.py          # Modelos de entrada/salida y validaciones (Pydantic)
├── plazo.py             # Función pura que calcula "vencida" / "urgente" / "normal"
├── rutas_materias.py    # Endpoints de materias
├── rutas_tareas.py      # Endpoints de tareas
└── static/
    ├── index.html       # Pantalla única
    ├── estilos.css
    └── app.js           # Lógica del frontend (fetch, render, filtros)

tests/
├── unit/
│   └── test_plazo.py
└── integration/
    ├── conftest.py      # Cliente de pruebas con base de datos temporal
    ├── test_materias.py
    └── test_tareas.py

datos/                   # Archivo SQLite generado en ejecución (ignorado por git)
requirements.txt
README.md                # En español: cómo instalar, ejecutar y probar
```

**Decisión de estructura**: un solo proyecto (opción simple) porque el backend y el frontend se ejecutan en un único proceso FastAPI; el frontend estático vive en `app/static/` y no necesita compilación. Se omite una capa de "servicios" o "repositorios": las rutas llaman directamente a funciones de `db.py`, suficiente para dos tablas.

## Seguimiento de Complejidad

No hay violaciones de la constitución que justificar.
