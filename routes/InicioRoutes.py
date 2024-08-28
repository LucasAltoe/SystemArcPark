from datetime import date
from fastapi import status, APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Usuario import Usuario
from repositories.EstacionamentoRepo import EstacionamentoRepo

from repositories.MovimentacaoRepo import MovimentacaoRepo
from util.security import validar_usuario_logado


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/inicio", response_class=HTMLResponse)
async def getInicio(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        # Obter todas as entradas
        entradas = MovimentacaoRepo.getEntradasById(usuario.IdEstacionamento)

        # Filtrar as entradas que possuem apenas DataHoraEntrada preenchido
        veiculos_pendentes = [entrada for entrada in entradas if entrada.DataHoraEntrada and not entrada.DataHoraSaida]

        numero_veiculos_pendentes = len(veiculos_pendentes)

        numero_total_vagas = EstacionamentoRepo.getNumeroVagas(usuario.IdEstacionamento)
        
        ocupacao_total = numero_veiculos_pendentes / numero_total_vagas

        # Calcular a ocupação de carros em relação ao número total de vagas
        vagas_ocupadas_carros = len([entrada for entrada in veiculos_pendentes if entrada.TipoVeiculo == "Carro"])
        razao_ocupacao_carros = vagas_ocupadas_carros / numero_total_vagas

        # Calcular a ocupação de motos em relação ao número total de vagas
        vagas_ocupadas_motos = len([entrada for entrada in veiculos_pendentes if entrada.TipoVeiculo == "Moto"])
        razao_ocupacao_motos = vagas_ocupadas_motos / numero_total_vagas

        # Calcular o faturamento das saídas do dia
        today = date.today()
        saidas_do_dia = MovimentacaoRepo.getSaidasById(usuario.IdEstacionamento)
        faturamento_dia = sum(saida.Preco for saida in saidas_do_dia)

        return templates.TemplateResponse("Inicio/inicio.html", {"request": request,"active_page": "inicio", "numero_veiculos_pendentes": numero_veiculos_pendentes, "ocupacao_total": ocupacao_total, "razao_ocupacao_carros": razao_ocupacao_carros, "razao_ocupacao_motos": razao_ocupacao_motos, "faturamento_dia": "{:.2f}".format(faturamento_dia).replace('.', ','), "usuario": usuario})
    
    else:
        return RedirectResponse("/login", status.HTTP_302_FOUND)

