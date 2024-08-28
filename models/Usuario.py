from dataclasses import dataclass


@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    admin: bool = False


    def __init__(
        self,
        id: int,
        nome: str,
        email: str,
        admin: bool = False
    ):
        self.id = id
        self.nome = nome
        self.email = email
        self.admin = admin