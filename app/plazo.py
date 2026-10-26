"""Regla de negocio del estado de plazo de una tarea (ver data-model.md)."""
from datetime import datetime, timedelta

# Una tarea pendiente es "urgente" si faltan 48 horas o menos para su entrega.
VENTANA_URGENTE = timedelta(hours=48)


def calcular_estado_plazo(fecha_entrega: datetime, completada: bool, ahora: datetime) -> str:
    """Devuelve "vencida", "urgente", "normal" o "ninguno".

    El cálculo es por horas exactas, no por días de calendario: una entrega dentro de
    48 horas o menos es urgente aunque caiga "pasado mañana", y una que ya llegó a su
    hora (fecha_entrega == ahora) cuenta como vencida. Las tareas completadas no
    tienen estado de plazo. Ambas fechas deben incluir zona horaria.
    """
    if completada:
        return "ninguno"
    if fecha_entrega <= ahora:
        return "vencida"
    if fecha_entrega - ahora <= VENTANA_URGENTE:
        return "urgente"
    return "normal"
