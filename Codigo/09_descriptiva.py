import pandas as pd

# Cargar la base final
df = pd.read_csv("/Users/edselcisneros/Documents/Prediccion-churn-/CasosContactCenter_Estandarizado.csv")

# Mostrar solo las columnas numéricas
desc = df.describe()

print("📊 Estadísticas descriptivas generales (variables numéricas):")
print(desc)

# También puedes exportar el resumen como CSV (opcional)
desc.to_csv("/Users/edselcisneros/Documents/Prediccion-churn-/EstadisticasDescriptivas_General.csv")
print("\n📁 Archivo 'EstadisticasDescriptivas_General.csv' guardado.")