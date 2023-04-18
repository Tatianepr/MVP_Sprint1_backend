from sqlalchemy import Column, String, Integer, Boolean, Date, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime, date
from typing import Union

from model import Base


class Despesa(Base):
    __tablename__ = 'despesa'

    id = Column("pk_despesa", Integer, primary_key=True)
    descricao = Column(String(140), unique=True)
    valor = Column(Float)
    pago = Column(Boolean)
    data_vencimento = Column(Date)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o produto e o comentário.
    # Essa relação é implicita, não está salva na tabela 'produto',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    # comentarios = relationship("Comentario")

    def __init__(self, descricao: str, valor: float, pago: Boolean, data_vencimento: Date,
                 data_insercao: Union[DateTime, None] = None):
        """
        Cria uma Despesa

        Arguments:
            descricao: nome da despesa.
            valor: valor esperado para da despesa
            data_vencimento: vencimento da despesa
            data_insercao: data de quando a despesa foi inserida na base
        """
        self.descricao = descricao
        self.valor = valor
        self.pago = pago
        self.data_vencimento = data_vencimento

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    # def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao Produto
        """
        # self.comentarios.append(comentario)
