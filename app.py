
from flask import Flask, jsonify, request
import json
from functions import todosProductos, limiteProductos

app = Flask(__name__)

@app.route('/mercadoLibre',methods=["GET"])
def mercadoLibre():
    url='https://listado.mercadolibre.com.pe/'
    data = json.loads(request.data)
    #si la llave limite no esta en data
    if 'limite' not in data:
        #devuelve todos los productos
        titulos,urls,precios = todosProductos(url,data["producto"])
    else:
        titulos,urls,precios = limiteProductos(url,data["producto"],data["limite"])
    return jsonify({
        "datos":{
            "titulos":titulos,
            "urls":urls,
            "precios":precios
        }
    })

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)