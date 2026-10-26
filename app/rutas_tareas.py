"""Endpoints de tareas bajo /api/tareas."""
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Response
from fastapi.exceptions import RequestValidationError

from app import db
from app.esquemas import TareaEntrada, TareaSalida, fecha_a_texto_utc
from app.plazo import calcular_estado_plazo

router = APIRouter(prefix="/api/tareas", tags=["tareas"])

MENSAJE_NO_EXISTE = "La tarea no existe."
MENSAJE_MATERIA_NO_EXISTE = "La materia no existe."


def _tarea_o_404(tarea_id: int) -> dict:
    tarea = db.obtener_tarea(tarea_id)
    if tarea is None:
        raise HTTPException(status_code=404, detail=MENSAJE_NO_EXISTE)
    return tarea


def _exigir_materia(materia_id: int) -> None:
    """Una materia inexistente es un dato inválido del formulario (422), no un 404."""
    if db.obtener_materia(materia_id) is None:
        # Mismo formato que los errores de Pydantic, para que el manejador de main.py
        # lo devuelva como {"campos": {"materia_id": "..."}}.
        raise RequestValidationError(
            [
                {
                    "type": "value_error",
                    "loc": ("body", "materia_id"),
                    "msg": MENSAJE_MATERIA_NO_EXISTE,
                    "ctx": {"error": MENSAJE_MATERIA_NO_EXISTE},
                }
            ]
        )


def _con_estado_plazo(tarea: dict, ahora: datetime | None = None) -> dict:
    """Añade estado_plazo a una tarea leída de la base, según el momento actual."""
    ahora = ahora or datetime.now(timezone.utc)
    # fecha_entrega se guarda como "AAAA-MM-DDTHH:MM:SSZ"; fromisoformat entiende la Z.
    fecha_entrega = datetime.fromisoformat(tarea["fecha_entrega"])
    return {**tarea, "estado_plazo": calcular_estado_plazo(fecha_entrega, tarea["completada"], ahora)}


@router.get("", response_model=list[TareaSalida])
def listar():
    # Un único "ahora" para todo el listado, así todas las tareas se comparan con el mismo instante.
    ahora = datetime.now(timezone.utc)
    return [_con_estado_plazo(tarea, ahora) for tarea in db.listar_tareas()]


@router.post("", response_model=TareaSalida, status_code=201)
def crear(datos: TareaEntrada):
    _exigir_materia(datos.materia_id)
    tarea_id = db.crear_tarea(
        datos.materia_id, datos.titulo, datos.descripcion, fecha_a_texto_utc(datos.fecha_entrega)
    )
    return _con_estado_plazo(db.obtener_tarea(tarea_id))


@router.put("/{tarea_id}", response_model=TareaSalida)
def editar(tarea_id: int, datos: TareaEntrada):
    _tarea_o_404(tarea_id)
    _exigir_materia(datos.materia_id)
    db.actualizar_tarea(
        tarea_id,
        datos.materia_id,
        datos.titulo,
        datos.descripcion,
        fecha_a_texto_utc(datos.fecha_entrega),
    )
    return _con_estado_plazo(db.obtener_tarea(tarea_id))


@router.delete("/{tarea_id}", status_code=204)
def borrar(tarea_id: int):
    _tarea_o_404(tarea_id)
    db.borrar_tarea(tarea_id)
    return Response(status_code=204)
