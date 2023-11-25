import pandas
import numpy as np
import optionsEncuestaPreliminar as EncuestaPreliminar

def getDataFrameRespuestasCategoricasNormalizadas(df_csv):
    # normalizando preguntas con respuestas categoricas a minúsculas
        # * dichas preguntas son las de las columnas 13 -> 26
    df_normalizado = df_csv.copy()
    nombres_columnas = df_normalizado.columns.tolist()
    nombres_columnas = nombres_columnas[13-1:26]

    for columna in nombres_columnas:
        df_normalizado[columna] = df_csv[columna].apply(lambda x: x.lower())
            
    return df_normalizado

def getIncidenciasTresPreguntas(df_csv, posiciones_preguntas):

    # * utilizar parte de este método para plasmar incidencias en CSV
    nombre_columnas = df_csv.columns.tolist()

    incidencia_interes = df_csv[['Número de control:', 
                                 nombre_columnas[posiciones_preguntas[0]], 
                                 nombre_columnas[posiciones_preguntas[1]],
                                 nombre_columnas[posiciones_preguntas[2]]]]
    incidencia_interes['pivot'] = np.ones(39)

    grupo_incidencias_count = incidencia_interes.groupby(by=[
                                            nombre_columnas[posiciones_preguntas[0]], 
                                           nombre_columnas[posiciones_preguntas[1]], 
                                           nombre_columnas[posiciones_preguntas[2]]]).count().unstack()

    print(grupo_incidencias_count)

def getContingenciasEncuestaPreliminar(encuesta_csv_file):
    df_encuesta = pandas.read_csv(encuesta_csv_file, encoding='utf-8')
    df_normalizado = getDataFrameRespuestasCategoricasNormalizadas(df_encuesta)

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

        getIncidenciasTresPreguntas(df_normalizado, incidencias)

    print("FIN Incidencias detectas en la Encuesta Preliminar")

def getAprobados(csv_file):
    df_merge = pandas.read_csv(csv_file, encoding='utf-8')

    # * obtención del nombre de las columnas del merge
    nombre_columnas_merge = df_merge.columns.tolist()

    # * consulta de datos donde el Post-Test fue aprobado
    df_aprobados = df_merge[df_merge[nombre_columnas_merge[31]] == 'aprobado']

    # * filtrado de columnas de interes...
    df_aprobados = df_aprobados[nombre_columnas_merge]

    # * despliegue de datos...
    nombre_columnas_aprobados = df_aprobados.columns.to_list()

    print("INICIO DATOS RECABADOS PARA SUJETOS QUE APROBARON EL POST-TEST")
    for idx, nombre_columna in enumerate(nombre_columnas_aprobados):
        print(f"\n• {idx+1}: {nombre_columna}")
        print(df_aprobados[nombre_columna].to_string(index=False))
    print("\nFIN DATOS RECABADOS PARA SUJETOS QUE APROBARON EL POST-TEST")

def main():
    ENCUESTA_PRELIMINAR_CSV_FILE = "../csv/EncuestaPreliminar.csv"
    BIG_MERGED_DATASET_CSV_FILE = '../csv/Merge_EncuestaPreliminar_ValidPreTestPostTest.csv'

    getAprobados(BIG_MERGED_DATASET_CSV_FILE)
    #getContingenciasEncuestaPreliminar(ENCUESTA_PRELIMINAR_CSV_FILE)

if __name__ == '__main__':
    main()