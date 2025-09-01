import pandas as pd

# Cargar archivo limpio del paso anterior
df = pd.read_csv("/Users/edselcisneros/Documents/Prediccion-churn-/CasosContactCenter_Limpio.csv")

# Buscar duplicados (considera todos los campos)
duplicados = df[df.duplicated(keep=False)]

# Mostrar duplicados con índice
if not duplicados.empty:
    print("🔍 Registros duplicados encontrados:")
    print(duplicados)
    print("\n🧾 Índices de filas duplicadas:")
    print(duplicados.index.tolist())
else:
    print("✅ No se encontraron registros duplicados.")

# Eliminar duplicados
df_sin_duplicados = df.drop_duplicates()
print(f"\n🗑️ Filas eliminadas por duplicación: {len(df) - len(df_sin_duplicados)}")

# Guardar archivo final sin duplicados
df_sin_duplicados.to_csv("CasosContactCenter_Final.csv", index=False)
print("\n✅ Archivo final guardado como 'CasosContactCenter_Final.csv'")