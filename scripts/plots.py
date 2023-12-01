import re
import pandas
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm 
import optionsEncuestaPreliminar as EncuestaPreliminar
from matplotlib import ticker
from matplotlib.patches import Patch
from matplotlib.colors import LinearSegmentedColormap
from pandas.plotting import parallel_coordinates
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

def numberLineRanking(df_csv, etiquetas, nombre_tematicas, cantidad_tematicas, colores_por_idx):

    NOMBRE_ARCHIVO = '../results/plots/ranking_Aprobados_respuestastematicaspreguntasabiertas.png'

    fig, axes = plt.subplots(cantidad_tematicas, figsize=(15, 8))
    plt.subplots_adjust(wspace=0.5, hspace=2)
    plt.suptitle(f"Ranking de afinidad en respuestas abiertas de los aprobados del Post-Test", fontsize=12)
    
    # Crear la figura y los ejes
    for idx, tematica in enumerate(nombre_tematicas):
        valores = df_csv.iloc[:, idx].tolist()

        #margen_format = dict(facecolor='black', edgecolor='black', arrowstyle='-', shrinkA=0, shrinkB=0)
        #axes[idx].annotate('', xy=(40, 0), xytext=(0, 0), arrowprops=margen_format, annotation_clip=False)
        axes[idx].spines[['left', 'right', 'top']].set_visible(False)
        axes[idx].yaxis.set_major_locator(ticker.NullLocator())
        axes[idx].xaxis.set_major_locator(ticker.MultipleLocator(4.00))
        axes[idx].xaxis.set_minor_locator(ticker.MultipleLocator(1.00))
        axes[idx].xaxis.set_tick_params(labelsize=8)
        
        if idx == 0:

            # Dibujar la línea numérica
            # * linea extendida de margenes
            # * flecha alusiva de la direccion del ranking (izquierda mas afin ; derecha menos afin)
            arrow_format = dict(facecolor='black', edgecolor='black', arrowstyle='->', linestyle='dashed', shrinkA=0, shrinkB=0)
            axes[idx].set_xlim(0, 40)
            axes[idx].set_ylim(0, 1)
            axes[idx].annotate('', xy=(35, 2.125), xytext=(5, 2.125), arrowprops=arrow_format, annotation_clip=False)
            
            # Dibujar los valores y etiquetas
            axes[idx].text(0, 2, 'Mayor afinidad', horizontalalignment='left', fontsize=10)
            axes[idx].text(40, 2, 'Menor afinidad', horizontalalignment='right', fontsize=10)
            axes[idx].text(0 - 0.8, 0, tematica, rotation='vertical', ha='left', va='center', fontsize=8)

        # * REFERENCIA: 
            # * https://stackoverflow.com/questions/23186804/graph-point-on-straight-line-number-line-in-python
            # * https://stackoverflow.com/questions/33737736/matplotlib-axis-arrow-tip
            # * https://matplotlib.org/stable/gallery/ticks/tick-formatters.html

        else:
            axes[idx].set_xlim(0, 40)
            axes[idx].set_ylim(0, 1)
            axes[idx].text(0 - 0.8, 0, tematica, rotation='vertical', ha='left', va='center', fontsize=8)
        
        # * OJO: gc -> verde flourescente (99FF33) ; ge -> naranja flourescente (FF9933)
        idx_grupo = 0
        for valor, etiqueta in zip(valores, etiquetas):
            axes[idx].plot(valor, 0.4, 'o', color=colores_por_idx[idx_grupo])
            axes[idx].text(valor, 1, etiqueta, rotation=24, ha='center', va='center', fontsize=7)
            idx_grupo+=1

    plt.savefig(NOMBRE_ARCHIVO)
    plt.close()
    print(f"GRAFICA {NOMBRE_ARCHIVO} realizada con éxito!")

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

