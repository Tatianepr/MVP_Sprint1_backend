# pydantic - framework para geração de documentação das APIs
# serve também para validar requisições enviadas
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from model.despesa import Despesa

# from schemas import ComentarioSchema

# aqui está exemplificado o uso de schemas para definir um formato de uma requisição.


class DespesaSchema(BaseModel):
    """ Define como um novo produto a ser inserido deve ser representado
        define um modelo de dados e como será comunicado com o cliente
    """
    descricao: str = "Inglês"
    valor: float = 460.50
    pago: bool = False
    data_vencimento: date = datetime.strptime('13/04/2023', '%d/%m/%Y').date()


class DespesaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da despesa.
    """
    descricao: str = "inglês"

class DespesaBuscaEdicaoSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca para edição da despesa. 
    """
    id: int = 1
    descricao: str = "inglês"
    valor: float = 12.50
    data_vencimento: date = datetime.strptime('13/04/2023', '%d/%m/%Y').date()

class ListagemDespesasSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    despesas: List[DespesaSchema]


def apresenta_despesas(despesas: List[Despesa]):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for despesa in despesas:
        result.append({
            "id":despesa.id,
            "descricao": despesa.descricao,
            "valor": despesa.valor,
            "pago": despesa.pago,
            "data_vencimento": despesa.data_vencimento.strftime('%d/%m/%Y'),
        })

    return {"despesas": result}


class DespesaViewSchema(BaseModel):
    """ Define como uma despesa será retornada: despesa + comentários.
    """
    id: int = 1
    descricao: str = "Ingês"
    valor: float = 12.50
    pago: bool = False
    data_vencimento: date = datetime.strptime('13/04/2023', '%d/%m/%Y').date()
   


class DespesaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    descricao: str


def apresenta_despesa(despesa: Despesa):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "id": despesa.id,
        "nome": despesa.descricao,
        "valor": despesa.valor,
        "pago": despesa.pago,
        "data_vencimento": despesa.data_vencimento.strftime('%d/%m/%Y')
    }
