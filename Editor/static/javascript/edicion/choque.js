document.addEventListener('DOMContentLoaded', function() {
    // Verificación en tiempo real al cambiar un local
    document.querySelectorAll('.local-selector').forEach(selector => {
        selector.addEventListener('change', async function() {
            const localId = this.value;
            const cell = this.closest('td');
            const dia = cell.dataset.dia;
            const clase = cell.dataset.clase;
            const grupoId = this.name.match(/turnos\[(\d+)\]/)[1];
            
            // Limpiar estado anterior
            cell.classList.remove('celda-error');
            this.classList.remove('select-error');
            const mensajesError = cell.querySelectorAll('.mensaje-error-dinamico');
            mensajesError.forEach(msg => msg.remove());
            
            // Si no hay local seleccionado, no hacer nada
            if (!localId) return;
            
            try {
                // Verificar disponibilidad del local mediante AJAX
                const response = await fetch('/verificar-disponibilidad/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: JSON.stringify({
                        local_id: localId,
                        dia: dia,
                        clase: clase,
                        grupo_id: grupoId,
                        semana: window.CONFIG.semanaActual
                    })
                });
                
                const data = await response.json();
                
                if (data.ocupado) {
                    // Marcar celda y selectores con error
                    cell.classList.add('celda-error');
                    this.classList.add('select-error');
                    
                    // Crear mensaje de error
                    const mensajeError = document.createElement('div');
                    mensajeError.className = 'mensaje-error mensaje-error-dinamico';
                    mensajeError.textContent = 'Local ocupado para ese momento';
                    cell.appendChild(mensajeError);
                }
            } catch (error) {
                console.error('Error al verificar disponibilidad:', error);
            }
        });
    });
});

// Función auxiliar para obtener el token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}