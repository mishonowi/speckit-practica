"use strict";

/**
 * Llama a la API JSON y devuelve el cuerpo de la respuesta (o null si no hay).
 * Si la API responde con error, lanza un Error con el mensaje en español
 * y, cuando existan, los mensajes por campo en `error.campos`.
 */
async function api(metodo, ruta, cuerpo) {
  const opciones = { method: metodo, headers: {} };
  if (cuerpo !== undefined) {
    opciones.headers["Content-Type"] = "application/json";
    opciones.body = JSON.stringify(cuerpo);
  }

  let respuesta;
  try {
    respuesta = await fetch(ruta, opciones);
  } catch (e) {
    throw new Error("No se pudo conectar con la aplicación. Inténtalo de nuevo.");
  }

  if (respuesta.status === 204) {
    return null;
  }

  let datos = null;
  try {
    datos = await respuesta.json();
  } catch (e) {
    // Respuesta sin JSON: se usa el mensaje genérico de abajo.
  }

  if (!respuesta.ok) {
    const error = new Error((datos && datos.detalle) || "Ocurrió un error inesperado.");
    error.campos = (datos && datos.campos) || {};
    throw error;
  }
  return datos;
}

// ---------------------------------------------------------------------------
// Materias (Historia 1)
// ---------------------------------------------------------------------------

// Misma paleta que valida el servidor (app/esquemas.py). `texto` es el color
// de la marca ✓ con contraste suficiente sobre cada color.
const COLORES = [
  { valor: "#E53935", nombre: "Rojo", texto: "#ffffff" },
  { valor: "#FB8C00", nombre: "Naranja", texto: "#000000" },
  { valor: "#FDD835", nombre: "Amarillo", texto: "#000000" },
  { valor: "#43A047", nombre: "Verde", texto: "#000000" },
  { valor: "#00897B", nombre: "Turquesa", texto: "#000000" },
  { valor: "#1E88E5", nombre: "Azul", texto: "#000000" },
  { valor: "#8E24AA", nombre: "Morado", texto: "#ffffff" },
  { valor: "#6D4C41", nombre: "Marrón", texto: "#ffffff" },
];

const LIMITE_NOMBRE_MATERIA = 50;

let materias = [];

const formMateria = document.getElementById("form-materia");
const campoMateriaId = document.getElementById("materia-id");
const campoNombre = document.getElementById("materia-nombre");
const contadorNombre = document.getElementById("materia-nombre-contador");
const errorNombre = document.getElementById("materia-nombre-error");
const errorColor = document.getElementById("materia-color-error");
const errorMateria = document.getElementById("materia-error");
const botonGuardarMateria = document.getElementById("materia-guardar");
const botonCancelarMateria = document.getElementById("materia-cancelar");
const listaMaterias = document.getElementById("lista-materias");
const avisoVacioMaterias = document.getElementById("materias-vacio");

function colorPorValor(valor) {
  return COLORES.find((c) => c.valor === valor) || COLORES[0];
}

function dibujarColores() {
  const contenedor = document.getElementById("materia-colores");
  COLORES.forEach((color) => {
    const etiqueta = document.createElement("label");
    etiqueta.className = "color-opcion";

    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "materia-color";
    radio.value = color.valor;

    const muestra = document.createElement("span");
    muestra.className = "muestra";
    muestra.style.background = color.valor;
    muestra.style.setProperty("--marca", color.texto);
    muestra.textContent = "✓";
    muestra.setAttribute("aria-hidden", "true");

    const nombre = document.createElement("span");
    nombre.className = "solo-lectores";
    nombre.textContent = color.nombre;

    etiqueta.append(radio, muestra, nombre);
    contenedor.append(etiqueta);
  });
}

function colorSeleccionado() {
  const marcado = formMateria.querySelector('input[name="materia-color"]:checked');
  return marcado ? marcado.value : "";
}

function marcarColor(valor) {
  formMateria.querySelectorAll('input[name="materia-color"]').forEach((radio) => {
    radio.checked = radio.value === valor;
  });
}

function actualizarContadorNombre() {
  contadorNombre.textContent = `${campoNombre.value.length}/${LIMITE_NOMBRE_MATERIA}`;
}

function limpiarErroresMateria() {
  errorNombre.textContent = "";
  errorColor.textContent = "";
  errorMateria.textContent = "";
}

