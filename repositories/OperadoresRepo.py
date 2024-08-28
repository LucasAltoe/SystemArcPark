from typing import List
from models.Operadores import Operadores
from util.Database import Database


class OperadoresRepo:
    @classmethod
    def createTable(cls):
        sql = """CREATE TABLE IF NOT EXISTS Operadores (
                IdOperador INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL,
                CPF TEXT NOT NULL,
                Contato TEXT NOT NULL,
                Senha TEXT NOT NULL,
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
    def insert(cls, operadores: Operadores) -> Operadores:
        sql = "INSERT INTO Operadores (Nome, CPF, Contato, Senha, IdEstacionamento) VALUES (?, ?, ?, ?, ?)"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(
            sql,
            (
                operadores.Nome,
                operadores.CPF,
                operadores.Contato,
                operadores.Senha,
                operadores.IdEstacionamento
            ),
        )
        if result.rowcount > 0:
            operadores.IdOperador = result.lastrowid
            conn.commit()
        conn.close()
        return operadores

    @classmethod
    def update(cls, operadores: Operadores) -> Operadores:
        sql = "UPDATE Operadores SET Nome=?, CPF=?, Contato=?, Senha=?, IdEstacionamento=? WHERE IdOperador=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (operadores.Nome, operadores.CPF, operadores.Contato, operadores.Senha, operadores.IdEstacionamento, operadores.IdOperador))
        if result.rowcount > 0:
            conn.commit()
            conn.close()
            return operadores
        else:
            conn.close()
            return None

    @classmethod
    def delete(cls, id: int) -> bool:
        sql = "DELETE FROM Operadores WHERE IdOperador=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (id,))
        if result.rowcount > 0:
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False

    @classmethod
    def getPage(cls, id: int, pagina: int, tamanhoPagina: int) -> List[Operadores]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = "SELECT IdOperador, Nome, CPF, Contato, Senha, IdEstacionamento FROM Operadores WHERE IdEstacionamento = ? ORDER BY Nome LIMIT ? , ?"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, inicio, tamanhoPagina)).fetchall()
        objetos = [Operadores(*x) for x in resultado]
        return objetos
    
    @classmethod
    def getTotalPages(cls, id: int, tamanhoPagina: int) -> int:
        sql = "SELECT CEIL(CAST((SELECT COUNT(*) FROM Operadores WHERE IdEstacionamento = ?) AS FLOAT) / ?) AS qtdePaginas"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, tamanhoPagina, )).fetchone()
        return int(resultado[0])

    @classmethod
    def getOne(cls, id: int) -> Operadores:
        sql = "SELECT IdOperador, Nome, CPF, Contato, Senha, IdEstacionamento FROM Operadores WHERE IdOperador=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (id,)).fetchone()
        if result is None:
            return None
        else:
            operadores = Operadores(*result)
            return operadores
