from dataclasses import dataclass

@dataclass
class Operadores:
    IdOperador: int
    Nome: str
    CPF: str
    Contato: str
    Senha: str
    IdEstacionamento: int

    def __init__(
        self,
        IdOperador: int,
        Nome: str,
        CPF: str,
        Contato: str,
        Senha: str,
        IdEstacionamento: int
    ):
        self.IdOperador = IdOperador
        self.Nome = Nome
        self.CPF = CPF
        self.Contato = Contato
        self.Senha = Senha
        self.IdEstacionamento = IdEstacionamento