def getNumberLineRankingTematicasPreguntasAbiertas(df_csv):
    def create_custom_colormap(start_color_hex, end_color_hex, num_levels):
        start_color_rgb = tuple(int(start_color_hex[i:i+2], 16) / 255.0 for i in (0, 2, 4))
        
        # Define a more distinct end color
        end_color_rgb = tuple(int(end_color_hex[i:i+2], 16) / 255.0 for i in (0, 2, 4))

        colors = [start_color_rgb]
        for i in range(1, num_levels - 1):
            ratio = i / (num_levels - 1)
            color = [start + ratio * (end - start) for start, end in zip(start_color_rgb, end_color_rgb)]
            colors.append(color)

        colors.append(end_color_rgb)

        return LinearSegmentedColormap.from_list('custom_colormap', colors, N=num_levels)

    def assign_colors(id_grupo_list):

        # * contadores para mantener el control del conteo
        gc_idx = 0
        ge_idx = 0
        colores_por_idx = []        

        # * Count occurrences of 'gc' and 'ge' in the 'ID Grupo' column
        gc_count = sum('gc' in x for x in id_grupo_list)
        ge_count = sum('ge' in x for x in id_grupo_list)

        # * Gradientes para colores
        gc_gradient = create_custom_colormap("08FF08", "024002", gc_count) # * green-ish
        ge_gradient = create_custom_colormap("FF5100", "61360E", ge_count) # * orange-ish

        for id_grupo in id_grupo_list:
            if 'gc' in id_grupo:
                color_asignado = gc_gradient(gc_idx)
                colores_por_idx.append(color_asignado)
                gc_idx += 1
            elif 'ge' in id_grupo:
                color_asignado = ge_gradient(ge_idx)
                colores_por_idx.append(color_asignado)
                ge_idx += 1

        return colores_por_idx
    
    df_csv = df_csv.drop(columns= ["# Control"])
    df_csv = df_csv[df_csv["Aprobado_Post-Test"]=='aprobado']
    df_csv = df_csv.drop(columns= ["Aprobado_Post-Test"])
    
    # Sort the DataFrame by the 'ID Grupo' column in ascending order
    df_csv = df_csv.sort_values(by='ID Grupo')

    # * ids enmascarados de los sujetos aprobados
    etiquetas = df_csv["ID Grupo"].tolist()

    # * listado de colores por ID Grupo
    colores_por_idx = assign_colors(etiquetas)
    
    df_csv = df_csv.drop(columns= ["ID Grupo"])
    
    # * Nombres de las columnas
    nombres_columnas = df_csv.columns.tolist()
    
    # * nombre clave de la tematica (tomado de las columnas)
    nombre_tematicas = [re.search(r'p\d+_\d+', s).group(0) for s in nombres_columnas if re.search(r'p\d+_\d+', s)]
    cantidad_tematicas = len(nombre_tematicas)

    numberLineRanking(df_csv, etiquetas, nombre_tematicas, cantidad_tematicas, colores_por_idx)

# TODO modificar para generar Parallel Coordinates plot
def getParallelCoordinatesRespuestasAprobados(df_csv):
    # Define your color-coding column
    color_column = 'ID Grupo'

    # Define the columns for the parallel coordinates plot
    parallel_columns = ['Column1', 'Column2', 'Column3']  # Add your actual column names here

    # Basic parallel coordinates plot with 'dimensions' parameter
    plt.figure(figsize=(10, 6))  # Adjust figure size as needed
    parallel_coordinates(df_csv, color_column, dimensions=parallel_columns, color=['blue', 'green', 'red'])

    # Additional formatting
    plt.title('Your Title Here', fontsize=16)  # Adjust title font size as needed
    plt.xlabel('X-axis Label', fontsize=12)  # Adjust X-axis label font size as needed
    plt.ylabel('Y-axis Label', fontsize=12)  # Adjust Y-axis label font size as needed

    # Display the plot
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
    getNumberLineRankingTematicasPreguntasAbiertas(df_ranking_csv)

if __name__ == "__main__":
    main()
