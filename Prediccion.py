import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

modelo = joblib.load('modelo/modelo_rf.pkl')

COLUMNAS_MODELO = [
    'edad',
    'sexo',
    'comorbilidades',
    'uso_leña',
    'tipo_vivienda',
    'pm25',
    'consultas_respiratorias',
    'estrato',
    'actividad_fisica'
]

# Pre-cargar los LabelEncoders (deben ser los mismos usados en entrenamiento)
label_encoders = {
    'sexo': LabelEncoder().fit(['Masculino', 'Femenino']),
    'comorbilidades': LabelEncoder().fit(['Ninguna', 'Hipertensión', 'Diabetes', 'Otras']),
    'tipo_vivienda': LabelEncoder().fit(['Cerrada', 'Ventilada', 'Hacinada'])
}

# Mapeo de clases numéricas a nombres
CLASES_RIESGO = {0: 'Bajo', 1: 'Medio', 2: 'Alto'}

def predecir_riesgo(datos_dict):
    try:
        # Filtrar y preparar datos
        datos_filtrados = {k: datos_dict[k] for k in COLUMNAS_MODELO if k in datos_dict}
        df = pd.DataFrame([datos_filtrados])

        # Convertir variables categóricas
        df['sexo'] = label_encoders['sexo'].transform(df['sexo'])
        df['tipo_vivienda'] = label_encoders['tipo_vivienda'].transform(df['tipo_vivienda'])
        df['comorbilidades'] = label_encoders['comorbilidades'].transform(df['comorbilidades'])

        # Asegurar tipos de datos numéricos
        df['edad'] = df['edad'].astype(int)
        df['pm25'] = df['pm25'].astype(float)
        df['consultas_respiratorias'] = df['consultas_respiratorias'].astype(int)
        df['estrato'] = df['estrato'].astype(int)
        df['uso_leña'] = df['uso_leña'].astype(int)
        df['actividad_fisica'] = df['actividad_fisica'].astype(int)

        # Validar que todas las columnas esperadas están presentes
        for col in COLUMNAS_MODELO:
            if col not in df.columns:
                raise ValueError(f"Columna faltante: {col}")

        # Reordenar columnas según lo esperado por el modelo
        df = df[COLUMNAS_MODELO]

        # Realizar predicción
        prediccion = modelo.predict(df)[0]
        proba = modelo.predict_proba(df)[0]  # Array de probabilidades por clase

        return {
            'prediccion': int(prediccion),
            'probabilidades': {CLASES_RIESGO[i]: round(float(p), 2) for i, p in enumerate(proba)},
            'categoria_riesgo': CLASES_RIESGO.get(prediccion, 'Desconocido')
        }
    except Exception as e:
        raise RuntimeError(f"Error en predicción: {str(e)}")