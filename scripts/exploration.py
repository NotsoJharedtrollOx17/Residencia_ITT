import pandas
import numpy
import optionsEncuestaPreliminar as EncuestaPreliminar

def explorationIncidenciasInteres(csv_file):
    df = pandas.read_csv(csv_file, encoding='utf-8')
    print("\tEXPLORACION DE INCIDENCIAS DE DATOS")
    
    # * Nombres de las preguntas para iterar alrededor de ellas
    nombres_columnas = df.columns.tolist()
    
    incidencias_interes = EncuestaPreliminar.getIndicesIncidenciasInteres()
    
        # Iterar a través de las incidencias e imprimir las columnas correspondientes
    for id_incidencia, incidencia in enumerate(incidencias_interes):
        print(f"\nColumnas para la incidencia {incidencia}:")
        for idx in incidencia:
            print(f"•{idx}: {nombres_columnas[idx]}")    

def explorationNombreColumnas(csv_file):
    df = pandas.read_csv(csv_file, encoding='utf-8')
    #print(df)

    # * Obtener las dimensiones de los datos (filas x columnas)
    filas, columnas = df.shape

    print("\tEXPLORACION INICIAL DE DATOS")
    print(f"Ruta del archivo explorado: {csv_file}\n")
    print(f"Dimensiones de los datos: {filas} filas x {columnas} columnas\n")

    # * Imprimir los nombres de las columnas
    nombres_columnas = df.columns.tolist()

    print("Nombres de las columnas:")
    for idx, nombre in enumerate(nombres_columnas):
        print(f"•{idx+1}: {nombre}")

    # * Prueba de acceso de nombre_columnas por medio de indices
    #print(nombres_columnas[3])

    # * prueba de tipo de datos desplegados
    #datos = df.iloc[:, 3]
    #datos = datos.value_counts()
    #datos = datos.values

    #print(datos)
    #print(numpy.array(datos.tolist()))

def main():
    CSV_FILE = "../csv/EncuestaPreliminar.csv"

    explorationNombreColumnas(CSV_FILE)
    #explorationIncidenciasInteres(CSV_FILE)


if __name__ == "__main__":
    main()
