import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

def limpiar_y_transformar_dataset(input_filename, output_filename):
    input_path = os.path.join("ingenieria_datos", "data", input_filename)
    output_path = os.path.join("ingenieria_datos", "data", output_filename)

    df = pd.read_csv(input_path)

    # Verificar si hay valores nulos
    print("Valores nulos en el dataset:")
    print(df.isnull().sum())

    # Filtrar datos irreales
    df = df[(df['edad'] >= 60) & (df['edad'] <= 100)]
    df = df[df['pm25'] < 100]
    df = df[df['consultas_respiratorias'] < 20]
    df = df[(df['estrato'] >= 1) & (df['estrato'] <= 6)]
    df = df[df['sexo'].isin(['Masculino', 'Femenino'])]
    df = df[df['comorbilidades'].isin(['Ninguna', 'Hipertensión', 'Diabetes', 'Otras'])]
    df = df[df['tipo_vivienda'].isin(['Cerrada', 'Ventilada', 'Hacinada'])]

    # Asegurar tipos correctos
    df["edad"] = df["edad"].astype(int)
    df["pm25"] = df["pm25"].astype(float)
    df["consultas_respiratorias"] = df["consultas_respiratorias"].astype(int)

    # Transformación categórica
    label_cols = ["sexo", "comorbilidades", "tipo_vivienda", "riesgo_respiratorio"]
    for col in label_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])

    # Normalización de columnas numéricas
    numeric_cols = ["edad", "pm25", "consultas_respiratorias"]
    scaler = MinMaxScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    # Guardar el dataset limpio
    df.to_csv(output_path, index=False)
    print("limpieza y transformacion de datos terminada y guardada. Dataset listo para usar.")

    return "Dataset procesado y guardado exitosamente."
