from flask import Flask, render_template, request
from ingenieria_datos.creadordataseed import generar_data_seed
from ingenieria_datos.limpieza_datos import limpiar_y_transformar_dataset

import re
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("Menu.html")

@app.route("/fase1")
def fase1():
    return render_template("Fase1.html")

@app.route("/fase2")
def fase2():
    return render_template("Fase2.html")

@app.route("/datos")
def menu():
    return render_template("datos.html")

@app.route('/generar', methods=['POST'])
def generar():
    mensaje = generar_data_seed() 
    return mensaje

@app.route('/procesar', methods=['POST'])
def procesar():
    mensaje = limpiar_y_transformar_dataset("dataseed_respiratorio.csv", "data_ready.csv")
    return mensaje

@app.route("/fase3")
def fase3():
    return render_template("Fase3.html")




if __name__ == '__main__':
    app.run(debug=True)