function reiniciarFormularioMateria() {
  formMateria.reset();
  campoMateriaId.value = "";
  botonGuardarMateria.textContent = "Agregar materia";
  botonCancelarMateria.hidden = true;
  limpiarErroresMateria();
  actualizarContadorNombre();
}

function dibujarMaterias() {
  listaMaterias.replaceChildren();
  avisoVacioMaterias.hidden = materias.length > 0;

  materias.forEach((materia) => {
    const item = document.createElement("li");
    item.className = "materia-item";

    const chip = document.createElement("span");
    chip.className = "materia-chip";
    chip.textContent = materia.nombre;
    chip.style.background = materia.color;
    chip.style.color = colorPorValor(materia.color).texto;

    const total = document.createElement("span");
    total.className = "materia-total";
    total.textContent = materia.total_tareas === 1 ? "1 tarea" : `${materia.total_tareas} tareas`;

    const editar = document.createElement("button");
    editar.type = "button";
    editar.className = "secundario";
    editar.textContent = "Editar";
    editar.setAttribute("aria-label", `Editar la materia ${materia.nombre}`);
    editar.addEventListener("click", () => empezarEdicionMateria(materia));

    const borrar = document.createElement("button");
    borrar.type = "button";
    borrar.className = "secundario";
    borrar.textContent = "Borrar";
    borrar.setAttribute("aria-label", `Borrar la materia ${materia.nombre}`);
    borrar.addEventListener("click", () => borrarMateria(materia));

    item.append(chip, total, editar, borrar);
    listaMaterias.append(item);
  });
}

async function cargarMaterias() {
  try {
    materias = await api("GET", "/api/materias");
    dibujarMaterias();
  } catch (error) {
    errorMateria.textContent = error.message;
  }
}

function empezarEdicionMateria(materia) {
  limpiarErroresMateria();
  campoMateriaId.value = materia.id;
  campoNombre.value = materia.nombre;
  marcarColor(materia.color);
  botonGuardarMateria.textContent = "Guardar cambios";
  botonCancelarMateria.hidden = false;
  actualizarContadorNombre();
  campoNombre.focus();
}

async function guardarMateria(evento) {
  evento.preventDefault();
  limpiarErroresMateria();

  const nombre = campoNombre.value.trim();
  const color = colorSeleccionado();
  // Comprobación inmediata en pantalla; el servidor valida de nuevo siempre.
  if (!nombre) {
    errorNombre.textContent = "El nombre no puede estar vacío.";
    campoNombre.focus();
    return;
  }
  if (!color) {
    errorColor.textContent = "Elige un color para la materia.";
    return;
  }

  const id = campoMateriaId.value;
  try {
    if (id) {
      await api("PUT", `/api/materias/${id}`, { nombre, color });
    } else {
      await api("POST", "/api/materias", { nombre, color });
    }
    reiniciarFormularioMateria();
    await cargarMaterias();
  } catch (error) {
    // Se conserva lo escrito en el formulario para que el estudiante lo corrija.
    const campos = error.campos || {};
    errorNombre.textContent = campos.nombre || "";
    errorColor.textContent = campos.color || "";
    if (!campos.nombre && !campos.color) {
      // Un 409 (nombre repetido) llega sin campos: se muestra junto al nombre.
      errorNombre.textContent = error.message;
      campoNombre.focus();
    } else if (campos.nombre) {
      campoNombre.focus();
    }
  }
}

async function borrarMateria(materia) {
  // El mensaje indica cuántas tareas se perderán; si se cancela no se llama a la API.
  const n = materia.total_tareas;
  const aviso =
    n === 0
      ? `¿Borrar la materia "${materia.nombre}"?`
      : `¿Borrar la materia "${materia.nombre}"? Se borrarán ${n} ${n === 1 ? "tarea" : "tareas"}.`;
  if (!window.confirm(aviso)) {
    return;
  }
  try {
    await api("DELETE", `/api/materias/${materia.id}`);
    if (campoMateriaId.value === String(materia.id)) {
      reiniciarFormularioMateria();
    }
    await cargarMaterias();
  } catch (error) {
    errorMateria.textContent = error.message;
  }
}

dibujarColores();
actualizarContadorNombre();
campoNombre.addEventListener("input", actualizarContadorNombre);
formMateria.addEventListener("submit", guardarMateria);
botonCancelarMateria.addEventListener("click", reiniciarFormularioMateria);
cargarMaterias();
