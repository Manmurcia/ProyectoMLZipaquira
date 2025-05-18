import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score
import numpy as np

def evaluar_modelo(ruta_modelo="modelo/modelo_rf.pkl", ruta_datos="ingenieria_datos/data/data_ready.csv", ruta_graficas="static/img"):
    try:
        os.makedirs(ruta_graficas, exist_ok=True)

        # Cargar datos y modelo
        df = pd.read_csv(ruta_datos)
        X = df.drop("riesgo_respiratorio", axis=1)
        y = df["riesgo_respiratorio"]

        modelo = joblib.load(ruta_modelo)
        y_pred = modelo.predict(X)

        # 1. Matriz de confusión
        cm = confusion_matrix(y, y_pred)  # <-- Falta esta línea
        plt.figure(figsize=(6, 4))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
        plt.title("Matriz de Confusión")
        plt.xlabel("Predicción")
        plt.ylabel("Real")
        plt.tight_layout()
        plt.savefig(os.path.join(ruta_graficas, "matriz_confusion.png"))
        plt.close()

        # 2. Métricas por clase
        reporte = classification_report(y, y_pred, output_dict=True)
        df_reporte = pd.DataFrame(reporte).transpose().iloc[:-3, :]
        df_reporte[["precision", "recall", "f1-score"]].plot(kind="bar", figsize=(8, 5))
        plt.title("Métricas por Clase")
        plt.ylabel("Valor")
        plt.ylim(0, 1)
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.savefig(os.path.join(ruta_graficas, "metricas_clase.png"))
        plt.close()

        # 3. Validación cruzada (accuracy por fold)
        scores = cross_val_score(modelo, X, y, cv=5, scoring='accuracy')
        plt.figure(figsize=(6, 4))
        sns.barplot(x=[f"Fold {i+1}" for i in range(5)], y=scores)
        plt.ylim(0, 1)
        plt.title("Validación Cruzada (Accuracy por Fold)")
        plt.ylabel("Accuracy")
        plt.tight_layout()
        plt.savefig(os.path.join(ruta_graficas, "validacion_cruzada.png"))
        plt.close()

        # 4. Importancia de variables
        importancias = modelo.feature_importances_
        indices = np.argsort(importancias)[::-1]
        nombres = X.columns[indices]
        plt.figure(figsize=(8, 5))
        sns.barplot(x=importancias[indices], y=nombres)
        plt.title("Importancia de Variables")
        plt.xlabel("Importancia")
        plt.tight_layout()
        plt.savefig(os.path.join(ruta_graficas, "importancia_variables.png"))
        plt.close()

        return {
            "reporte_texto": classification_report(y, y_pred),
            "scores_cv": scores.tolist(),  
            "graficas": [
                "matriz_confusion.png",
                "metricas_clase.png",
                "validacion_cruzada.png",
                "importancia_variables.png"
            ]
        }
    except Exception as e:
        print(f"Error en EvaluarModelo: {str(e)}")
        raise
