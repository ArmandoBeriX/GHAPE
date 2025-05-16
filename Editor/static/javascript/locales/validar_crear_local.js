document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form"); // Selecciona el formulario
    const pisoInput = document.querySelector("input[name='piso']");
    const numeroInput = document.querySelector("input[name='numero']");
    const tipoSelect = document.querySelector("select[name='tipo']");
    const errorContainer = document.createElement("div"); // Crea un contenedor para los errores
    errorContainer.classList.add("alert", "alert-danger", "d-none"); // Clases de Bootstrap para el estilo
    form.insertBefore(errorContainer, form.firstChild); // Inserta el contenedor antes del formulario

    form.addEventListener("submit", function(event) {
        let valid = true; // Variable para rastrear la validez del formulario
        let errorMessage = "";

        // Limpiar mensajes de error anteriores
        errorContainer.innerHTML = "";
        errorContainer.classList.add("d-none"); // Ocultar el contenedor inicialmente

        // Validación del campo 'piso'
        const pisoValue = parseInt(pisoInput.value);
        if (isNaN(pisoValue) || pisoValue < 1 || pisoValue > 5) {
            valid = false;
            errorMessage += "El piso debe ser un número entre 1 y 5.<br>";
        }

        // Validación del campo 'numero'
        const numeroValue = parseInt(numeroInput.value);
        if (isNaN(numeroValue) || numeroValue < 1 || numeroValue > 20) {
            valid = false;
            errorMessage += "El número debe ser un número entre 1 y 20.<br>";
        }

        // Validación del campo 'tipo'
        if (tipoSelect.value === "") {
            valid = false;
            errorMessage += "Debes seleccionar un tipo de local.<br>";
        }

        // Si hay errores, prevenir el envío del formulario y mostrar los mensajes
        if (!valid) {
            event.preventDefault(); // Previene el envío del formulario
            errorContainer.innerHTML = errorMessage; // Muestra los mensajes de error
            errorContainer.classList.remove("d-none"); // Muestra el contenedor
        }
    });
});