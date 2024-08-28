from dataclasses import dataclass
from datetime import time
from typing import Optional


@dataclass
class Estacionamento:
    IdEstacionamento: int
    Nome: str
    CNPJ: str
    Email: str
    CEP: str
    Endereco: str
    Senha: str
    DomingoInicio: str
    DomingoFim: str
    SegundaInicio: str
    SegundaFim: str
    TercaInicio: str
    TercaFim: str
    QuartaInicio: str
    QuartaFim: str
    QuintaInicio: str
    QuintaFim: str
    SextaInicio: str
    SextaFim: str
    SabadoInicio: str
    SabadoFim: str
    NumeroVagas: int
    admin: Optional[bool] = True
    token: Optional[str] = ""

    def __init__(
        self,
        IdEstacionamento: int,
        Nome: str,
        CNPJ: str,
        Email: str,
        CEP: str,
        Endereco: str,
        Senha: str,
        DomingoInicio: str,
        DomingoFim: str,
        SegundaInicio: str,
        SegundaFim: str,
        TercaInicio: str,
        TercaFim: str,
        QuartaInicio: str,
        QuartaFim: str,
        QuintaInicio: str,
        QuintaFim: str,
        SextaInicio: str,
        SextaFim: str,
        SabadoInicio: str,
        SabadoFim: str,
        NumeroVagas: int,
        admin: Optional[bool] = True,
        token: Optional[str] = ""
    ):
        self.IdEstacionamento = IdEstacionamento
        self.Nome = Nome
        self.CNPJ = CNPJ
        self.Email = Email
        self.CEP = CEP
        self.Endereco = Endereco
        self.Senha = Senha
        self.DomingoInicio = DomingoInicio
        self.DomingoFim = DomingoFim
        self.SegundaInicio = SegundaInicio
        self.SegundaFim = SegundaFim
        self.TercaInicio = TercaInicio
        self.TercaFim = TercaFim
        self.QuartaInicio = QuartaInicio
        self.QuartaFim = QuartaFim
        self.QuintaInicio = QuintaInicio
        self.QuintaFim = QuintaFim
        self.SextaInicio = SextaInicio
        self.SextaFim = SextaFim
        self.SabadoInicio = SabadoInicio
        self.SabadoFim = SabadoFim
        self.NumeroVagas = NumeroVagas
        self.admin = admin
        self.token = token

