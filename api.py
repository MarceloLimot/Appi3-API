import flask
from flask import Flask

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask("API")

credpath = r"appi3-7e0c1-firebase-adminsdk-rxlwa-f202ad8fc5.json"
login = credentials.Certificate(credpath)
firebase_admin.initialize_app(login)
db = firestore.client()
produtos = db.collection("Produtos").stream()
lista_produto = list(produtos)
tamanho = len(lista_produto)


@app.route("/", methods=["GET"])
def home():
    return {"produtos": f"{tamanho}"}


@app.route("/produtos/<string:cod_prod>/", methods=["GET"])
def busca_prod(cod_prod):
    cont_item = 0
    busca = 0
    for produto in lista_produto:
        cont_item = cont_item + 1
        prod = produto.to_dict()
        if cod_prod == prod.get('cod'):
            itens_produto = dict(nome=prod.get('nome'),
                                 qtd=prod.get('qtd'),
                                 valor=prod.get('valor'))
            return itens_produto
            busca = 1
        if cont_item >= tamanho and busca == 0:
            return {"Erro": "Nenhum produto encontrado com o codigo informado!"}


if __name__ == "__main__":
    app.run(debug=True)
