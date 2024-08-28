document.addEventListener('DOMContentLoaded', function () {
  const ocupacaoCarrosCanvas = document.getElementById('OcupacaoCarros');
  const ocupacaoCarrosPercent = parseFloat(ocupacaoCarrosCanvas.getAttribute('data-ocupacao'));

  // Cálculo para o gráfico de carros
  const ocupacaoC = ocupacaoCarrosPercent * 100;
  
  // Criação do gráfico de setores CARROS
  const OcCarros = document.getElementById('OcupacaoCarros').getContext('2d');
  const OcupacaoCarros = new Chart(OcCarros, {
    type: 'pie',
    data: {
      labels: ['Ocupado', 'Vazio'],
      datasets: [{
        data: [ocupacaoC, 100 - ocupacaoC],
        backgroundColor: ['#35C15A', '#E6E8E6']
      }]
    },
    options: chartOptions
  });

  const ocupacaoMotosCanvas = document.getElementById('OcupacaoMotos');
  const ocupacaoMotosPercent = parseFloat(ocupacaoMotosCanvas.getAttribute('data-ocupacao'));

  // Cálculo para o gráfico de motos
  const ocupacaoM = ocupacaoMotosPercent * 100;
  
  // Criação do gráfico de setores MOTOS
  const OcMotos = document.getElementById('OcupacaoMotos').getContext('2d');
  const OcupacaoMotos = new Chart(OcMotos, {
    type: 'pie',
    data: {
      labels: ['Ocupado', 'Vazio'],
      datasets: [{
        data: [ocupacaoM, 100 - ocupacaoM],
        backgroundColor: ['#3772FF', '#E6E8E6']
      }]
    },
    options: chartOptions
  });

  const ocupacaoTotalCanvas = document.getElementById('OcupacaoTotal');
  const ocupacaoTotalPercent = parseFloat(ocupacaoTotalCanvas.getAttribute('data-ocupacao'));

  // Cálculo para o gráfico de ocupação total
  const ocupacaoTotal = ocupacaoTotalPercent * 100;
  
  // Criação do gráfico de setores OCUPAÇÃO TOTAL
  const OcTotal = document.getElementById('OcupacaoTotal').getContext('2d');
  const OcupacaoTotal = new Chart(OcTotal, {
    type: 'pie',
    data: {
      labels: ['Ocupado', 'Vazio'],
      datasets: [{
        data: [ocupacaoTotal, 100 - ocupacaoTotal],
        backgroundColor: ['#DF2935', '#E6E8E6']
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