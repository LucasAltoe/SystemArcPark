from datetime import datetime
from fastapi import APIRouter, Depends, Form, status, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Usuario import Usuario

from repositories.MovimentacaoRepo import MovimentacaoRepo
from repositories.TabelaPrecoRepo import TabelaPrecoRepo
from util.formatarhora import hora_brasil
from util.security import validar_usuario_logado


router = APIRouter()

templates = Jinja2Templates(directory="templates")



@router.get("/saidas", response_class=HTMLResponse)
async def getSaidas(request: Request, pa: int = 1, tp: int = 9, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        saidas_do_dia = MovimentacaoRepo.getPageSaidas(usuario.IdEstacionamento, pa, tp)
        totalPaginas = MovimentacaoRepo.getTotalPagesSaidas(usuario.IdEstacionamento, tp)

        return templates.TemplateResponse("Saidas/saidas.html", {"request": request, "active_page": "saidas", "saidas": saidas_do_dia, "paginaAtual": pa, "tamanhoPagina": tp, "totalPaginas": totalPaginas, "usuario": usuario })

    else:
        return RedirectResponse("/login", status.HTTP_302_FOUND)


@router.post("/saidas", response_class=HTMLResponse)
async def cadastrar_saida(id_movimentacao: int = Form(...), usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        data_hora_saida = hora_brasil()

        movimentacao = MovimentacaoRepo.getOne(id_movimentacao)

        if movimentacao is None:
            return "Movimentacao not found"

        data_hora_entrada = datetime.strptime(movimentacao.DataHoraEntrada, "%d/%m/%Y %H:%M")

        tabela_preco = TabelaPrecoRepo.getOne(movimentacao.IdTabelaPreco)

        if tabela_preco is None:
            return "TabelaPreco not found"

        preco = MovimentacaoRepo.calcular_preco(
            movimentacao.TipoVeiculo,
            data_hora_entrada,
            tabela_preco
        )

        movimentacao.DataHoraSaida = data_hora_saida
        movimentacao.Preco = preco

        MovimentacaoRepo.update(movimentacao)

        return RedirectResponse("/saidas", status_code=status.HTTP_303_SEE_OTHER)
    
    else:
        return RedirectResponse("/login", status.HTTP_302_FOUND)
