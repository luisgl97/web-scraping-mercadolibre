
from flask import Flask, jsonify, render_template, request, Response
import json

from numpy import product
from functions import todosProductos, limiteProductos
import requests

app = Flask(__name__)
# Api url: https://web-scraping-mercado-libre.herokuapp.com/
#url en postman : https://web-scraping-mercado-libre.herokuapp.com/mercadoLibre 
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

@app.route("/descargarInfo",methods=["GET","POST"])
def descargarInfo():
   
    if request.method == "POST":
        
        producto =  request.form["producto"]
        limite = request.form["limite"]
        
        print(limite)
        
        #Consumir API
        r = requests.get('https://web-scraping-mercado-libre.herokuapp.com/', json={"producto":producto, "limite":int(limite)})
        print(r.status_code)
        print(producto,limite)
        
        if r.status_code==200:
            data = json.loads(r.text)
            # print(data["datos"]["precios"])
            # print(data["datos"]["titulos"])
            # print(data["datos"]["urls"])
            t = ""
            for i,j,z in zip(data["datos"]["precios"],data["datos"]["titulos"],data["datos"]["urls"]):
                print(i,j,z)
                t+=f"{j}|{z}|{i}\n"
                
            return Response(
                t,
                mimetype="text",
                headers = {
                    "Content-disposition":"attachment;filename=datos.txt"
                }
            )
            #print(data)
        return "error"
        pass
    return render_template('index.html')

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)