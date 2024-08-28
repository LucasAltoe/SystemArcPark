from datetime import date, datetime
from fastapi import HTTPException, status, APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Usuario import Usuario

from repositories.EstacionamentoRepo import EstacionamentoRepo
from repositories.MensalistasRepo import MensalistasRepo
from repositories.MovimentacaoRepo import MovimentacaoRepo
from util.security import validar_usuario_logado


router = APIRouter()

templates = Jinja2Templates(directory="templates")



@router.get("/financeiro", response_class=HTMLResponse)
async def getFinanceiro(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        saidas = MovimentacaoRepo.getSaidasById(usuario.IdEstacionamento)
    
        saidas_validas = [movimentacao for movimentacao in saidas if movimentacao.Preco is not None]
        
        if saidas_validas:

            # Faturamento Total
            faturamento_total = sum(movimentacao.Preco for movimentacao in saidas_validas)

            # Ticket Médio
            numero_saidas = len(saidas_validas)
            ticket_medio = faturamento_total / numero_saidas
            
            # Faturamento Por Vaga
            numero_total_vagas = EstacionamentoRepo.getNumeroVagas(usuario.IdEstacionamento)
            faturamento_por_vaga = faturamento_total / numero_total_vagas

            # Faturamento proveniente de carros e motos
            # Inicializa as variáveis de soma para carros e motos
            faturamento_carros = 0
            faturamento_motos = 0

            for movimentacao in saidas_validas:
                if movimentacao.TipoVeiculo == "Carro":
                    faturamento_carros += movimentacao.Preco
                elif movimentacao.TipoVeiculo == "Moto":
                    faturamento_motos += movimentacao.Preco

            # Provisionado Mensalistas
            mensalistas = MensalistasRepo.getAllById(usuario.IdEstacionamento)
            faturamento_mensalistas = 0.0
            for mensalista in mensalistas:
                # Converte as datas de início e fim de contrato para objetos de data
                data_inicio_contrato = datetime.strptime(mensalista.InicioContrato, '%Y-%m-%d').date()
                data_fim_contrato = datetime.strptime(mensalista.FimContrato, '%Y-%m-%d').date()

                # Calcula o número de meses entre o início e o fim do contrato
                meses_contrato = (data_fim_contrato.year - data_inicio_contrato.year) * 12 + (data_fim_contrato.month - data_inicio_contrato.month)

                # Adiciona o valor mensal multiplicado pelos meses de contrato ao faturamento provisionado mensal
                faturamento_mensalistas += mensalista.ValorMensal * meses_contrato

            # Calcular tempo de permanência médio
            tempos_de_permanencia = [(datetime.strptime(movimentacao.DataHoraSaida, '%d/%m/%Y %H:%M') - datetime.strptime(movimentacao.DataHoraEntrada, '%d/%m/%Y %H:%M')).seconds / 60 for movimentacao in saidas_validas]
            permanencia_media = sum(tempos_de_permanencia) / len(tempos_de_permanencia)
            
            # Calcular o número de saídas por tipo de veículo
            numero_carros = sum(1 for movimentacao in saidas_validas if movimentacao.TipoVeiculo == "Carro")
            numero_motos = sum(1 for movimentacao in saidas_validas if movimentacao.TipoVeiculo == "Moto")

            # Calcular a lotação por hora
            lotacao_por_hora = [0] * 24
            for movimentacao in saidas_validas:
                hora_entrada = datetime.strptime(movimentacao.DataHoraEntrada, '%d/%m/%Y %H:%M').hour
                hora_saida = datetime.strptime(movimentacao.DataHoraSaida, '%d/%m/%Y %H:%M').hour
                for hora in range(hora_entrada, hora_saida + 1):
                    lotacao_por_hora[hora] += 1

            # Calcular o faturamento por dia
            faturamento_por_dia = [0] * 31
            for movimentacao in saidas_validas:
                dia = datetime.strptime(movimentacao.DataHoraSaida, '%d/%m/%Y %H:%M').day
                faturamento_por_dia[dia - 1] += movimentacao.Preco

            return templates.TemplateResponse("Financeiro/financeiro.html", {"request": request, "active_page": "financeiro", "faturamento_total": "{:.2f}".format(faturamento_total).replace('.', ','), "faturamento_por_vaga": "{:.2f}".format(faturamento_por_vaga).replace('.', ','), "faturamento_carros": "{:.2f}".format(faturamento_carros).replace('.', ','), "faturamento_motos": "{:.2f}".format(faturamento_motos).replace('.', ','), "faturamento_mensalistas": "{:.2f}".format(faturamento_mensalistas).replace('.', ','), "permanencia_media": "{:.1f}".format(permanencia_media).replace('.', ','), "lotacao_por_hora": lotacao_por_hora, "numero_carros": numero_carros, "numero_motos": numero_motos, "faturamento_por_dia": faturamento_por_dia, "ticket_medio": "{:.2f}".format(ticket_medio).replace('.', ','), "usuario": usuario})
        
        else:
            return templates.TemplateResponse("Financeiro/financeiro.html", {
                "request": request,
                "active_page": "financeiro",
                "error_message": "Não há saídas cadastradas. Cadastre uma saída, por favor." if not saidas_validas else None,
            })


    else:
        return RedirectResponse("/login", status.HTTP_302_FOUND)
