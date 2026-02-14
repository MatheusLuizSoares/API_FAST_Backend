from fastapi import APIRouter, HTTPException
## ESSE é o meu prefixo do meu router, ou seja, todas as rotas que eu criar aqui dentro do auth_router vão começar com /pedidos
order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

## ESSE é o meu endpoint, ou seja, a rota completa para acessar essa função vai ser /pedidos/lista
@order_router.get("/")
async def pedidos():
    return {"message": "Voçe acessou a rota de pedidos"}
