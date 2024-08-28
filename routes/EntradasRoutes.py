from fastapi import APIRouter, Depends, Form, HTTPException, Request,  status
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
import qrcode

from models.Movimentacao import Movimentacao
from models.Usuario import Usuario

from repositories.MovimentacaoRepo import MovimentacaoRepo
from repositories.TabelaPrecoRepo import TabelaPrecoRepo
from util.formatarhora import hora_brasil
from util.security import validar_usuario_logado


router = APIRouter()

templates = Jinja2Templates(directory="templates")



@router.get("/entradas", response_class=HTMLResponse)
async def getEntradas(request: Request, pa: int = 1, tp: int = 9, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        entradas = MovimentacaoRepo.getPageEntradas(usuario.IdEstacionamento ,pa, tp)
        totalPaginas = MovimentacaoRepo.getTotalPagesEntradas(usuario.IdEstacionamento , tp)

        tabelas = TabelaPrecoRepo.getAllForSelect(usuario.IdEstacionamento)

        return templates.TemplateResponse("Entradas/entradas.html", {"request": request, "active_page": "entradas", "entradas": entradas, "tabelas": tabelas, "paginaAtual": pa, "tamanhoPagina": tp, "totalPaginas": totalPaginas, "usuario": usuario})
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/entradas", response_class=HTMLResponse)
async def cadastrar_entrada(tabela: int = Form(...), tipo_veiculo: str = Form(...), cliente: str = "Rotativo", usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        # Obter o horário atual
        data_hora_entrada = hora_brasil()

        # Obter todas as entradas
        entradas = MovimentacaoRepo.getAll()

        if entradas:
            # Se houver entradas cadastradas, obter o último ID da tabela Movimentacao e adicionar 1 para gerar um novo ID
            last_movimentacao = entradas[-1]
            id_movimentacao = last_movimentacao.IdMovimentacao + 1
        else:
            # Caso não haja entradas cadastradas, o ID da primeira movimentação será 1
            id_movimentacao = 1

        # Cadastrar a entrada na tabela Movimentacao
        movimentacao = Movimentacao(
            IdMovimentacao=id_movimentacao,
            TipoVeiculo=tipo_veiculo,
            Cliente=cliente,
            DataHoraEntrada=data_hora_entrada,
            DataHoraSaida=None,
            Preco=None,
            IdTabelaPreco=tabela,  # Usar o valor selecionado no select como IdTabelaPreco
            QRCodePath=None,
            IdEstacionamento=usuario.IdEstacionamento
        )

        # Gerar o QR Code com as informações da entrada
        qr_code_data = f"ID: {id_movimentacao}\nTipo de Veículo: {tipo_veiculo}\nCliente: {cliente}\nData e Hora de Entrada: {data_hora_entrada}\nIdEstacionamento: {usuario.IdEstacionamento}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_code_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Salvar o QR Code como um arquivo na pasta qr_codes
        qr_code_image_path = f"qr_codes/entrada_{id_movimentacao}.png"
        img.save(qr_code_image_path)

        # Associar o caminho do QR Code à movimentação
        movimentacao.QRCodePath = qr_code_image_path

        # Inserir a entrada no banco de dados
        MovimentacaoRepo.insert(movimentacao)
        
        return RedirectResponse("/entradas", status_code=status.HTTP_303_SEE_OTHER)
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


# Rota para o botão "Carro"
@router.post("/carro", response_class=HTMLResponse)
async def cadastrar_entrada_carro():
    return await cadastrar_entrada(tipo_veiculo="Carro")

# Rota para o botão "Moto"
@router.post("/moto", response_class=HTMLResponse)
async def cadastrar_entrada_moto():
    return await cadastrar_entrada(tipo_veiculo="Moto")

@router.get("/qr_codes/entrada_{id_movimentacao}.png", response_class=FileResponse)
async def get_qr_code_image(id_movimentacao: int):
    qr_code_image_path = f"qr_codes/entrada_{id_movimentacao}.png"
    return qr_code_image_path


@router.post("/excluir_movimentacao")
async def excluir_movimentacao(id_movimentacao: int = Form(...)):
    deletar = MovimentacaoRepo.delete(id_movimentacao)

    if deletar:
        return RedirectResponse("/entradas", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return {"error": "Falha ao excluir a movimentação"}


