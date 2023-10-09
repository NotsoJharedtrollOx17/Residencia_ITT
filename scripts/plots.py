import pandas
import numpy
import seaborn as sns
import matplotlib.pyplot as plt
import optionsEncuestaPreliminar as EncuestaPreliminar
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
        abreviaciones = EncuestaPreliminar.getOpcionesPregunta5_6(abreviar=True)
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
    opciones_pregunta3 = EncuestaPreliminar.getOpcionesPregunta3()
    opciones_pregunta4 = EncuestaPreliminar.getOpcionesPregunta4()
    opciones_pregunta5_6 = EncuestaPreliminar.getOpcionesPregunta5_6()
    opciones_pregunta7 = EncuestaPreliminar.getOpcionesPregunta7()
    opciones_pregunta27 = EncuestaPreliminar.getOpcionesPregunta27()

    # * dichas preguntas son las de las columnas 3 -> 7 Y 27
    print("INICIO Histogramas de los Datos Demograficos")
    histograma(df_csv, 3, opciones_pregunta3)
    histograma(df_csv, 4, opciones_pregunta4)
    histograma(df_csv, 5, opciones_pregunta5_6)
    histograma(df_csv, 6, opciones_pregunta5_6)
    histograma(df_csv, 7, opciones_pregunta7)
    histograma(df_csv, 27, opciones_pregunta27)
    print("FIN Histogramas de los Datos Demograficos")
    print()

def getHistogramaDiagnosticoAprendizajeQuimica(df_csv):
    # * el orden de preguntas es en relación con el orden provisto en el Google Sheets
    opciones_pregunta13_1622_24 = EncuestaPreliminar.getOpcionesPregunta13_1622_24()
    opciones_pregunta15_23 = EncuestaPreliminar.getOpcionesPregunta15_23()
    opciones_pregunta14 = EncuestaPreliminar.getOpcionesPregunta14()
    opciones_pregunta25 = EncuestaPreliminar.getOpcionesPregunta25()
    opciones_pregunta26 = EncuestaPreliminar.getOpcionesPregunta26()

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

