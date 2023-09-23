import pandas
import matplotlib.pyplot as plt

# * permite hacer las graficas con fondo transparente
plt.rcParams.update({"figure.facecolor": (1, 1, 1, 0)})


# TODO alternativa de despliegue de opciones muy largas como anidado en leyenda
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

    axes.set_xlabel("Respuesta", fontsize=14)
    axes.set_ylabel("Número de incidencias", fontsize=14)
    axes.set_title(f"{nombre_pregunta[columna_csv-1]}", fontsize=16)
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
    print(f"GRAFICA {nombre_archivo} realizada con éxito!")

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

    print("INICIO Histogramas de los Datos Demograficos")
    histograma(df_csv, 3, opciones_pregunta3)
    histograma(df_csv, 4, opciones_pregunta4)
    histograma(df_csv, 5, opciones_pregunta56)
    histograma(df_csv, 6, opciones_pregunta56)
    histograma(df_csv, 7, opciones_pregunta7)
    histograma(df_csv, 27, opciones_pregunta27)
    print("FIN Histogramas de los Datos Demograficos\n")

def getHistogramaDiagnosticoAprendizajeQuimica(df_csv):
    print("INICIO Histogramas del diagnóstico respecto al aprendizaje de Química")
    print("FIN Histogramas del diagnóstico respecto al aprendizaje de Química")

def main():
    CSV_FILE = "../csv/EncuestaPreliminar.csv"
    df_csv = pandas.read_csv(CSV_FILE)

    getHistogramaDatosDemograficos(df_csv)
    getHistogramaDiagnosticoAprendizajeQuimica(df_csv)

if __name__ == "__main__":
    main()
