import pandas as pd

# Cargar el archivo original
df = pd.read_csv("/Users/edselcisneros/Documents/Prediccion-churn-/Archivoscsv/CasosContactCenter.csv")

# 1. Convertir 'Fecha' a datetime
df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

# 2. Convertir 'Hora' a datetime.time (solo la hora, no la fecha)
df['Hora'] = pd.to_datetime(df['Hora'], errors='coerce').dt.time

# 3. Convertir 'AHT' a numérico (float)
df['AHT'] = pd.to_numeric(df['AHT'], errors='coerce')

# 4. Convertir 'RespCSAT' a entero (nullable Int64)
df['RespCSAT'] = pd.to_numeric(df['RespCSAT'], errors='coerce').astype('Int64')

# 5. Convertir 'RespFCR' a entero (nullable Int64)
df['RespFCR'] = pd.to_numeric(df['RespFCR'], errors='coerce').astype('Int64')

# 6. Convertir columnas categóricas a tipo object
categorical_cols = [
    'Por.que.medio.se.enter.de.nosotros',
    'Por.que.canal.nos.esta.contactando',
    'Motivo',
    'Tipificacion_Proceso',
    'Genera.folio.de.seguimiento',
    'id_user',
    'id_caso',
    'id_agente'
]

df[categorical_cols] = df[categorical_cols].astype('object')

# 7. Mostrar tipos de datos finales como verificación
print("📋 Tipos de datos actualizados:")
print(df.dtypes)

# 8. Guardar una copia opcional con sufijo
df.to_csv("CasosContactCenter_TiposConvertidos.csv", index=False)
print("\n✅ Archivo guardado como 'CasosContactCenter_TiposConvertidos.csv'")