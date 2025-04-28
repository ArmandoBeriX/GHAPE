document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form"); // Selecciona el formulario
    const errorContainer = document.createElement("div"); // Crea un contenedor para los errores
    errorContainer.classList.add("alert", "alert-danger", "d-none"); // Clases de Bootstrap para el estilo
    form.insertBefore(errorContainer, form.firstChild); // Inserta el contenedor antes del formulario

    form.addEventListener("submit", function(event) {
        let valid = true; // Variable para rastrear la validez del formulario
        let errorMessage = "";


        // Limpiar mensajes de error anteriores
        errorContainer.innerHTML = "";
        errorContainer.classList.add("d-none"); // Ocultar el contenedor inicialmente

        // Obtener todas las filas de turnos en la tabla
        const turnosRows = document.querySelectorAll("tbody tr");

        turnosRows.forEach(row => {
            const asignaturaSelect = row.querySelector("select[name$='[asignatura]']");
            const localSelect = row.querySelector("select[name$='[local]']");
            const tipoSelect = row.querySelector("select[name$='[tipo]']");

            const asignaturaValue = asignaturaSelect.value;
            const localValue = localSelect.value;
            const tipoValue = tipoSelect.value;

            // Validar que si se selecciona un tipo, se deben llenar los otros dos campos
            if (tipoValue) {
                if (!asignaturaValue || asignaturaValue === "" || asignaturaValue === "none" ||
                    !localValue || localValue === "" || localValue === "none") {
                    valid = false;
                    errorMessage += `En la clase ${row.cells[0].innerText}, debes seleccionar tanto la asignatura como el local si eliges un tipo de turno.<br>`;
                }
            } else {
                // Si todos están vacíos, también se permite, no se acumula error
                if (!asignaturaValue && !localValue && !tipoValue) {
                    // No hacer nada, ya que todos están vacíos es aceptable
                }
            }
        });

        // Si hay errores, prevenir el envío del formulario y mostrar los mensajes
        if (!valid) {
            event.preventDefault(); // Previene el envío del formulario
            errorContainer.innerHTML = errorMessage; // Muestra los mensajes de error
            errorContainer.classList.remove("d-none"); // Muestra el contenedor
        }
    });
});


