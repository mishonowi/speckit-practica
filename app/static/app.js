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
    dibujarSelectorMaterias();
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
    // Las tareas muestran el nombre y color de su materia: se recargan ambas listas.
    await recargarTodo();
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
    // El borrado elimina también sus tareas (cascada): se recargan ambas listas.
    await recargarTodo();
  } catch (error) {
    errorMateria.textContent = error.message;
  }
}

dibujarColores();
actualizarContadorNombre();
campoNombre.addEventListener("input", actualizarContadorNombre);
formMateria.addEventListener("submit", guardarMateria);
botonCancelarMateria.addEventListener("click", reiniciarFormularioMateria);

// ---------------------------------------------------------------------------
// Tareas (Historia 2)
// ---------------------------------------------------------------------------

const LIMITE_TITULO = 100;
const LIMITE_DESCRIPCION = 500;
// Si el estudiante elige solo el día, la entrega es al final de ese día (hora local).
const HORA_POR_DEFECTO = "23:59";

let tareas = [];

const formTarea = document.getElementById("form-tarea");
const camposTarea = document.getElementById("tarea-campos");
const campoTareaId = document.getElementById("tarea-id");
const campoTareaMateria = document.getElementById("tarea-materia");
const campoTitulo = document.getElementById("tarea-titulo");
const campoDescripcion = document.getElementById("tarea-descripcion");
const campoFecha = document.getElementById("tarea-fecha");
const campoHora = document.getElementById("tarea-hora");
const contadorTitulo = document.getElementById("tarea-titulo-contador");
const contadorDescripcion = document.getElementById("tarea-descripcion-contador");
const errorTareaMateria = document.getElementById("tarea-materia-error");
const errorTitulo = document.getElementById("tarea-titulo-error");
const errorDescripcion = document.getElementById("tarea-descripcion-error");
const errorFecha = document.getElementById("tarea-fecha-error");
const errorTarea = document.getElementById("tarea-error");
const botonGuardarTarea = document.getElementById("tarea-guardar");
const botonCancelarTarea = document.getElementById("tarea-cancelar");
const avisoSinMaterias = document.getElementById("tareas-sin-materias");
const listaTareas = document.getElementById("lista-tareas");
const avisoVacioTareas = document.getElementById("tareas-vacio");
const aviso = document.getElementById("aviso");

const formatoFecha = new Intl.DateTimeFormat("es", {
  weekday: "short",
  day: "numeric",
  month: "short",
  year: "numeric",
  hour: "2-digit",
  minute: "2-digit",
});

function dosDigitos(numero) {
  return String(numero).padStart(2, "0");
}

/**
 * Convierte la fecha ("AAAA-MM-DD") y la hora ("HH:MM") elegidas en el formulario
 * a ISO 8601 con el desplazamiento horario del dispositivo, p. ej. "2026-11-05T18:00:00-04:00".
 * El desplazamiento se calcula para esa fecha concreta (por si hay horario de verano).
 */
function fechaConDesplazamiento(fecha, hora) {
  const [anio, mes, dia] = fecha.split("-").map(Number);
  const [horas, minutos] = hora.split(":").map(Number);
  const local = new Date(anio, mes - 1, dia, horas, minutos);
  const desplazamiento = -local.getTimezoneOffset(); // en minutos; Bolivia = -240
  const signo = desplazamiento >= 0 ? "+" : "-";
  const absoluto = Math.abs(desplazamiento);
  return (
    `${fecha}T${hora}:00` +
    `${signo}${dosDigitos(Math.floor(absoluto / 60))}:${dosDigitos(absoluto % 60)}`
  );
}

/** Separa una fecha UTC de la API en día y hora locales para el formulario. */
function partesLocales(fechaUtc) {
  const fecha = new Date(fechaUtc);
  return {
    dia: `${fecha.getFullYear()}-${dosDigitos(fecha.getMonth() + 1)}-${dosDigitos(fecha.getDate())}`,
    hora: `${dosDigitos(fecha.getHours())}:${dosDigitos(fecha.getMinutes())}`,
  };
}

