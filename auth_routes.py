from models import db
from sqlalchemy.orm import sessionmaker
from dependencies import pegar_sessao, verificar_token
from fastapi import APIRouter, HTTPException, Depends
from models import Usuario
from main import bcrypt_context
from schemas import UsuarioSchema, loginSchema
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from main import AlgORITHM, Access_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from fastapi.security import OAuth2PasswordRequestForm
#ESSE é o meu prefixo do meu router, ou seja, todas as rotas que eu criar aqui dentro do auth_router vão começar com /auth
auth_router = APIRouter(prefix="/auth", tags=["auth"])


def criar_token(id_usuario, duracao_token=timedelta(minutes=Access_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, algorithm=AlgORITHM)
    return jwt_codificado


  
def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif bcrypt_context.verify(senha, usuario.senha) == False:
        return False
    return usuario

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
 usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
 if not usuario:
    raise HTTPException(status_code=400, detail="Email ou senha incorretos")
 else:
      access_token = criar_token(usuario.id)
      reflesh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
      return {"access_token": access_token, "refresh_token": reflesh_token, "token_type": "bearer"}
 

@auth_router.post("/Login.form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
 usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
 if not usuario:
    raise HTTPException(status_code=400, detail="Email ou senha incorretos")
 else:
      access_token = criar_token(usuario.id)
     
      return {"access_token": access_token, "token_type": "bearer"}
 

@auth_router.get("/refresh")
async def use_refresh_token(
    usuario_id: str = Depends(verificar_token),
    session: Session = Depends(pegar_sessao)
):
    usuario = session.query(Usuario).filter(Usuario.id == int(usuario_id)).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    access_token = criar_token(usuario.id)
    return {"access_token": access_token, "token_type": "bearer"}

##autenticar_usuario é uma função que verifica se um usuário com o email e senha fornecidos existe no banco de dados. Ele consulta o banco de dados para encontrar um usuário com o email fornecido, e se encontrar, verifica se a senha fornecida corresponde à senha armazenada no banco de dados usando a função verify do bcrypt_context. Se o usuário não for encontrado ou a senha não corresponder, a função retorna False. Caso contrário, ela retorna o objeto do usuário autenticado.



# Criar_token é uma função que gera um token JWT para um usuário autenticado. Ele recebe o ID do usuário como argumento, calcula a data de expiração do token com base no tempo atual e no tempo de expiração definido, e cria um dicionário de informações que inclui o ID do usuário e a data de expiração. Em seguida, ele codifica esse dicionário em um token JWT usando a chave secreta e o algoritmo especificados, e retorna o token codificado.


 ## acess_token é o token de acesso que será retornado para o cliente após um login bem-sucedido. Ele é criado usando a função criar_token, que gera um token único para o usuário com base em seu ID. O token_type "bearer" indica que o token é do tipo Bearer, que é um tipo comum de token de acesso usado em APIs para autenticação e autorização. O cliente pode usar esse token para acessar rotas protegidas na API, enviando-o no cabeçalho Authorization das requisições subsequentes.
    
        
## depends é uma função do FastAPI que permite injetar dependências em suas rotas. Nesse caso, estamos usando Depends(pegar_sessao) para injetar a sessão do banco de dados na função de registro. Isso significa que toda vez que a rota de registro for chamada, o FastAPI irá criar uma nova sessão do banco de dados e passá-la para a função de registro como um argumento


##reflesh_token é um token de atualização que é criado para permitir que o cliente obtenha um novo token de acesso sem precisar fazer login novamente. Ele é criado usando a função criar_token, mas com uma duração de token mais longa (neste caso, 7 dias). O cliente pode usar esse token de atualização para solicitar um novo token de acesso quando o token de acesso atual expirar, sem precisar fornecer as credenciais do usuário novamente. Isso melhora a experiência do usuário, permitindo que eles permaneçam autenticados por um período mais longo sem precisar fazer login repetidament