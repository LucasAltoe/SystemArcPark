from dataclasses import dataclass
from datetime import date

@dataclass
class TabelaPreco:
    IdTabelaPreco: int
    NomeTabela: str
    DataCadastro: date
    PrimeiraHoraCarro: float
    PrimeiraHoraMoto: float
    FracaoCarro: float
    FracaoMoto: float
    IdEstacionamento: int

    def __init__(
        self,
        IdTabelaPreco: int,
        NomeTabela: str,
        DataCadastro: date,
        PrimeiraHoraCarro: float,
        PrimeiraHoraMoto: float,
        FracaoCarro: float,
        FracaoMoto: float,
        IdEstacionamento: int
    ):
        self.IdTabelaPreco = IdTabelaPreco
        self.NomeTabela = NomeTabela
        self.DataCadastro = DataCadastro
        self.PrimeiraHoraCarro = PrimeiraHoraCarro
        self.PrimeiraHoraMoto = PrimeiraHoraMoto
        self.FracaoCarro = FracaoCarro
        self.FracaoMoto = FracaoMoto
        self.IdEstacionamento = IdEstacionamento

