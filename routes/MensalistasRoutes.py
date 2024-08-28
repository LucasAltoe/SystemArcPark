from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Form, HTTPException, Request,  status
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
import qrcode

from models.Mensalistas import Mensalistas
from models.Usuario import Usuario
from repositories.MensalistasRepo import MensalistasRepo
from util.security import validar_usuario_logado


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/mensalistas", response_class=HTMLResponse)
async def getMensalistas(request: Request, pa: int = 1, tp: int = 9, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        mensalistas = MensalistasRepo.getPage(usuario.IdEstacionamento, pa, tp)
        totalPaginas = MensalistasRepo.getTotalPages(usuario.IdEstacionamento, tp)

        return templates.TemplateResponse("Mensalistas/mensalistas.html", {"request": request, "active_page": "mensalistas", "mensalistas": mensalistas, "paginaAtual": pa, "tamanhoPagina": tp, "totalPaginas": totalPaginas, "usuario": usuario})

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/cadastroMensalistas", response_class=HTMLResponse)
async def getCadastroMensalistas(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        return templates.TemplateResponse("Mensalistas/cadastroMensalistas.html", {"request": request, "active_page": "mensalistas", "usuario": usuario})
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/cadastroMensalistas")
async def postCadastroMensalistas(
    NomeMensalista: str = Form(""), 
    ContatoMensalista: str = Form(""), 
    InicioContratoMensalista: str = Form(""), 
    FimContratoMensalista: str = Form(""),
    ValorMensalista: Optional[float] = Form(None),
    PlacaMensalista: str = Form(""),
    VagasMensalista: int = Form(0),
    usuario: Usuario = Depends(validar_usuario_logado)):
    
    if usuario:
        mensalistas = MensalistasRepo.getAll()

        if mensalistas:
            last_mensalista = mensalistas[-1]
            id_mensalista = last_mensalista.IdMensalista + 1
        else:
            id_mensalista = 1

        mensalista = Mensalistas(
        IdMensalista=id_mensalista,
        Nome=NomeMensalista,
        Contato=ContatoMensalista,
        InicioContrato=InicioContratoMensalista,
        FimContrato=FimContratoMensalista,
        ValorMensal=ValorMensalista,
        Placa=PlacaMensalista,
        Vagas=VagasMensalista,
        IdEstacionamento=usuario.IdEstacionamento,
        QRCodePath=None
        )

        MensalistasRepo.insert(mensalista)

        qr_data = f"Nome: {NomeMensalista}\nContato: {ContatoMensalista}\nPlaca: {PlacaMensalista}\nInicio Contrato: {InicioContratoMensalista}\nFim Contrato: {FimContratoMensalista}\nValor Mensal: {ValorMensalista}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        qr_code_image = qr.make_image(fill_color="blue", back_color="white")
        
        qr_code_path = f"tokens_mensalistas/token_{id_mensalista}.png"
        qr_code_image.save(qr_code_path)

        mensalista.QRCodePath = qr_code_path
        MensalistasRepo.update(mensalista)
        
        return RedirectResponse("/mensalistas", status_code=status.HTTP_303_SEE_OTHER)
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/tokens_mensalistas/token_{id_mensalista}.png", response_class=FileResponse)
async def get_qr_code_image_mensalistas(id_mensalista: int, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        qr_code_image_path_mensalistas = f"tokens_mensalistas/token_{id_mensalista}.png"
        return qr_code_image_path_mensalistas
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)



@router.post("/excluir_mensalista")
async def excluir_mensalista(id_mensalista: int = Form(...)):
    deletar = MensalistasRepo.delete(id_mensalista)

    if deletar:
        return RedirectResponse("/mensalistas", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return {"error": "Falha ao excluir mensalista"}