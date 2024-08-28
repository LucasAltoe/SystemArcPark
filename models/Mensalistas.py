from dataclasses import dataclass
from datetime import date


@dataclass
class Mensalistas:
    IdMensalista: int
    Nome: str
    Contato: str
    InicioContrato: date
    FimContrato: date
    ValorMensal: float
    Placa: str
    Vagas: int
    IdEstacionamento: int
    QRCodePath: str

    def __init__(
        self,
        IdMensalista: int,
        Nome: str,
        Contato: str,
        InicioContrato: date,
        FimContrato: date,
        ValorMensal: float,
        Placa: str,
        Vagas: int,
        IdEstacionamento: int,
        QRCodePath: str,
    ):
        self.IdMensalista = IdMensalista
        self.Nome = Nome
        self.Contato = Contato
        self.InicioContrato = InicioContrato
        self.FimContrato = FimContrato
        self.ValorMensal = ValorMensal
        self.Placa = Placa
        self.Vagas = Vagas
        self.IdEstacionamento = IdEstacionamento
        self.QRCodePath = QRCodePath