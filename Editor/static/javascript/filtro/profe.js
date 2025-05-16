// Función principal para asignar profesores a la columna
function asignarProfesores() {
    // Obtener todas las filas de la tabla (clases)
    const filas = document.querySelectorAll('tbody tr');
    
    filas.forEach(fila => {
        // Obtener el número de clase (de la primera celda)
        const clase = fila.cells[0].textContent.trim().charAt(0); // "1ª" -> "1"
        
        // Celda de profesores (última celda)
        const celdaProfesores = fila.cells[fila.cells.length - 1];
        celdaProfesores.innerHTML = ''; // Limpiar contenido previo
        
        // Array para profesores únicos
        const profesoresUnicos = new Set();
        
        // Recorrer celdas de días (excluyendo primera y última celda)
        for (let i = 1; i < fila.cells.length - 1; i++) {
            const celdasTurno = fila.cells[i].querySelectorAll('div.mb-1');
            
            celdasTurno.forEach(turno => {
                // Extraer asignatura y tipo del turno
                const contenido = turno.textContent.trim();
                const [asignaturaTipo, local] = contenido.split('\n');
                const [asignatura, tipo] = asignaturaTipo.split(' - ');
                
                // Buscar profesores que coincidan (usando data attributes)
                const profesores = document.querySelectorAll(
                    `[data-asignatura="${asignatura.trim()}"][data-tipo="${tipo.trim()}"]`
                );
                
                profesores.forEach(profesor => {
                    profesoresUnicos.add(profesor.textContent.trim());
                });
            });
        }
        
        // Mostrar profesores en la celda
        if (profesoresUnicos.size > 0) {
            profesoresUnicos.forEach(profesor => {
                const divProfesor = document.createElement('div');
                divProfesor.className = 'mb-1';
                divProfesor.textContent = profesor;
                celdaProfesores.appendChild(divProfesor);
            });
        } else {
            const span = document.createElement('span');
            span.className = 'text-muted';
            span.textContent = 'Sin profesor asignado';
            celdaProfesores.appendChild(span);
        }
    });
}

// Ejecutar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // También ejecutar cuando haya cambios (opcional)
    const observer = new MutationObserver(asignarProfesores);
    observer.observe(document.body, { 
        childList: true, 
        subtree: true 
    });
    
    // Ejecutar inicialmente
    asignarProfesores();
});