import pandas
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import paxplot
import optionsEncuestaPreliminar as EncuestaPreliminar
import matplotlib.cm as cm 
import matplotlib.colors
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

# * REFERENCE: https://stackoverflow.com/questions/58303175/plotting-three-dimensions-of-categorical-data-in-python
def incidenciasTresPreguntas(df_csv, posiciones_preguntas):

    # * utilizar parte de este método para plasmar incidencias en CSV
    sns.set(context="talk")
    nombre_archivo = f"incidencias_preguntas{posiciones_preguntas[0]}_{posiciones_preguntas[1]}_{posiciones_preguntas[2]}"
    nombre_columnas = df_csv.columns.tolist()

    incidencia_interes = df_csv[[#nombre_columnas[1], 
                                           nombre_columnas[posiciones_preguntas[0]], 
                                           nombre_columnas[posiciones_preguntas[1]], 
                                           nombre_columnas[posiciones_preguntas[2]]]]
    incidencia_interes['pivot'] = np.ones(39)

    grupo_incidencias = incidencia_interes.groupby(by=[
                                            nombre_columnas[posiciones_preguntas[0]], 
                                           nombre_columnas[posiciones_preguntas[1]], 
                                           nombre_columnas[posiciones_preguntas[2]]]).count().unstack()

    # * Revisar las incidencias detectadas
    max_value = int(grupo_incidencias.max().max()) # * Cantidad mas grande de TODAS LAS INCIDENCIAS
    nxplots = len(grupo_incidencias.index.levels[0])
    nyplots = len(grupo_incidencias.index.levels[1])
    fig, axes = plt.subplots(nxplots,
                            nyplots,
                            sharey=True,
                            sharex=True,
                            figsize=(14,16))
    fig.suptitle(f'Incidencias Pregunta {posiciones_preguntas[0]} \u2229 Pregunta {posiciones_preguntas[1]} \u2229 Pregunta{posiciones_preguntas[2]}')

    # * colors for bar graph
    colors = [cm.viridis(v) for v in np.linspace(0, 1, len(grupo_incidencias.columns.levels[1]))]
    
    # * obtencion de valores a graficar
    for a, opciones_1 in enumerate(grupo_incidencias.index.levels[0]): # * respuestas de la 1er. pregunta
        for i, opciones_2 in enumerate(grupo_incidencias.index.levels[1]): # * respuestas de la  2da. pregunta

            # * revision de entrada acorde a las opciones dadas
            try: 
                datos_combinacion = grupo_incidencias.loc[opciones_1, opciones_2]
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
    opciones_pregunta4 = EncuestaPreliminar.getOpcionesPregunta4()
    opciones_pregunta5 = EncuestaPreliminar.getOpcionesPregunta5_6()
    opciones_pregunta6 = EncuestaPreliminar.getOpcionesPregunta5_6()
    abreviaciones_pregunta4 = EncuestaPreliminar.getOpcionesPregunta4(abreviar=True)
    abreviaciones_pregunta5 = EncuestaPreliminar.getOpcionesPregunta5_6(abreviar=True)
    abreviaciones_pregunta6 = EncuestaPreliminar.getOpcionesPregunta5_6(abreviar=True)
    index = None
    abreviacion = None

    # * para segunda pregunta...
    for i, j in enumerate(grupo_incidencias.index.levels[1]):
        if posiciones_preguntas[1] == 4 or posiciones_preguntas[1] == 5:
            j_lower = j.lower()  # Convertir a minúsculas
            index = [opcion.lower() for opcion in opciones_pregunta5].index(j_lower)
            abreviacion = abreviaciones_pregunta5[index]
            axes[nxplots-1, i].set_xlabel(abreviacion)
        else:
            axes[nxplots-1, i].set_xlabel(j)

    # * para primer pregunta...
    for i, j in enumerate(grupo_incidencias.index.levels[0]):
        j_lower = j.lower()  # Convertir a minúsculas
        if posiciones_preguntas[0] == 3:    
            index = [opcion.lower() for opcion in opciones_pregunta4].index(j_lower)
            abreviacion = abreviaciones_pregunta4[index]
            axes[i,0].set_ylabel(abreviacion)
        elif posiciones_preguntas[0] == 4:
            index = [opcion.lower() for opcion in opciones_pregunta5].index(j_lower)
            abreviacion = abreviaciones_pregunta5[index]
            axes[i,0].set_ylabel(abreviacion)
        else:
            axes[i,0].set_ylabel(j)

    # * cuando tenemos "5" como tercer posición
    if posiciones_preguntas[2] == 5:
        abreviaciones = []
        
        for i, j in enumerate(grupo_incidencias.columns.levels[1]):
            j_lower = j.lower()  # Convertir a minúsculas
            index = [opcion.lower() for opcion in opciones_pregunta6].index(j_lower)
            abreviacion = abreviaciones_pregunta6[index]
            abreviaciones.append(abreviacion)

        # * leyenda para la gráfica general
        # * colors for bar graph
        colors = [cm.viridis(v) for v in np.linspace(0, 1, len(abreviaciones))]
        fig.subplots_adjust(right=0.82)
        fig.legend([Patch(facecolor=i) for i in colors],
                abreviaciones,
                title=f"Pregunta {posiciones_preguntas[2]}",
                loc="center right")
    else:
        # * leyenda para la gráfica general
        fig.subplots_adjust(right=0.82)
        fig.legend([Patch(facecolor=i) for i in colors],
                grupo_incidencias.columns.levels[1],
                title=f"Pregunta {posiciones_preguntas[2]}",
                loc="center right")
    
    plt.savefig(f"../results/plots/{nombre_archivo}")
    plt.close()    
    print(f"GRAFICA {nombre_archivo} realizada con éxito!")

