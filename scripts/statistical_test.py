import pandas
from scipy.stats import shapiro
from scipy.stats import ttest_rel
from scipy.stats import wilcoxon
from scipy.stats import fisher_exact

def getNormality(df, labels):
    # * Prueba shapiro-Wilk para normalidad de los datos
    pretest_normal = None
    posttest_normal = None
    both_normal = None
    test = ""

    for idx, label in enumerate(labels):
        print(f"\n{label}")
        shapiro_wilk, p_value = shapiro(df[label])
        print(f"Estadística de prueba Shapiro-Wilk: {shapiro_wilk}")
        print(f"Valor p: {p_value}")

        # Interpretación
        alpha = 0.05

        '''
            H_0: Los datos ESTAN NORMALIZADOS
            H_1: Los datos NO ESTAN NORMALIZADOS 
        '''
        if p_value < alpha:
            print("La hipótesis nula de No-Normalidad entre los datos es rechazada.")
            print("Hay evidencia suficiente para afirmar que existe normalidad en los datos.")
            print("USAR Paired t-test\n")

            if label == "Pre-Test":
                pretest_normal = True
            if label == "Post-Test":
                posttest_normal = True
        else:
            print("No hay suficiente evidencia para rechazar la hipótesis nula.")
            print("No se puede afirmar que existe normalidad en los datos.")
            print("USAR Wilcoxon Signed test.\n")

            if label == "Pre-Test":
                pretest_normal = False
            if label == "Post-Test":
                posttest_normal = False
        
    both_normal = pretest_normal and posttest_normal

    if both_normal:
        print("• USAR Paired t-test para EVALUAR GRUPO CONTROL!!!\n")
        test = "paired"
    else:
        print("• USAR Wilcoxon Signed test para EVALUAR GRUPO EXPERIMENTAL!!!\n")
        test = "wilcoxon"

    return test

def getExistenciaNormalidadDatos(df_grupo_control, 
                                 df_grupo_experimental):
    
    PRETEST_POSTTEST_LABELS = ['Pre-Test', 'Post-Test']

    # * Resultados
    print("EXISTENCIA DE NORMALIDAD EN DATOS DE GRUPO DE CONTROL")
    test_control = getNormality(df_grupo_control, PRETEST_POSTTEST_LABELS)

    print("EXISTENCIA DE NORMALIDAD EN DATOS DE GRUPO EXPERIMENTAL")
    test_experimental = getNormality(df_grupo_experimental, PRETEST_POSTTEST_LABELS)

    return test_control, test_experimental

def getEstadisticaPairedT(df_grupo):
    # * para evitar celdas con ceros ; se aplica a TODOS LOS VALORES
    small_constant = 1
    df_grupo['Pre-Test'] += small_constant
    df_grupo['Post-Test'] += small_constant

    paired_t, p_value = ttest_rel(df_grupo['Pre-Test'], 
                                  df_grupo['Post-Test'], 
                                  alternative='less')
    print(f"\nEstadística de prueba Paired-T: {paired_t}")
    print(f"Valor p: {p_value}")

    # Interpretación
    alpha = 0.05

    if p_value < alpha:
        print("La hipótesis nula de NO MEJORIA es rechazada.")
        print("Hay evidencia suficiente para afirmar que HUBO MEJORIA.\n")
    else:
        print("No hay suficiente evidencia para rechazar la hipótesis nula.")
        print("No se puede afirmar que HUBO MEJORIA\n")
    
def getEstadisticaWilcoxon(df_grupo):
    # * para evitar celdas con ceros ; se aplica a TODOS LOS VALORES
    small_constant = 1
    df_grupo['Pre-Test'] += small_constant
    df_grupo['Post-Test'] += small_constant

    _wilcoxon, p_value = wilcoxon(df_grupo['Pre-Test'], 
                                  df_grupo['Post-Test'],
                                  zero_method='zsplit', 
                                  alternative='less')
    print(f"\nEstadística de prueba Wilcoxon: {_wilcoxon}")
    print(f"Valor p: {p_value}")

    # Interpretación
    alpha = 0.05

    if p_value < alpha:
        print("La hipótesis nula de NO MEJORIA es rechazada.")
        print("Hay evidencia suficiente para afirmar que HUBO MEJORIA.\n")
    else:
        print("No hay suficiente evidencia para rechazar la hipótesis nula.")
        print("No se puede afirmar que HUBO MEJORIA\n")

