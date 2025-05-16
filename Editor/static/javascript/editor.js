document.addEventListener('DOMContentLoaded', function() {
    const celdas = document.querySelectorAll('table td');
    const areaNegra = document.getElementById('areaNegra');
    let celdaSeleccionada = null;

    celdas.forEach(function(celda) {
        celda.addEventListener('click', function() {
            if (this.textContent.trim() === '') {
                if (celdaSeleccionada) {
                    celdaSeleccionada.style.backgroundColor = '';
                    celdaSeleccionada.style.color = '';
                }

                this.style.backgroundColor = 'black';
                this.style.color = 'white';
                celdaSeleccionada = this;

                obtenerDatos(areaNegra);
            }
        });
    });
});

function obtenerDatos(area) {
    fetch('/obtener-datos/')
        .then(response => response.json())
        .then(data => mostrarFormulario(area, data.asignaturas, data.locales))
        .catch(error => console.error('Error al obtener datos:', error));
}

function mostrarFormulario(area, asignaturas, locales) {
    area.innerHTML = `
        <form id="formularioDatos">
            <div class="mb-3">
                <label for="asignatura" class="form-label">Asignatura:</label>
                <select id="asignatura" name="asignatura" class="form-control" required>
                    ${asignaturas.map(asig => `<option value="${asig.id}">${asig.nombre}</option>`).join('')}
                </select>
            </div>
            <div class="mb-3">
                <label for="local" class="form-label">Local:</label>
                <select id="local" name="local" class="form-control" required>
                    ${locales.map(loc => `<option value="${loc.id}">${loc.codigo}</option>`).join('')}
                </select>
            </div>
            <button type="submit" class="btn btn-primary">Guardar</button>
        </form>
    `;

    const formulario = document.getElementById('formularioDatos');
    formulario.addEventListener('submit', function(event) {
        event.preventDefault();

        const asignaturaId = document.getElementById('asignatura').value;
        const localId = document.getElementById('local').value;

        console.log('Asignatura ID:', asignaturaId);
        console.log('Local ID:', localId);

        area.innerHTML = 'Contenido adicional aquí'; // Limpiar el área negra después de guardar
    });
}