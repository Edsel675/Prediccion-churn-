import pandas as pd
import re

# Cargar los datos
df = pd.read_csv("/Users/edselcisneros/Documents/Prediccion-churn-/Archivoscsv/CasosContactCenter.csv")

print("======== PROCESO DE CALIDAD: VALIDACIÓN DE COLUMNAS ========")

# 1. Validar columna 'Fecha' (debe tener formato YYYY-MM-DD o similar)
print("\n🔍 Errores en columna 'Fecha':")
errores_fecha = df[~pd.to_datetime(df['Fecha'], errors='coerce').notna()]
print(errores_fecha[['Fecha']])

# 2. Validar columna 'Hora' (debe tener formato HH:MM:SS o HH:MM)
print("\n🔍 Errores en columna 'Hora':")
errores_hora = df[~df['Hora'].astype(str).str.match(r'^\d{1,2}:\d{2}(:\d{2})?$')]
print(errores_hora[['Hora']])

# 3. Validar columna 'AHT' (debe ser número positivo, sin nulos o letras)
print("\n🔍 Errores en columna 'AHT':")
errores_aht = df[~df['AHT'].astype(str).str.match(r'^\d+(\.\d+)?$')]
print(errores_aht[['AHT']])

# 4. Validar columna 'Por.que.medio.se.enter.de.nosotros' (inconsistencias de puntuación y nulos)
print("\n🔍 Inconsistencias en 'Por.que.medio.se.enter.de.nosotros':")
errores_medio = df[df['Por.que.medio.se.enter.de.nosotros'].astype(str).str.contains(r'[.,\-_/]|^\s*$')]
print(errores_medio[['Por.que.medio.se.enter.de.nosotros']])

# 5. Validar 'Por.que.canal.nos.esta.contactando' (inconsistencias de puntuación y nulos)
print("\n🔍 Inconsistencias en 'Por.que.canal.nos.esta.contactando':")
errores_canal = df[df['Por.que.canal.nos.esta.contactando'].astype(str).str.contains(r'[.,\-_/]|^\s*$')]
print(errores_canal[['Por.que.canal.nos.esta.contactando']])

# 6. Validar 'Motivo' (detectar símbolos raros)
print("\n🔍 Inconsistencias en columna 'Motivo':")
errores_motivo = df[df['Motivo'].astype(str).str.contains(r'[.,\-_/]|^\s*$')]
print(errores_motivo[['Motivo']])

# 7. Validar 'Tipificacion_Proceso' (símbolos o vacíos)
print("\n🔍 Inconsistencias en 'Tipificacion_Proceso':")
errores_tip = df[df['Tipificacion_Proceso'].astype(str).str.contains(r'[.,\-_/]|^\s*$')]
print(errores_tip[['Tipificacion_Proceso']])

# 8. Validar 'Genera.folio.de.seguimiento' (esperado sí/no o 0/1)
print("\n🔍 Valores no esperados en 'Genera.folio.de.seguimiento':")
valores_esperados = ['Sí', 'No', 'Si', 'NO', 'YES', 'NO', '1', '0']
errores_folio = df[~df['Genera.folio.de.seguimiento'].astype(str).isin(valores_esperados)]
print(errores_folio[['Genera.folio.de.seguimiento']])

# 9. Validar 'id_user' (debe existir y no estar vacío)
print("\n🔍 Errores en columna 'id_user':")
errores_id_user = df[df['id_user'].isnull() | (df['id_user'].astype(str).str.strip() == "")]
print(errores_id_user[['id_user']])

# 10. Validar 'id_caso' (debe ser numérico y no nulo)
print("\n🔍 Errores en columna 'id_caso':")
errores_id_caso = df[~df['id_caso'].astype(str).str.match(r'^\d+$')]
print(errores_id_caso[['id_caso']])

# 11. Validar 'id_agente' (debe ser numérico o texto no vacío)
print("\n🔍 Errores en columna 'id_agente':")
errores_id_agente = df[df['id_agente'].astype(str).str.strip() == ""]
print(errores_id_agente[['id_agente']])

# 12. Validar 'RespCSAT' (esperado: 1-5, NA, o nulo)
print("\n🔍 Errores en columna 'RespCSAT':")
errores_csat = df[~df['RespCSAT'].astype(str).isin(['1','2','3','4','5','NA','na','NaN','nan',''])]
print(errores_csat[['RespCSAT']])

# 13. Validar 'RespFCR' (esperado: 1/0, sí/no, vacío)
print("\n🔍 Errores en columna 'RespFCR':")
valores_validos_fcr = ['1', '0', 'Sí', 'No', 'Si', 'NO', '']
errores_fcr = df[~df['RespFCR'].astype(str).isin(valores_validos_fcr)]
print(errores_fcr[['RespFCR']])