from flask import Flask, render_template, request, jsonify
from ingenieria_datos.creadordataseed import generar_data_seed
from ingenieria_datos.limpieza_datos import limpiar_y_transformar_dataset
from ModeloEntrenamiento import entrenar_modelo
from EvaluarModelo import evaluar_modelo
from Prediccion import predecir_riesgo

import re
from datetime import datetime

def crear_app():

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
    def menu_datos():
        return render_template("Datos.html")

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

    @app.route('/entrenar', methods=['GET', 'POST'])
    def entrenar():
        if request.method == 'POST':
            resultado = entrenar_modelo()
            return render_template(
                "Modelo.html",
                mensaje=resultado["mensaje"],
                mejores_parametros=resultado["mejores_parametros"],
                reporte=resultado["reporte"],
                matriz=resultado["matriz"]
            )
        return render_template("Modelo.html")
    
    @app.route("/fase4")
    def fase4():
        return render_template("Fase4.html")
    
    @app.route('/evaluar')
    def evaluar():
        try:
            resultados = evaluar_modelo()
            return render_template(
                "Evaluacion.html",
                reporte=resultados["reporte_texto"]  # Solo el texto, las imágenes ya están en static/img/
            )
        except Exception as e:
            return f"Error: {str(e)}", 500
    
    @app.route("/fase5")
    def fase5():
        return render_template("Fase5.html")
    
    @app.route('/predecir', methods=['GET', 'POST'])
    def predecir():
        resultado = None
        error = None
        if request.method == 'POST':
            try:
                datos = {
                    'edad': int(request.form['edad']),
                    'sexo': request.form['sexo'],
                    'comorbilidades': request.form['comorbilidades'],
                    'uso_leña': int(request.form['uso_leña']),
                    'tipo_vivienda': request.form['tipo_vivienda'],
                    'pm25': float(request.form['pm25']),
                    'consultas_respiratorias': int(request.form['consultas_respiratorias']),
                    'estrato': int(request.form['estrato']),
                    'actividad_fisica': int(request.form['actividad_fisica'])
                }
                resultado = predecir_riesgo(datos)
            except Exception as e:
                error = str(e)
        return render_template('Prediccion.html', resultado=resultado, error=error)
    
    return app

if __name__ == '__main__':
    app = crear_app()
    app.run(debug=True)
