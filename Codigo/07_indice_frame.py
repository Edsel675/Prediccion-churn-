import pandas as pd

# Cargar el DataFrame final limpio
df = pd.read_csv("/Users/edselcisneros/Documents/Prediccion-churn-/CasosContactCenter_Final.csv")

# Restablecer el índice
df.reset_index(drop=True, inplace=True)

# Guardar con índice actualizado
df.to_csv("/Users/edselcisneros/Documents/Prediccion-churn-/CasosContactCenter_ConIndice.csv", index=False)
print("✅ Índice restablecido. Archivo guardado como 'CasosContactCenter_ConIndice.csv'")