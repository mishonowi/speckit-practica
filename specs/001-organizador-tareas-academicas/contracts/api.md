# Contrato de la API: Organizador de Tareas Académicas

API JSON bajo el prefijo `/api`. Sin autenticación (un usuario por dispositivo). Las fechas viajan en ISO 8601; las respuestas usan UTC con sufijo `Z`. Los nombres de campos están en español, como en [data-model.md](../data-model.md).

## Formato de errores

Todos los errores devuelven JSON con mensajes en español:

```json
{ "detalle": "Hay datos inválidos.", "campos": { "nombre": "El nombre no puede estar vacío." } }
```

`campos` solo aparece en errores de validación (422).

| Código | Cuándo |
|--------|--------|
| 404 | La materia o la tarea no existe. |
| 409 | Ya existe una materia con ese nombre. |
| 422 | Datos inválidos (vacíos, muy largos, color fuera de la paleta, fecha sin zona horaria, materia inexistente, filtro desconocido). |

## Materias

| Método y ruta | Descripción | Respuesta exitosa |
|---------------|-------------|-------------------|
| `GET /api/materias` | Lista todas las materias, ordenadas por nombre. | 200 `[Materia]` |
| `POST /api/materias` | Crea una materia. Cuerpo: `{nombre, color}`. | 201 `Materia` |
| `PUT /api/materias/{id}` | Edita nombre y color. Cuerpo: `{nombre, color}`. | 200 `Materia` |
| `DELETE /api/materias/{id}` | Borra la materia **y todas sus tareas** (la confirmación la pide el frontend usando `total_tareas`). | 204 sin cuerpo |

**Materia** (respuesta): `{ "id": 1, "nombre": "Cálculo II", "color": "#1E88E5", "total_tareas": 3 }`

## Tareas

| Método y ruta | Descripción | Respuesta exitosa |
|---------------|-------------|-------------------|
| `GET /api/tareas` | Lista las tareas ordenadas por `fecha_entrega` ascendente. Parámetros opcionales: `materia_id` (entero) y `estado` (`pendiente` \| `completada`; sin `estado` se devuelven todas). Los filtros se combinan con AND. | 200 `[Tarea]` (lista vacía si nada coincide) |
| `POST /api/tareas` | Crea una tarea. Cuerpo: `{materia_id, titulo, descripcion?, fecha_entrega}`. | 201 `Tarea` |
| `PUT /api/tareas/{id}` | Edita `materia_id`, `titulo`, `descripcion` y `fecha_entrega`. | 200 `Tarea` |
| `PATCH /api/tareas/{id}/completada` | Marca o desmarca. Cuerpo: `{ "completada": true }`. | 200 `Tarea` |
| `DELETE /api/tareas/{id}` | Borra la tarea. | 204 sin cuerpo |

**Tarea** (respuesta):

```json
{
  "id": 7,
  "materia_id": 1,
  "materia_nombre": "Cálculo II",
  "materia_color": "#1E88E5",
  "titulo": "Taller 3",
  "descripcion": null,
  "fecha_entrega": "2026-10-28T22:00:00Z",
  "completada": false,
  "estado_plazo": "urgente"
}
```

`estado_plazo` ∈ `vencida` | `urgente` | `normal` | `ninguno`, calculado por el servidor según las reglas de [data-model.md](../data-model.md) en el momento de la consulta.

## Frontend

`GET /` sirve la pantalla única (`app/static/index.html`); `GET /estilos.css` y `GET /app.js` sirven sus recursos. No hay otras rutas de interfaz.

## Correspondencia con requisitos

| Requisito | Endpoint(s) |
|-----------|-------------|
| RF-001, RF-002, RF-003 | `/api/materias` (POST, PUT, DELETE) |
| RF-004, RF-005, RF-006 | `/api/tareas` (POST, PUT, DELETE) |
| RF-007 a RF-010 | `GET /api/tareas` (orden y `estado_plazo`) |
| RF-011 | `PATCH /api/tareas/{id}/completada` |
| RF-012 | `GET /api/tareas?materia_id=&estado=` |
