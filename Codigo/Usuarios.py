import pandas as pd
import re

# Debes cambiar la ruta al archivo CSV según tu estructura de carpetas
df = pd.read_csv(r'C:\Users\emirp\OneDrive\Escritorio\concentracion\Prediccion-churn-\data\usuarios.csv')

print(df.columns)
# Parte 1 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Tareas clave:
# validar rangos de edad, estados válidos, género definido, ids únicos, textos sin caracteres raros.

# 1. Validar rangos de edad
edades_invalidas = df[(df['age'] < 18) | (df['age'] > 75)]
print("Edades fuera de rango:\n", edades_invalidas[['id_user', 'age']])

# 2. Validar estados válidos (ejemplo: lista de estados permitidos)
estados_validos = ['VE', 'NL', 'SO','BC','EM','MI','DF','JA','CM','AG','PU','CH','CL', 'HG', 'CO', 'TM', 'QR', 'SI', 'YU', 'OA', 'TL', 'GT', 'CS', 'QT', 'MO', 'BS', 'TB', 'GR', 'SL', 'DG', 'ZA']  # Modifica según tus estados válidos
estados_invalidos = df[~df['state'].isin(estados_validos)]
print("Estados inválidos:\n", estados_invalidos[['state']])

# 3. Validar género definido
generos_validos = ['male', 'female']
generos_invalidos = df[~df['gender'].isin(generos_validos)]
print("Géneros indefinidos:\n", generos_invalidos[['id_user', 'gender']])

# 4. Validar ids únicos
if df['id_user'].is_unique:
    print("Todos los IDs son únicos.")
else:
    print("IDs duplicados encontrados:\n", df[df.duplicated('id_user', keep=False)][['id_user']])

# 5. Validar textos sin caracteres raros (ejemplo en 'occupation')
def tiene_caracteres_raros(texto):
    # Permite letras, acentos, ñ, espacios, slash, punto, coma, guion y paréntesis
    # Además, revisa si hay caracteres no imprimibles
    patron = r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s/.,\-()]'
    texto_str = str(texto)
    contiene_raros = bool(re.search(patron, texto_str))
    contiene_no_imprimibles = not texto_str.isprintable()
    return contiene_raros or contiene_no_imprimibles

ocupaciones_raras = df[df['occupation'].apply(tiene_caracteres_raros)]
print("Ocupaciones con caracteres raros:\n", ocupaciones_raras[['id_user', 'occupation']])

# Parte 2 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Cambiar tipos de datos
# Ejemplo de columnas: 'creationflow', 'age', 'gender', 'occupation', 'qualification', 'state',
# 'stateofbirth', 'usertype', 'userchannel', 'id_user'

# Cambiar columnas no numéricas a tipo object
cols_object = ['creationflow', 'gender', 'occupation', 'qualification', 'state', 'stateofbirth', 'usertype', 'userchannel', 'id_user']
df[cols_object] = df[cols_object].astype('object')

# Si tienes columnas de fecha, conviértelas a datetime (ejemplo: 'fecha_registro')
# df['fecha_registro'] = pd.to_datetime(df['fecha_registro'], errors='coerce')

# Cambiar 'age' a tipo numérico si no lo es
df['age'] = pd.to_numeric(df['age'], errors='coerce')

# Mostrar los tipos de datos finales
print("Tipos de datos actualizados:\n", df.dtypes)

# Variables cambiadas:
print("Variables cambiadas a object:", cols_object)
print("Variable 'age' cambiada a numérico.")

# Parte 3 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Identificar valores faltantes/ceros y eliminarlos o imputarlos

# 1. Mostrar nombre y total de valores nulos y ceros por variable
print("\nValores nulos y ceros por columna:")
for col in df.columns:
    nulos = df[col].isnull().sum()
    ceros = (df[col] == 0).sum() if df[col].dtype in ['int64', 'float64'] else 0
    print(f"{col}: nulos={nulos}, ceros={ceros}")

# 2. Identificar columnas con más del 15% de datos nulos
umbral = 0.15
total_filas = len(df)
cols_mas_15_nulos = [col for col in df.columns if df[col].isnull().sum() / total_filas > umbral]
if cols_mas_15_nulos:
    print("\n¡Atención! Las siguientes columnas tienen más del 15% de datos nulos:")
    print(cols_mas_15_nulos)

# 3. Eliminar filas con 2 o más nulos y/o ceros
def contar_nulos_ceros(row):
    nulos = row.isnull().sum()
    ceros = sum((row[col] == 0) if row[col] is not None and type(row[col]) in [int, float] else False for col in row.index)
    return nulos + ceros

df['nulos_ceros'] = df.apply(contar_nulos_ceros, axis=1)
df = df[df['nulos_ceros'] < 2].drop(columns=['nulos_ceros'])

# 4. Imputar nulos restantes con la media por grupo
# Ejemplo: Imputar 'age' nulo con la media por 'gender' y 'state'
for col in df.columns:
    if df[col].isnull().sum() > 0 and df[col].dtype in ['int64', 'float64']:
        df[col] = df.groupby(['gender', 'state'])[col].transform(lambda x: x.fillna(x.mean()))

# Si quedan nulos, imputar con la media general
df = df.fillna(df.mean(numeric_only=True))

print("\nDatos después de limpieza e imputación:")
print(df.info())

# Parte 4 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Identificar y eliminar registros duplicados

# Buscar duplicados considerando todas las columnas
duplicados = df[df.duplicated(keep=False)]

if not duplicados.empty:
    print("\nRegistros duplicados encontrados (índices):")
    print(duplicados.index.tolist())
    print(f"Total de registros duplicados: {len(duplicados)}")
else:
    print("\nNo se encontraron registros duplicados.")

# Eliminar duplicados, conservando el primer registro
df = df.drop_duplicates(keep='first').reset_index(drop=True)

# Parte 5 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
df_filtrado = df[(df['age'] > 25) & (df['state'] == 'DF')]

print(f"\nTotal de registros después de filtrado: {len(df_filtrado)}")
print(df_filtrado.head())

# De momento no tengo suficiente informacion para eliminar mas registros.

# Parte 6 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# NO es necesario.

# Parte 7 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Estandarizar nombres de columnas: minúsculas y sin espacios
df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

print("\nNombres de columnas estandarizados:")
print(df.columns)

# Comentario:
# Fue necesario cambiar los nombres de las columnas para asegurar que no tengan espacios y estén en minúsculas.
# Por ejemplo, 'User Channel' se convierte en 'user_channel', 'State of Birth' en 'state_of_birth', etc.

# Parte 8 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Estadística descriptiva de todas las variables numéricas de la base de datos general

print("\nEstadística descriptiva de variables numéricas (base de datos general):")
print(df.describe())

# Parte 9 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Por el momento no tengo suficiente información para realizar análisis adicionales.

# Parte 10 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
