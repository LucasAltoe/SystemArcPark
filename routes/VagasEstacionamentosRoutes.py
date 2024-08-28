from fastapi import HTTPException, status, APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.Usuario import Usuario

from repositories.EstacionamentoRepo import EstacionamentoRepo
from repositories.MovimentacaoRepo import MovimentacaoRepo
from repositories.TabelaPrecoRepo import TabelaPrecoRepo
from util.security import validar_usuario_cliente_logado


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/vagas", response_class=HTMLResponse)
async def getVagas(
    request: Request, usuario_cliente: Usuario = Depends(validar_usuario_cliente_logado)
):
    if usuario_cliente:
        estacionamentos = EstacionamentoRepo.getAll()
        
        # Calcular o número de vagas disponíveis para cada estacionamento
        for estacionamento in estacionamentos:
            numero_total_vagas = estacionamento.NumeroVagas
            
            # Obter todas as entradas
            entradas = MovimentacaoRepo.getAll()
            
            # Filtrar as entradas para o estacionamento atual
            entradas_estacionamento = [entrada for entrada in entradas if entrada.IdEstacionamento == estacionamento.IdEstacionamento]
            
            # Filtrar as entradas que possuem apenas DataHoraEntrada preenchido
            veiculos_pendentes = [entrada for entrada in entradas_estacionamento if entrada.DataHoraEntrada and not entrada.DataHoraSaida]
            
            numero_veiculos_pendentes = len(veiculos_pendentes)
            
            ocupacao_total = numero_total_vagas - numero_veiculos_pendentes
            
            estacionamento.VagasDisponiveis = ocupacao_total

        return templates.TemplateResponse(
            "Vagas/vagas.html",
            {"request": request, "active_page": "vagas", "estacionamentos": estacionamentos, "usuario_cliente": usuario_cliente},
        )

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/vagasInformacoes/{id_estacionamento}")
async def vagas_informacoes(request: Request, id_estacionamento: int, usuario_cliente: bool = Depends(validar_usuario_cliente_logado)):
    if usuario_cliente:
        estacionamento = EstacionamentoRepo.getOne(id_estacionamento)

        if estacionamento is None:
            return {"detail": "Estacionamento not found"}

        tabelas = TabelaPrecoRepo.getOne(id_estacionamento)

        return templates.TemplateResponse("Vagas/vagasInformacoes.html", {"request": request, "estacionamento": estacionamento, "tabelas": tabelas, "usuario_cliente": usuario_cliente})

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
