import pandas
import numpy
import json
import optionsEncuestaPreliminar as EncuestaPreliminar
from time import time

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
        print(f"•{idx}: {nombre}")

def explorationNumerosControlEncuestaTests(encuesta_csv_file, 
                                            tests_grupo_control_csv_file, 
                                            tests_grupo_experimental_csv_file):
    
    TESTS_GRUPO_CONTROL_VALIDADOS_CSV_FILE = '../csv/VALID_PreTestPostTest_grupoControl.csv'
    TESTS_GRUPO_EXPERIMENTAL_VALIDADOS_CSV_FILE = '../csv/VALID_PreTestPostTest_grupoExperimental.csv'

    df_encuesta = pandas.read_csv(encuesta_csv_file, encoding='utf-8')
    df_grupo_control = pandas.read_csv(tests_grupo_control_csv_file, encoding='utf-8')
    df_grupo_experimental = pandas.read_csv(tests_grupo_experimental_csv_file, encoding='utf-8')
    df_grupo_control['# Control'] = df_grupo_control['# Control'].astype(str)
    df_grupo_experimental['# Control'] = df_grupo_experimental['# Control'].astype(str)

    # * concatenacion de los datos recabados en la realización del pre-test y post-test
    df_tests = pandas.concat([df_grupo_control, df_grupo_experimental], axis=0)

    # * validacion a datos de tipo string para los numeros de control
    df_encuesta = pandas.DataFrame({'Número de control:': df_encuesta['Número de control:'].astype(str)})
    #df_grupo_control = pandas.DataFrame({'# Control': df_grupo_control['# Control'].astype(str)})
    #df_grupo_experimental = pandas.DataFrame({'# Control': df_grupo_experimental['# Control'].astype(str)})
    df_tests = pandas.DataFrame({'# Control': df_tests['# Control'].astype(str)})

    # * Obtener datos de los participantes que SI respondieron la encuesta a tiempo
    numeros_de_control_comunes = pandas.merge(df_encuesta, df_tests, 
                                              how='outer', 
                                              right_on='# Control', 
                                              left_on='Número de control:', 
                                              indicator=True)
    
    numeros_de_control_no_comunes = numeros_de_control_comunes[
        numeros_de_control_comunes['Número de control:'].isna()]
    
    numeros_no_validos_grupo_control = df_grupo_control[
        df_grupo_control['# Control'].
        isin(numeros_de_control_no_comunes['# Control'])]
    
    numeros_no_validos_grupo_experimental = df_grupo_experimental[
        df_grupo_experimental['# Control'].
        isin(numeros_de_control_no_comunes['# Control'])] 

    # * Obtener ... dentro del GRUPO CONTROL
    numeros_validos_grupo_control = df_grupo_control[
        ~df_grupo_control['# Control'].
        isin(numeros_de_control_no_comunes['# Control'])]
    
    # * Obtener ... dentro del GRUPO EXPERIMENTAL
    numeros_validos_grupo_experimental = df_grupo_experimental[
        ~df_grupo_experimental['# Control'].
        isin(numeros_de_control_no_comunes['# Control'])] 

    # * Mostrar los resultados
    print("\nNúmeros de Control NO Válidos:")
    print(numeros_de_control_no_comunes)

    print("\nNúmeros de Control NO Válidos Grupo CONTROL")
    print(numeros_no_validos_grupo_control)

    print("\nNúmeros de Control NO Válidos Grupo EXPERIMENTAL")
    print(numeros_no_validos_grupo_experimental)

    print("\nNúmeros de Control Válidos Grupo CONTROL")
    print(numeros_validos_grupo_control)

    print("\nNúmeros de Control Válidos Grupo EXPERIMENTAL")
    print(numeros_validos_grupo_experimental)
    
    numeros_validos_grupo_control.to_csv(
        TESTS_GRUPO_CONTROL_VALIDADOS_CSV_FILE, index=False)
    print(f"\nCSV {TESTS_GRUPO_CONTROL_VALIDADOS_CSV_FILE} realizado con éxito!")

    numeros_validos_grupo_experimental.to_csv(
        TESTS_GRUPO_EXPERIMENTAL_VALIDADOS_CSV_FILE, index=False)
    print(f"CSV {TESTS_GRUPO_EXPERIMENTAL_VALIDADOS_CSV_FILE} realizado con éxito!")
    
