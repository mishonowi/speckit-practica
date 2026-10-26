"""Pruebas de la Historia 2: crear tareas y verlas ordenadas por fecha."""

COLOR = "#1E88E5"
FECHA = "2026-11-05T22:00:00Z"


def crear_materia(cliente, nombre="Cálculo II", color=COLOR):
    return cliente.post("/api/materias", json={"nombre": nombre, "color": color}).json()


def crear_tarea(cliente, materia_id, titulo="Taller 3", fecha=FECHA, descripcion=None):
    cuerpo = {"materia_id": materia_id, "titulo": titulo, "fecha_entrega": fecha}
    if descripcion is not None:
        cuerpo["descripcion"] = descripcion
    return cliente.post("/api/tareas", json=cuerpo)


# --- T018: caso principal ---------------------------------------------------

def test_crear_tarea_valida_con_descripcion(cliente):
    materia = crear_materia(cliente)

    respuesta = crear_tarea(cliente, materia["id"], descripcion="Ejercicios 1 al 10")

    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert isinstance(cuerpo["id"], int)
    assert cuerpo["materia_id"] == materia["id"]
    assert cuerpo["materia_nombre"] == "Cálculo II"
    assert cuerpo["materia_color"] == COLOR
    assert cuerpo["titulo"] == "Taller 3"
    assert cuerpo["descripcion"] == "Ejercicios 1 al 10"
    assert cuerpo["fecha_entrega"] == FECHA
    assert cuerpo["completada"] is False


def test_crear_tarea_sin_descripcion(cliente):
    materia = crear_materia(cliente)

    respuesta = crear_tarea(cliente, materia["id"])

    assert respuesta.status_code == 201
    assert respuesta.json()["descripcion"] is None


def test_descripcion_vacia_o_solo_espacios_se_guarda_como_nula(cliente):
    materia = crear_materia(cliente)

    for descripcion in ["", "   "]:
        respuesta = crear_tarea(cliente, materia["id"], descripcion=descripcion)
        assert respuesta.status_code == 201
        assert respuesta.json()["descripcion"] is None


def test_titulo_se_guarda_sin_espacios_sobrantes(cliente):
    materia = crear_materia(cliente)

    assert crear_tarea(cliente, materia["id"], titulo="  Taller 3  ").json()["titulo"] == "Taller 3"


def test_fecha_con_desplazamiento_horario_se_guarda_en_utc(cliente):
    materia = crear_materia(cliente)

    # 18:00 en Bolivia (UTC-4) son las 22:00 UTC.
    respuesta = crear_tarea(cliente, materia["id"], fecha="2026-11-05T18:00:00-04:00")

    assert respuesta.json()["fecha_entrega"] == "2026-11-05T22:00:00Z"


def test_la_materia_cuenta_sus_tareas(cliente):
    materia = crear_materia(cliente)
    crear_tarea(cliente, materia["id"])
    crear_tarea(cliente, materia["id"], titulo="Taller 4")

    assert cliente.get("/api/materias").json()[0]["total_tareas"] == 2


# --- T019: orden del listado ------------------------------------------------

def test_listado_ordenado_por_fecha_y_desempate_por_id(cliente):
    materia = crear_materia(cliente)
    crear_tarea(cliente, materia["id"], "Lejana", "2026-12-01T12:00:00Z")
    crear_tarea(cliente, materia["id"], "Próxima", "2026-11-01T12:00:00Z")
    crear_tarea(cliente, materia["id"], "Media A", "2026-11-15T12:00:00Z")
    # Misma hora que "Media A" escrita con otra zona horaria: empata y va después por id.
    crear_tarea(cliente, materia["id"], "Media B", "2026-11-15T08:00:00-04:00")

    titulos = [t["titulo"] for t in cliente.get("/api/tareas").json()]

    assert titulos == ["Próxima", "Media A", "Media B", "Lejana"]


def test_listado_vacio(cliente):
    respuesta = cliente.get("/api/tareas")

    assert respuesta.status_code == 200
    assert respuesta.json() == []


# --- T020: errores de validación --------------------------------------------

def test_titulo_vacio_o_solo_espacios_es_rechazado(cliente):
    materia = crear_materia(cliente)

    for titulo in ["", "   "]:
        respuesta = crear_tarea(cliente, materia["id"], titulo=titulo)
        assert respuesta.status_code == 422
        assert "titulo" in respuesta.json()["campos"]
    assert cliente.get("/api/tareas").json() == []


def test_titulo_de_101_caracteres_es_rechazado_y_100_aceptado(cliente):
    materia = crear_materia(cliente)

    respuesta = crear_tarea(cliente, materia["id"], titulo="a" * 101)
    assert respuesta.status_code == 422
    assert "100" in respuesta.json()["campos"]["titulo"]

    assert crear_tarea(cliente, materia["id"], titulo="a" * 100).status_code == 201


def test_descripcion_de_501_caracteres_es_rechazada_y_500_aceptada(cliente):
    materia = crear_materia(cliente)

    respuesta = crear_tarea(cliente, materia["id"], descripcion="a" * 501)
    assert respuesta.status_code == 422
    assert "500" in respuesta.json()["campos"]["descripcion"]

    assert crear_tarea(cliente, materia["id"], descripcion="a" * 500).status_code == 201


def test_fecha_sin_zona_horaria_es_rechazada(cliente):
    materia = crear_materia(cliente)

    for fecha in ["2026-11-05T22:00:00", "2026-11-05"]:
        respuesta = crear_tarea(cliente, materia["id"], fecha=fecha)
        assert respuesta.status_code == 422
        assert "zona horaria" in respuesta.json()["campos"]["fecha_entrega"]


