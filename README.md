# Organizador de Tareas Académicas (UPB)

Aplicación web local para que estudiantes organicen sus materias y tareas.
Un solo usuario por dispositivo, sin inicio de sesión.

## Requisitos

- Python 3.12 o superior

## Instalación

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecución

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Abrir `http://127.0.0.1:8000` en el navegador. Los datos se guardan en `datos/tareas.db`.

## Pruebas

```powershell
pytest
```
