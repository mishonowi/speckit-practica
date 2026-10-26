# Modelo de Datos: Organizador de Tareas Académicas

Relación: una **Materia** tiene cero o más **Tareas**; cada Tarea pertenece a exactamente una Materia.

## Materia

| Campo | Tipo | Reglas de validación |
|-------|------|----------------------|
| `id` | entero, generado | Identificador único. |
| `nombre` | texto | Obligatorio; se recortan espacios; no puede quedar vacío; máximo 50 caracteres; único sin distinguir mayúsculas/minúsculas (RF-002). |
| `color` | texto `#RRGGBB` | Obligatorio; debe pertenecer a la paleta fija de 8 colores. |

Campo calculado en las respuestas: `total_tareas` (cantidad de tareas de la materia), usado para el mensaje de confirmación al borrar (RF-003).

**Paleta de colores permitida**: `#E53935`, `#FB8C00`, `#FDD835`, `#43A047`, `#00897B`, `#1E88E5`, `#8E24AA`, `#6D4C41`.

## Tarea

| Campo | Tipo | Reglas de validación |
|-------|------|----------------------|
| `id` | entero, generado | Identificador único. |
| `materia_id` | entero | Obligatorio; debe existir una materia con ese id. Clave foránea con borrado en cascada. |
| `titulo` | texto | Obligatorio; se recortan espacios; no vacío; máximo 100 caracteres. |
| `descripcion` | texto o nulo | Opcional; máximo 500 caracteres; si viene vacía se guarda como nula. |
| `fecha_entrega` | fecha y hora (UTC) | Obligatoria; debe enviarse en ISO 8601 con zona horaria; se permiten fechas pasadas. |
| `completada` | booleano | Por defecto `false` (pendiente). |

Campo calculado en las respuestas: `estado_plazo` ∈ {`vencida`, `urgente`, `normal`, `ninguno`}.

## Estados y transiciones

- **Estado de la tarea**: `pendiente` ⇄ `completada` (RF-011: se puede marcar y desmarcar).
- **Estado de plazo** (solo se calcula para tareas pendientes, con `ahora` = momento actual):

```text
completada                                  → ninguno
fecha_entrega <= ahora                      → vencida
ahora < fecha_entrega <= ahora + 48 horas   → urgente
fecha_entrega >  ahora + 48 horas           → normal
```

El estado de plazo no se almacena: se deriva en cada consulta. Con el paso del tiempo una tarea pasa de `normal` → `urgente` → `vencida` sin intervención del estudiante.

## Esquema de almacenamiento (SQLite)

```text
materia(id PK, nombre TEXT UNIQUE NOT NULL, color TEXT NOT NULL)
tarea(id PK, materia_id FK→materia ON DELETE CASCADE, titulo TEXT NOT NULL,
      descripcion TEXT NULL, fecha_entrega TEXT NOT NULL (ISO 8601 UTC),
      completada INTEGER NOT NULL DEFAULT 0)
índice sobre tarea(fecha_entrega)
```

## Orden del listado

Por `fecha_entrega` ascendente (la más próxima primero); desempate por `id` ascendente.