def test_fecha_invalida_es_rechazada(cliente):
    materia = crear_materia(cliente)

    for fecha in ["mañana", "2026-13-45T10:00:00Z", 1700000000]:
        respuesta = crear_tarea(cliente, materia["id"], fecha=fecha)
        assert respuesta.status_code == 422
        assert "fecha_entrega" in respuesta.json()["campos"]


def test_materia_inexistente_es_rechazada(cliente):
    respuesta = crear_tarea(cliente, 999)

    assert respuesta.status_code == 422
    assert respuesta.json()["campos"]["materia_id"] == "La materia no existe."


def test_falta_titulo_materia_o_fecha_indica_el_campo(cliente):
    materia = crear_materia(cliente)
    completo = {"materia_id": materia["id"], "titulo": "Taller 3", "fecha_entrega": FECHA}

    for campo in completo:
        cuerpo = {k: v for k, v in completo.items() if k != campo}
        respuesta = cliente.post("/api/tareas", json=cuerpo)
        assert respuesta.status_code == 422
        assert respuesta.json()["campos"][campo] == "Este campo es obligatorio."
    assert cliente.get("/api/tareas").json() == []


def test_fecha_pasada_se_permite(cliente):
    materia = crear_materia(cliente)

    assert crear_tarea(cliente, materia["id"], fecha="2020-01-01T12:00:00Z").status_code == 201


# --- T021: edición, borrado, inexistentes y cascada -------------------------

def test_editar_tarea(cliente):
    calculo = crear_materia(cliente)
    fisica = crear_materia(cliente, "Física I", "#43A047")
    tarea = crear_tarea(cliente, calculo["id"], descripcion="Primera versión").json()

    respuesta = cliente.put(
        f"/api/tareas/{tarea['id']}",
        json={
            "materia_id": fisica["id"],
            "titulo": "Informe de laboratorio",
            "descripcion": "",
            "fecha_entrega": "2026-11-10T13:30:00Z",
        },
    )

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["id"] == tarea["id"]
    assert cuerpo["materia_nombre"] == "Física I"
    assert cuerpo["materia_color"] == "#43A047"
    assert cuerpo["titulo"] == "Informe de laboratorio"
    assert cuerpo["descripcion"] is None
    assert cuerpo["fecha_entrega"] == "2026-11-10T13:30:00Z"


def test_editar_con_datos_invalidos_no_cambia_la_tarea(cliente):
    materia = crear_materia(cliente)
    tarea = crear_tarea(cliente, materia["id"]).json()

    respuesta = cliente.put(
        f"/api/tareas/{tarea['id']}",
        json={"materia_id": 999, "titulo": "Otro", "fecha_entrega": FECHA},
    )

    assert respuesta.status_code == 422
    assert cliente.get("/api/tareas").json()[0]["titulo"] == "Taller 3"


def test_borrar_tarea(cliente):
    materia = crear_materia(cliente)
    tarea = crear_tarea(cliente, materia["id"]).json()

    assert cliente.delete(f"/api/tareas/{tarea['id']}").status_code == 204
    assert cliente.get("/api/tareas").json() == []


def test_tarea_inexistente_da_404(cliente):
    materia = crear_materia(cliente)
    cuerpo = {"materia_id": materia["id"], "titulo": "Taller", "fecha_entrega": FECHA}

    assert cliente.put("/api/tareas/999", json=cuerpo).status_code == 404
    respuesta = cliente.delete("/api/tareas/999")
    assert respuesta.status_code == 404
    assert respuesta.json()["detalle"] == "La tarea no existe."


def test_borrar_materia_borra_sus_tareas_en_cascada(cliente):
    calculo = crear_materia(cliente)
    fisica = crear_materia(cliente, "Física I")
    crear_tarea(cliente, calculo["id"], "Taller 3")
    crear_tarea(cliente, calculo["id"], "Taller 4")
    crear_tarea(cliente, fisica["id"], "Informe")

    cliente.delete(f"/api/materias/{calculo['id']}")

    titulos = [t["titulo"] for t in cliente.get("/api/tareas").json()]
    assert titulos == ["Informe"]


# --- HU3: estado de plazo (T029) --------------------------------------------

def _dentro_de(**desplazamiento):
    """Fecha ISO relativa al momento actual (las pruebas no dependen del reloj fijo)."""
    from datetime import datetime, timedelta, timezone

    return (datetime.now(timezone.utc) + timedelta(**desplazamiento)).strftime("%Y-%m-%dT%H:%M:%SZ")


def test_listado_incluye_estado_de_plazo(cliente):
    materia = crear_materia(cliente)
    crear_tarea(cliente, materia["id"], "Atrasada", _dentro_de(days=-2))
    crear_tarea(cliente, materia["id"], "Mañana", _dentro_de(hours=24))
    crear_tarea(cliente, materia["id"], "Lejana", _dentro_de(days=10))

    estados = {t["titulo"]: t["estado_plazo"] for t in cliente.get("/api/tareas").json()}

    assert estados == {"Atrasada": "vencida", "Mañana": "urgente", "Lejana": "normal"}


def test_crear_y_editar_devuelven_estado_de_plazo(cliente):
    materia = crear_materia(cliente)

    creada = crear_tarea(cliente, materia["id"], fecha=_dentro_de(hours=5)).json()
    assert creada["estado_plazo"] == "urgente"

    editada = cliente.put(
        f"/api/tareas/{creada['id']}",
        json={"materia_id": materia["id"], "titulo": "Taller 3", "fecha_entrega": _dentro_de(days=-1)},
    ).json()
    assert editada["estado_plazo"] == "vencida"
