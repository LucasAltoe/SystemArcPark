import pytz
from datetime import datetime

def hora_brasil():
    # Definir o fuso horário para São Paulo
    sao_paulo = pytz.timezone('America/Sao_Paulo')

    # Obter a data e hora atual no fuso horário de São Paulo
    data_hora_atual = datetime.now(sao_paulo)

    # Formatar a data e hora como uma string
    data_hora_formatada = data_hora_atual.strftime("%d/%m/%Y %H:%M")

    return data_hora_formatada

