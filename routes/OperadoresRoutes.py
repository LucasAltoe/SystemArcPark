from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, Request,  status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Operadores import Operadores
from models.Usuario import Usuario

from repositories.OperadoresRepo import OperadoresRepo
from util.security import obter_hash_senha, validar_usuario_logado


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/operadores", response_class=HTMLResponse)
async def getOperadores(request: Request, pa: int = 1, tp: int = 9, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        operadores = OperadoresRepo.getPage(usuario.IdEstacionamento, pa, tp)
        totalPaginas = OperadoresRepo.getTotalPages(usuario.IdEstacionamento, tp)
        
        return templates.TemplateResponse("Operadores/operadores.html", {"request": request, "active_page": "operadores", "operadores": operadores, "paginaAtual": pa, "tamanhoPagina": tp, "totalPaginas": totalPaginas, "usuario": usuario})
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/cadastroOperadores", response_class=HTMLResponse)
async def getCadastroOperadores(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        return templates.TemplateResponse("Operadores/cadastroOperadores.html", {"request": request, "active_page": "operadores", "usuario": usuario})
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/cadastroOperadores")
async def postCadastroOperadores(
    NomeOperador: str = Form(""), 
    CpfOperador: str = Form(""), 
    ContatoOperador: str = Form(""), 
    SenhaOperador: str = Form(""),
    usuario: Usuario = Depends(validar_usuario_logado)):
    
    if usuario:
        operador = Operadores(0, NomeOperador, CpfOperador, ContatoOperador, obter_hash_senha(SenhaOperador), usuario.IdEstacionamento)
        
        OperadoresRepo.insert(operador)

        return RedirectResponse("/operadores", status_code=status.HTTP_303_SEE_OTHER)
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/excluir_operador")
async def excluir_operador(id_operador: int = Form(...)):
    deletar = OperadoresRepo.delete(id_operador)

    if deletar:
        return RedirectResponse("/operadores", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return {"error": "Falha ao excluir operador"}