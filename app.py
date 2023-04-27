# openapi3 - framework baseado no Flask que verifica dados e gera documentação automatizada
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, jsonify
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc
from model import Session
from logger import logger
from schemas.error import ErrorSchema
from schemas.despesa import ListagemDespesasSchema, DespesaBuscaEdicaoSchema, DespesaViewSchema, DespesaSchema,Despesa, apresenta_despesa, apresenta_despesas, DespesaBuscaSchema, DespesaDelSchema, retorna_despesa, DespesaPutSchema
from schemas.categoria import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

""" Gerando documentação
    são 3 os principais elementos : Tags, Rotas com padrões de respostas bem definidas e Schemas. 
"""

# definindo tags, uma para cada contexto
home_tag = Tag(name="Documentação das APIs",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
despesa_tag = Tag(
    name="Despesa", description="Adição, visualização, edição e remoção de despesas da base, vinculadas a categorias.")

categoria_tag = Tag(name="Categoria", description="Adição e listagem de categorias cadastradas na base.")


# agrupa as tags nas rotas conforme seu contexto. aqui está a tag home_tag sendo usada.
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/despesa', tags=[despesa_tag],
          responses={"200": DespesaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_despesa(form: DespesaSchema):
    """Adiciona uma nova despesa à base de dados e associa uma categoria existente.

    Retorna uma representação da despesa.
    """
    categoria_id = form.categoria_id
    logger.debug(f"Adicionado despesas a categoria #{categoria_id}")
                 
    # criando conexão com a base
    session = Session()
    # verificando se existe a categoria cadastrada
    categoria=session.query(Categoria).filter(Categoria.id==categoria_id).first()
           
    if not categoria:
        error_msg = "Categoria não encontrada na base :/"
        logger.warning(f"Erro ao adicionar despesa para a categoria '{categoria_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    
    try:
        despesa = Despesa(
            descricao=form.descricao,
            valor=form.valor,
            pago=form.pago,
            data_vencimento=form.data_vencimento)
      
        # adicionando o despesa a categoria.
        categoria.adiciona_despesa(despesa)

        session.commit()

        logger.debug(f"Adicionando a despesa: '{despesa.descricao}'")
      
        # usa como retorno os schemas criados no diretório schemas
        return apresenta_despesa(despesa, categoria), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Despesa de mesmo nome já salvo na base :/"
        logger.warning(
            f"Erro ao adicionar despesa '{despesa.descricao}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(
            f"Erro ao adicionar despesa '{despesa.descricao}', {error_msg}")
        return {"mesage": error_msg}, 400

@app.get('/despesas', tags=[despesa_tag],
         responses={"200": ListagemDespesasSchema, "404": ErrorSchema})
def get_despesas():
    """Faz a busca por todos as despesas cadastradas.

    Retorna uma representação da listagem de despesas.
    """
    logger.debug(f"Coletando despesas ")

    # criando conexão com a base
    session = Session()
    despesas = session.query(Despesa, Categoria).join(Categoria).all()
    

    if not despesas:
        # se não há despesas cadastradas
        return {"despesas": []}, 200
    else:
        logger.debug(f"%d despesas encontradas" % len(despesas))
        # retorna a representação da despesa
        return apresenta_despesas(despesas), 200


@app.get('/despesa', tags=[despesa_tag],
         responses={"200": DespesaViewSchema, "404": ErrorSchema})
def get_despesa(query: DespesaBuscaSchema):
    """Faz a busca por uma Despesa a partir do nome. Função não usada no front-end.

    Retorna uma representação da despesa encontrada.
    """
    despesa_descricao = query.descricao
    logger.debug(f"Coletando dados sobre despesa #{despesa_descricao}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    despesa = session.query(Despesa, Categoria).join(Categoria).filter(
        Despesa.descricao == despesa_descricao).first()

    if not despesa:
        # se a despesa não foi encontrada
        error_msg = "Despesa não encontrada na base :/"
        logger.warning(
            f"Erro ao buscar despesa '{despesa_descricao}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Despesa encontrada: '{despesa_descricao}'")
        # retorna a representação da despesa
        return retorna_despesa(despesa), 200


@app.delete('/despesa', tags=[despesa_tag],
            responses={"200": DespesaDelSchema, "404": ErrorSchema})
def del_despesa(query: DespesaBuscaSchema):
    """Deleta uma despesa a partir do nome informado

    Retorna uma mensagem de confirmação da remoção.
    """
    despesa_descricao = unquote(unquote(query.descricao))
    print(despesa_descricao)
    logger.debug(f"Deletando dados sobre despesa #{despesa_descricao}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Despesa).filter(
        Despesa.descricao == despesa_descricao).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado despesa #{despesa_descricao}")
        return {"mesage": "Despesa removida", "id": despesa_descricao}
    else:
        # se a despesa não foi encontrada
        error_msg = "Despesa não encontrado na base :/"
        logger.warning(
            f"Erro ao deletar despesa #'{despesa_descricao}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.put('/paga', tags=[despesa_tag],
         responses={"200": DespesaDelSchema, "404": ErrorSchema})
def paga_despesa(query: DespesaBuscaSchema):
    """Atualiza o status de pagamento de uma despesa a partir do nome informado. 

    """
    despesa_descricao = unquote(unquote(query.descricao))
    print(despesa_descricao)
    logger.debug(f"Atualizando dados sobre despesa #{despesa_descricao}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    despesa = session.query(Despesa).filter(
        Despesa.descricao == despesa_descricao).first()

    if despesa:
        despesa.pago = not despesa.pago
        session.commit()
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Atualizando despesa #{despesa_descricao}")
        return {"mesage": "Despesa atualizada", "descricao": despesa_descricao}
    else:
        # se o produto não foi encontrado
        error_msg = "Despesa não encontrado na base :/"
        logger.warning(
            f"Erro ao atualizar despesa #'{despesa_descricao}', {error_msg}")
        return {"mesage": error_msg}, 404

@app.put('/despesa', tags=[despesa_tag], 
         responses={"200": DespesaPutSchema, "404": ErrorSchema})
def edita_despesa(query: DespesaBuscaEdicaoSchema):
    """Atualiza uma despesa a partir do nome informado. 

    API responsável por editar descrição, valor, data de vencimento e categoria associada. 

    """
    despesa_id = query.id
    despesa_descricao = query.descricao
    despesa_valor = query.valor
    despesa_vencimento = query.data_vencimento
    despesa_id_categoria=query.categoria_id

    print(despesa_descricao)
    
    logger.debug(f"Atualizando dados sobre despesa #{despesa_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a edição de acordo com o ID da despesa.
    despesa = session.query(Despesa).filter(
        Despesa.id == despesa_id).first()
    # retorna representação da despesa editada.
    if despesa:
        despesa.descricao =  despesa_descricao
        despesa.valor = despesa_valor
        despesa.data_vencimento = despesa_vencimento
        despesa.categoria = despesa_id_categoria

        session.commit()
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Atualizando despesa #{despesa_id}")
        return {"mesage": "Despesa atualizada com sucesso", "despesa": apresenta_despesa(despesa)}, 200
 
    else:
        # se o produto não foi encontrado
        error_msg = "Despesa não encontrado na base :/"
        logger.warning(
            f"Erro ao atualizar despesa #'{despesa_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    

@app.post('/categoria', tags=[categoria_tag],
          responses={"200": CategoriaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_categoria(form: CategoriaSchema):
    """Adiciona uma nova categoria à base de dados

    Retorna uma representação da categoria.
    """
    categoria = Categoria(
        nome=form.nome)
    logger.debug(f"Adicionando a categoria: '{categoria.nome}'")
    try:
        # criando conexão com a base
        session = Session()

        # adicionando uma categoria
        session.add(categoria)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado categoria de nome: '{categoria.nome}'")

        # usa como retorno os schemas criados no diretório schemas
        return apresenta_categoria(categoria), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Categoria de mesmo nome já salvo na base :/"
        logger.warning(
            f"Erro ao adicionar categoria '{categoria.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(
            f"Erro ao adicionar categoria '{categoria.nome}', {error_msg}")
        return {"mesage": error_msg}, 400

@app.get('/categorias', tags=[categoria_tag],
         responses={"200": ListagemCategoriasSchema, "404": ErrorSchema})
def get_categorias():
    """Faz a busca por todas as categorias cadastradas

    Retorna uma representação da listagem de categorias.
    """

    logger.debug(f"Coletando categorias ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    categorias = session.query(Categoria).all()

    if not categorias:
        # se não há categorias cadastradas
        return {"categorias": []}, 200
    else:
        logger.debug(f"%d categorias encontradas" % len(categorias))
        # retorna a representação de comentarios
        print(categorias)
        return apresenta_categorias(categorias), 200
