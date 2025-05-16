// static/javascript/edicion/disponibilidad.js

class DisponibilidadChecker {
    constructor(semanaActual, horarioId = null) {
        this.semanaActual = semanaActual;
        this.horarioId = horarioId;
        this.cache = new Map();
        this.pendingRequests = new Map();
    }

    async verificar(localId, dia, clase, grupoId) {
        // Primero verificar en los datos precargados
        if (window.CONFIG.turnosOcupados) {
            const ocupadoPrecargado = window.CONFIG.turnosOcupados.some(turno => 
                turno.local == localId && 
                turno.dia == dia && 
                turno.clase == clase
            );
            
            if (ocupadoPrecargado) return true;
        }

        // Si no está en los datos precargados, verificar remoto
        return await this._verificarRemoto(localId, dia, clase, grupoId);
    }

    async _verificarRemoto(localId, dia, clase, grupoId) {
        const cacheKey = `${localId}-${dia}-${clase}-${grupoId}-${this.semanaActual}`;
        
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        if (this.pendingRequests.has(cacheKey)) {
            return this.pendingRequests.get(cacheKey);
        }

        const requestPromise = this._fetchDisponibilidad(localId, dia, clase, grupoId)
            .then(data => {
                this.cache.set(cacheKey, data.ocupado);
                this.pendingRequests.delete(cacheKey);
                return data.ocupado;
            });

        this.pendingRequests.set(cacheKey, requestPromise);
        return requestPromise;
    }

    async _fetchDisponibilidad(localId, dia, clase, grupoId) {
        try {
            const response = await fetch('/verificar-disponibilidad/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this._getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    local_id: localId,
                    dia: dia,
                    clase: clase,
                    grupo_id: grupoId,
                    semana: this.semanaActual,
                    horario_id: this.horarioId
                })
            });
            
            if (!response.ok) throw new Error('Error en la respuesta');
            return await response.json();
        } catch (error) {
            console.error('Error al verificar disponibilidad:', error);
            return { ocupado: false };
        }
    }

    _getCookie(name) {
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
}

function mostrarErrorDisponibilidad(cell, selector) {
    cell.classList.add('celda-error');
    selector.classList.add('select-error');
    
    // Verificar si ya existe un mensaje de error
    if (!cell.querySelector('.mensaje-error-dinamico')) {
        const mensajeError = document.createElement('div');
        mensajeError.className = 'mensaje-error mensaje-error-dinamico';
        mensajeError.textContent = 'Local ocupado para ese momento';
        cell.appendChild(mensajeError);
    }
}

function limpiarErroresDisponibilidad(cell, selector) {
    cell.classList.remove('celda-error');
    selector.classList.remove('select-error');
    const mensajesError = cell.querySelectorAll('.mensaje-error-dinamico');
    mensajesError.forEach(msg => msg.remove());
}

function initDisponibilidadVerification(semanaActual, horarioId = null) {
    const checker = new DisponibilidadChecker(semanaActual, horarioId);
    
    document.querySelectorAll('.local-selector').forEach(selector => {
        selector.addEventListener('change', async function() {
            const localId = this.value;
            const cell = this.closest('td');
            const dia = cell.dataset.dia;
            const clase = cell.dataset.clase;
            const grupoId = this.name.match(/turnos\[(\d+)\]/)[1];
            
            limpiarErroresDisponibilidad(cell, this);
            
            if (!localId) return;
            
            const ocupado = await checker.verificar(localId, dia, clase, grupoId);
            
            if (ocupado) {
                mostrarErrorDisponibilidad(cell, this);
            }
        });
    });
}