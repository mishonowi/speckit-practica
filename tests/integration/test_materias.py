"""Pruebas de la Historia 1: registrar materias."""

COLOR = "#1E88E5"


def crear(cliente, nombre="Cálculo II", color=COLOR):
    return cliente.post("/api/materias", json={"nombre": nombre, "color": color})


# --- T010: caso principal ---------------------------------------------------

def test_crear_materia_valida(cliente):
    respuesta = crear(cliente)

    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["nombre"] == "Cálculo II"
    assert cuerpo["color"] == COLOR
    assert cuerpo["total_tareas"] == 0
    assert isinstance(cuerpo["id"], int)


def test_listar_materias_ordenadas_por_nombre(cliente):
    crear(cliente, "Física I")
    crear(cliente, "Álgebra")
    crear(cliente, "Cálculo II")

    nombres = [m["nombre"] for m in cliente.get("/api/materias").json()]

    assert nombres == ["Álgebra", "Cálculo II", "Física I"]


def test_nombre_se_guarda_sin_espacios_sobrantes(cliente):
    assert crear(cliente, "  Química  ").json()["nombre"] == "Química"


# --- T011: errores de validación --------------------------------------------

def test_nombre_vacio_o_solo_espacios_es_rechazado(cliente):
    for nombre in ["", "   "]:
        respuesta = crear(cliente, nombre)
        assert respuesta.status_code == 422
        assert "nombre" in respuesta.json()["campos"]
    assert cliente.get("/api/materias").json() == []


def test_nombre_de_51_caracteres_es_rechazado_y_50_aceptado(cliente):
    respuesta = crear(cliente, "a" * 51)
    assert respuesta.status_code == 422
    assert "50" in respuesta.json()["campos"]["nombre"]

    assert crear(cliente, "a" * 50).status_code == 201


def test_falta_nombre_o_color_es_rechazado(cliente):
    assert cliente.post("/api/materias", json={"color": COLOR}).status_code == 422
    respuesta = cliente.post("/api/materias", json={"nombre": "Física"})
    assert respuesta.status_code == 422
    assert "color" in respuesta.json()["campos"]


def test_color_fuera_de_la_paleta_es_rechazado(cliente):
    for color in ["#000000", "rojo", "#e53935 "]:
        respuesta = crear(cliente, "Física", color)
        assert respuesta.status_code == 422
        assert "color" in respuesta.json()["campos"]


def test_nombre_repetido_sin_distinguir_mayusculas_(cliente):
    assert crear(cliente, "Física I").status_code == 201
    assert crear(cliente, "física i").status_code == 409
    assert crear(cliente, "Álgebra").status_code == 201

    respuesta = crear(cliente, "álgebra")

    assert respuesta.status_code == 409
    assert "Ya existe" in respuesta.json()["detalle"]
    assert len(cliente.get("/api/materias").json()) == 2


# --- T012: edición, borrado e inexistentes ----------------------------------

def test_editar_materia(cliente):
    materia = crear(cliente).json()

    respuesta = cliente.put(
        f"/api/materias/{materia['id']}", json={"nombre": "Cálculo III", "color": "#43A047"}
    )

    assert respuesta.status_code == 200
    assert respuesta.json()["nombre"] == "Cálculo III"
    assert respuesta.json()["color"] == "#43A047"


def test_editar_a_nombre_existente_da_409_pero_el_propio_nombre_es_valido(cliente):
    crear(cliente, "Física I")
    materia = crear(cliente, "Cálculo II").json()

    conflicto = cliente.put(
        f"/api/materias/{materia['id']}", json={"nombre": "física i", "color": COLOR}
    )
    propio = cliente.put(
        f"/api/materias/{materia['id']}", json={"nombre": "Cálculo II", "color": "#43A047"}
    )

    assert conflicto.status_code == 409
    assert propio.status_code == 200


def test_borrar_materia(cliente):
    materia = crear(cliente).json()

    assert cliente.delete(f"/api/materias/{materia['id']}").status_code == 204
    assert cliente.get("/api/materias").json() == []


def test_materia_inexistente_da_404(cliente):
    cuerpo = {"nombre": "Física", "color": COLOR}

    assert cliente.put("/api/materias/999", json=cuerpo).status_code == 404
    respuesta = cliente.delete("/api/materias/999")
    assert respuesta.status_code == 404
    assert respuesta.json()["detalle"] == "La materia no existe."
