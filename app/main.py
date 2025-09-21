from http import HTTPStatus
from fastapi import FastAPI
from app.api.v1 import customer

app = FastAPI(title="SecureTransfer API", version="1.0.0")

# Registra as rotas dos clientes
app.include_router(customer.router, prefix="/api/v1/customers", tags=["customers"])

#Endpoint pra dar sorte no projeto
@app.get('/', status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Olá mundo!'}