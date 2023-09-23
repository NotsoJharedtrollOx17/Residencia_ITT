import pandas
import matplotlib.pyplot as plt

# * permite hacer las graficas con fondo transparente
plt.rcParams.update({"figure.facecolor": (1, 1, 1, 0)})


# TODO alternativa de despliegue de opciones muy largas como anidado en leyenda
def histogram(df, columna_csv, opciones):
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
    bars = axes.bar(conteo.index, conteo.values, alpha=0.7, color=colores)
    axes.set_xlabel("Opciones de Respuesta")
    axes.set_ylabel("Conteo")
    axes.set_title(f"{nombre_pregunta[columna_csv-1]}")

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


def main():
    CSV_FILE = "../csv/EncuestaPreliminar.csv"
    df_csv = pandas.read_csv(CSV_FILE)

    opciones_pregunta3 = ["17", "18", "19", "20", "21 o más"]
    opciones_pregunta4 = [
        "Clase Alta",
        "Clase Media Alta",
        "Clase Media",
        "Clase Media Baja",
        "Clase Baja",
    ]
    opciones_pregunta5 = [
        "Primaria terminada o trunca",
        "Secundaria terminada o trunca",
        "Prepatoria/Bachillerato Técnico terminado o trunco",
        "Licenciatura terminada o trunca",
        "Posgrados (Maestría, Doctorado, etc.)",
    ]
    opciones_pregunta6 = opciones_pregunta5
    opciones_pregunta7 = ["Sí", "No"]
    opciones_pregunta29 = ["Mujer", "Hombre", "No-binary", "Prefiero no decir"]

    histogram(df_csv, 3, opciones_pregunta3)
    histogram(df_csv, 4, opciones_pregunta4)
    histogram(df_csv, 5, opciones_pregunta5)
    histogram(df_csv, 6, opciones_pregunta6)
    histogram(df_csv, 7, opciones_pregunta7)
    histogram(df_csv, 29, opciones_pregunta29)


if __name__ == "__main__":
    main()
