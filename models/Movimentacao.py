from dataclasses import dataclass
from datetime import datetime

@dataclass
class Movimentacao:
    IdMovimentacao: int
    TipoVeiculo: str
    Cliente: str
    DataHoraEntrada: datetime
    DataHoraSaida: datetime
    Preco: float
    IdTabelaPreco: int
    QRCodePath: str
    IdEstacionamento: int

    def __init__(
        self,
        IdMovimentacao: int,
        TipoVeiculo: str,
        Cliente: str,
        DataHoraEntrada: datetime,
        DataHoraSaida: datetime,
        Preco: float,
        IdTabelaPreco: int,
        QRCodePath: str,
        IdEstacionamento: int
    ):
        self.IdMovimentacao = IdMovimentacao
        self.TipoVeiculo = TipoVeiculo
        self.Cliente = Cliente
        self.DataHoraEntrada = DataHoraEntrada
        self.DataHoraSaida = DataHoraSaida
        self.Preco = Preco
        self.IdTabelaPreco = IdTabelaPreco
        self.QRCodePath = QRCodePath
        self.IdEstacionamento = IdEstacionamento