def getEstadisticaFisher(df_grupo):

    reprobado_pretest_reprobado_posttest = ((df_grupo['Aprobado_Pre-Test'] == 'reprobado') & (df_grupo['Aprobado_Post-Test'] == 'reprobado')).sum()
    reprobado_pretest_aprobado_posttest = ((df_grupo['Aprobado_Pre-Test'] == 'reprobado') & (df_grupo['Aprobado_Post-Test'] == 'aprobado')).sum()
    aprobado_pretest_reprobado_posttest = ((df_grupo['Aprobado_Pre-Test'] == 'aprobado') & (df_grupo['Aprobado_Post-Test'] == 'reprobado')).sum()
    aprobado_pretest_aprobado_posttest = ((df_grupo['Aprobado_Pre-Test'] == 'aprobado') & (df_grupo['Aprobado_Post-Test'] == 'aprobado')).sum()

    '''
        PRE-TEST/POST-TEST  REPROBADO APROBADO
                 REPROBADO     o_1      o_2
        
                 APROBADO      o_3      o_4
    '''
    # * para evitar celdas con ceros ; se aplica a TODOS LOS VALORES
    small_constant = 1
    fisher, p_value = fisher_exact([[reprobado_pretest_reprobado_posttest+small_constant, 
                                     reprobado_pretest_aprobado_posttest+small_constant],
                                    [aprobado_pretest_reprobado_posttest+small_constant,
                                     aprobado_pretest_aprobado_posttest+small_constant]])
    
    print(f"Estadística de prueba Fisher Exact: {fisher}")
    print(f"Valor p: {p_value}")

        # Interpretación
    alpha = 0.05

    '''
        H_0: NO EXISTE UNA FUERTE ASOCIACION entre los resultados del pre-test y del post-test
        H_1: SI EXISTE UNA FUERTE ASOCIACION entre los resultados...
    '''
    if p_value < alpha:
        print("La hipótesis nula de NO ASOCIACION es rechazada")
        print("Hay evidencia suficiente para afirmar que SI EXISTE UNA FUERTE ASOCIACION entre los resultados del pre-test y del post-test")        
    else:
        print("No hay suficiente evidencia para rechazar la hipótesis nula.")
        print("No se puede afirmar que existe una fuerte asociacion entre los resultados del pre-test y del post-test.")

def getPorcentajesAprobaciónPostTest(df_grupo_control, df_grupo_experimental):
    # * obteniendo el numero de registros (n_rows_control, n_rows_experimental)
    n_rows_control, n_columns_control = df_grupo_control.shape
    n_rows_experimental, n_columns_experimental = df_grupo_experimental.shape
    n_poblacion = n_rows_control + n_rows_experimental

    # * ... de aprobados en el post-test
    n_aprobados_control = df_grupo_control['Aprobado_Post-Test'].value_counts()['aprobado']
    n_aprobados_experimental = df_grupo_experimental['Aprobado_Post-Test'].value_counts()['aprobado']

    # * porcentaje..
    porcentaje_aprobados_grupo_control = round(((n_aprobados_control / n_rows_control) * 100), 2)
    porcentaje_aprobados_grupo_experimental = round(((n_aprobados_experimental / n_rows_experimental) * 100), 2)
    porcentaje_aprobados_poblacion_control = round(((n_aprobados_control / n_poblacion) * 100), 2)
    porcentaje_aprobados_poblacion_experimental = round(((n_aprobados_experimental / n_poblacion) * 100), 2)

    index = ['Control', 'Experimental']
    datos = {
        'total_muestra': [n_rows_control, n_rows_experimental],
        'total_aprobados_grupo': [n_aprobados_control, n_aprobados_experimental],
        'porcentaje_aprobados_grupo': [f"{porcentaje_aprobados_grupo_control}% ({n_aprobados_control}/{n_rows_control})", 
                                       f"{porcentaje_aprobados_grupo_experimental}% ({n_aprobados_experimental}/{n_rows_experimental})"],
        'porcentaje_aprobados_poblacion': [f"{porcentaje_aprobados_poblacion_control}% ({n_aprobados_control}/{n_poblacion})", 
                                       f"{porcentaje_aprobados_poblacion_experimental}% ({n_aprobados_experimental}/{n_poblacion})"],
    }

    df_datos_aprobacion = pandas.DataFrame(datos, index=index)
    df_datos_aprobacion = df_datos_aprobacion.transpose()

    print(df_datos_aprobacion)

