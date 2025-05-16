// static/javascript/reloj.js

function resaltarHoraActual() {
    const ahora = new Date();
    const horas = ahora.getHours();
    const minutos = ahora.getMinutes();
    const horaActual = horas * 60 + minutos; // Convertir a minutos totales

    // Definir los rangos de horarios en minutos
    const horarios = [
        { inicio: 8 * 60, fin: 9 * 60 + 20 },   // 8:00 - 9:20
        { inicio: 9 * 60 + 30, fin: 10 * 60 + 50 }, // 9:30 - 10:50
        { inicio: 11 * 60, fin: 12 * 60 + 20 }, // 11:00 - 12:20
        { inicio: 12 * 60 + 30, fin: 13 * 60 + 50 }, // 12:30 - 1:50
        { inicio: 14 * 60, fin: 15 * 60 + 20 }, // 2:00 - 3:20
        { inicio: 15 * 60 + 30, fin: 16 * 60 + 50 } // 3:30 - 4:50
    ];

    // Encontrar qué rango de horario coincide con la hora actual
    let claseActual = -1;
    horarios.forEach((horario, index) => {
        if (horaActual >= horario.inicio && horaActual <= horario.fin) {
            claseActual = index + 1; // +1 porque las clases empiezan en 1
        }
    });

    // Si estamos en un horario de clase, resaltar la fila correspondiente
    if (claseActual > 0) {
        const tablas = document.querySelectorAll('.table');
        tablas.forEach(tabla => {
            const filas = tabla.querySelectorAll('tbody tr');
            filas.forEach((fila, index) => {
                // index + 1 porque la primera fila es la clase 1
                if (index + 1 === claseActual) {
                    fila.classList.add('table-active');
                } else {
                    fila.classList.remove('table-active');
                }
            });
        });
    }
}

// Ejecutar al cargar la página y cada minuto para actualizar
document.addEventListener('DOMContentLoaded', function() {
    resaltarHoraActual();
    setInterval(resaltarHoraActual, 60000); // Actualizar cada minuto
});