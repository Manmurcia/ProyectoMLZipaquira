import pandas as pd
import random
import os

def generar_data_seed(n=200, ruta_salida="ingenieria_datos/data/dataseed_respiratorio.csv"):
    # Crear datos aleatorios
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

    df = pd.DataFrame(data)
    
    # Asegurar que el directorio existe
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    
    # Guardar con manejo de errores
    try:
        df.to_csv(ruta_salida, index=False)
        return f"✅ Archivo guardado en: {os.path.abspath(ruta_salida)}"
    except Exception as e:
        return f"❌ Error al guardar: {e}"

# Ejemplo de uso
print(generar_data_seed())
