from transformers import pipeline

def main():
    MODEL_NAME = 'dccuchile/bert-base-spanish-wwm-cased'
    
# Crear un pipeline y cargar el modelo en la ruta especificada
    pipe = pipeline("text-generation", model=MODEL_NAME)
    print(f'MODELO {MODEL_NAME} descargado con éxito')

    
if __name__ == '__main__':
    main()