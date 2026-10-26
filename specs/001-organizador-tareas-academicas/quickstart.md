# Guía de Validación Rápida: Organizador de Tareas Académicas

Guion para comprobar de extremo a extremo que la funcionalidad cumple la especificación. Detalles de la API en [contracts/api.md](contracts/api.md) y de los datos en [data-model.md](data-model.md).

## Requisitos previos

- Python 3.12 o superior instalado.
- Terminal en la raíz del repositorio.

## Preparación

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecutar las pruebas automatizadas

```powershell
pytest
```

**Resultado esperado**: todas las pruebas pasan, incluyendo las de la regla de plazo (límites de 48 horas y hora exacta) y las de la API (validación, duplicados, borrado en cascada, filtros).

## Ejecutar la aplicación

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Abrir `http://127.0.0.1:8000` en el navegador. Para probar en celular, usar las herramientas de desarrollo del navegador (modo dispositivo móvil).

## Escenarios de validación manual

| # | Historia | Pasos | Resultado esperado |
|---|----------|-------|--------------------|
| 1 | HU1 | Crear la materia "Cálculo II" con un color. | Aparece en la lista con su color. |
| 2 | HU1 | Intentar crear una materia sin nombre; luego otra "cálculo ii". | Mensaje de error en español en ambos casos; no se crean. |
| 3 | HU2 | Crear tres tareas con fechas distintas (una en el pasado, una en 24 horas, una en 10 días). | Listado ordenado de la fecha más próxima a la más lejana, cada tarea con el color de su materia. |
| 4 | HU2 | Intentar crear una tarea sin título o sin fecha. | Mensaje de error indicando el campo faltante. |
| 5 | HU3 | Observar las tres tareas anteriores. | La del pasado aparece "vencida", la de 24 horas "urgente", la de 10 días sin indicador. |
| 6 | HU4 | Marcar como completada la tarea vencida. | Se distingue como completada y deja de verse "vencida"; al desmarcarla vuelve a "vencida". |
| 7 | HU5 | Filtrar por materia, por estado "Completadas" y por ambos; luego un filtro sin resultados. | Solo se ven las tareas que cumplen; el filtro sin resultados muestra un mensaje de lista vacía. |
| 8 | RF-003 | Borrar una materia con 2 tareas; primero cancelar, luego confirmar. | La confirmación indica "2 tareas"; al cancelar no cambia nada; al confirmar desaparecen la materia y sus tareas. |
| 9 | RF-005 | Escribir un título de 101 caracteres. | Se rechaza con un mensaje que indica el límite de 100. |
| 10 | RF-013 | Cerrar el servidor, volver a iniciarlo y recargar la página. | Las materias y tareas siguen ahí. |
| 11 | RF-016 | Recorrer los formularios solo con teclado y con ancho de pantalla de celular. | Todo es accesible y no hay desplazamiento horizontal. |

## Criterio de aceptación de esta guía

La funcionalidad se considera validada cuando `pytest` pasa por completo y los 11 escenarios manuales producen el resultado esperado.
