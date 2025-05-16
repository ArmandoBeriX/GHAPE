// Función para mostrar u ocultar el mensaje de "No hay resultados"
function mostrarMensajeNoResultados(mostrar) {
    const mensajeNoResultados = document.getElementById('mensaje-no-resultados');
    if (mostrar) {
        mensajeNoResultados.classList.remove('hidden');
    } else {
        mensajeNoResultados.classList.add('hidden');
    }
}

// Función para filtrar los horarios
function filtrarHorarios() {
    const ano = document.getElementById('ano-filtro').value;
    const semana = document.getElementById('semana-filtro').value;
    const grupo = document.getElementById('grupo-filtro').value;

    const horarios = document.querySelectorAll('.horario-card');
    let resultadosEncontrados = false;

    horarios.forEach(horario => {
        const horarioAno = horario.getAttribute('data-ano');
        const horarioSemana = horario.getAttribute('data-semana');
        const horarioGrupo = horario.getAttribute('data-grupo');

        const coincideAno = ano === '' || horarioAno === ano;
        const coincideSemana = semana === '' || horarioSemana === semana;
        const coincideGrupo = grupo === '' || horarioGrupo === grupo;

        if (coincideAno && coincideSemana && coincideGrupo) {
            horario.classList.remove('hidden');
            resultadosEncontrados = true;
        } else {
            horario.classList.add('hidden');
        }
    });

    // Mostrar u ocultar el mensaje de "No hay resultados"
    mostrarMensajeNoResultados(!resultadosEncontrados);
}

// Función para limpiar los filtros
function limpiarFiltros() {
    document.getElementById('ano-filtro').value = '';
    document.getElementById('semana-filtro').value = '';
    document.getElementById('grupo-filtro').value = '';

    const horarios = document.querySelectorAll('.horario-card');
    horarios.forEach(horario => horario.classList.remove('hidden'));

    // Ocultar el mensaje de "No hay resultados" al limpiar los filtros
    mostrarMensajeNoResultados(false);
}

// Asignar eventos a los botones
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('filtrar-btn').addEventListener('click', filtrarHorarios);
    document.getElementById('limpiar-btn').addEventListener('click', limpiarFiltros);
});