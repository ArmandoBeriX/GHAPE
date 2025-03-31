document.addEventListener('DOMContentLoaded', () => {
    const { turnosOcupados, semanaActual } = window.CONFIG;

    const resetErrores = () => {
        document.querySelectorAll('.celda-colision').forEach(c => c.classList.remove('celda-colision'));
        document.querySelectorAll('.error-colision').forEach(e => e.remove());
    };

    const crearError = (mensaje, tabla) => {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-colision';
        errorDiv.innerHTML = `
            <i class="fas fa-exclamation-triangle"></i>
            ${mensaje}
        `;
        tabla.parentNode.insertBefore(errorDiv, tabla.nextSibling);
    };

    document.querySelectorAll('.local-selector').forEach(select => {
        select.addEventListener('change', function(e) {
            resetErrores();
            
            const localId = parseInt(this.value);
            if (!localId) return;

            const celda = this.closest('td');
            const dia = parseInt(celda.dataset.dia);
            const clase = parseInt(celda.dataset.clase);
            const tabla = celda.closest('table');

            const colision = turnosOcupados.some(t => 
                t.local_id === localId &&
                t.dia === dia &&
                t.clase === clase
            );

            if (colision) {
                celda.classList.add('celda-colision');
                crearError(
                    `Conflicto en clase ${clase}, ${diaToNombre(dia)}: 
                    Local ya ocupado en la semana ${semanaActual}.`,
                    tabla
                );
            }
        });
    });

    const diaToNombre = (dia) => {
        const nombres = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'];
        return nombres[dia - 1] || `Día ${dia}`;
    };
});