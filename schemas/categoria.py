from pydantic import BaseModel
from typing import Optional, List
from model.categoria import Categoria


class CategoriaSchema(BaseModel):
    """ Define como uma nova categoria a ser inserida deve ser representada.
    """
    #id: int = 1
    nome: str = "Alimentação"

class CategoriaViewSchema(BaseModel):
    """ Define como um categoria será retornada.
    """
    id: int = 1
    nome: str = "Alimentação"


class CategoriaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no ID da categoria.
    """
    id: int = "1"

class ListagemCategoriasSchema(BaseModel):
    """ Define como uma listagem de categorias será retornada.
    """
    categoria:List[CategoriaViewSchema]

def apresenta_categorias(categorias: List[Categoria]):
    """ Retorna uma representação da categoria seguindo o schema definido em
        Categoria.
    """
    result = []
    for categoria in categorias:
        result.append({
            "id": categoria.id,
            "nome": categoria.nome,
        })

    return {"categorias": result}

def apresenta_categoria(categoria: Categoria):
    """ Retorna uma representação da Categoria seguindo o schema definido em
        Categoria.
    """
    return {
        "id": categoria.id,
        "nome": categoria.nome
    }

class CategoriaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str