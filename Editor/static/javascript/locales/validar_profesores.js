document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form"); // Selecciona el formulario
    const nombreInput = document.querySelector("input[name='nombre']"); // Campo de nombre
    const asignaturaSelect = document.querySelector("select[name='asignatura']"); // Campo de asignatura
    const errorContainer = document.createElement("div"); // Crea un contenedor para los errores
    errorContainer.classList.add("alert", "alert-danger", "d-none"); // Clases de Bootstrap para el estilo
    form.insertBefore(errorContainer, form.firstChild); // Inserta el contenedor antes del formulario

    form.addEventListener("submit", function(event) {
        let valid = true; // Variable para rastrear la validez del formulario
        let errorMessage = "";

        // Limpiar mensajes de error anteriores
        errorContainer.innerHTML = "";
        errorContainer.classList.add("d-none"); // Ocultar el contenedor inicialmente

        // Validación del campo 'nombre'
        const nombreValue = nombreInput.value.trim();
        
        // Verificar longitud
        if (nombreValue.length > 253) {
            valid = false;
            errorMessage += "El nombre no debe exceder 253 caracteres.<br>";
        }

        // Verificar caracteres permitidos (solo letras y espacios)
        if (!/^[A-Za-z\s]*$/.test(nombreValue)) {
            valid = false;
            errorMessage += "El campo nombre no debe contener caracteres especiales ni números.<br>";
        }

        // Validación del campo 'asignatura'
        if (asignaturaSelect.value === "none") { // Asegúrate de que la opción por defecto tenga el valor "none"
            valid = false;
            errorMessage += "Debes seleccionar una asignatura.<br>";
        }

        // Si hay errores, prevenir el envío del formulario y mostrar los mensajes
        if (!valid) {
            event.preventDefault(); // Previene el envío del formulario
            errorContainer.innerHTML = errorMessage; // Muestra los mensajes de error
            errorContainer.classList.remove("d-none"); // Muestra el contenedor
        }
    });
});
