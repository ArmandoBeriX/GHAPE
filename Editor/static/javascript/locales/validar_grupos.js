document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form"); // Selecciona el formulario
    const matriculaInput = document.querySelector("input[name='matricula']"); // Campo de matrícula
    const grupoInput = document.querySelector("input[name='grupo']"); // Campo de grupo
    const errorContainer = document.createElement("div"); // Crea un contenedor para los errores
    errorContainer.classList.add("alert", "alert-danger", "d-none"); // Clases de Bootstrap para el estilo
    form.insertBefore(errorContainer, form.firstChild); // Inserta el contenedor antes del formulario

    form.addEventListener("submit", function(event) {
        let valid = true; // Variable para rastrear la validez del formulario
        let errorMessage = "";

        // Limpiar mensajes de error anteriores
        errorContainer.innerHTML = "";
        errorContainer.classList.add("d-none"); // Ocultar el contenedor inicialmente

        // Validación del campo 'matricula'
        const matriculaValue = parseInt(matriculaInput.value);
        if (isNaN(matriculaValue) || matriculaValue < 1 || matriculaValue > 99) {
            valid = false;
            errorMessage += "La matrícula debe ser un número entre 1 y 99.<br>";
        }

        // Validación del campo 'grupo'
        const grupoValue = parseInt(grupoInput.value);
        if (isNaN(grupoValue) || grupoValue < 1 || grupoValue > 9) {
            valid = false;
            errorMessage += "El grupo debe ser un número entre 1 y 9.<br>";
        }

        // Si hay errores, prevenir el envío del formulario y mostrar los mensajes
        if (!valid) {
            event.preventDefault(); // Previene el envío del formulario
            errorContainer.innerHTML = errorMessage; // Muestra los mensajes de error
            errorContainer.classList.remove("d-none"); // Muestra el contenedor
        }
    });
});
