"""Conexión a SQLite y creación de las tablas de la aplicación."""
import os
import sqlite3
import unicodedata
from pathlib import Path

RUTA_POR_DEFECTO = "datos/tareas.db"

ESQUEMA = """
CREATE TABLE IF NOT EXISTS materia (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    color  TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS tarea (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    materia_id    INTEGER NOT NULL REFERENCES materia(id) ON DELETE CASCADE,
    titulo        TEXT NOT NULL,
    descripcion   TEXT,
    fecha_entrega TEXT NOT NULL,
    completada    INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_tarea_fecha_entrega ON tarea(fecha_entrega);
"""


def ruta_base_de_datos() -> str:
    # Se lee en cada llamada para que las pruebas puedan usar una base temporal.
    return os.environ.get("TAREAS_DB", RUTA_POR_DEFECTO)


def conectar() -> sqlite3.Connection:
    conexion = sqlite3.connect(ruta_base_de_datos())
    conexion.row_factory = sqlite3.Row
    # SQLite no aplica las claves foráneas (ni el borrado en cascada) sin esto.
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_tablas() -> None:
    ruta = ruta_base_de_datos()
    if ruta != ":memory:":
        Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    with conectar() as conexion:
        conexion.executescript(ESQUEMA)


# --- Materias ---------------------------------------------------------------

_SELECT_MATERIA = """
    SELECT m.id, m.nombre, m.color, COUNT(t.id) AS total_tareas
    FROM materia m LEFT JOIN tarea t ON t.materia_id = m.id
"""


def _clave_de_orden(texto: str) -> str:
    """Minúsculas y sin tildes, para ordenar alfabéticamente en español."""
    sin_tildes = unicodedata.normalize("NFD", texto.casefold())
    return "".join(c for c in sin_tildes if not unicodedata.combining(c))


def listar_materias() -> list[dict]:
    with conectar() as conexion:
        filas = conexion.execute(_SELECT_MATERIA + " GROUP BY m.id").fetchall()
    # Se ordena en Python para que "Álgebra" quede junto a la A y no después de la Z.
    return sorted((dict(fila) for fila in filas), key=lambda m: _clave_de_orden(m["nombre"]))


def obtener_materia(materia_id: int) -> dict | None:
    with conectar() as conexion:
        fila = conexion.execute(
            _SELECT_MATERIA + " WHERE m.id = ? GROUP BY m.id", (materia_id,)
        ).fetchone()
    return dict(fila) if fila else None


def existe_nombre_de_materia(nombre: str, excepto_id: int | None = None) -> bool:
    """Compara con casefold() porque NOCASE de SQLite no iguala letras acentuadas."""
    clave = nombre.casefold()
    with conectar() as conexion:
        filas = conexion.execute("SELECT id, nombre FROM materia").fetchall()
    return any(f["id"] != excepto_id and f["nombre"].casefold() == clave for f in filas)


def crear_materia(nombre: str, color: str) -> int:
    with conectar() as conexion:
        cursor = conexion.execute(
            "INSERT INTO materia (nombre, color) VALUES (?, ?)", (nombre, color)
        )
        return cursor.lastrowid


def actualizar_materia(materia_id: int, nombre: str, color: str) -> None:
    with conectar() as conexion:
        conexion.execute(
            "UPDATE materia SET nombre = ?, color = ? WHERE id = ?",
            (nombre, color, materia_id),
        )


def borrar_materia(materia_id: int) -> None:
    # Las tareas de la materia se eliminan por ON DELETE CASCADE.
    with conectar() as conexion:
        conexion.execute("DELETE FROM materia WHERE id = ?", (materia_id,))