def getIncidenciasEncuestaPreliminar(df_csv):

    incidencias_interes = EncuestaPreliminar.getIndicesIncidenciasInteres()

    # * el orden de preguntas es en relación con el orden provisto en el Google Sheets

    print("INICIO Incidencias detectas en la Encuesta Preliminar")
    
    for idx, incidencias in enumerate(incidencias_interes):
        if idx == 0:
            print("Para la pregunta No 03: ") # * (4 INCIDENCIAS DE INTERES) ACOMODO CORRECTO 
        if idx == 4:
            print("Para la pregunta No 04: ") # * (3 INCIDENCIAS DE INTERES) ACOMODO CORRECTO 
        if idx == 7:
            print("Para la pregunta No 06: ") # * (1 INCIDENCIA DE INTERES) ACOMODO CORRECTO
        if idx == 8:
            print("Para la pregunta No 12: ") # * (4 INCIDENCIAS DE INTERES) ACOMODO CORRECTO
        if idx == 12:
            print("Para la pregunta No 14: ") # * (2 INCIDENCIAS DE INTERES) ACOMODO CORRECTO
        if idx == 14:
            print("Para la pregunta No 17:") # * (3 INCIDENCIAS DE INTERES) ACOMODO CORRECTO
        if idx == 17:
            print("Para la pregunta No 18: ") # * (1 INCIDENCIA DE INTERES) ACOMODO CORRECTO

        incidenciasTresPreguntas(df_csv, incidencias)

    print("FIN Incidencias detectas en la Encuesta Preliminar")

def getParallelCoordinatesRankingTematicasRespuestasPreguntasAbiertas(df_csv):
    df_csv = df_csv.drop(columns= ["# Control"])
    df_csv = df_csv[df_csv["Aprobado_Post-Test"]=='aprobado']
    df_csv = df_csv.drop(columns= ["Aprobado_Post-Test"])
    columns = df_csv.columns
    len_columns = len(columns)

    # * filtros importantes
        # * para obtener los valores que pertenecen al Grupo de Control
    filtro_grupo_control = df_csv["ID Grupo"].str.contains("gc")
        # * ... Grupo Experimental
    filtro_grupo_experimental = df_csv["ID Grupo"].str.contains("ge")

    # * aplicacion de los filtros
    df_grupo_control = df_csv[filtro_grupo_control]
    df_grupo_experimental = df_csv[filtro_grupo_experimental]

    ids_grupo = df_grupo_control['ID Grupo'].values
    ids_grupo = np.concatenate((df_grupo_experimental['ID Grupo'].values, ids_grupo), axis=None)

    # * graficacion del parallel coordinate plot
        # * colores para los grupos
    labels = ['ID Grupo', 
              'p08_1', 'p08_2', 
              'p09_1', 'p09_2', 
              'p10_1', 'p10_2', 
              'p11_1', 'p11_2', 
              'p12_1', 'p12_2']

    colormap = matplotlib.colors.ListedColormap(['green', 'orange'])
    config_grupo_control = {'alpha': 0.5, 'color': 'green', 'zorder': 0, 'label': 'GC'}
    config_grupo_experimental = {'alpha': 0.5, 'color': 'orange', 'zorder': 0, 'label': 'GE'}

    print(ids_grupo.tolist())

    # * creación del grafico
    paxfig = paxplot.pax_parallel(n_axes=len_columns)
    
    # TODO fix the display ; ID Grupo bar looks extremely squashed
    # * configuración de las etiquetas
        # * color naranja en el parallel plot para el grupo de control
    paxfig.plot(df_grupo_control.to_numpy(), line_kwargs = config_grupo_control)
    
        # * color azul en el parallel plot para el grupo de control
    paxfig.plot(df_grupo_experimental.to_numpy(), line_kwargs = config_grupo_experimental)
    paxfig.set_labels(labels)
    paxfig.set_ticks(ax_idx=0, ticks=list(range(0, 13)), labels=ids_grupo.tolist())
    paxfig.set_even_ticks(
        ax_idx=0,
        n_ticks=13,
    )
    for idx in list(range(1, len_columns)):
        #paxfig.set_ticks(ax_idx=idx, ticks=list(range(0, 13)), labels=ids_grupo.tolist())
        paxfig.set_lim(ax_idx=idx, bottom=1.0, top=39)
    #paxfig.add_legend()
    #paxfig.add_legend(labels=['GC', 'GE'])

    plt.show()


def main():
    ENCUESTA_PRELIMINAR_CSV_FILE = "../csv/EncuestaPreliminar.csv"
    RANKING_TEMATICAS_PREGUNTAS_ABIERTAS_ENCUESTA_CSV_FILE = '../csv/Ranking_Tematicas_PreguntasAbiertas_EncuestaPreliminar_ValidPreTestPostTest.csv'

    df_ranking_csv = pandas.read_csv(RANKING_TEMATICAS_PREGUNTAS_ABIERTAS_ENCUESTA_CSV_FILE, encoding='utf-8')
    df_encuesta_csv = pandas.read_csv(ENCUESTA_PRELIMINAR_CSV_FILE, encoding='utf-8')
    #df_normalizado = getDataFrameRespuestasCategoricasNormalizadas(df_encuesta_csv)

    #getHistogramaDatosDemograficos(df_normalizado)
    #getHistogramaDiagnosticoAprendizajeQuimica(df_normalizado)
    #getWordCloudOpinionesQuimica(df_normalizado)
    #getIncidenciasEncuestaPreliminar(df_normalizado)
    getParallelCoordinatesRankingTematicasRespuestasPreguntasAbiertas(df_ranking_csv)

if __name__ == "__main__":
    main()
