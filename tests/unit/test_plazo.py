"""Pruebas de la Historia 3: regla de "vencida" / "urgente" (cálculo por horas exactas)."""
from datetime import datetime, timedelta, timezone

from app.plazo import calcular_estado_plazo

AHORA = datetime(2026, 10, 26, 10, 0, tzinfo=timezone.utc)


def estado(desplazamiento: timedelta, completada: bool = False) -> str:
    return calcular_estado_plazo(AHORA + desplazamiento, completada, AHORA)


# --- T028 -------------------------------------------------------------------

def test_fecha_pasada_es_vencida():
    assert estado(-timedelta(days=3)) == "vencida"
    assert estado(-timedelta(seconds=1)) == "vencida"


def test_fecha_igual_a_ahora_es_vencida():
    assert estado(timedelta(0)) == "vencida"


def test_dentro_de_47_horas_es_urgente():
    assert estado(timedelta(hours=47)) == "urgente"
    assert estado(timedelta(seconds=1)) == "urgente"


def test_exactamente_48_horas_es_urgente():
    # El límite es inclusivo (spec, casos límite).
    assert estado(timedelta(hours=48)) == "urgente"


def test_48_horas_y_1_segundo_es_normal():
    assert estado(timedelta(hours=48, seconds=1)) == "normal"
    assert estado(timedelta(days=10)) == "normal"


def test_se_calcula_por_horas_y_no_por_dias_de_calendario():
    # Escenario de la spec: hoy 10:00, entrega mañana 23:00 (37 h) → urgente;
    # pasado mañana 23:00 (61 h) ya no lo es aunque sea "dentro de dos días".
    assert estado(timedelta(hours=37)) == "urgente"
    assert estado(timedelta(hours=61)) == "normal"


def test_tarea_completada_no_tiene_estado_de_plazo():
    for desplazamiento in [-timedelta(days=3), timedelta(0), timedelta(hours=5), timedelta(days=10)]:
        assert estado(desplazamiento, completada=True) == "ninguno"


def test_zonas_horarias_distintas_representan_el_mismo_instante():
    bolivia = timezone(timedelta(hours=-4))
    # 2026-10-28 06:00 en Bolivia = 2026-10-28 10:00 UTC = exactamente 48 h después de AHORA.
    entrega = datetime(2026, 10, 28, 6, 0, tzinfo=bolivia)

    assert calcular_estado_plazo(entrega, False, AHORA) == "urgente"
