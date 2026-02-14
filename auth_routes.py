from fastapi import APIRouter, HTTPException
#ESSE é o meu prefixo do meu router, ou seja, todas as rotas que eu criar aqui dentro do auth_router vão começar com /auth
auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def autenticar():
    return {"message": "Voçe acessou a rota de autenticação"}

