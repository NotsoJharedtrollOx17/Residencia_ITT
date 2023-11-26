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

def getRankingTematicasPreguntasAbiertasAcordeGrupo(summary_json_file, merge_encuesta_csv_file):
    RANKING_TEMATICAS_PREGUNTAS_ABIERTAS_ENCUESTA_CSV_FILE = '../csv/Ranking_Tematicas_PreguntasAbiertas_EncuestaPreliminar_ValidPreTestPostTest.csv'

    df_merge = pandas.read_csv(merge_encuesta_csv_file, encoding='utf-8')
    df_merge = df_merge[["# Control", "ID Grupo", "Aprobado_Post-Test"]]

    with open(summary_json_file, 'r') as file:
        data = json.load(file)

    # * PRIMER CICLO: acceder a los datos de interes: id_tema y numero_control_respuestas
    for id_pregunta, pregunta in enumerate(data):
        df_tematicas = None
        numero_pregunta = pregunta["id_pregunta"]
        id_temas = pregunta["summary"]["id_tema"]
        numeros_control_respuestas = pregunta["summary"]["numero_control_respuestas"]

        # * SEGUNDO CICLO: asignación de ranking a la afinidad de las respuestas de dichos numeros de control
        for idx, numeros_control in enumerate(numeros_control_respuestas):
            nombre_columna_nueva = f'Rank_ID_Temática_{id_temas[idx]}'

            df_tematicas = pandas.DataFrame({
                "# Control": numeros_control,
                nombre_columna_nueva: list(range(1,39+1))
            })

            # * union de todos los datos a comparar para facilidad de análisis
            df_merge = pandas.merge(df_merge, df_tematicas, how='outer', on='# Control',)

    nombres_columnas = df_merge.columns.tolist()

    print("INICIO RANKING DE TEMATICAS DETECTADAS EN LAS RESPUESTAS DE LAS PREGUNTAS ABIERTAS DE LA ENCUESTA PRELIMINAR")
    print("Nombres de las columnas:")
    for idx, nombre in enumerate(nombres_columnas):
        print(f"•{idx}: {nombre}")

        # * generacion de CSV del merge
    df_merge.to_csv(
        RANKING_TEMATICAS_PREGUNTAS_ABIERTAS_ENCUESTA_CSV_FILE, index=False)
    print(f"CSV {RANKING_TEMATICAS_PREGUNTAS_ABIERTAS_ENCUESTA_CSV_FILE} realizado con éxito!")
    print("\nFIN RANKING DE TEMATICAS DETECTADAS EN LAS RESPUESTAS DE LAS PREGUNTAS ABIERTAS DE LA ENCUESTA PRELIMINAR")

def main():
    SUMMARY_FILE = '../results/summaries/PreguntasAbiertasEncuestaPreliminar.json'
    ENCUESTA_PRELIMINAR_CSV_FILE = "../csv/EncuestaPreliminar.csv"
    BIG_MERGED_DATASET_CSV_FILE = '../csv/Merge_EncuestaPreliminar_ValidPreTestPostTest.csv'

    #getAprobados(BIG_MERGED_DATASET_CSV_FILE)
    getRankingTematicasPreguntasAbiertasAcordeGrupo(SUMMARY_FILE, BIG_MERGED_DATASET_CSV_FILE)

if __name__ == '__main__':
    main()