def getPruebasEstadisticas(tests_grupo_control_csv_file, 
                           tests_grupo_experimental_csv_file):

    print("INICIO PRUEBAS ESTADISTICAS SOBRE EL PRE-TEST Y POST-TEST")    
    
    # * lectura preliminar de CSV a dataframes para manipulacion mas facil
    df_grupo_control = pandas.read_csv(tests_grupo_control_csv_file, encoding='utf-8')
    df_grupo_experimental = pandas.read_csv(tests_grupo_experimental_csv_file, encoding='utf-8')
    df_grupo_control['# Control'] = df_grupo_control['# Control'].astype(str)
    df_grupo_experimental['# Control'] = df_grupo_experimental['# Control'].astype(str)
    test_control, test_experimental = "", ""

    # * calculo de estadisticos descriptivos breves para estas dos columnas
    descriptivos_control = df_grupo_control[['Pre-Test', 'Post-Test']].describe()
    descriptivos_experimental = df_grupo_experimental[['Pre-Test', 'Post-Test']].describe()

    # * evaluación de normalidad en los datos para determinar el tipo de prueba estadística a aplicar en cada grupo
        # * debe ser un solo archivo para evitar complicaciones.
    test_control, test_experimental = getExistenciaNormalidadDatos(df_grupo_control, df_grupo_experimental)

    # * evaluación de los grupos de control y experimental con base al tipo de prueba...
    '''
        H_0: Pre-test >= Post-test (NO HAY MEJORA) 
        H_1: Pre-test < Post-test  (HAY MEJORA)
    '''
    print("GRUPO CONTROL (ENSENANZA TRADICIONAL)\n")
    print("DESCRIPTIVOS: ")
    print(descriptivos_control)

    if test_control == "paired":
        getEstadisticaPairedT(df_grupo_control)
    if test_control == "wilcoxon":
        getEstadisticaWilcoxon(df_grupo_control)
    getEstadisticaFisher(df_grupo_control)

    print("GRUPO EXPERIMENTAL (HERRAMIENTAS DIGITALES)\n")
    print("DESCRIPTIVOS: ")
    print(descriptivos_experimental)
    
    if test_experimental == "paired":
        getEstadisticaPairedT(df_grupo_experimental)
    if test_experimental == "wilcoxon":
        getEstadisticaWilcoxon(df_grupo_experimental)
    getEstadisticaFisher(df_grupo_experimental)

    print("PORCENTAJES DE APROBACION APLICADO EL POST-TEST")
    getPorcentajesAprobaciónPostTest(df_grupo_control, df_grupo_experimental)

    print("FIN PRUEBAS ESTADISTICAS SOBRE EL PRE-TEST Y POST-TEST")    

def main():
    TESTS_GRUPO_CONTROL_VALIDADOS_CSV_FILE = '../csv/VALID_PreTestPostTest_grupoControl.csv'
    TESTS_GRUPO_EXPERIMENTAL_VALIDADOS_CSV_FILE = '../csv/VALID_PreTestPostTest_grupoExperimental.csv'

    getPruebasEstadisticas(TESTS_GRUPO_CONTROL_VALIDADOS_CSV_FILE, TESTS_GRUPO_EXPERIMENTAL_VALIDADOS_CSV_FILE)

if __name__ == '__main__':
    main()
