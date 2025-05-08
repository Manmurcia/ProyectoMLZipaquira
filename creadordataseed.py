import pandas as pd
import random

# Crear dataset sintético
def generar_data_seed(n=100):
    data = {
        "edad": [random.randint(60, 90) for _ in range(n)],
        "sexo": [random.choice(["Masculino", "Femenino"]) for _ in range(n)],
        "comorbilidades": [random.choice(["Ninguna", "Hipertensión", "Diabetes", "Otras"]) for _ in range(n)],
        "uso_leña": [random.choice([0, 1]) for _ in range(n)],
        "tipo_vivienda": [random.choice(["Cerrada", "Ventilada", "Hacinada"]) for _ in range(n)],
        "pm25": [round(random.uniform(10, 60), 2) for _ in range(n)],
        "consultas_respiratorias": [random.randint(0, 10) for _ in range(n)],
        "estrato": [random.choice([1, 2, 3]) for _ in range(n)],
        "actividad_fisica": [random.choice([0, 1]) for _ in range(n)],
        "riesgo_respiratorio": [random.choice(["Bajo", "Medio", "Alto"]) for _ in range(n)]
    }
    return pd.DataFrame(data)

df_seed = generar_data_seed(200)
df_seed.to_csv("data_seed_respiratorio.csv", index=False)