import pandas
import numpy
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.cm import get_cmap
from matplotlib.patches import Patch
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

# TODO refactorizar para aceptar labels de las respuestas codificadas en getHistogramaDiagnosticoAprendizajeQuimica
# * considerar extraer esos datos del metodo como una clase Singleton para no batallar
# * REFERENCE: https://stackoverflow.com/questions/58303175/plotting-three-dimensions-of-categorical-data-in-python
def getHistogramaIncidenciasTresPreguntas(df_csv, 
                                opciones_1rapregunta, 
                                opciones_2dapregunta, 
                                opciones_3rapregunta):
    
    # ? ya despliega la grafica pero toda martajada...
    df_csv = df_csv.copy()
    nombre_columnas = df_csv.columns.tolist()

    # ! SIEMPRE INCLUIR nombre_columna[1] que es el número de control
    incidencia_interes = df_csv[[#nombre_columnas[1], 
                                           nombre_columnas[3], 
                                           nombre_columnas[4], 
                                           nombre_columnas[5]]]
    incidencia_interes['pivot'] = numpy.ones(39)

    grupo_incidencias = incidencia_interes.groupby(by=[
                                            nombre_columnas[3], 
                                           nombre_columnas[4], 
                                           nombre_columnas[5]]).count().unstack()

    #print(grupo_incidencias.index.levels[0])
    #print(grupo_incidencias.index.levels[1])
    #print(grupo_incidencias.columns.levels[1])
    #print("Columnas del CSV: ", df_csv.columns)
    #print(grupo_incidencias.to_string(index=True))

    # * Revisar las incidencias detectadas
    max_value = int(grupo_incidencias.max().max())
    nombre_columnas_grupo = grupo_incidencias.columns.tolist()

    # List of blood types, to use later as categories in subplots
    # * Revisar nombres para labels de la gráfica
    # ** Guarda las etiquetas de la tercer columna original de df_csv
    #labels_pregunta3 = ['Pri tt', 'Sec tt', 'Prepa/Bach tt', 'Lic tt', 'Posgrados']

    # colors for bar graph
    colors = [get_cmap('viridis')(v) for v in numpy.linspace(0,1,len(nombre_columnas_grupo))]

    sns.set(context="talk")
    nxplots = len(opciones_1rapregunta)
    #print(nxplots)
    nyplots = len(opciones_2dapregunta)
    #print(nyplots)
    fig, axes = plt.subplots(nxplots,
                            nyplots,
                            sharey=True,
                            sharex=True,
                            figsize=(14,16))

    fig.suptitle('City, occupation, and blood type') # TODO cambiar titulo de la gráfica

    # grafica de los datos
    for a, b in enumerate(grupo_incidencias.index.levels[0]):
        for i, j in enumerate(grupo_incidencias.columns.levels[1]):
            try:
                datos_combinacion = grupo_incidencias.loc[b, j]
            except KeyError:
                datos_combinacion = 0  # Asigna 0 si la combinación no existe
            
            axes[a, i].bar(opciones_3rapregunta, datos_combinacion, color=colors)
            axes[a, i].xaxis.set_ticks([])

    # tamaño de enumeración vertical de cada subplot
    for a, b in enumerate(opciones_1rapregunta):
        for i, j in enumerate(opciones_2dapregunta):
            axes[a, i].set_yticks(range(0, max_value + 1))  # Aquí configuramos los ticks
            axes[a, i].tick_params(axis='y', labelsize=10)  # Ajusta el tamaño de letra a tu preferencia (10 en este ejemplo)

    axeslabels = fig.add_subplot(111, frameon=False)
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    plt.grid(False)
    axeslabels.set_ylabel('City',rotation='horizontal',y=1,weight="bold")
    axeslabels.set_xlabel('Occupation',weight="bold")

    # x- and y-axis labels
    # * para segunda pregunta...
    for i, j in enumerate(opciones_2dapregunta): # TODO usar las abreviaciones para los casos particulares
        axes[nyplots-1, i].set_xlabel(j)
    # * para primer pregunta... 
    for i, j in enumerate(opciones_1rapregunta):
        axes[i, 0].set_ylabel(j)

    # Tune this manually to make room for the legend
    fig.subplots_adjust(right=0.82)

    fig.legend([Patch(facecolor = i) for i in colors],
            opciones_3rapregunta,
            title="Blood type",
            loc="center right")
    
    plt.show() # TODO cambiar a plt.savefig(f"../results/plots/{nombre_archivo}")

def main():
    CSV_FILE = "../csv/EncuestaPreliminar.csv"
    df_csv = pandas.read_csv(CSV_FILE, encoding='utf-8')
    df_normalizado = getDataFrameRespuestasCategoricasNormalizadas(df_csv)

    #getHistogramaDatosDemograficos(df_normalizado)
    #getHistogramaDiagnosticoAprendizajeQuimica(df_normalizado)
    #getWordCloudOpinionesQuimica(df_normalizado)

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

    getHistogramaIncidenciasTresPreguntas(df_normalizado, opciones_pregunta4, opciones_pregunta56, opciones_pregunta56)

if __name__ == "__main__":
    main()