function mostrarAviso(mensaje) {
  aviso.textContent = mensaje;
  aviso.hidden = !mensaje;
}

function actualizarContadoresTarea() {
  contadorTitulo.textContent = `${campoTitulo.value.length}/${LIMITE_TITULO}`;
  contadorDescripcion.textContent = `${campoDescripcion.value.length}/${LIMITE_DESCRIPCION}`;
}

function limpiarErroresTarea() {
  [errorTareaMateria, errorTitulo, errorDescripcion, errorFecha, errorTarea].forEach((p) => {
    p.textContent = "";
  });
}

function reiniciarFormularioTarea() {
  formTarea.reset();
  campoTareaId.value = "";
  botonGuardarTarea.textContent = "Agregar tarea";
  botonCancelarTarea.hidden = true;
  limpiarErroresTarea();
  actualizarContadoresTarea();
}

/** Rellena el selector de materias conservando la opción elegida si sigue existiendo. */
function dibujarSelectorMaterias() {
  const elegida = campoTareaMateria.value;
  const vacia = new Option("Elige una materia", "");
  const opciones = materias.map((m) => new Option(m.nombre, String(m.id)));
  campoTareaMateria.replaceChildren(vacia, ...opciones);
  if (materias.some((m) => String(m.id) === elegida)) {
    campoTareaMateria.value = elegida;
  }

  // Sin materias no se puede crear ninguna tarea: se guía al estudiante.
  const sinMaterias = materias.length === 0;
  avisoSinMaterias.hidden = !sinMaterias;
  camposTarea.disabled = sinMaterias;
}

function crearBoton(texto, etiqueta, alHacerClic) {
  const boton = document.createElement("button");
  boton.type = "button";
  boton.className = "secundario";
  boton.textContent = texto;
  boton.setAttribute("aria-label", etiqueta);
  boton.addEventListener("click", alHacerClic);
  return boton;
}

function dibujarTarea(tarea) {
  const item = document.createElement("li");
  item.className = "tarea-item";
  // La franja izquierda repite el color de la materia para reconocerla de un vistazo.
  item.style.setProperty("--color-materia", tarea.materia_color);

  const cabecera = document.createElement("div");
  cabecera.className = "tarea-cabecera";

  const titulo = document.createElement("h4");
  titulo.className = "tarea-titulo";
  titulo.textContent = tarea.titulo;

  const chip = document.createElement("span");
  chip.className = "materia-chip tarea-materia";
  chip.textContent = tarea.materia_nombre;
  chip.style.background = tarea.materia_color;
  chip.style.color = colorPorValor(tarea.materia_color).texto;

  cabecera.append(titulo, chip);

  const fecha = document.createElement("p");
  fecha.className = "tarea-fecha";
  const tiempo = document.createElement("time");
  tiempo.dateTime = tarea.fecha_entrega;
  tiempo.textContent = formatoFecha.format(new Date(tarea.fecha_entrega));
  fecha.append("Entrega: ", tiempo);

  item.append(cabecera, fecha);

  if (tarea.descripcion) {
    const descripcion = document.createElement("p");
    descripcion.className = "tarea-descripcion";
    descripcion.textContent = tarea.descripcion;
    item.append(descripcion);
  }

  const acciones = document.createElement("div");
  acciones.className = "acciones";
  acciones.append(
    crearBoton("Editar", `Editar la tarea ${tarea.titulo}`, () => empezarEdicionTarea(tarea)),
    crearBoton("Borrar", `Borrar la tarea ${tarea.titulo}`, () => borrarTarea(tarea))
  );
  item.append(acciones);

  return item;
}

function dibujarTareas() {
  avisoVacioTareas.hidden = tareas.length > 0;
  listaTareas.replaceChildren(...tareas.map(dibujarTarea));
}

