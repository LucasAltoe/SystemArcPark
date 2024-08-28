from typing import List
from models.Cliente import Cliente
from util.Database import Database


class ClienteRepo:
    @classmethod
    def createTable(cls):
        sql = """CREATE TABLE IF NOT EXISTS Cliente (
                IdCliente INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL,
                CPF_CNPJ TEXT NOT NULL,
                Email TEXT NOT NULL,
                Contato TEXT NOT NULL,
                Senha TEXT NOT NULL,
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
    def insert(cls, cliente: Cliente) -> Cliente:
        sql = "INSERT INTO Cliente (Nome, CPF_CNPJ, Email, Contato, Senha) VALUES (?, ?, ?, ?, ?)"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(
            sql,
            (
                cliente.Nome,
                cliente.CPF_CNPJ,
                cliente.Email,
                cliente.Contato,
                cliente.Senha
            ),
        )
        if result.rowcount > 0:
            cliente.IdCliente = result.lastrowid
            conn.commit()
        conn.close()
        return cliente

    @classmethod
    def update(cls, cliente: Cliente) -> Cliente:
        sql = "UPDATE Cliente SET Nome=?, CPF_CNPJ=?, Email=?, Contato=?, Senha=? WHERE IdCliente=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(
            sql,
            (
                cliente.Nome,
                cliente.CPF_CNPJ,
                cliente.Email,
                cliente.Contato,
                cliente.Senha,
                cliente.IdCliente
            )
        )
        if result.rowcount > 0:
            conn.commit()
            conn.close()
            return cliente
        else:
            conn.close()
            return None
        
    @classmethod
    def updateSenha(cls, id: int, senha: str) -> bool:
        sql = "UPDATE Cliente SET Senha=? WHERE IdCliente=?"
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
        sql = "UPDATE Cliente SET token=? WHERE Email=?"
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
    def emailExists(cls, email: str) -> bool:
        sql = "SELECT EXISTS (SELECT 1 FROM Cliente WHERE Email=?)"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email,)).fetchone()        
        return bool(resultado[0])

    @classmethod
    def getSenhaDeEmail(cls, email: str) -> str | None:
        sql = "SELECT Senha FROM Cliente WHERE Email=?"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email,)).fetchone()
        if resultado:
            return str(resultado[0])
        else:
            return None

    @classmethod
    def delete(cls, id: int) -> bool:
        sql = "DELETE FROM Cliente WHERE IdCliente=?"
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
    def getAll(cls) -> List[Cliente]:
        sql = "SELECT IdCliente, Nome, CPF_CNPJ, Email, Contato, Senha FROM Cliente"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql).fetchall()
        objects = [Cliente(*x) for x in result]
        return objects

    @classmethod
    def getOne(cls, id: int) -> Cliente:
        sql = "SELECT IdCliente, Nome, CPF_CNPJ, Email, Contato, Senha FROM Cliente WHERE IdCliente=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (id, )).fetchone()
        if result:
            object = Cliente(*result)
            return object
        else:
            return None
        
    @classmethod
    def getSenhaDeEmail(cls, email: str) -> str | None:
        sql = "SELECT Senha FROM Cliente WHERE Email=?"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email,)).fetchone()
        if resultado:
            return str(resultado[0])
        else:
            return None

    @classmethod
    def getUserByToken(cls, token: str) -> Cliente:
        sql = "SELECT IdCliente, Nome, CPF_CNPJ, Email, Contato, Senha FROM Cliente WHERE token=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        # quando se executa fechone em um cursor sem resultado, ele retorna None
        resultado = cursor.execute(sql, (token,)).fetchone()
        if resultado:
            objeto = Cliente(*resultado)
            return objeto
        else:
            return None

