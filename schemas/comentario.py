from pydantic import BaseModel
from typing import Optional, List
from model.produto import Comentario


class ComentarioSchema(BaseModel):
    """ Define como um novo comentário a ser inserido deve ser representado
    """
    produto_id: int = 1
    texto: str = "Só comprar se o preço realmente estiver bom!"


class ComentarioBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no ID do produto.
    """
    produto_id: int = "1"

class ListagemComentariosSchema(BaseModel):
    """ Define como uma listagem de comentários será retornada.
    """
    comentarios:List[ComentarioSchema]

def apresenta_comentarios(comentarios: List[Comentario]):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for comentario in comentarios:
        result.append({
            "id": comentario.id,
            "texto": comentario.texto,
        })

    return {"comentarios": result}