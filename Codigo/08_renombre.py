import pandas as pd

# Cargar el archivo final con índice corregido
df = pd.read_csv("/Users/edselcisneros/Documents/Prediccion-churn-/CasosContactCenter_ConIndice.csv")

# Renombrar columnas: reemplazar espacios, puntos y poner minúsculas
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace(".", "_")

# Verificación
print("✅ Nuevos nombres de columnas:")
print(df.columns)

# Guardar resultado con nombres estandarizados
df.to_csv("/Users/edselcisneros/Documents/Prediccion-churn-/CasosContactCenter_Estandarizado.csv", index=False)
print("\n📁 Archivo guardado como 'CasosContactCenter_Estandarizado.csv'")