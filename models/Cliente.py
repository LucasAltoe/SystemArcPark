from dataclasses import dataclass
from typing import Optional

@dataclass
class Cliente:
    IdCliente: int
    Nome: str
    CPF_CNPJ: str
    Email: str
    Contato: str
    Senha: str
    token: Optional[str] = ""

    def __init__(
        self,
        IdCliente: int,
        Nome: str,
        CPF_CNPJ: str,
        Email: str,
        Contato: str,
        Senha: str,
        token: Optional[str] = ""
    ):
        self.IdCliente = IdCliente
        self.Nome = Nome
        self.CPF_CNPJ = CPF_CNPJ
        self.Email = Email
        self.Contato = Contato
        self.Senha = Senha
        self.token = token