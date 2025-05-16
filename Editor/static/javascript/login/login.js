// static/javascript/login/login.js

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');

    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            // Limpia errores previos
            clearErrors();

            // Validación
            let isValid = true;

            if (!usernameInput.value.trim()) {
                showError(usernameInput, 'El usuario es obligatorio');
                isValid = false;
            } else if (usernameInput.value.trim().length < 4) {
                showError(usernameInput, 'Mínimo 4 caracteres');
                isValid = false;
            }

            if (!passwordInput.value.trim()) {
                showError(passwordInput, 'La contraseña es obligatoria');
                isValid = false;
            } else if (passwordInput.value.trim().length < 8) {
                showError(passwordInput, 'Mínimo 8 caracteres');
                isValid = false;
            }

            if (!isValid) {
                event.preventDefault(); // Detiene el envío del formulario
            }
        });

        // Función para mostrar errores
        function showError(input, message) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback d-block';
            errorDiv.textContent = message;
            
            // Añade estilos de error al input
            input.classList.add('is-invalid');
            
            // Inserta el mensaje después del input
            input.parentNode.appendChild(errorDiv);
        }

        // Función para limpiar errores
        function clearErrors() {
            // Elimina mensajes de error
            document.querySelectorAll('.invalid-feedback').forEach(el => el.remove());
            
            // Remueve estilos de error
            document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
        }

        // Validación en tiempo real (opcional)
        usernameInput.addEventListener('input', () => {
            if (usernameInput.value.trim().length >= 4) {
                usernameInput.classList.remove('is-invalid');
            }
        });

        passwordInput.addEventListener('input', () => {
            if (passwordInput.value.trim().length >= 8) {
                passwordInput.classList.remove('is-invalid');
            }
        });
    }
});