from models import db
from sqlalchemy.orm import sessionmaker
from dependencies import pegar_sessao
from fastapi import APIRouter, HTTPException, Depends
from models import Usuario
from main import bcrypt_context
from schemas import UsuarioSchema, loginSchema
from sqlalchemy.orm import Session

#ESSE é o meu prefixo do meu router, ou seja, todas as rotas que eu criar aqui dentro do auth_router vão começar com /auth
auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(email)
   token = f""



@auth_router.get("/")
async def home():
    return {"message": "Voçe acessou a rota de autenticação"}

@auth_router.post("/Registro")
async def registro(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
  
    senha_criptografada = bcrypt_context.hash(usuario_schema.senha)

    novo_usuario = Usuario(
        nome=usuario_schema.nome,
        email=usuario_schema.email,
        senha=senha_criptografada,
        ativo=True,
        admin=usuario_schema.admin
    )

    session.add(novo_usuario)
    session.commit()

    return {"msg": f"Usuário criado com sucesso, {usuario_schema.email}"}


@auth_router.post("/Login")
async def login(login_schema: loginSchema, session: Session = Depends(pegar_sessao)):
 usuario= session.query(Usuario).filter(Usuario.email == login_schema.email).first()
 if not usuario:
    raise HTTPException(status_code=400, detail="Email ou senha incorretos")
 else:
      access_token = criar_token(usuario.id)
      return {"access_token": access_token, "token_type": "bearer"}
 






 ## acess_token é o token de acesso que será retornado para o cliente após um login bem-sucedido. Ele é criado usando a função criar_token, que gera um token único para o usuário com base em seu ID. O token_type "bearer" indica que o token é do tipo Bearer, que é um tipo comum de token de acesso usado em APIs para autenticação e autorização. O cliente pode usar esse token para acessar rotas protegidas na API, enviando-o no cabeçalho Authorization das requisições subsequentes.
    


        
## depends é uma função do FastAPI que permite injetar dependências em suas rotas. Nesse caso, estamos usando Depends(pegar_sessao) para injetar a sessão do banco de dados na função de registro. Isso significa que toda vez que a rota de registro for chamada, o FastAPI irá criar uma nova sessão do banco de dados e passá-la para a função de registro como um argumento

