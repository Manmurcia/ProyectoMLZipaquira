import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
import joblib

def entrenar_modelo(ruta_csv="ingenieria_datos/data/data_ready.csv", ruta_modelo="modelo/modelo_rf.pkl"):
    os.makedirs(os.path.dirname(ruta_modelo), exist_ok=True)

    df = pd.read_csv(ruta_csv)
    X = df.drop("riesgo_respiratorio", axis=1)
    y = df["riesgo_respiratorio"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # Hiperparámetros
    param_grid = {
        "n_estimators": [100, 150, 200],
        "max_depth": [None, 10, 20],
        "min_samples_split": [2, 5, 10]
    }

    grid = GridSearchCV(
        RandomForestClassifier(random_state=42),
        param_grid,
        cv=5,
        n_jobs=-1,
        scoring='accuracy'
    )
    grid.fit(X_train, y_train)

    modelo_optimizado = grid.best_estimator_
    y_pred = modelo_optimizado.predict(X_test)

    reporte = classification_report(y_test, y_pred)
    matriz = confusion_matrix(y_test, y_pred)

    joblib.dump(modelo_optimizado, ruta_modelo)

    return {
        "mensaje": f"Modelo entrenado correctamente y guardado en {ruta_modelo}.",
        "mejores_parametros": grid.best_params_,
        "reporte": reporte,
        "matriz": matriz
    }
