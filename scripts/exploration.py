import pandas
import numpy
import json
import optionsEncuestaPreliminar as EncuestaPreliminar
from time import time

# TODO añadir el fragmento del JSON al método
'''
import pandas as pd
import random
import json

def explorationGrupoControlGrupoExperimental(csv_file, output_file):
    NOMBRE_COLUMNA = 'Número de control:'

    df = pd.read_csv(csv_file, encoding='utf-8')

    # Paso 1: Mezclar aleatoriamente los registros
    df = df.sample(frac=1, random_state=42)

    # Paso 2: Divide en grupo de control y grupo experimental
    mitad = len(df) // 2

    grupo_control = df.iloc[:mitad]
    grupo_experimental = df.iloc[mitad:]

    # Si quedó un registro sin asignar, puedes decidir cómo manejarlo. Por ejemplo, puedes incluirlo en el grupo de control:
    if len(grupo_control) < len(grupo_experimental):
        grupo_control = grupo_control.append(grupo_experimental.iloc[-1])
        grupo_experimental = grupo_experimental.iloc[:-1]

    listado_grupo_control = grupo_control[NOMBRE_COLUMNA].tolist()
    listado_grupo_experimental = grupo_experimental[NOMBRE_COLUMNA].tolist()

    # Guarda los listados en un archivo JSON
    data = {
        "Grupo de Control": listado_grupo_control,
        "Grupo Experimental": listado_grupo_experimental
    }

    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    # Muestra los números de control para cada grupo
    print("\nEXPLORACION DE GRUPO DE CONTROL Y GRUPO EXPERIMENTAL")
    print("\nCONTROL")
    for idx, ncontrol_control in enumerate(listado_grupo_control):
        print(f"{ncontrol_control}")
    print("\nEXPERIMENTAL")
    for idx, ncontrol_exp in enumerate(listado_grupo_experimental):
        print(f"{ncontrol_exp}")

# Llama a la función pasando el archivo CSV y el nombre del archivo JSON de salida como argumentos
explorationGrupoControlGrupoExperimental('tu_archivo.csv', 'salida.json')
'''

def explorationGrupoControlGrupoExperimental(csv_file):
    NOMBRE_COLUMNA = 'Número de control:'
    NOMBRE_JSON = '../results/summaries/Particion_GrupoControl_GrupoExperimental.json'

    df = pandas.read_csv(csv_file, encoding='utf-8')
    
    # * Paso 1: Mezclar aleatoriamente los registros
    df = df.sample(frac=1, random_state=42)  # Aquí, random_state es una semilla para reproducibilidad

    # * Paso 2: Divide en grupo de control y grupo experimental
    mitad = len(df) // 2  # Esto siempre redondeará hacia abajo al número entero más cercano

    timestamp = int(time())

    grupo_control = df.iloc[:mitad]
    grupo_experimental = df.iloc[mitad:]

    # * Si quedó un registro sin asignar, puedes decidir cómo manejarlo. Por ejemplo, puedes incluirlo en el grupo de control:
    if len(grupo_control) < len(grupo_experimental):
        grupo_control = grupo_control.append(grupo_experimental.iloc[-1])
        grupo_experimental = grupo_experimental.iloc[:-1]

    listado_grupo_control = grupo_control[NOMBRE_COLUMNA].tolist()
    listado_grupo_experimental = grupo_experimental[NOMBRE_COLUMNA].tolist()

    # * Muestra los números de control para cada grupo
    print("\nEXPLORACION DE GRUPO DE CONTROL Y GRUPO EXPERIMENTAL")
    print("\nCONTROL")
    for idx, ncontrol_control in enumerate(listado_grupo_control):
        print(f"{ncontrol_control}")
    print("\nEXPERIMENTAL")
    for idx, ncontrol_exp in enumerate(listado_grupo_experimental):
        print(f"{ncontrol_exp}")

    # * Guarda los listados en un archivo JSON
    data = {
        "tiempo_particion_unix": timestamp,
        "grupo_control": listado_grupo_control,
        "grupo_experimental": listado_grupo_experimental,
    }

    with open(NOMBRE_JSON, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print("SUMMARY Particion_GrupoControl_GrupoExperimental.json realizado con éxito!")       

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

    #explorationNombreColumnas(CSV_FILE)
    #explorationIncidenciasInteres(CSV_FILE)
    explorationGrupoControlGrupoExperimental(CSV_FILE)

if __name__ == "__main__":
    main()
