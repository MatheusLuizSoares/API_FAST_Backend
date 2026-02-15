from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float,ForeignKey
from sqlalchemy.orm import  declarative_base
from sqlalchemy_utils.types import ChoiceType


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


    def __init__(self, nome, email, senha, ativo=True, admin=False):
     self.nome = nome
     self.email = email
     self.senha = senha
     self.ativo = ativo
     self.admin = admin

  
#pedido
class Pedido(Base):
    __tablename__ = "pedidos"
  #  status_pedidos = {
   #     "PENDENTE": "PENDENTE",
    #    "FINALIZADO": "FINALIZADO",
     #   "CANCELADO": "CANCELADO"
    #}


    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    #foreign key para relacionar o pedido com o usuário que fez o pedido
    usuario_id = Column("usuario_id", Integer, ForeignKey("usuarios.id"))
    valor_total = Column("valor_total", Float)
    status = Column("status", String) #pendente, pago, cancelado
   

    def __init__(self, usuario_id, valor_total, status="PEDENTE"):
        self.usuario_id = usuario_id
        self.valor_total = valor_total
        self.status = status

#itenspedido
class ItemPedido(Base):
    __tablename__ = "itens_pedido"
    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    pedido_id = Column("pedido_id", Integer, ForeignKey("pedidos.id"))
    nome_produto = Column("nome_produto", String)
    quantidade = Column("quantidade", Integer)
    tamanho = Column("tamanho", String)
    sabor = Column("sabor", String)
    preco_unitario = Column("preco_unitario", Float)

    def __init__(self, pedido_id, nome_produto, quantidade, preco_unitario):
        self.pedido_id = pedido_id
        self.nome_produto = nome_produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario                  