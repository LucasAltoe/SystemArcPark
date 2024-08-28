from fastapi import Form, HTTPException, status, APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Usuario import Usuario
from repositories.ClienteRepo import ClienteRepo
from repositories.EstacionamentoRepo import EstacionamentoRepo
from starlette.status import HTTP_303_SEE_OTHER

from util.security import obter_hash_senha, validar_usuario_cliente_logado, validar_usuario_logado, verificar_senha
from util.validators import *


router = APIRouter()

templates = Jinja2Templates(directory="templates")


# Estacionamento
@router.get("/perfilEstacionamento", response_class=HTMLResponse)
async def getPerfilEstacionamento(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    if usuario:
        estacionamentos = EstacionamentoRepo.getOne(usuario.IdEstacionamento)
        if estacionamentos:
            return templates.TemplateResponse(
                "Perfil/perfilEstacionamento.html",
                {"request": request, "usuario": usuario, "estacionamentos": estacionamentos},
            )
        else:
            return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/alterarPerfilEstacionamento", response_class=HTMLResponse)
async def getAlterarPerfilEstacionamento(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        return templates.TemplateResponse("Perfil/alterarPerfilEstacionamento.html", {"request": request, "usuario": usuario})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/alterarPerfilEstacionamento", response_class=HTMLResponse)
async def postAlterarPerfilEstacionamento(
    usuario: Usuario = Depends(validar_usuario_logado),
    NomeEstacionamento: str = Form(""),
    EmailEstacionamento: str = Form(""),
    CnpjEstacionamento: str = Form(""),
    CepEstacionamento: str = Form(""),
    EnderecoEstacionamento: str = Form(""),
    AberturaSegunda: str = Form(""),
    FechamentoSegunda: str = Form(""),
    AberturaTerca: str = Form(""),
    FechamentoTerca: str = Form(""),
    AberturaQuarta: str = Form(""),
    FechamentoQuarta: str = Form(""),
    AberturaQuinta: str = Form(""),
    FechamentoQuinta: str = Form(""),
    AberturaSexta: str = Form(""),
    FechamentoSexta: str = Form(""),
    AberturaSabado: str = Form(""),
    FechamentoSabado: str = Form(""),
    AberturaDomingo: str = Form(""),
    FechamentoDomingo: str = Form(""),
    NumeroVagas: int = Form(0)
    ):
    
    if usuario:
        estacionamento = EstacionamentoRepo.getOne(usuario.IdEstacionamento)

        estacionamento.Nome = NomeEstacionamento
        estacionamento.Email = EmailEstacionamento
        estacionamento.CNPJ = CnpjEstacionamento
        estacionamento.CEP = CepEstacionamento
        estacionamento.Endereco = EnderecoEstacionamento
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
            return RedirectResponse("/perfilEstacionamento", status_code=HTTP_303_SEE_OTHER)
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    

@router.get("/alterarSenha", response_class=HTMLResponse)
async def getAlterarSenhaEstacionamento(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    if usuario:
        return templates.TemplateResponse(
            "Perfil/alterarSenha.html",
            {"request": request, "usuario": usuario},
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/alterarSenha", response_class=HTMLResponse)
async def postAlterarSenhaEstacionamento(
    request: Request,
    usuario: bool = Depends(validar_usuario_logado),
    SenhaAntiga: str = Form(""),
    NovaSenha: str = Form(""),
    ConfirmarNovaSenha: str = Form("")):
    
    if usuario:
        # # normalização dos dados
        # SenhaAntiga = SenhaAntiga.strip()
        # NovaSenha = NovaSenha.strip()
        # ConfirmarNovaSenha = ConfirmarNovaSenha.strip()    

        # # verificação de erros
        # erros = {}
        # # validação do campo senhaAtual
        # is_not_empty(SenhaAntiga, "SenhaAntiga", erros)
        # is_password(SenhaAntiga, "SenhaAntiga", erros)    
        # # validação do campo novaSenha
        # is_not_empty(NovaSenha, "NovaSenha", erros)
        # is_password(NovaSenha, "NovaSenha", erros)
        # # validação do campo confNovaSenha
        # is_not_empty(ConfirmarNovaSenha, "ConfirmarNovaSenha", erros)
        # is_matching_fields(ConfirmarNovaSenha, "ConfirmarNovaSenha", NovaSenha, "Nova Senha", erros)
        
        # # só verifica a senha no banco de dados se não houverem erros de validação
        # if len(erros) == 0:    
        #     hash_senha_bd = EstacionamentoRepo.getSenhaDeEmail(usuario.email)
        #     if hash_senha_bd:
        #         if not verificar_senha(SenhaAntiga, hash_senha_bd):            
        #             add_error("senhaAtual", "Senha atual está incorreta.", erros)
       
        # # se tem erro, mostra o formulário novamente
        # if len(erros) > 0:
        #     valores = {}        
        #     return templates.TemplateResponse(
        #         "Perfil/alterarSenha.html",
        #         {
        #             "request": request,
        #             "usuario": usuario,                
        #             "erros": erros,
        #             "valores": valores,
        #         },
        #     )
    
        hash_nova_senha = obter_hash_senha(NovaSenha)
        EstacionamentoRepo.updateSenha(usuario.IdEstacionamento, hash_nova_senha)
        return templates.TemplateResponse("Perfil/sucessoSenha.html", {"request": request, "usuario": usuario})
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)




# Cliente
@router.get("/perfilCliente", response_class=HTMLResponse)
async def getPerfilCliente(
    request: Request, usuario_cliente: bool = Depends(validar_usuario_cliente_logado)
):
    if usuario_cliente:
        cliente = ClienteRepo.getOne(usuario_cliente.IdCliente)
        
        return templates.TemplateResponse(
            "Perfil/perfilCliente.html",
                {"request": request, "usuario_cliente": usuario_cliente, "cliente": cliente},
        )
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/alterarPerfilCliente", response_class=HTMLResponse)
async def getAlterarPerfilCliente(request: Request, usuario_cliente: bool = Depends(validar_usuario_cliente_logado)):
    if usuario_cliente:
        return templates.TemplateResponse("Perfil/alterarPerfilCliente.html", {"request": request, "usuario_cliente": usuario_cliente})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/alterarPerfilCliente", response_class=HTMLResponse)
async def postAlterarPerfilCliente(
    usuario_cliente: bool = Depends(validar_usuario_cliente_logado),
    NomeCliente: str = Form(""),
    CpfCliente: str = Form(""),
    EmailCliente: str = Form(""),
    ContatoCliente: str = Form("")):
    
    if usuario_cliente:
        cliente = ClienteRepo.getOne(usuario_cliente.IdCliente)

        cliente.Nome = NomeCliente
        cliente.CPF_CNPJ = CpfCliente
        cliente.Email = EmailCliente
        cliente.Contato = ContatoCliente

        updated_cliente = ClienteRepo.update(cliente)

        if updated_cliente:
            return RedirectResponse("/perfilCliente", status_code=HTTP_303_SEE_OTHER)
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/alterarSenhaCliente", response_class=HTMLResponse)
async def getAlterarSenhaCliente(
    request: Request, usuario_cliente: bool = Depends(validar_usuario_cliente_logado)
):
    if usuario_cliente:
        return templates.TemplateResponse(
            "Perfil/alterarSenhaCliente.html",
            {"request": request, "usuario_cliente": usuario_cliente},
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/alterarSenhaCliente", response_class=HTMLResponse)
async def postAlterarSenhaCliente(
    request: Request,
    usuario_cliente: bool = Depends(validar_usuario_cliente_logado),
    SenhaAntiga: str = Form(""),
    NovaSenha: str = Form(""),
    ConfirmarNovaSenha: str = Form("")):
    
    if usuario_cliente:
        # # normalização dos dados
        # SenhaAntiga = SenhaAntiga.strip()
        # NovaSenha = NovaSenha.strip()
        # ConfirmarNovaSenha = ConfirmarNovaSenha.strip()    

        # # verificação de erros
        # erros = {}
        # # validação do campo senhaAtual
        # is_not_empty(SenhaAntiga, "SenhaAntiga", erros)
        # is_password(SenhaAntiga, "SenhaAntiga", erros)    
        # # validação do campo novaSenha
        # is_not_empty(NovaSenha, "NovaSenha", erros)
        # is_password(NovaSenha, "NovaSenha", erros)
        # # validação do campo confNovaSenha
        # is_not_empty(ConfirmarNovaSenha, "ConfirmarNovaSenha", erros)
        # is_matching_fields(ConfirmarNovaSenha, "ConfirmarNovaSenha", NovaSenha, "Nova Senha", erros)
        
        # # só verifica a senha no banco de dados se não houverem erros de validação
        # if len(erros) == 0:    
        #     hash_senha_bd = EstacionamentoRepo.getSenhaDeEmail(usuario.email)
        #     if hash_senha_bd:
        #         if not verificar_senha(SenhaAntiga, hash_senha_bd):            
        #             add_error("senhaAtual", "Senha atual está incorreta.", erros)
        
        # # se tem erro, mostra o formulário novamente
        # if len(erros) > 0:
        #     valores = {}        
        #     return templates.TemplateResponse(
        #         "Perfil/alterarSenha.html",
        #         {
        #             "request": request,
        #             "usuario": usuario,                
        #             "erros": erros,
        #             "valores": valores,
        #         },
        #     )
    
        hash_nova_senha = obter_hash_senha(NovaSenha)
        ClienteRepo.updateSenha(usuario_cliente.IdCliente, hash_nova_senha)

        return templates.TemplateResponse("Perfil/sucessoSenha.html", {"request": request, "usuario_cliente": usuario_cliente})
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)



# Operador
@router.get("/alterarSenhaOperador", response_class=HTMLResponse)
async def getAlterarSenhaOperador(request: Request, logado: bool = Depends(validar_usuario_logado)):
    if logado:
        return templates.TemplateResponse("TelasOperadores/alterarSenhaOperador.html", {"request": request, "logado": logado})
    else:
        return RedirectResponse("/login", status.HTTP_302_FOUND)
