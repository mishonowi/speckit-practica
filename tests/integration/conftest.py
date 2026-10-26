import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def cliente(tmp_path, monkeypatch):
    """Cliente de pruebas con una base SQLite temporal distinta en cada prueba."""
    monkeypatch.setenv("TAREAS_DB", str(tmp_path / "prueba.db"))
    # Usar el cliente como administrador de contexto ejecuta el arranque (crea las tablas).
    with TestClient(app) as cliente:
        yield cliente
