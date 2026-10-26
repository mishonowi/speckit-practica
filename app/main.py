"""Aplicación FastAPI: API JSON bajo /api y frontend estático en /."""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException

from app import db
from app.rutas_materias import router as router_materias

CARPETA_ESTATICA = Path(__file__).parent / "static"


@asynccontextmanager
async def ciclo_de_vida(_app: FastAPI):
    db.crear_tablas()
    yield


app = FastAPI(title="Organizador de Tareas Académicas", lifespan=ciclo_de_vida)


def _mensaje_de_error(error: dict) -> str:
    """Traduce un error de validación de Pydantic a un mensaje en español."""
    tipo = error.get("type", "")
    contexto = error.get("ctx", {})
    if tipo == "missing":
        return "Este campo es obligatorio."
    if tipo == "string_too_long":
        return f"No puede superar {contexto.get('max_length')} caracteres."
    if tipo == "string_too_short":
        return "No puede estar vacío."
    if tipo == "value_error":
        # Los validadores propios lanzan ValueError con el mensaje ya en español.
        return str(contexto.get("error", "Valor inválido.")).removeprefix("Value error, ")
    return "Valor inválido."


@app.exception_handler(RequestValidationError)
async def errores_de_validacion(_peticion: Request, excepcion: RequestValidationError):
    campos = {}
    for error in excepcion.errors():
        # loc = ("body", "campo") o ("query", "campo"); el nombre es el último elemento.
        nombre = str(error["loc"][-1])
        campos.setdefault(nombre, _mensaje_de_error(error))
    return JSONResponse(
        status_code=422,
        content={"detalle": "Hay datos inválidos.", "campos": campos},
    )


@app.exception_handler(HTTPException)
async def errores_http(_peticion: Request, excepcion: HTTPException):
    return JSONResponse(
        status_code=excepcion.status_code,
        content={"detalle": excepcion.detail},
    )


# Los routers de /api se registran antes del montaje estático.
app.include_router(router_materias)

# Debe ir al final: captura todo lo que no sea /api.
app.mount("/", StaticFiles(directory=CARPETA_ESTATICA, html=True), name="frontend")
