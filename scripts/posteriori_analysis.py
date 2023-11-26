import pandas
import json

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

def getTematicasPreguntasAbiertasAcordeGrupo(summary_json_file, merge_encuesta_csv_file):
    df_merge = pandas.read_csv(merge_encuesta_csv_file, encoding='utf-8')
    
    with open(summary_json_file, 'r') as file:
        data = json.load(file)

    # * PRIMER CICLO: acceder a los datos de interes: id_tema y numero_control_respuestas
    for id_pregunta, pregunta in enumerate(data):
        df_tema1 = None
        df_tema2 = None
        numero_pregunta = pregunta["id_pregunta"]
        id_temas = pregunta["summary"]["id_tema"]
        numeros_control_respuestas = pregunta["summary"]["numero_control_respuestas"]

        for idx, numeros_control in enumerate(numeros_control_respuestas):
            nombre_columna_nueva = f'ID_Temática_Pregunta{numero_pregunta}'
            print(numeros_control)
            
        # * concatenacion de los datos recabados en con las tematicas correctas
        df_tematicas = pandas.concat([df_tema1, df_tema2], axis=0)
        df_tematicas = df_tematicas[['# Control', nombre_columna_nueva]]

        # * union de todos los datos a comparar para facilidad de análisis
        df_merge = pandas.merge(df_merge, df_tematicas, how='outer', on='# Control',)
        
def main():
    SUMMARY_FILE = '../results/summaries/PreguntasAbiertasEncuestaPreliminar.json'
    ENCUESTA_PRELIMINAR_CSV_FILE = "../csv/EncuestaPreliminar.csv"
    BIG_MERGED_DATASET_CSV_FILE = '../csv/Merge_EncuestaPreliminar_ValidPreTestPostTest.csv'

    #getAprobados(BIG_MERGED_DATASET_CSV_FILE)
    getTematicasPreguntasAbiertasAcordeGrupo(SUMMARY_FILE, BIG_MERGED_DATASET_CSV_FILE)

if __name__ == '__main__':
    main()