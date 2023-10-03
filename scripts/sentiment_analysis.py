import pandas
import json
import g4f # TODO descargar dependencia
from nltk.corpus import stopwords
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

def getSpanishStopWords():
    stop_words = list(stopwords.words('spanish'))
    return stop_words

def getTemasDeRespuestas(idx ,df_csv, count, lda, nombre_pregunta):
    datos = df_csv.values
    n_palabras_tema = 6
    descripcion_temas = []
    id_temas = []
    
    # * obtencion de los temas recurrentes
    input_features = count.fit_transform(datos)
    input_features_name = count.get_feature_names_out()
    output = lda.fit_transform(input_features)

    # * despliegue de temas recurrentes
    print(f' \n{nombre_pregunta}')
    for tema_idx, tema in enumerate(lda.components_):
        palabras_tema = ' '.join([input_features_name[i]
                      for i in tema.argsort()\
                        [:-n_palabras_tema -1:-1]])

        id_temas.append(tema_idx)
        descripcion_temas.append(palabras_tema) 
        
        print(f'Tema {tema_idx+1}: ')
        print(palabras_tema)
    
    summary = {
        'nombre_pregunta': nombre_pregunta,
        'id_tema': id_temas,
        'descripción_tema': descripcion_temas 
    }
    
    json_summary = {
        'idx': idx,
        'summary': summary,
    }

    # * estructura json de temas recurrentes
    return json_summary

# TODO redactar método ; utiliza de entrada el archivo JSON generado en getTemasDeRespuestas()
def getTematicasCoherentesConLLM(summary_file):
    
    with open(summary_file, 'r') as file:
        data = json.load(file)
    
# Itera sobre los datos
    for id_pregunta, pregunta in enumerate(data):
        nombre_pregunta = pregunta['summary']['nombre_pregunta']
        descripciones = pregunta['summary']['descripción_tema']

        # Prefacio
        prefacio = f"En relación a la pregunta: {nombre_pregunta}, las respuestas obtenidas se analizaron con un modelo NLP que detectó una de las siguientes tematicas en forma de una serie de palabras: "

        print(f'\nPregunta {id_pregunta+1}: {nombre_pregunta}')
        # Genera oraciones para cada tema
        for id_descripcion, descripcion_tema in enumerate(descripciones):
            # Combinación del prefacio y descripción del tema
            texto_entrada = f"{prefacio} {descripcion_tema}; ¿Podrias generarme SOLO UNA oración breve que utilize esas palabras y que suene como un tema coherente y descriptivo acorde a la pregunta? SOLO DESPLIEGAME LA ORACION EN TU RESPUESTA"
            
            # * inferencia por API de ChatGPT
            output = g4f.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                provider = g4f.Provider.You,
                messages = [{
                    "role": "user",
                    "content": texto_entrada
                }]
            )

            # Imprime la respuesta generada
            print(f'\tTematica {id_descripcion+1}:')
            print(f'{output}\n')

def main():
    SUMMARY_FILE = '../results/summaries/PreguntasAbiertasEncuestaPreliminar.json'
    CSV_FILE = "../csv/EncuestaPreliminar.csv"

    df_csv = pandas.read_csv(CSV_FILE, encoding='utf-8')
    df_pregunta_abiertas = df_csv.iloc[:, 7:12]
    nombre_preguntas_abiertas = df_pregunta_abiertas.columns.tolist()
    datos_parajson = []

    count = CountVectorizer(stop_words=getSpanishStopWords(),
                            max_df=0.1,
                            max_features=200)
    
    lda = LatentDirichletAllocation(n_components=2,
                                    random_state=123,
                                    learning_method='batch')

#    print("INICIO SUMMARY de temas recurrentes en preguntas abiertas de la Encuesta Preliminar")
#    for idx, nombre_pregunta in enumerate(nombre_preguntas_abiertas):
#        temas = getTemasDeRespuestas(idx, df_pregunta_abiertas.iloc[:, idx], count, lda, nombre_pregunta)
#        datos_parajson.append(temas)
#    with open(SUMMARY_FILE, 'w') as file:
#        json.dump(datos_parajson, file, indent=2)
#    print(f'\nSUMMARY {SUMMARY_FILE} generado con éxito')
    print("\nFIN SUMMARY de temas recurrentes en preguntas abiertas de la Encuesta Preliminar")
    
    print("INICIO DESCRIPCION COHERENTE de temas recurrentes con LLM")
    getTematicasCoherentesConLLM(SUMMARY_FILE)
    print("FIN DESCRIPCION COHERENTE de temas recurrentes con LLM")

if __name__ == '__main__':
    main()