# * considerar extraer esos datos del metodo como una clase Singleton para no batallar
# * REFERENCE: https://stackoverflow.com/questions/58303175/plotting-three-dimensions-of-categorical-data-in-python
def incidenciasTresPreguntas(df_csv, 
                                opciones_1rapregunta, 
                                opciones_2dapregunta, 
                                opciones_3rapregunta,
                                posiciones_preguntas):

    # * utilizar parte de este método para plasmar incidencias en CSV
    sns.set(context="talk")
    nombre_archivo = f"incidencias_preguntas{posiciones_preguntas[0]}_{posiciones_preguntas[1]}_{posiciones_preguntas[2]}"
    nombre_columnas = df_csv.columns.tolist()

    incidencia_interes = df_csv[[#nombre_columnas[1], 
                                           nombre_columnas[posiciones_preguntas[0]], 
                                           nombre_columnas[posiciones_preguntas[1]], 
                                           nombre_columnas[posiciones_preguntas[2]]]]
    incidencia_interes['pivot'] = numpy.ones(39)

    grupo_incidencias = incidencia_interes.groupby(by=[
                                            nombre_columnas[posiciones_preguntas[0]], 
                                           nombre_columnas[posiciones_preguntas[1]], 
                                           nombre_columnas[posiciones_preguntas[2]]]).count().unstack()


    #print(grupo_incidencias.to_string())

    # * Revisar las incidencias detectadas
    max_value = int(grupo_incidencias.max().max()) # * Cantidad mas grande de TODAS LAS INCIDENCIAS
    
    # * Revisar nombres para labels de la gráfica
    # ** Guarda las etiquetas de la tercer columna original de df_csv
    #labels_pregunta3 = ['Pri tt', 'Sec tt', 'Prepa/Bach tt', 'Lic tt', 'Posgrados']

    # * colors for bar graph
    colors = ["royalblue", "darkorange", "limegreen", "mediumpurple", "indianred"]
    nxplots = len(opciones_1rapregunta)
    nyplots = len(opciones_2dapregunta)
    fig, axes = plt.subplots(nxplots,
                            nyplots,
                            sharey=True,
                            sharex=True,
                            figsize=(14,16))
    fig.suptitle(f'Incidencias Pregunta {posiciones_preguntas[0]} \u2229 Pregunta {posiciones_preguntas[1]} \u2229 Pregunta{posiciones_preguntas[2]}')

    # * grafica de los datos
    for a, b in enumerate(grupo_incidencias.index.levels[0]): # * respuestas de la 1er. pregunta
        for i, j in enumerate(grupo_incidencias.index.levels[1]): # * respuestas de la  2da. pregunta
            try:
                datos_combinacion = grupo_incidencias.loc[b, j]
            except KeyError:
                datos_combinacion = 0  # Asigna 0 si la combinación no existe
            
            axes[a, i].bar(grupo_incidencias.columns.levels[1], datos_combinacion, color=colors)
            axes[a, i].xaxis.set_ticks([])
            axes[a, i].set_yticks(range(0, max_value+1))  # Aquí configuramos los ticks
            axes[a, i].tick_params(axis='y', labelsize=9)  # Ajusta el tamaño de letra a tu preferencia (10 en este ejemplo)

    # * tamaño de enumeración vertical de cada subplot
    for a in range(nxplots):
        for i in range(nyplots):
            axes[a, i].tick_params(axis='both', labelsize=8)

    # * nombre de los ejes grandes
    axeslabels = fig.add_subplot(111, frameon=False)
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    plt.grid(False)
    axeslabels.set_ylabel(f'Pregunta {posiciones_preguntas[0]}', y=1.01, rotation='horizontal')
    axeslabels.set_xlabel(f'Pregunta {posiciones_preguntas[1]}', loc='center')

    # * etiquetas para los ejes de las subgraficas
    # * para segunda pregunta...
    for i, j in enumerate(opciones_2dapregunta):
        axes[nxplots-1, i].set_xlabel(j)
        #axes[nyplots-1, i].tick_params(axis='x', labelsize=9)  # Ajusta el tamaño de letra a tu preferencia (10 en este ejemplo)
    # * para primer pregunta... 
    for i, j in enumerate(opciones_1rapregunta):
        axes[i, 0].set_ylabel(j)
        #axes[i, 0].tick_params(axis='y', labelsize=9)  # Ajusta el tamaño de letra a tu preferencia (10 en este ejemplo)

    fig.subplots_adjust(right=0.82)

    # * leyenda para la gráfica general
    fig.legend([Patch(facecolor = i) for i in colors],
            opciones_3rapregunta,
            title=f"Pregunta {posiciones_preguntas[2]}",
            loc="center right")
    
    plt.savefig(f"../results/plots/{nombre_archivo}")
    plt.close()    
    print(f"GRAFICA {nombre_archivo} realizada con éxito!")

