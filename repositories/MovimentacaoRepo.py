import datetime
from typing import List
from models.Movimentacao import Movimentacao
from util.Database import Database
from datetime import date, datetime

from util.formatarhora import hora_brasil

class MovimentacaoRepo:
    @classmethod
    def createTable(cls):
        sql = """CREATE TABLE IF NOT EXISTS Movimentacao (
                IdMovimentacao INTEGER PRIMARY KEY AUTOINCREMENT,
                TipoVeiculo TEXT NOT NULL,
                Cliente TEXT NOT NULL,
                DataHoraEntrada DATETIME NOT NULL,
                DataHoraSaida DATETIME,
                Preco REAL,
                IdTabelaPreco INTEGER NULL,
                QRCodePath TEXT,
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
    def insert(cls, movimentacao: Movimentacao) -> Movimentacao:
        sql = "INSERT INTO Movimentacao (TipoVeiculo, Cliente, DataHoraEntrada, DataHoraSaida, Preco, IdTabelaPreco, QRCodePath, IdEstacionamento) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (movimentacao.TipoVeiculo, movimentacao.Cliente, movimentacao.DataHoraEntrada, movimentacao.DataHoraSaida, movimentacao.Preco, movimentacao.IdTabelaPreco, movimentacao.QRCodePath, movimentacao.IdEstacionamento))
        if result.rowcount > 0:
            movimentacao.id = result.lastrowid
        conn.commit()
        conn.close()
        return movimentacao

    @classmethod
    def update(cls, movimentacao: Movimentacao) -> Movimentacao:
        sql = "UPDATE Movimentacao SET TipoVeiculo=?, Cliente=?, DataHoraEntrada=?, DataHoraSaida=?, Preco=?, IdTabelaPreco=?, QRCodePath=?, IdEstacionamento=? WHERE IdMovimentacao=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (movimentacao.TipoVeiculo, movimentacao.Cliente, movimentacao.DataHoraEntrada, movimentacao.DataHoraSaida, movimentacao.Preco, movimentacao.IdTabelaPreco, movimentacao.QRCodePath, movimentacao.IdEstacionamento, movimentacao.IdMovimentacao))
        if result.rowcount > 0:
            conn.commit()
            conn.close()
            return movimentacao
        else:
            conn.close()
            return None

    @classmethod
    def delete(cls, id: int) -> bool:
        sql = "DELETE FROM Movimentacao WHERE IdMovimentacao=?"
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
    def getAll(cls) -> List[Movimentacao]:
        sql = "SELECT IdMovimentacao, TipoVeiculo, Cliente, DataHoraEntrada, DataHoraSaida, Preco, IdTabelaPreco, QRCodePath, IdEstacionamento FROM Movimentacao"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql).fetchall()
        objects = [Movimentacao(*x) for x in result]
        return objects
    
    @classmethod
    def getEntradasById(cls, id: int) -> List[Movimentacao]:
        sql = "SELECT IdMovimentacao, TipoVeiculo, Cliente, DataHoraEntrada, DataHoraSaida, Preco, IdTabelaPreco, QRCodePath, IdEstacionamento FROM Movimentacao WHERE DataHoraSaida IS NULL AND IdEstacionamento = ?"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id,)).fetchall()
        objetos = [Movimentacao(*x) for x in resultado]
        return objetos
    
    @classmethod
    def getSaidasById(cls, id: int) -> List[Movimentacao]:
        sql = "SELECT IdMovimentacao, TipoVeiculo, Cliente, DataHoraEntrada, DataHoraSaida, Preco, IdTabelaPreco, QRCodePath, IdEstacionamento FROM Movimentacao WHERE DataHoraSaida IS NOT NULL AND IdEstacionamento = ?"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id,)).fetchall()
        objetos = [Movimentacao(*x) for x in resultado]
        return objetos

    @classmethod
    def getOne(cls, id: int) -> Movimentacao:
        sql = "SELECT IdMovimentacao, TipoVeiculo, Cliente, DataHoraEntrada, DataHoraSaida, Preco, IdTabelaPreco, QRCodePath, IdEstacionamento FROM Movimentacao WHERE IdMovimentacao=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (id,)).fetchone()
        if result is None:
            return None
        else:
            movimentacao = Movimentacao(*result)
            return movimentacao

    @classmethod
    def getPageEntradas(cls, id: int, pagina: int, tamanhoPagina: int) -> List[Movimentacao]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = "SELECT IdMovimentacao, TipoVeiculo, Cliente, DataHoraEntrada, DataHoraSaida, Preco, IdTabelaPreco, QRCodePath, IdEstacionamento FROM Movimentacao WHERE DataHoraSaida IS NULL AND IdEstacionamento = ? ORDER BY DataHoraEntrada DESC LIMIT ? , ?"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, inicio, tamanhoPagina)).fetchall()
        objetos = [Movimentacao(*x) for x in resultado]
        return objetos
    
    @classmethod
    def getPageSaidas(cls, id: int, pagina: int, tamanhoPagina: int) -> List[Movimentacao]:
        today = date.today()
        inicio = (pagina - 1) * tamanhoPagina
        data_inicio = today.strftime('%d/%m/%Y')
        sql = """SELECT IdMovimentacao, TipoVeiculo, Cliente, DataHoraEntrada, DataHoraSaida, Preco, IdTabelaPreco, QRCodePath, IdEstacionamento FROM Movimentacao WHERE DataHoraSaida IS NOT NULL AND DataHoraSaida BETWEEN ? || ' 00:00' AND ? || ' 23:59' AND IdEstacionamento = ? ORDER BY DataHoraSaida DESC LIMIT ?, ?"""
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (data_inicio, data_inicio, id, inicio, tamanhoPagina)).fetchall()
        objetos = [Movimentacao(*x) for x in resultado]

        return objetos

    @classmethod
    def getTotalPagesEntradas(cls, id: int, tamanhoPagina: int) -> int:
        sql = "SELECT CEIL(CAST((SELECT COUNT(*) FROM Movimentacao WHERE DataHoraSaida IS NULL AND IdEstacionamento = ?) AS FLOAT) / ?) AS qtdePaginas"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, tamanhoPagina, )).fetchone()
        return int(resultado[0])

    @classmethod
    def getTotalPagesSaidas(cls, id: int, tamanhoPagina: int) -> int:
        today = date.today()
        data_inicio = today.strftime('%d/%m/%Y')
        sql = """SELECT CEIL(CAST((SELECT COUNT(*) FROM Movimentacao WHERE DataHoraSaida IS NOT NULL AND DataHoraSaida BETWEEN ? || ' 00:00' AND ? || ' 23:59' AND IdEstacionamento = ?) AS FLOAT) / ?) AS qtdePaginas """
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (data_inicio, data_inicio, id, tamanhoPagina, )).fetchone()
        return int(resultado[0])

    @classmethod
    def calcular_preco(cls, tipo_veiculo, data_hora_entrada, tabela_preco):
        if tipo_veiculo == 'Carro':
            preco_primeira_hora = tabela_preco.PrimeiraHoraCarro
            preco_fracao = tabela_preco.FracaoCarro
        elif tipo_veiculo == 'Moto':
            preco_primeira_hora = tabela_preco.PrimeiraHoraMoto
            preco_fracao = tabela_preco.FracaoMoto
        else:
            raise ValueError("Tipo de veículo inválido. Deve ser 'Carro' ou 'Moto'.")
        
        data_hora_saida = datetime.strptime(hora_brasil(), '%d/%m/%Y %H:%M')

        horas_permanencia = (data_hora_saida - data_hora_entrada).total_seconds() / 3600

        if horas_permanencia <= 1:
            preco_total = preco_primeira_hora
        else:
            horas_inteiras = int(horas_permanencia)
            minutos_fracao = (horas_permanencia - horas_inteiras) * 60

            if minutos_fracao > 0:
                horas_inteiras += 1

            preco_total = preco_primeira_hora + (preco_fracao * (horas_inteiras - 1))

        return preco_total
