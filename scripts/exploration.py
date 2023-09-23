import pandas

def exploration(csv_file):
    df = pandas.read_csv(csv_file)

    # Obtener las dimensiones de los datos (filas x columnas)
    filas, columnas = df.shape
    
    print("\tEXPLORACION INICIAL DE DATOS")
    print(f'Ruta del archivo explorado: {csv_file}\n')
    print(f'Dimensiones de los datos: {filas} filas x {columnas} columnas\n')

    # Imprimir los nombres de las columnas
    nombres_columnas = df.columns.tolist()
    print('Nombres de las columnas:')
    for idx, nombre in enumerate(nombres_columnas):
        print(f'•{idx+1}: {nombre}')

def main():
    CSV_FILE = '.\csv\EncuestaPreliminar.csv'
    
    exploration(CSV_FILE)
    
if __name__ == '__main__':
    main()