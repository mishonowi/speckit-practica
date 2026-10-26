"""Modelos de entrada/salida y utilidades de validación."""
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
