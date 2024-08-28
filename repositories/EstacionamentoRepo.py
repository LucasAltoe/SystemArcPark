from typing import List
from models.Estacionamento import Estacionamento
from util.Database import Database


class EstacionamentoRepo:
    @classmethod
    def createTable(cls):
        sql = """CREATE TABLE IF NOT EXISTS Estacionamento (
                IdEstacionamento INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL,
                CNPJ TEXT NOT NULL,
                Email TEXT NOT NULL,
                CEP TEXT NOT NULL,
                Endereco TEXT NOT NULL,
                Senha TEXT NOT NULL,
                DomingoInicio TEXT NULL,
                DomingoFim TEXT NULL,
                SegundaInicio TEXT NULL,
                SegundaFim TEXT NULL,
                TercaInicio TEXT NULL,
                TercaFim TEXT NULL,
                QuartaInicio TEXT NULL,
                QuartaFim TEXT NULL,
                QuintaInicio TEXT NULL,
                QuintaFim TEXT NULL,
                SextaInicio TEXT NULL,
                SextaFim TEXT NULL,
                SabadoInicio TEXT NULL,
                SabadoFim TEXT NULL,
                NumeroVagas INTEGER NULL,
                admin BOOLEAN NOT NULL DEFAULT 1,
                token TEXT,
                UNIQUE (Email))
                """

        conn = Database.createConnection()
        cursor = conn.cursor()
        tableCreated = (cursor.execute(sql).rowcount > 0)
        conn.commit()
        conn.close()
        return tableCreated

    @classmethod
    def insert(cls, estacionamento: Estacionamento) -> Estacionamento:
        sql = "INSERT INTO Estacionamento (Nome, CNPJ, Email, CEP, Endereco, Senha, DomingoInicio, DomingoFim, SegundaInicio, SegundaFim, TercaInicio, TercaFim, QuartaInicio, QuartaFim, QuintaInicio, QuintaFim, SextaInicio, SextaFim, SabadoInicio, SabadoFim, NumeroVagas) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(
            sql,
            (
                estacionamento.Nome,
                estacionamento.CNPJ,
                estacionamento.Email,
                estacionamento.CEP,
                estacionamento.Endereco,
                estacionamento.Senha,
                estacionamento.DomingoInicio,
                estacionamento.DomingoFim,
                estacionamento.SegundaInicio,
                estacionamento.SegundaFim,
                estacionamento.TercaInicio,
                estacionamento.TercaFim,
                estacionamento.QuartaInicio,
                estacionamento.QuartaFim,
                estacionamento.QuintaInicio,
                estacionamento.QuintaFim,
                estacionamento.SextaInicio,
                estacionamento.SextaFim,
                estacionamento.SabadoInicio,
                estacionamento.SabadoFim,
                estacionamento.NumeroVagas
            ),
        )
        if result.rowcount > 0:
            estacionamento.IdEstacionamento = result.lastrowid
            conn.commit()
        conn.close()
        return estacionamento

    @classmethod
    def update(cls, estacionamento: Estacionamento) -> Estacionamento:
        sql = "UPDATE Estacionamento SET Nome=?, CNPJ=?, Email=?, CEP=?, Endereco=?, Senha=?, DomingoInicio=?, DomingoFim=?, SegundaInicio=?, SegundaFim=?, TercaInicio=?, TercaFim=?, QuartaInicio=?, QuartaFim=?, QuintaInicio=?, QuintaFim=?, SextaInicio=?, SextaFim=?, SabadoInicio=?, SabadoFim=?, NumeroVagas=? WHERE IdEstacionamento=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (estacionamento.Nome, estacionamento.CNPJ, estacionamento.Email, estacionamento.CEP, estacionamento.Endereco, estacionamento.Senha, estacionamento.DomingoInicio, estacionamento.DomingoFim, estacionamento.SegundaInicio, estacionamento.SegundaFim, estacionamento.TercaInicio, estacionamento.TercaFim, estacionamento.QuartaInicio, estacionamento.QuartaFim, estacionamento.QuintaInicio, estacionamento.QuintaFim, estacionamento.SextaInicio, estacionamento.SextaFim, estacionamento.SabadoInicio, estacionamento.SabadoFim, estacionamento.NumeroVagas, estacionamento.IdEstacionamento))
        if result.rowcount > 0:
            conn.commit()
            conn.close()
            return estacionamento
        else:
            conn.close()
            return None
        
    @classmethod
    def updateSenha(cls, id: int, senha: str) -> bool:
        sql = "UPDATE Estacionamento SET Senha=? WHERE IdEstacionamento=?"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (senha, id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False
        
    @classmethod
    def updateToken(cls, email: str, token: str) -> bool:
        sql = "UPDATE Estacionamento SET token=? WHERE Email=?"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (token, email))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False
        
    @classmethod
    def updateAdmin(cls, id: int, admin: bool) -> bool:
        sql = "UPDATE Estacionamento SET admin=? WHERE IdEstacionamento=?"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (admin, id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False
        
    @classmethod
    def emailExists(cls, email: str) -> bool:
        sql = "SELECT EXISTS (SELECT 1 FROM Estacionamento WHERE Email=?)"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email,)).fetchone()        
        return bool(resultado[0])
    
    @classmethod
    def getSenhaDeEmail(cls, email: str) -> str | None:
        sql = "SELECT Senha FROM Estacionamento WHERE Email=?"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email,)).fetchone()
        if resultado:
            return str(resultado[0])
        else:
            return None

    @classmethod
    def delete(cls, id: int) -> bool:
        sql = "DELETE FROM Estacionamento WHERE IdEstacionamento=?"
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
    def getAll(cls) -> List[Estacionamento]:
        sql = "SELECT IdEstacionamento, Nome, CNPJ, Email, CEP, Endereco, Senha, DomingoInicio, DomingoFim, SegundaInicio, SegundaFim, TercaInicio, TercaFim, QuartaInicio, QuartaFim, QuintaInicio, QuintaFim, SextaInicio, SextaFim, SabadoInicio, SabadoFim, NumeroVagas, admin FROM Estacionamento"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql).fetchall()
        objects = [Estacionamento(*x) for x in result]
        return objects

    @classmethod
    def getOne(cls, id: int) -> Estacionamento:
        sql = "SELECT IdEstacionamento, Nome, CNPJ, Email, CEP, Endereco, Senha, DomingoInicio, DomingoFim, SegundaInicio, SegundaFim, TercaInicio, TercaFim, QuartaInicio, QuartaFim, QuintaInicio, QuintaFim, SextaInicio, SextaFim, SabadoInicio, SabadoFim, NumeroVagas, admin FROM Estacionamento WHERE IdEstacionamento=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (id, )).fetchone()
        if result:
            object = Estacionamento(*result)
            return object
        else:
            return None
    
    @classmethod
    def getNumeroVagas(cls, id: int) -> Estacionamento:
        sql = "SELECT NumeroVagas FROM Estacionamento WHERE IdEstacionamento=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (id, )).fetchone()
        if result:
            return int(result[0])
        else:
            return None

    @classmethod
    def getUserByToken(cls, token: str) -> Estacionamento:
        sql = "SELECT IdEstacionamento, Nome, CNPJ, Email, CEP, Endereco, Senha, DomingoInicio, DomingoFim, SegundaInicio, SegundaFim, TercaInicio, TercaFim, QuartaInicio, QuartaFim, QuintaInicio, QuintaFim, SextaInicio, SextaFim, SabadoInicio, SabadoFim, NumeroVagas, admin FROM Estacionamento WHERE token=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        # quando se executa fechone em um cursor sem resultado, ele retorna None
        resultado = cursor.execute(sql, (token,)).fetchone()
        if resultado:
            objeto = Estacionamento(*resultado)
            return objeto
        else:
            return None

