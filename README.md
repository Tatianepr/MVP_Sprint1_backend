# Minha API

Este é o XXX da sprint XXX do custo de **Engenharia de Software** da **XXXX**

O objetivo aqui é disponibilizar o projeto XXXX, onde foi desenvolvido um controle simples de despesas.

## Principais APIs

1) DELETE - despesa
2) GET - despesa
3) POST -despesa
4) PUT - despesa
5) GET - despesas
---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

PAra criar um ambiente virtual: 

```
python -m virtualenv env
.\env\Scripts\activate.bat
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.
```
(env)$ pip install -r requirements.txt
```



Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```flask run --host 0.0.0.0 --port 5000 --reload
(env)$ 
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