def explorationBigMergedDataset(encuesta_csv_file):
    BIG_MERGED_DATASET_CSV_FILE = '../csv/Merge_EncuestaPreliminar_ValidPreTestPostTest.csv'
    TESTS_GRUPO_CONTROL_VALIDADOS_CSV_FILE = '../csv/VALID_PreTestPostTest_grupoControl.csv'
    TESTS_GRUPO_EXPERIMENTAL_VALIDADOS_CSV_FILE = '../csv/VALID_PreTestPostTest_grupoExperimental.csv'

    df_encuesta = pandas.read_csv(encuesta_csv_file, encoding='utf-8')
    df_grupo_control = pandas.read_csv(TESTS_GRUPO_CONTROL_VALIDADOS_CSV_FILE, encoding='utf-8')
    df_grupo_experimental = pandas.read_csv(TESTS_GRUPO_EXPERIMENTAL_VALIDADOS_CSV_FILE, encoding='utf-8')
    
    n_rows_control, n_columns_control = df_grupo_control.shape
    n_rows_experimental, n_columns_experimental = df_grupo_experimental.shape

    # * reescritura de los datos a tipo string ; evita problemas en el merge por errores de conversion de datos e Google Sheets a Google Docs
    df_encuesta['Número de control:'] = df_encuesta['Número de control:'].astype(str)
    df_grupo_control['# Control'] = df_grupo_control['# Control'].astype(str)
    df_grupo_experimental['# Control'] = df_grupo_experimental['# Control'].astype(str)
    
    # * agregación de columnas para asignar ID de grupo de control o el ID de grupo experimental
        # * Grupo de control: gc_nn
        # * Grupo Experimental: ge_nn
    list_id_grupo_control = []
    list_id_grupo_experimental = []
    id_grupo = ""

    for idx in range (1, n_rows_control+1):
        if idx <= 9:
            id_grupo = f"gc0{idx}"
        else:
            id_grupo = f"gc{idx}"

        list_id_grupo_control.append(id_grupo)

    for idx in range (1, n_rows_experimental+1):
        id_grupo = ""

        if idx <= 9:
            id_grupo = f"ge0{idx}"
        else:
            id_grupo = f"ge{idx}"

        list_id_grupo_experimental.append(id_grupo)

    df_grupo_control.insert(0, "ID Grupo", list_id_grupo_control)
    df_grupo_experimental.insert(0, "ID Grupo", list_id_grupo_experimental)

    # * concatenacion de los datos recabados en la realización del pre-test y post-test
    df_tests = pandas.concat([df_grupo_control, df_grupo_experimental], axis=0)

    # * union de todos los datos a comparar para facilidad de análisis
    df_big_merged_dataset = pandas.merge(df_encuesta, df_tests, 
                                              how='outer', 
                                              right_on='# Control', 
                                              left_on='Número de control:',)
    
    # * eliminacion de campos repetidos o innecesarios
    df_big_merged_dataset = df_big_merged_dataset.drop(columns=['Marca temporal', 'Número de control:'])

    # * ordenación de campos para mayor legibilidad
    df_big_merged_dataset.insert(0, 'ID Grupo', df_big_merged_dataset.pop('ID Grupo'))
    df_big_merged_dataset.insert(0, '# Control', df_big_merged_dataset.pop('# Control'))
    df_big_merged_dataset.insert(2, 'Seleccione su identidad de género:', df_big_merged_dataset.pop('Seleccione su identidad de género:'))

    # * generacion de CSV del merge
    df_big_merged_dataset.to_csv(
        BIG_MERGED_DATASET_CSV_FILE, index=False)
    print(f"CSV {BIG_MERGED_DATASET_CSV_FILE} realizado con éxito!")

def main():
    BIG_MERGED_DATASET_CSV_FILE = '../csv/Merge_EncuestaPreliminar_ValidPreTestPostTest.csv'
    ENCUESTA_PRELIMINAR_CSV_FILE = "../csv/EncuestaPreliminar.csv"
    TESTS_GRUPO_CONTROL_CSV_FILE = "../csv/PreTestPostTest_grupoControl.csv"
    TESTS_GRUPO_EXPERIMENTAL_CSV_FILE = "../csv/PreTestPostTest_grupoExperimental.csv"

    #explorationNombreColumnas(ENCUESTA_PRELIMINAR_CSV_FILE)
    #explorationIncidenciasInteres(ENCUESTA_PRELIMINAR_CSV_FILECSV_FILE)
    #explorationGrupoControlGrupoExperimental(ENCUESTA_PRELIMINAR_CSV_FILECSV_FILE)
    #explorationNumerosControlEncuestaTests(ENCUESTA_PRELIMINAR_CSV_FILE, TESTS_GRUPO_CONTROL_CSV_FILE, TESTS_GRUPO_EXPERIMENTAL_CSV_FILE)
    explorationBigMergedDataset(ENCUESTA_PRELIMINAR_CSV_FILE)
    explorationNombreColumnas(BIG_MERGED_DATASET_CSV_FILE)

if __name__ == "__main__":
    main()