def getIncidenciasEncuestaPreliminar(df_csv):

    incidencias_interes = [
        [3,4,5],
        [3,12,13],
        [3,22,23],
        [3,24,25],
        [4,5,20],
        [4,5,24],
        [4,5,25],
        [6,12,13],
        [12,13,14],
        [12,13,22],
        [12,13,23],
        [12,13,25],
        [14,20,21],
        [14,22,23],
        [17,18,22],
        [17,18,23],
        [17,18,24],
        [18,19,22],
    ]

    # * el orden de preguntas es en relación con el orden provisto en el Google Sheets
    opciones_pregunta4 = EncuestaPreliminar.getOpcionesPregunta4(abreviar=True)
    opciones_pregunta5_6 = EncuestaPreliminar.getOpcionesPregunta5_6(abreviar=True)
    opciones_pregunta7 = EncuestaPreliminar.getOpcionesPregunta7()
    opciones_pregunta13_1622_24 = EncuestaPreliminar.getOpcionesPregunta13_1622_24()
    opciones_pregunta14 = EncuestaPreliminar.getOpcionesPregunta14()
    opciones_pregunta15_23 = EncuestaPreliminar.getOpcionesPregunta15_23()
    opciones_pregunta25 = EncuestaPreliminar.getOpcionesPregunta25()
    opciones_pregunta26 = EncuestaPreliminar.getOpcionesPregunta26()

    print("INICIO Incidencias detectas en la Encuesta Preliminar")
    print("Para la pregunta No 03: ") # * (4 INCIDENCIAS DE INTERES) ACOMODO CORRECTO 
    incidenciasTresPreguntas(df_csv, opciones_pregunta4, opciones_pregunta5_6, opciones_pregunta5_6, incidencias_interes[0])
    incidenciasTresPreguntas(df_csv, opciones_pregunta4, opciones_pregunta13_1622_24, opciones_pregunta14, incidencias_interes[1])
    incidenciasTresPreguntas(df_csv, opciones_pregunta4, opciones_pregunta15_23, opciones_pregunta13_1622_24, incidencias_interes[2])
    incidenciasTresPreguntas(df_csv, opciones_pregunta4, opciones_pregunta25, opciones_pregunta26, incidencias_interes[3])
    print("Para la pregunta No 04: ") # * (3 INCIDENCIAS DE INTERES) ACOMODO CORRECTO 
    incidenciasTresPreguntas(df_csv, opciones_pregunta5_6, opciones_pregunta5_6, opciones_pregunta13_1622_24, incidencias_interes[4])
    incidenciasTresPreguntas(df_csv, opciones_pregunta5_6, opciones_pregunta5_6, opciones_pregunta25, incidencias_interes[5])
    incidenciasTresPreguntas(df_csv, opciones_pregunta5_6, opciones_pregunta5_6, opciones_pregunta26, incidencias_interes[6])
    print("Para la pregunta No 06: ") # * (1 INCIDENCIA DE INTERES) ACOMODO CORRECTO
    incidenciasTresPreguntas(df_csv, opciones_pregunta7, opciones_pregunta13_1622_24, opciones_pregunta14, incidencias_interes[7])
    print("Para la pregunta No 12: ") # * (4 INCIDENCIAS DE INTERES) ACOMODO CORRECTO
    incidenciasTresPreguntas(df_csv, opciones_pregunta13_1622_24, opciones_pregunta14, opciones_pregunta15_23, incidencias_interes[8])
    incidenciasTresPreguntas(df_csv, opciones_pregunta13_1622_24, opciones_pregunta14, opciones_pregunta15_23, incidencias_interes[9])
    incidenciasTresPreguntas(df_csv, opciones_pregunta13_1622_24, opciones_pregunta14, opciones_pregunta13_1622_24, incidencias_interes[10])
    incidenciasTresPreguntas(df_csv, opciones_pregunta13_1622_24, opciones_pregunta14, opciones_pregunta26, incidencias_interes[11])
    print("Para la pregunta No 14: ") # * (2 INCIDENCIAS DE INTERES) ACOMODO CORRECTO
    incidenciasTresPreguntas(df_csv, opciones_pregunta15_23, opciones_pregunta13_1622_24, opciones_pregunta13_1622_24, incidencias_interes[12])
    incidenciasTresPreguntas(df_csv, opciones_pregunta15_23, opciones_pregunta15_23, opciones_pregunta13_1622_24, incidencias_interes[13])
    print("Para la pregunta No 17:") # * (3 INCIDENCIAS DE INTERES) ACOMODO CORRECTO
    incidenciasTresPreguntas(df_csv, opciones_pregunta13_1622_24, opciones_pregunta13_1622_24, opciones_pregunta15_23, incidencias_interes[14])
    incidenciasTresPreguntas(df_csv, opciones_pregunta13_1622_24, opciones_pregunta13_1622_24, opciones_pregunta13_1622_24, incidencias_interes[15])
    incidenciasTresPreguntas(df_csv, opciones_pregunta13_1622_24, opciones_pregunta13_1622_24, opciones_pregunta25, incidencias_interes[16])
    print("Para la pregunta No 18: ") # * (1 INCIDENCIA DE INTERES) ACOMODO CORRECTO
    incidenciasTresPreguntas(df_csv, opciones_pregunta13_1622_24, opciones_pregunta13_1622_24, opciones_pregunta15_23, incidencias_interes[17])
    print("FIN Incidencias detectas en la Encuesta Preliminar")

def main():
    CSV_FILE = "../csv/EncuestaPreliminar.csv"
    df_csv = pandas.read_csv(CSV_FILE, encoding='utf-8')
    df_normalizado = getDataFrameRespuestasCategoricasNormalizadas(df_csv)

    #getHistogramaDatosDemograficos(df_normalizado)
    #getHistogramaDiagnosticoAprendizajeQuimica(df_normalizado)
    #getWordCloudOpinionesQuimica(df_normalizado)
    getIncidenciasEncuestaPreliminar(df_normalizado)

if __name__ == "__main__":
    main()
