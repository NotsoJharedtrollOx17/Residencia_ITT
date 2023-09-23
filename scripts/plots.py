import pandas
import matplotlib.pyplot as plt

# * permite hacer las graficas con fondo transparente
plt.rcParams.update({"figure.facecolor": (1, 1, 1, 0)})


# TODO histogramas de las preguntas demográficas
def histogram(csv_file, columna_csv, opciones):
    df = pandas.read_csv(csv_file)
    datos = df.iloc[:, columna_csv]
    contador_incidencias = [datos.count(opcion) for opcion in opciones]
    etiquetas = opciones

    fig, axes = plt.subplots(figsize=(10, 6))
    bars = axes.bar(etiquetas, contador_incidencias, alpha=0.7)
    axes.set_xlabel("Opciones de Respuesta")
    axes.set_ylabel("Conteo")
    axes.set_title(f"Histograma de Opciones Pregunta DEMOGRAFICA {columna_csv}")

    plt.savefig(f".\\results\plots\histograma_preguntademografica{columna_csv}")
    n_filas, n_columnas = df.shape


def main():
    CSV_FILE = ".\csv\EncuestaPreliminar.csv"

    opciones_pregunta3 = ["17", "18", "19", "20", "21 o mas"]
    opciones_pregunta4 = ["Alta", "Media Alta", "Media", "Media Baja", "Baja"]
    opciones_pregunta5 = [
        "Primaria terminada o trunca",
        "Secundaria terminada o trunca",
        "Prepatoria/Bachillerato tecnico terminado o trunco",
        "Licenciatura terminada o trunca",
        "Posgrados (Maestrias, Doctorados, etc.)",
    ]
    opciones_pregunta6 = opciones_pregunta5
    opciones_pregunta7 = ["Si", "No"]
    opciones_pregunta29 = ["Mujer", "Hombre", "No-binary", "Prefiero no decir"]

    histogram(CSV_FILE, 3, opciones_pregunta3)
    histogram(CSV_FILE, 4, opciones_pregunta4)
    histogram(CSV_FILE, 5, opciones_pregunta5)
    histogram(CSV_FILE, 6, opciones_pregunta6)
    histogram(CSV_FILE, 7, opciones_pregunta7)
    histogram(CSV_FILE, 29, opciones_pregunta29)


if __name__ == "__main__":
    main()
