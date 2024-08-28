from typing import List
from models.TabelaPreco import TabelaPreco
from util.Database import Database


class TabelaPrecoRepo:
    @classmethod
    def createTable(cls):
        sql = """CREATE TABLE IF NOT EXISTS TabelaPreco (
                IdTabelaPreco INTEGER PRIMARY KEY AUTOINCREMENT,
                NomeTabela TEXT NOT NULL,
                DataCadastro DATE NOT NULL,
                PrimeiraHoraCarro REAL NOT NULL,
                PrimeiraHoraMoto REAL NOT NULL,
                FracaoCarro REAL NOT NULL,
                FracaoMoto REAL NOT NULL,
                IdEstacionamento INTEGER NOT NULL,
                CONSTRAINT fkIdEstacionamento FOREIGN KEY (IdEstacionamento) REFERENCES Estacionamento(IdEstacionamento)
                )"""

        conn = Database.createConnection()
        cursor = conn.cursor()
        tableCreated = (cursor.execute(sql).rowcount > 0)
        conn.commit()
        conn.close()
        return tableCreated

    @classmethod
    def insert(cls, tabela: TabelaPreco) -> TabelaPreco:
        sql = "INSERT INTO TabelaPreco (NomeTabela, DataCadastro, PrimeiraHoraCarro, PrimeiraHoraMoto, FracaoCarro, FracaoMoto, IdEstacionamento) VALUES (?, ?, ?, ?, ?, ?, ?)"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (tabela.NomeTabela, tabela.DataCadastro, tabela.PrimeiraHoraCarro, tabela.PrimeiraHoraMoto, tabela.FracaoCarro, tabela.FracaoMoto, tabela.IdEstacionamento))
        if result.rowcount > 0:
            tabela.id = result.lastrowid
        conn.commit()
        conn.close()
        return tabela

    @classmethod
    def update(cls, tabela: TabelaPreco) -> TabelaPreco:
        sql = "UPDATE TabelaPreco SET NomeTabela=?, DataCadastro=?, PrimeiraHoraCarro=?, PrimeiraHoraMoto=?, FracaoCarro=?, FracaoMoto=?, IdEstacionamento=? WHERE IdTabelaPreco=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (tabela.NomeTabela, tabela.DataCadastro, tabela.PrimeiraHoraCarro, tabela.PrimeiraHoraMoto, tabela.FracaoCarro, tabela.FracaoMoto, tabela.IdEstacionamento, tabela.IdTabelaPreco))
        if result.rowcount > 0:
            conn.commit()
            conn.close()
            return tabela
        else:
            conn.close()
            return None

    @classmethod
    def delete(cls, id: int) -> bool:
        sql = "DELETE FROM TabelaPreco WHERE IdTabelaPreco=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (id, ))
        if result.rowcount > 0:
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False
    
    @classmethod
    def getAllForSelect(cls, id: int) -> List[TabelaPreco]:
        sql = "SELECT TabelaPreco.IdTabelaPreco, TabelaPreco.NomeTabela, TabelaPreco.DataCadastro, TabelaPreco.PrimeiraHoraCarro, TabelaPreco.PrimeiraHoraMoto, TabelaPreco.FracaoCarro, TabelaPreco.FracaoMoto, TabelaPreco.IdEstacionamento FROM TabelaPreco WHERE TabelaPreco.IdEstacionamento = ?"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id,)).fetchall()
        objetos = [TabelaPreco(IdTabelaPreco=x[0], NomeTabela=x[1], DataCadastro=x[2], PrimeiraHoraCarro=x[3], PrimeiraHoraMoto=x[4], FracaoCarro=x[5], FracaoMoto=x[6], IdEstacionamento=x[7]) for x in resultado]
        return objetos


    @classmethod
    def getOne(cls, id: int) -> TabelaPreco:
        sql = "SELECT IdTabelaPreco, NomeTabela, DataCadastro, PrimeiraHoraCarro, PrimeiraHoraMoto, FracaoCarro, FracaoMoto, IdEstacionamento FROM TabelaPreco WHERE IdTabelaPreco=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (id, )).fetchone()
        if result is None:
            return None
        else:
            tabela = TabelaPreco(*result)
            return tabela
