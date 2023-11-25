import pandas
import numpy
import optionsEncuestaPreliminar as EncuestaPreliminar

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
    BIG_MERGED_DATASET_CSV_FILE = '../csv/Merge_EncuestaPreliminar_ValidPreTestPostTest.csv'

    getAprobados(BIG_MERGED_DATASET_CSV_FILE)
    

if __name__ == '__main__':
    main()