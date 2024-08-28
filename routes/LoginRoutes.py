from typing import Annotated
from fastapi import APIRouter, Depends, Form, Query, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from models.Cliente import Cliente
from models.Estacionamento import Estacionamento
from models.Usuario import Usuario
from repositories.ClienteRepo import ClienteRepo
from repositories.EstacionamentoRepo import EstacionamentoRepo
from util.security import gerar_token, obter_hash_senha, validar_usuario_logado, verificar_senha
from util.validators import *


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
async def getLogin(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    return templates.TemplateResponse("Login/login.html", {"request": request, "usuario": usuario})

@router.post("/login")
async def postLogin(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    email: str = Form(""),
    senha: str = Form(""),
    returnUrl: str = Query("/"),
):
    # normalização de dados
    email = email.strip().lower()
    senha = senha.strip()
    
    # validação de dados
    erros = {}
    # validação do campo email
    is_not_empty(email, "email", erros)
    is_email(email, "email", erros)
    # validação do campo senha
    is_not_empty(senha, "senha", erros)
        
    # só checa a senha no BD se os dados forem válidos
    if len(erros) == 0:
        hash_senha_bd = EstacionamentoRepo.getSenhaDeEmail(email)
        hash_senha_cliente = ClienteRepo.getSenhaDeEmail(email)

        # Estacionamento
        if hash_senha_bd:
            if verificar_senha(senha, hash_senha_bd):
                token = gerar_token()
                if EstacionamentoRepo.updateToken(email, token):
                    response = RedirectResponse("/inicio", status.HTTP_302_FOUND)
                    response.set_cookie(
                        key="auth_token", value=token, max_age=1800, httponly=True
                    )
                    return response
                else:
                    raise Exception(
                        "Não foi possível alterar o token do usuário no banco de dados."
                    )
            else:            
                add_error("senha", "Email ou senha incorretos.", erros)
        else:
            add_error("email", "Usuário não cadastrado.", erros)
        
        # Cliente
        if hash_senha_cliente:
            if verificar_senha(senha, hash_senha_cliente):
                token = gerar_token()
                if ClienteRepo.updateToken(email, token):
                    response = RedirectResponse("/vagas", status.HTTP_302_FOUND)
                    response.set_cookie(
                        key="auth_token", value=token, max_age=1800, httponly=True
                    )
                    return response
                else:
                    raise Exception(
                        "Não foi possível alterar o token do usuário no banco de dados."
                    )
            else:            
                add_error("senha", "Email ou senha incorretos.", erros)
        else:
            add_error("email", "Usuário não cadastrado.", erros)

    # se tem algum erro, mostra o formulário novamente
    if len(erros) > 0:
        valores = {}
        valores["email"] = email        
        return templates.TemplateResponse(
            "Login/login.html",
            {
                "request": request,
                "usuario": usuario,
                "erros": erros,
                "valores": valores,
            },
        )


@router.get("/logout")
async def getLogout(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):   
    if (usuario):
        EstacionamentoRepo.updateToken(usuario.Email, "") 
    response = RedirectResponse("/", status.HTTP_302_FOUND)
    response.set_cookie(key="auth_token", value="", httponly=True, expires="1970-01-01T00:00:00Z")    
    return response


@router.get("/nivelAcesso", response_class=HTMLResponse)
async def getNivelAcesso(request: Request):
    return templates.TemplateResponse("Login/nivelAcesso.html", {"request": request})

@router.get("/cadastroEstacionamento", response_class=HTMLResponse)
async def getCadastroEstacionamento(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    return templates.TemplateResponse("Login/cadastroEstacionamento.html", {"request": request, "usuario": usuario})


@router.post("/cadastroEstacionamento")
async def postCadastroEstacionamento(
    NomeEstacionamento: str = Form(""),
    CnpjEstacionamento: str = Form(""),
    EmailEstacionamento: str = Form(""),
    CepEstacionamento: str = Form(""),
    EnderecoEstacionamento: str = Form(""),
    Senha: str = Form(""),
    AberturaDomingo: str = Form(""),
    FechamentoDomingo: str = Form(""),
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
    NumeroVagas: int = Form(0)):


    # normalização dos dados
    # NomeEstacionamento = capitalizar_nome_proprio(NomeEstacionamento).strip()
    # CnpjEstacionamento = CnpjEstacionamento.strip()
    # EmailEstacionamento = EmailEstacionamento.lower().strip()
    # CepEstacionamento = CepEstacionamento.strip()
    # EnderecoEstacionamento = EnderecoEstacionamento.strip()
    # Senha = Senha.strip()
    # AberturaDomingo = AberturaDomingo.strip()
    # FechamentoDomingo = FechamentoDomingo.strip()
    # AberturaSegunda = AberturaSegunda.strip()
    # FechamentoSegunda = FechamentoSegunda.strip()
    # AberturaTerca = AberturaTerca.strip()
    # FechamentoTerca = FechamentoTerca.strip()
    # AberturaQuarta = AberturaQuarta.strip()
    # FechamentoQuarta = FechamentoQuarta.strip()
    # AberturaQuinta = AberturaQuinta.strip()
    # FechamentoQuinta = FechamentoQuinta.strip()
    # AberturaSexta = AberturaSexta.strip()
    # FechamentoSexta = FechamentoSexta.strip()
    # AberturaSabado = AberturaSabado.strip()
    # FechamentoSabado = FechamentoSabado.strip()
    # NumeroVagas = NumeroVagas.strip()
    # NomeTabela = capitalizar_nome_proprio(NomeTabela).strip()


    # verificação de erros
    erros = {}
    # validação de campos preenchidos
    # is_not_empty(NomeEstacionamento, "NomeEstacionamento", erros)
    # is_not_empty(CnpjEstacionamento, "CnpjEstacionamento", erros)
    # is_not_empty(EmailEstacionamento, "EmailEstacionamento", erros)
    # is_not_empty(CepEstacionamento, "CepEstacionamento", erros)
    # is_not_empty(EnderecoEstacionamento, "EnderecoEstacionamento", erros)
    # is_not_empty(Senha, "Senha", erros)
    # is_not_empty(AberturaDomingo, "AberturaDomingo", erros)
    # is_not_empty(FechamentoDomingo, "FechamentoDomingo", erros)
    # is_not_empty(AberturaSegunda, "AberturaSegunda", erros)
    # is_not_empty(FechamentoSegunda, "FechamentoSegunda", erros)
    # is_not_empty(AberturaTerca, "AberturaTerca", erros)
    # is_not_empty(FechamentoTerca, "FechamentoTerca", erros)
    # is_not_empty(AberturaQuarta, "AberturaQuarta", erros)
    # is_not_empty(FechamentoQuarta, "FechamentoQuarta", erros)
    # is_not_empty(AberturaQuinta, "AberturaQuinta", erros)
    # is_not_empty(FechamentoQuinta, "FechamentoQuinta", erros)
    # is_not_empty(AberturaSexta, "AberturaSexta", erros)
    # is_not_empty(FechamentoSexta, "FechamentoSexta", erros)
    # is_not_empty(AberturaSabado, "AberturaSabado", erros)
    # is_not_empty(FechamentoSabado, "FechamentoSabado", erros)
    # is_not_empty(NumeroVagas, "NumeroVagas", erros)
    # is_not_empty(NomeTabela, "NomeTabela", erros)
    # is_not_empty(PhCarro, "PhCarro", erros)
    # is_not_empty(PhMoto, "PhMoto", erros)
    # is_not_empty(FrCarro, "FrCarro", erros)
    # is_not_empty(FrMoto, "FrMoto", erros)


    # is_estacionamento_name(NomeEstacionamento, "NomeEstacionamento", erros)
    # is_in_range(NomeEstacionamento, "NomeEstacionamento", 3, 40, erros)
    # # validação do campo email
    # if is_email(EmailEstacionamento, "EmailEstacionamento", erros):
    #     if EstacionamentoRepo.emailExiste(EmailEstacionamento):
    #         add_error("EmailEstacionamento", "Já existe um estacionamento cadastrado com este e-mail.", erros)
    # # validação do campo senha
    # is_password(Senha, "Senha", erros)
    # # validação do campo cnpj
    # is_cnpj(CnpjEstacionamento, "CnpjEstacionamento", erros)
    # # validação do campo cep
    # is_cep(CepEstacionamento, "CepEstacionamento", erros)
    # # validação dos campos de preço da tabela
    # is_in_range(PhCarro, "PhCarro" ,0, 500, erros)
    # is_in_range(PhMoto, "PhMoto" ,0, 500, erros)
    # is_in_range(FrCarro, "FrCarro" ,0, 500, erros)
    # is_in_range(FrMoto, "FrMoto" ,0, 500, erros)



    # se tem erro, mostra o formulário novamente
    # if len(erros) > 0:
    #     valores = {}
    #     valores["nome"] = nome
    #     valores["email"] = email.lower()
    #     valores["idProjeto"] = idProjeto
    #     projetos = ProjetoRepo.obterTodosParaSelect()
    #     return templates.TemplateResponse(
    #         "aluno/novo.html",
    #         {
    #             "request": request,
    #             "usuario": usuario,
    #             "projetos": projetos,
    #             "erros": erros,
    #             "valores": valores,
    #         },
    #     )

    # inserção no banco de dados
    EstacionamentoRepo.insert(Estacionamento(0, 
        NomeEstacionamento, CnpjEstacionamento,
        EmailEstacionamento, CepEstacionamento,
        EnderecoEstacionamento, obter_hash_senha(Senha),
        AberturaDomingo, FechamentoDomingo,
        AberturaSegunda, FechamentoSegunda,
        AberturaTerca, FechamentoTerca,
        AberturaQuarta, FechamentoQuarta,
        AberturaQuinta, FechamentoQuinta,
        AberturaSexta, FechamentoSexta,
        AberturaSabado, FechamentoSabado,
        NumeroVagas
    ))


    # mostra página de login
    return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/cadastroCliente", response_class=HTMLResponse)
async def getCadastroCliente(request: Request):
    return templates.TemplateResponse("Login/cadastroCliente.html", {"request": request})

@router.post("/cadastroCliente")
async def postCadastroCliente(
    NomeCliente: str = Form(""),
    CpfCliente: str = Form(""),
    EmailCliente: str = Form(""),
    ContatoCliente: str = Form(""),
    Senha: str = Form(""),):

    ClienteRepo.insert(Cliente(0, NomeCliente, CpfCliente, EmailCliente, ContatoCliente, obter_hash_senha(Senha)))
    
    return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)


# Rota para verificar a criptografia das senhas
@router.get("/mostrarLogins", response_class=HTMLResponse)
async def getLogins(request: Request):
    logs = EstacionamentoRepo.getAll()

    return templates.TemplateResponse("Login/mostrar_logins.html", {"request": request, "logs": logs })