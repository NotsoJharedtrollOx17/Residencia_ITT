import pandas
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords

# * permite hacer las graficas con fondo transparente
plt.rcParams.update({"figure.facecolor": (1, 1, 1, 0)})


def wordCloud(df_csv, columna_csv):
    nombre_archivo = f"wordcloud_preguntacolumna{columna_csv}"
    nombre_pregunta = df_csv.columns.tolist()
    datos = df_csv.iloc[:, columna_csv-1]
    texto = " ".join(datos.values)
    palabras_filtradas = getFilteredSpanishWords(texto)

    # * Generación de la nube de palabras
    wordcloud = WordCloud(background_color='white', max_font_size=40).generate(palabras_filtradas)

    # * Parametros para graficos
    fig, axes = plt.subplots(figsize=(10, 6))
    axes.axis('off') # sin ejes
    axes.imshow(wordcloud, interpolation='bilinear')
    axes.set_title(f"{nombre_pregunta[columna_csv-1]}", fontsize=12)

    plt.savefig(f"../results/plots/{nombre_archivo}")
    plt.close()
    print(f"GRAFICA {nombre_archivo} realizada con éxito!")

def histograma(df, columna_csv, opciones):
    colores = ["royalblue", "darkorange", "limegreen", "mediumpurple", "indianred"]
    nombre_archivo = f"histograma_preguntacolumna{columna_csv}"
    nombre_pregunta = df.columns.tolist()
    datos = df.iloc[:, columna_csv - 1]

    # * Filtra los datos para mantener solo las opciones deseadas
    datos_filtrados = datos[datos.isin(opciones)]

    # * Cuenta las incidencias de cada opción
    conteo = datos_filtrados.value_counts().reindex(opciones, fill_value=0)

    # * Parametros para graficos
    fig, axes = plt.subplots(figsize=(10, 6))

        # * para abreviar las etiquetas de la pregunta 5 y 6...
    if (columna_csv == 5 or columna_csv == 6):
        abreviaciones = ['Pri tt', 'Sec tt', 'Prepa/Bach tt', 'Lic tt', 'Posgrados']
        bars = axes.bar(abreviaciones, conteo.values, alpha=0.7, color=colores)
    else: 
        bars = axes.bar(conteo.index, conteo.values, alpha=0.7, color=colores)

    axes.set_xlabel("Respuesta", fontsize=11)
    axes.set_ylabel("Número de incidencias", fontsize=11)
    axes.set_title(f"{nombre_pregunta[columna_csv-1]}", fontsize=12)
    axes.set_ylim(0, 42) # * Limite de escala
    axes.yaxis.set_major_locator(plt.MaxNLocator(integer=True)) # * Forzar la escala vertical a números enteros

    # * Agregar números en las barras
    for bar, count in zip(bars, conteo):
        axes.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(count),
            ha="center",
            va="bottom",
        )

    plt.savefig(f"../results/plots/{nombre_archivo}")
    plt.close()
    print(f"GRAFICA {nombre_archivo} realizada con éxito!")

def getWordCloudOpinionesQuimica(df_csv):
    # * dichas preguntas son las de las columnas 8 -> 11
    print("INICIO WordCloud de opiniones respecto a la materia de Química")
    for idx in range(8, 13):
        wordCloud(df_csv, idx)
    print("FIN WordCloud de opiniones respecto a la materia de Química")
    print()

def getHistogramaDatosDemograficos(df_csv):
    # * el orden de preguntas es en relación con el orden provisto en el Google Sheets
    opciones_pregunta3 = ["17", "18", "19", "20", "21 o más"]
    opciones_pregunta4 = [
        "Clase Alta",
        "Clase Media Alta",
        "Clase Media",
        "Clase Media Baja",
        "Clase Baja",
    ]
    opciones_pregunta56 = [ # * pregunta 5 Y 6
        "Primaria terminada o trunca",
        "Secundaria terminada o trunca",
        "Prepatoria/Bachillerato Técnico terminado o trunco",
        "Licenciatura terminada o trunca",
        "Posgrados (Maestría, Doctorado, etc.)",
    ]
    opciones_pregunta7 = ["Sí", "No"]
    opciones_pregunta27 = ["Mujer", "Hombre", "No binario", "Prefiero no decir"]

    # * dichas preguntas son las de las columnas 3 -> 7 Y 27
    print("INICIO Histogramas de los Datos Demograficos")
    histograma(df_csv, 3, opciones_pregunta3)
    histograma(df_csv, 4, opciones_pregunta4)
    histograma(df_csv, 5, opciones_pregunta56)
    histograma(df_csv, 6, opciones_pregunta56)
    histograma(df_csv, 7, opciones_pregunta7)
    histograma(df_csv, 27, opciones_pregunta27)
    print("FIN Histogramas de los Datos Demograficos")
    print()

def getHistogramaDiagnosticoAprendizajeQuimica(df_csv):
    # * el orden de preguntas es en relación con el orden provisto en el Google Sheets
    opciones_pregunta13_1622_24 = ['nunca', 'casi nunca', 'a veces', 'casi siempre', 'siempre']
    opciones_pregunta15_23 = ['muy malo', 'malo', 'regular', 'bueno', 'muy bueno']
    opciones_pregunta14 = ['menos de 5', '5 a 6', '7 a 8', '9 a 10', 'más de 10']
    opciones_pregunta25 = ['nula', 'muy poca', 'baja', 'moderada', 'bastante']
    opciones_pregunta26 = ['muy malo', 'malo', 'ni bueno ni malo', 'bueno', 'muy bueno']

    # * dichas preguntas son las de las columnas 13 -> 26
    print("INICIO Histogramas del diagnóstico respecto al aprendizaje de Química")
    histograma(df_csv, 13, opciones_pregunta13_1622_24)
    histograma(df_csv, 14, opciones_pregunta14)
    histograma(df_csv, 15, opciones_pregunta15_23)
    for idx in range(16, 23):
        histograma(df_csv, idx, opciones_pregunta13_1622_24)
    histograma(df_csv, 23, opciones_pregunta15_23)
    histograma(df_csv, 24, opciones_pregunta13_1622_24)
    histograma(df_csv, 25, opciones_pregunta25)
    histograma(df_csv, 26, opciones_pregunta26)
    print("FIN Histogramas del diagnóstico respecto al aprendizaje de Química")
    print()

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

def main():
    CSV_FILE = "../csv/EncuestaPreliminar.csv"
    df_csv = pandas.read_csv(CSV_FILE, encoding='utf-8')
    df_normalizado = getDataFrameRespuestasCategoricasNormalizadas(df_csv)

    getHistogramaDatosDemograficos(df_normalizado)
    getHistogramaDiagnosticoAprendizajeQuimica(df_normalizado)
    getWordCloudOpinionesQuimica(df_normalizado)

if __name__ == "__main__":
    main()
