from fastapi import FastAPI

# Cria a instância da aplicação
app = FastAPI(
    title="Zingresso - Microsserviço de Eventos",
    description="Este é o microsserviço responsável por gerenciar eventos e catálogos.",
    version="1.0.0"
)

# Uma rota de "health check" para saber se o serviço está no ar
@app.get("/")
def read_root():
    """ Rota raiz - Health Check """
    return {"status": "ok", "service": "svc-eventos"}