from typing import List
from models.Mensalistas import Mensalistas
from util.Database import Database


class MensalistasRepo:

    @classmethod
    def createTable(cls):
        sql = """CREATE TABLE IF NOT EXISTS Mensalistas (
                IdMensalista INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL,
                Contato TEXT NOT NULL,
                InicioContrato DATE NOT NULL,
                FimContrato DATE NOT NULL,
                ValorMensal REAL NOT NULL,
                Placa TEXT NOT NULL,
                Vagas INTEGER NOT NULL,
                IdEstacionamento INTEGER NOT NULL,
                QRCodePath TEXT,
                CONSTRAINT fkIdEstacionamento FOREIGN KEY (IdEstacionamento) REFERENCES Estacionamento(IdEstacionamento)
                )"""

        conn = Database.createConnection()
        cursor = conn.cursor()
        tableCreated = (cursor.execute(sql).rowcount > 0)
        conn.commit()
        conn.close()
        return tableCreated

    @classmethod
    def insert(cls, mensalistas: Mensalistas) -> Mensalistas:
        sql = "INSERT INTO Mensalistas (Nome, Contato, InicioContrato, FimContrato, ValorMensal, Placa, Vagas, IdEstacionamento, QRCodePath) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (mensalistas.Nome, mensalistas.Contato, mensalistas.InicioContrato, mensalistas.FimContrato, mensalistas.ValorMensal, mensalistas.Placa, mensalistas.Vagas, mensalistas.IdEstacionamento, mensalistas.QRCodePath))
        if result.rowcount > 0:
            mensalistas.IdMensalista = result.lastrowid
        conn.commit()
        conn.close()
        return mensalistas

    @classmethod
    def update(cls, mensalistas: Mensalistas) -> Mensalistas:
        sql = "UPDATE Mensalistas SET Nome=?, Contato=?, InicioContrato=?, FimContrato=?, ValorMensal=?, Placa=?, Vagas=?, IdEstacionamento=?, QRCodePath=? WHERE IdMensalista=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (mensalistas.Nome, mensalistas.Contato, mensalistas.InicioContrato, mensalistas.FimContrato, mensalistas.ValorMensal, mensalistas.Placa, mensalistas.Vagas, mensalistas.IdEstacionamento, mensalistas.QRCodePath, mensalistas.IdMensalista))
        if result.rowcount > 0:
            conn.commit()
            conn.close()
            return mensalistas
        else:
            conn.close()
            return None

    @classmethod
    def delete(cls, id: int) -> bool:
        sql = "DELETE FROM Mensalistas WHERE IdMensalista=?"
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
    def getAll(cls) -> List[Mensalistas]:
        sql = "SELECT IdMensalista, Nome, Contato, InicioContrato, FimContrato, ValorMensal, Placa, Vagas, IdEstacionamento, QRCodePath FROM Mensalistas"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql,).fetchall()
        objects = [Mensalistas(*x) for x in result]
        conn.close()
        return objects
    
    
    @classmethod
    def getAllById(cls, id: int) -> List[Mensalistas]:
        sql = "SELECT IdMensalista, Nome, Contato, InicioContrato, FimContrato, ValorMensal, Placa, Vagas, IdEstacionamento, QRCodePath FROM Mensalistas WHERE IdEstacionamento = ?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (id,)).fetchall()
        objects = [Mensalistas(*x) for x in result]
        conn.close()
        return objects
    

    @classmethod
    def getPage(cls, id: int, pagina: int, tamanhoPagina: int) -> List[Mensalistas]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = "SELECT IdMensalista, Nome, Contato, InicioContrato, FimContrato, ValorMensal, Placa, Vagas, IdEstacionamento, QRCodePath FROM Mensalistas WHERE IdEstacionamento = ? ORDER BY Nome LIMIT ? , ?"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, inicio, tamanhoPagina)).fetchall()
        objetos = [Mensalistas(*x) for x in resultado]
        return objetos
    
    @classmethod
    def getTotalPages(cls, id: int, tamanhoPagina: int) -> int:
        sql = "SELECT CEIL(CAST((SELECT COUNT(*) FROM Mensalistas WHERE IdEstacionamento = ?) AS FLOAT) / ?) AS qtdePaginas"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, tamanhoPagina, )).fetchone()
        return int(resultado[0])
    

    @classmethod
    def getOne(cls, id: int) -> Mensalistas:
        sql = "SELECT IdMensalista, Nome, Contato, InicioContrato, FimContrato, ValorMensal, Placa, Vagas, IdEstacionamento, QRCodePath FROM Mensalistas WHERE IdMensalista=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (id, )).fetchone()
        if result:
            object = Mensalistas(*result)
            conn.close()
            return object
        else:
            conn.close()
            return None

