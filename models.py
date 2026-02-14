from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float,ForeignKey
from sqlalchemy.orm import  declarative_base
# cria a conexão com o banco de dados, nesse caso, um banco de dados SQLite chamado "banco.db"
db = create_engine("sqlite:///banco.db")

# cria a base para as classes de modelo, que serão usadas para definir as tabelas do banco de dados
Base = declarative_base()

# criar as classes/tabelas do banco 
#usuario
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column("nome", String, index=True)
    email = Column("email", String, unique=True, index=True, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)


    def __init__(self, nome, email, senha, ativo:True, admin: bool = False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin
  
#pedido
class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    #foreign key para relacionar o pedido com o usuário que fez o pedido
    usuario_id = Column("usuario_id", Integer, ForeignKey("usuarios.id"))
    valor_total = Column("valor_total", Float)
    status = Column("status", String) #pendente, pago, cancelado
   

    def __init__(self, usuario_id, valor_total, status):
        self.usuario_id = usuario_id
        self.valor_total = valor_total
        self.status = status

#itenspedido
                  