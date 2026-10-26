"""Modelos de entrada/salida y utilidades de validación."""
from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator

# Paleta fija de colores de materia (formato #RRGGBB), ver data-model.md.
COLORES_PERMITIDOS = (
    "#E53935",
    "#FB8C00",
    "#FDD835",
    "#43A047",
    "#00897B",
    "#1E88E5",
    "#8E24AA",
    "#6D4C41",
)


def recortar(texto):
    """Quita los espacios al inicio y al final; deja pasar valores que no son texto."""
    return texto.strip() if isinstance(texto, str) else texto


class MateriaEntrada(BaseModel):
    """Datos que el estudiante envía para crear o editar una materia."""

    nombre: str = Field(min_length=1, max_length=50)
    color: str

    @field_validator("nombre", mode="before")
    @classmethod
    def _recortar_nombre(cls, valor):
        # Se recorta antes de medir la longitud: "   " cuenta como vacío.
        return recortar(valor)

    @field_validator("color")
    @classmethod
    def _color_de_la_paleta(cls, valor):
        if valor not in COLORES_PERMITIDOS:
            raise ValueError("Elige uno de los colores disponibles.")
        return valor


class MateriaSalida(BaseModel):
    id: int
    nombre: str
    color: str
    total_tareas: int


def fecha_a_texto_utc(fecha: datetime) -> str:
    """Formato único de almacenamiento: UTC con sufijo Z y precisión de segundos.

    Al tener todas las fechas el mismo formato, ordenarlas como texto en SQLite
    equivale a ordenarlas cronológicamente.
    """
    return fecha.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class TareaEntrada(BaseModel):
    """Datos que el estudiante envía para crear o editar una tarea."""

    materia_id: int
    titulo: str = Field(min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)
    fecha_entrega: datetime

    @field_validator("titulo", mode="before")
    @classmethod
    def _recortar_titulo(cls, valor):
        return recortar(valor)

    @field_validator("descripcion", mode="before")
    @classmethod
    def _descripcion_vacia_es_nula(cls, valor):
        valor = recortar(valor)
        return valor or None

    @field_validator("fecha_entrega", mode="before")
    @classmethod
    def _fecha_como_texto(cls, valor):
        # Pydantic aceptaría también números (segundos desde 1970); el contrato pide ISO 8601.
        if not isinstance(valor, str):
            raise ValueError("La fecha debe tener formato ISO 8601, por ejemplo 2026-11-05T18:00:00-04:00.")
        return valor

    @field_validator("fecha_entrega")
    @classmethod
    def _fecha_con_zona_horaria(cls, valor: datetime):
        # Sin zona horaria no se puede saber a qué momento exacto se refiere (regla de 48 horas).
        if valor.tzinfo is None:
            raise ValueError("La fecha debe incluir la zona horaria.")
        return valor


class TareaSalida(BaseModel):
    id: int
    materia_id: int
    materia_nombre: str
    materia_color: str
    titulo: str
    descripcion: str | None
    fecha_entrega: str
    completada: bool
