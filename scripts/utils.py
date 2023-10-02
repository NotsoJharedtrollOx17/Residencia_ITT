import pandas
from nltk.corpus import stopwords

# TODO rescribir metodos para que utilizen e importen correctamente este archivo
def loadCsvDataFrame(csv_file):
    df_csv = pandas.read_csv(csv_file, encoding='utf-8')

    return df_csv

def saveCsvDataFrame(df, filename):
    df.to_csv(filename, index=False)
    print(f"Archivo {filename} almacenado con éxito!")

def getDataFrameRespuestasCategoricasNormalizadas(df_csv):
    # normalizando preguntas con respuestas categoricas a minúsculas
        # * dichas preguntas son las de las columnas 13 -> 26
    df_normalizado = df_csv.copy()
    nombres_columnas = df_normalizado.columns.tolist()
    nombres_columnas = nombres_columnas[13-1:26]

    for columna in nombres_columnas:
        df_normalizado[columna] = df_csv[columna].apply(lambda x: x.lower())
            
    return df_normalizado

def getSpanishStopWords():
    stop_words = list(stopwords.words('spanish'))
    return stop_words

def getFilteredSpanishWords(texto):
    stop_words = getSpanishStopWords()
    texto.lower()
    palabras = texto.split()
    palabras_filtradas = [palabra for palabra in palabras if palabra not in stop_words]
    return ' '.join(palabras_filtradas)