async function cargarTareas() {
  try {
    tareas = await api("GET", "/api/tareas");
    mostrarAviso("");
    dibujarTareas();
    // Si la tarea en edición ya no existe (p. ej. se borró su materia), se cierra la edición.
    if (campoTareaId.value && !tareas.some((t) => String(t.id) === campoTareaId.value)) {
      reiniciarFormularioTarea();
    }
  } catch (error) {
    mostrarAviso(`No se pudieron cargar las tareas. ${error.message}`);
  }
}

async function recargarTodo() {
  await Promise.all([cargarMaterias(), cargarTareas()]);
}

function empezarEdicionTarea(tarea) {
  limpiarErroresTarea();
  const { dia, hora } = partesLocales(tarea.fecha_entrega);
  campoTareaId.value = tarea.id;
  campoTareaMateria.value = String(tarea.materia_id);
  campoTitulo.value = tarea.titulo;
  campoDescripcion.value = tarea.descripcion || "";
  campoFecha.value = dia;
  campoHora.value = hora;
  botonGuardarTarea.textContent = "Guardar cambios";
  botonCancelarTarea.hidden = false;
  actualizarContadoresTarea();
  campoTitulo.focus();
}

/** Comprobación inmediata en pantalla; devuelve el primer campo con error o null. */
function validarFormularioTarea() {
  let primerError = null;
  const marcar = (campo, parrafo, mensaje) => {
    parrafo.textContent = mensaje;
    primerError = primerError || campo;
  };
  if (!campoTareaMateria.value) {
    marcar(campoTareaMateria, errorTareaMateria, "Elige la materia de la tarea.");
  }
  if (!campoTitulo.value.trim()) {
    marcar(campoTitulo, errorTitulo, "El título no puede estar vacío.");
  }
  if (!campoFecha.value) {
    marcar(campoFecha, errorFecha, "Elige la fecha de entrega.");
  }
  return primerError;
}

function mostrarErroresDelServidor(error) {
  const campos = error.campos || {};
  errorTareaMateria.textContent = campos.materia_id || "";
  errorTitulo.textContent = campos.titulo || "";
  errorDescripcion.textContent = campos.descripcion || "";
  errorFecha.textContent = campos.fecha_entrega || "";
  if (Object.keys(campos).length === 0) {
    // Fallo de conexión, 404, etc.: mensaje general sin borrar lo escrito.
    errorTarea.textContent = error.message;
  }
}

async function guardarTarea(evento) {
  evento.preventDefault();
  limpiarErroresTarea();

  const campoConError = validarFormularioTarea();
  if (campoConError) {
    campoConError.focus();
    return;
  }

  const cuerpo = {
    materia_id: Number(campoTareaMateria.value),
    titulo: campoTitulo.value.trim(),
    descripcion: campoDescripcion.value.trim(),
    fecha_entrega: fechaConDesplazamiento(campoFecha.value, campoHora.value || HORA_POR_DEFECTO),
  };

  const id = campoTareaId.value;
  try {
    if (id) {
      await api("PUT", `/api/tareas/${id}`, cuerpo);
    } else {
      await api("POST", "/api/tareas", cuerpo);
    }
    reiniciarFormularioTarea();
    // total_tareas de las materias también cambia.
    await recargarTodo();
  } catch (error) {
    // Se conserva lo escrito en el formulario para que el estudiante lo corrija.
    mostrarErroresDelServidor(error);
  }
}

async function borrarTarea(tarea) {
  if (!window.confirm(`¿Borrar la tarea "${tarea.titulo}"?`)) {
    return;
  }
  try {
    await api("DELETE", `/api/tareas/${tarea.id}`);
    if (campoTareaId.value === String(tarea.id)) {
      reiniciarFormularioTarea();
    }
    await recargarTodo();
  } catch (error) {
    mostrarAviso(`No se pudo borrar la tarea. ${error.message}`);
  }
}

actualizarContadoresTarea();
campoTitulo.addEventListener("input", actualizarContadoresTarea);
campoDescripcion.addEventListener("input", actualizarContadoresTarea);
formTarea.addEventListener("submit", guardarTarea);
botonCancelarTarea.addEventListener("click", reiniciarFormularioTarea);
recargarTodo();
