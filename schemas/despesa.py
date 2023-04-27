# pydantic - framework para geração de documentação das APIs
# serve também para validar requisições enviadas
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from model.despesa import Despesa
from model.categoria import Categoria


# aqui está exemplificado o uso de schemas para definir um formato de uma requisição.


class DespesaSchema(BaseModel):
    """ Define como uma nova despesa a ser inserida deve ser representada
        define um modelo de dados e como será comunicado com o cliente
    """
    from schemas.categoria import CategoriaViewSchema
    descricao: str = "Inglês"
    valor: float = 460.50
    pago: bool = False
    data_vencimento: date = datetime.strptime('13/04/2023', '%d/%m/%Y').date()
    categoria_id: int = 1


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
    #pago: bool = False
    data_vencimento: date = datetime.strptime('13/04/2023', '%d/%m/%Y').date()
    categoria_id: int = 1

class DespesaViewSchema(BaseModel):
    """ Define como uma despesa será retornada: despesa + comentários.
    """

    id: int = 1
    descricao: str = "Ingês"
    valor: float = 12.50
    pago: bool = False
    data_vencimento: date = datetime.strptime('13/04/2023', '%d/%m/%Y').date()
    categoria_id: int = 1
    categoria_nome: str = "Alimentação"


class ListagemDespesasSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    despesas: List[DespesaViewSchema]


def apresenta_despesas(despesas: List[tuple[Despesa, Categoria]]):
    """ Retorna uma representação da despesa seguindo o schema definido em
        DespesaViewSchema.
    """
    result = []
    for Despesa, Categoria in despesas:
        result.append({
            "id":Despesa.id,
            "descricao": Despesa.descricao,
            "valor": Despesa.valor,
            "pago": Despesa.pago,
            "data_vencimento": Despesa.data_vencimento.strftime('%d/%m/%Y'),
            "categoria_id": Categoria.id,
            "categoria_nome": Categoria.nome
        })

    return {"despesas": result}

class DespesaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    descricao: str

class DespesaPutSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    Despesa: DespesaBuscaEdicaoSchema

def apresenta_despesa(despesa: Despesa, categoria: Categoria=None):
    """ Retorna uma representação da despesa seguindo o schema definido em
        ProdutoViewSchema.
    """
    if categoria:
        return {
            "id": despesa.id,
            "descricao": despesa.descricao,
            "valor": despesa.valor,
            "pago": despesa.pago,
            "data_vencimento": despesa.data_vencimento.strftime('%d/%m/%Y'),
            "categoria_id": categoria.id,
            "categoria_nome": categoria.nome
        }
    else:
        return {
            "id": despesa.id,
            "descricao": despesa.descricao,
            "valor": despesa.valor,
            "data_vencimento": despesa.data_vencimento.strftime('%d/%m/%Y'),
            "categoria_id": despesa.categoria
        }

def retorna_despesa(despesa: tuple[Despesa, Categoria]):
    """ Retorna uma representação da despesa seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "id": despesa.Despesa.id,
        "descricao": despesa.Despesa.descricao,
        "valor": despesa.Despesa.valor,
        "pago": despesa.Despesa.pago,
        "data_vencimento": despesa.Despesa.data_vencimento.strftime('%d/%m/%Y'),
        "categoria_id": despesa.Categoria.id,
        "categoria_nome": despesa.Categoria.nome
    }