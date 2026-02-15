from models import db
from sqlalchemy.orm import sessionmaker
from dependencies import pegar_sessao
from fastapi import APIRouter, HTTPException, Depends
from models import Usuario
from main import bcrypt_context

#ESSE é o meu prefixo do meu router, ou seja, todas as rotas que eu criar aqui dentro do auth_router vão começar com /auth
auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    return {"message": "Voçe acessou a rota de autenticação"}

@auth_router.post("/Registro")
async def registro(email: str, senha: str, nome: str, session=Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
  
    senha_criptografada = bcrypt_context.hash(senha)

    novo_usuario = Usuario(
        nome=nome,
        email=email,
        senha=senha_criptografada,
        ativo=True
    )

    session.add(novo_usuario)
    session.commit()

    return {"msg": "Usuário criado com sucesso"}

        
## depends é uma função do FastAPI que permite injetar dependências em suas rotas. Nesse caso, estamos usando Depends(pegar_sessao) para injetar a sessão do banco de dados na função de registro. Isso significa que toda vez que a rota de registro for chamada, o FastAPI irá criar uma nova sessão do banco de dados e passá-la para a função de registro como um argumento.