from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from typing import Union
from sqlalchemy.orm import relationship
from model import Base
from model.despesa import Despesa

class Categoria(Base):
    __tablename__ = 'categoria'

    id = Column("pk_categoria", Integer, primary_key=True)
    nome = Column(String(140))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre a despesa e a categoria.
    # Essa relação é implicita, não está salva na tabela 'despesa',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
   
    despesas = relationship("Despesa")

    def __init__(self, nome: str, data_insercao: Union[DateTime, None] = None):
        """
        Cria uma Categoria

        Arguments:
            nome: o nome de uma categoria.
            data_insercao: data de quando a categoria foi criada ou inserida.
                           à base
        """
        self.nome = nome
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_despesa(self, despesa:Despesa):
        """ Adiciona um novo comentário ao Produto
        """
        self.despesas.append(despesa)