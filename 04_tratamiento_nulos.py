import pandas as pd

# Cargar el archivo con tipos corregidos
df = pd.read_csv("/Users/edselcisneros/Documents/Prediccion-churn-/CasosContactCenter_TiposConvertidos.csv")
# Convertir columnas necesarias
df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
df['Hora'] = pd.to_datetime(df['Hora'], errors='coerce').dt.time

# Mostrar nulos y ceros por columna
print("🔍 Valores nulos y ceros por columna:")
for col in df.columns:
    ceros = (df[col] == 0).sum() if df[col].dtype != 'object' else 0
    nulos = df[col].isnull().sum()
    print(f"{col}: {nulos} nulos, {ceros} ceros")

# Identificar columnas con más del 15% de nulos
print("\n⚠️ Columnas con más del 15% de valores nulos:")
limite = 0.15 * len(df)
for col in df.columns:
    nulos = df[col].isnull().sum()
    if nulos > limite:
        print(f"- {col}: {nulos} nulos ({round(nulos/len(df)*100, 2)}%)")

# Contar cuántos nulos o ceros hay por fila (criterio: eliminar si tiene 2 o más)
print("\n🗑️ Eliminando filas con 2 o más nulos o ceros...")

# Función para contar nulos + ceros en cada fila
def contar_faltantes(fila):
    count = 0
    for col in df.columns:
        if pd.isnull(fila[col]):
            count += 1
        elif isinstance(fila[col], (int, float)) and fila[col] == 0:
            count += 1
    return count

df['total_faltantes'] = df.apply(contar_faltantes, axis=1)
df_limpio = df[df['total_faltantes'] < 2].drop(columns='total_faltantes')
print(f"Filas eliminadas: {len(df) - len(df_limpio)}")

# Imputación inteligente por grupo (ejemplo propuesto)
# Imputar AHT por combinación de 'Motivo' y 'Por.que.canal.nos.esta.contactando'
print("\n🛠️ Imputando valores restantes usando media por grupo...")

df_limpio['AHT'] = df_limpio.groupby(
    ['Motivo', 'Por.que.canal.nos.esta.contactando']
)['AHT'].transform(lambda x: x.fillna(x.mean()))

# Imputar RespCSAT por 'Por.que.canal.nos.esta.contactando'
df_limpio['RespCSAT'] = df_limpio.groupby(
    'Por.que.canal.nos.esta.contactando'
)['RespCSAT'].transform(lambda x: x.fillna(round(x.mean())))

# Imputar RespFCR por 'Motivo'
df_limpio['RespFCR'] = df_limpio.groupby(
    'Motivo'
)['RespFCR'].transform(lambda x: x.fillna(round(x.mean())))

# Guardar resultado final
df_limpio.to_csv("CasosContactCenter_Limpio.csv", index=False)
print("\n✅ Archivo final guardado como 'CasosContactCenter_Limpio.csv'")