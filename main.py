from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles
from repositories.ClienteRepo import ClienteRepo
from util.exceptionHandler import configurar as configurarExcecoes

from repositories.EstacionamentoRepo import EstacionamentoRepo
from repositories.MensalistasRepo import MensalistasRepo
from repositories.MovimentacaoRepo import MovimentacaoRepo
from repositories.OperadoresRepo import OperadoresRepo
from repositories.TabelaPrecoRepo import TabelaPrecoRepo

from routes.MainRoutes import router as mainRouter
from routes.LoginRoutes import router as loginRouter
from routes.InicioRoutes import router as inicioRouter
from routes.EntradasRoutes import router as entradasRouter
from routes.SaidasRoutes import router as saidasRouter
from routes.EstacionamentoRoutes import router as estacionamentoRouter
from routes.FinanceiroRoutes import router as financeiroRouter
from routes.MensalistasRoutes import router as mensalistasRouter
from routes.OperadoresRoutes import router as operadoresRouter
from routes.PerfilRoutes import router as perfilRouter
from routes.VagasEstacionamentosRoutes import router as vagasRouter


app = FastAPI()

app.mount(path="/static", app=StaticFiles(directory="static"), name="static")

# configurarExcecoes(app)

ClienteRepo.createTable()
EstacionamentoRepo.createTable()
MensalistasRepo.createTable()
MovimentacaoRepo.createTable()
OperadoresRepo.createTable()
TabelaPrecoRepo.createTable()


app.include_router(mainRouter)
app.include_router(loginRouter)
app.include_router(inicioRouter)
app.include_router(entradasRouter)
app.include_router(saidasRouter)
app.include_router(estacionamentoRouter)
app.include_router(financeiroRouter)
app.include_router(mensalistasRouter)
app.include_router(operadoresRouter)
app.include_router(perfilRouter)
app.include_router(vagasRouter)


#if __name__ == "__main__":
#    uvicorn.run(app="main:app", reload=True, host="0.0.0.0")