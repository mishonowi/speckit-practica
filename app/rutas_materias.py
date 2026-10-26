"""Endpoints de materias bajo /api/materias."""
from fastapi import APIRouter, HTTPException, Response

from app import db
from app.esquemas import MateriaEntrada, MateriaSalida

router = APIRouter(prefix="/api/materias", tags=["materias"])

MENSAJE_NO_EXISTE = "La materia no existe."
MENSAJE_DUPLICADA = "Ya existe una materia con ese nombre."


def _materia_o_404(materia_id: int) -> dict:
    materia = db.obtener_materia(materia_id)
    if materia is None:
        raise HTTPException(status_code=404, detail=MENSAJE_NO_EXISTE)
    return materia


@router.get("", response_model=list[MateriaSalida])
def listar():
    return db.listar_materias()


@router.post("", response_model=MateriaSalida, status_code=201)
def crear(datos: MateriaEntrada):
    if db.existe_nombre_de_materia(datos.nombre):
        raise HTTPException(status_code=409, detail=MENSAJE_DUPLICADA)
    materia_id = db.crear_materia(datos.nombre, datos.color)
    return db.obtener_materia(materia_id)


@router.put("/{materia_id}", response_model=MateriaSalida)
def editar(materia_id: int, datos: MateriaEntrada):
    _materia_o_404(materia_id)
    if db.existe_nombre_de_materia(datos.nombre, excepto_id=materia_id):
        raise HTTPException(status_code=409, detail=MENSAJE_DUPLICADA)
    db.actualizar_materia(materia_id, datos.nombre, datos.color)
    return db.obtener_materia(materia_id)


@router.delete("/{materia_id}", status_code=204)
def borrar(materia_id: int):
    _materia_o_404(materia_id)
    db.borrar_materia(materia_id)
    return Response(status_code=204)
