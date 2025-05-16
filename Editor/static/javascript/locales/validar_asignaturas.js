document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form"); // Selecciona el formulario
    const siglasInput = document.querySelector("input[name='siglas']"); // Campo de siglas
    const nombreInput = document.querySelector("input[name='nombre']"); // Campo de nombre
    const catedraInput = document.querySelector("input[name='catedra']"); // Campo de cátedra
    const errorContainer = document.createElement("div"); // Crea un contenedor para los errores
    errorContainer.classList.add("alert", "alert-danger", "d-none"); // Clases de Bootstrap para el estilo
    form.insertBefore(errorContainer, form.firstChild); // Inserta el contenedor antes del formulario

    form.addEventListener("submit", function(event) {
        let valid = true; // Variable para rastrear la validez del formulario
        let errorMessage = "";

        // Limpiar mensajes de error anteriores
        errorContainer.innerHTML = "";
        errorContainer.classList.add("d-none"); // Ocultar el contenedor inicialmente

        // Función para validar caracteres
        function validateField(input, fieldName) {
            const value = input.value.trim();
            const maxLength = fieldName === 'siglas' ? 10 : 254; // Longitud máxima según el campo

            // Verificar longitud
            if (value.length > maxLength) {
                valid = false;
                errorMessage += `${fieldName.charAt(0).toUpperCase() + fieldName.slice(1)} no debe exceder ${maxLength} caracteres.<br>`;
            }

            // Verificar caracteres especiales (permitir letras, números y espacios)
            if (!/^[\w\s]*$/.test(value)) {
                valid = false;
                errorMessage += `El campo ${fieldName} no debe contener caracteres especiales como @, &, *, etc.<br>`;
            }
        }

        // Validar cada campo
        validateField(siglasInput, 'siglas');
        validateField(nombreInput, 'nombre');
        validateField(catedraInput, 'catedra');

        // Si hay errores, prevenir el envío del formulario y mostrar los mensajes
        if (!valid) {
            event.preventDefault(); // Previene el envío del formulario
            errorContainer.innerHTML = errorMessage; // Muestra los mensajes de error
            errorContainer.classList.remove("d-none"); // Muestra el contenedor
        }
    });
});
