// Numero de Veiculos
document.addEventListener('DOMContentLoaded', function () {
    const numeroVeiculosCanvas = document.getElementById('numeroVeiculos');
    const numeroVeiculosCarro = parseInt(numeroVeiculosCanvas.getAttribute('data-veiculos-carro'));
    const numeroVeiculosMoto = parseInt(numeroVeiculosCanvas.getAttribute('data-veiculos-moto'));

    const labelNumeroVeiculos = ['Carro', 'Moto'];
    const dataNumeroVeiculos = [numeroVeiculosCarro, numeroVeiculosMoto];
    
    const NumVeiculos = document.getElementById('numeroVeiculos').getContext('2d');
    const NumeroVeiculos = new Chart(NumVeiculos, {
        type: 'doughnut',
        data: {
            labels: labelNumeroVeiculos,
            datasets: [{
                data: dataNumeroVeiculos,
                borderWidth: 1,
                backgroundColor: ['#3772FF', '#FDCA40']
            }]
        },
        options: chartOptions
    });

    });


    // Configuração do gráfico de setores
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        tooltips: {
            enabled: false
        }
};


// Lotacao por Hora
document.addEventListener("DOMContentLoaded", function () {
    const lotacaoPorHoraCanvas = document.getElementById('lotacaoPorHora');
    const datalotacaoPorHora = JSON.parse(lotacaoPorHoraCanvas.getAttribute('data-lotacao-hora'));

    const labelslotacaoPorHora = [
        '00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00',
        '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00',
        '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'
    ];

    new Chart(lotacaoPorHoraCanvas, {
        type: 'bar',
        data: {
            labels: labelslotacaoPorHora,
            datasets: [{
                label: 'Lotação (Número de Veículos)',
                data: datalotacaoPorHora,
                borderWidth: 0,
                backgroundColor: '#DF2935'
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});


// Faturamento por Dia
document.addEventListener("DOMContentLoaded", function () {
    const faturamentoPorDiaCanvas = document.getElementById('faturamentoPorDia');
    const labelsFaturamentoPorDia = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'];
    
    const datalotacaoPorDia = JSON.parse(faturamentoPorDiaCanvas.getAttribute('data-faturamento-dia'));

    new Chart(faturamentoPorDiaCanvas, {
        type: 'line',
        data: {
            labels: labelsFaturamentoPorDia,
            datasets: [{
                label: 'Faturamento (R$)',
                data: datalotacaoPorDia,
                borderWidth: 2,
                borderColor: '#26C8AD',
                backgroundColor: '#26C8AD'
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});

