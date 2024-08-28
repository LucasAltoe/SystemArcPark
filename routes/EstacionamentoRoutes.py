from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Form, HTTPException, Request,  status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_303_SEE_OTHER

from models.TabelaPreco import TabelaPreco
from models.Usuario import Usuario

from repositories.EstacionamentoRepo import EstacionamentoRepo
from repositories.TabelaPrecoRepo import TabelaPrecoRepo
from util.formatarhora import hora_brasil
from util.security import validar_usuario_logado


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/estacionamento", response_class=HTMLResponse)
async def getEstacionamento(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    if usuario:
        tabelas = TabelaPrecoRepo.getAllForSelect(usuario.IdEstacionamento)
        return templates.TemplateResponse(
            "Estacionamento/estacionamento.html",
            {"request": request, "usuario": usuario,
            "active_page": "estacionamento", "tabelas": tabelas},
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/cadastroTabelas", response_class=HTMLResponse)
async def getCadastroTabelas(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    if usuario:
        return templates.TemplateResponse(
            "Estacionamento/cadastroTabelas.html",
            {"request": request, "usuario": usuario,
                "active_page": "estacionamento"},
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/cadastroTabelas")
async def postCadastroTabelas(
        NomeTabela: str = Form(""),
        PhCarro: Optional[float] = Form(None),
        PhMoto: Optional[float] = Form(None),
        FrCarro: Optional[float] = Form(None),
        FrMoto: Optional[float] = Form(None),
        usuario: Usuario = Depends(validar_usuario_logado)):

    if usuario:
        data_cadastro = hora_brasil()

        nova_tabela = TabelaPreco(0, NomeTabela, data_cadastro, PhCarro, PhMoto, FrCarro, FrMoto, usuario.IdEstacionamento)
        
        TabelaPrecoRepo.insert(nova_tabela)

        return RedirectResponse("/estacionamento", status_code=status.HTTP_303_SEE_OTHER)
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/cadastroInformacoes")
async def postCadastroTabelas(
    AberturaSegunda: Annotated[str, Form()],
    FechamentoSegunda: Annotated[str, Form()],
    AberturaTerca: Annotated[str, Form()],
    FechamentoTerca: Annotated[str, Form()],
    AberturaQuarta: Annotated[str, Form()],
    FechamentoQuarta: Annotated[str, Form()],
    AberturaQuinta: Annotated[str, Form()],
    FechamentoQuinta: Annotated[str, Form()],
    AberturaSexta: Annotated[str, Form()],
    FechamentoSexta: Annotated[str, Form()],
    AberturaSabado: Annotated[str, Form()],
    FechamentoSabado: Annotated[str, Form()],
    AberturaDomingo: Annotated[str, Form()],
    FechamentoDomingo: Annotated[str, Form()],
    NumeroVagas: Annotated[int, Form()],
):

    estacionamento = EstacionamentoRepo.getOne(1)

    estacionamento.DomingoInicio = AberturaDomingo
    estacionamento.DomingoFim = FechamentoDomingo
    estacionamento.SegundaInicio = AberturaSegunda
    estacionamento.SegundaFim = FechamentoSegunda
    estacionamento.TercaInicio = AberturaTerca
    estacionamento.TercaFim = FechamentoTerca
    estacionamento.QuartaInicio = AberturaQuarta
    estacionamento.QuartaFim = FechamentoQuarta
    estacionamento.QuintaInicio = AberturaQuinta
    estacionamento.QuintaFim = FechamentoQuinta
    estacionamento.SextaInicio = AberturaSexta
    estacionamento.SextaFim = FechamentoSexta
    estacionamento.SabadoInicio = AberturaSabado
    estacionamento.SabadoFim = FechamentoSabado
    estacionamento.NumeroVagas = NumeroVagas

    updated_estacionamento = EstacionamentoRepo.update(estacionamento)

    if updated_estacionamento:
        return RedirectResponse("/estacionamento", status_code=HTTP_303_SEE_OTHER)
    else:
        return "Failed to update Estacionamento"
