import pandas
import optionsEncuestaPreliminar as EncuestaPreliminar
from scipy.stats import shapiro

# TODO aplicar tests estadisticos para determinar eficacia del tratamiento.
'''
    2. Determinar la prueba estadística indicada para medir el impacto del tratamiento y y de la técnica original
    3. En base a lo anterior, elaborar la prueba estadística correspondiente
'''

def getNormality(df, labels):
    # * Prueba shapiro-Wilk para normalidad de los datos
    pretest_posttest_normal = []

    for idx, label in enumerate(labels):
        print(f"\n{label}")
        shapiro_wilk, p_value = shapiro(df[label])
        print(f"Estadística de prueba Shapiro-Wilk: {shapiro_wilk}")
        print(f"Valor p: {p_value}")

        # Interpretación
        alpha = 0.05

        if p_value < alpha:
            print("La hipótesis nula de No-Normalidad entre los datos es rechazada.")
            print("Hay evidencia suficiente para afirmar que existe normalidad en los datos.")
            print("USAR Paired t-test\n")
            pretest_posttest_normal.append(True)
        else:
            print("No hay suficiente evidencia para rechazar la hipótesis nula.")
            print("No se puede afirmar que existe normalidad en los datos.")
            print("USAR Wilcoxon Signed test.\n")
            pretest_posttest_normal.append(False)

    both_normal = True if (pretest_posttest_normal[0] and pretest_posttest_normal[1]) else False

    if both_normal:
        print("• USAR Paired t-test para EVALUAR GRUPO CONTROL!!!\n")
    else:
        print("• USAR Wilcoxon Signed test para EVALUAR GRUPO EXPERIMENTAL!!!\n")

def getExistenciaNormalidadDatos(encuesta_csv_file, 
                                            tests_grupo_control_csv_file, 
                                            tests_grupo_experimental_csv_file):
    
    PRETEST_POSTTEST_LABELS = ['Pre-Test', 'Post-Test']

    #df_encuesta = pandas.read_csv(encuesta_csv_file, encoding='utf-8')
    df_grupo_control = pandas.read_csv(tests_grupo_control_csv_file, encoding='utf-8')
    df_grupo_experimental = pandas.read_csv(tests_grupo_experimental_csv_file, encoding='utf-8')
    df_grupo_control['# Control'] = df_grupo_control['# Control'].astype(str)
    df_grupo_experimental['# Control'] = df_grupo_experimental['# Control'].astype(str)

    # * Resultados
    print("EXISTENCIA DE NORMALIDAD EN DATOS DE GRUPO DE CONTROL")
    getNormality(df_grupo_control, PRETEST_POSTTEST_LABELS)

    print("EXISTENCIA DE NORMALIDAD EN DATOS DE GRUPO EXPERIMENTAL")
    getNormality(df_grupo_experimental, PRETEST_POSTTEST_LABELS)


def main():
    ENCUESTA_PRELIMINAR_CSV_FILE = "../csv/EncuestaPreliminar.csv"
    TESTS_GRUPO_CONTROL_VALIDADOS_CSV_FILE = '../csv/VALID_PreTestPostTest_grupoControl.csv'
    TESTS_GRUPO_EXPERIMENTAL_VALIDADOS_CSV_FILE = '../csv/VALID_PreTestPostTest_grupoExperimental.csv'
    
    print("lorem ipsum dolor")

    #shapiroWilkTest()

    getExistenciaNormalidadDatos(ENCUESTA_PRELIMINAR_CSV_FILE, TESTS_GRUPO_CONTROL_VALIDADOS_CSV_FILE, TESTS_GRUPO_EXPERIMENTAL_VALIDADOS_CSV_FILE)

if __name__ == '__main__':

    main()