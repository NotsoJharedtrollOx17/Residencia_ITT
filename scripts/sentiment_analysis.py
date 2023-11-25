import pandas
import json
import g4f
import nltk
from nltk.corpus import stopwords
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

def downloadStopWords():
    nltk.download('stopwords')
    print('STOPWORDS descargadas con éxito')

def getSpanishStopWords():
    stop_words = list(stopwords.words('spanish'))
    return stop_words

def getPalabrasRepresentativasRespuestas(idx ,df_respuestas, df_numeros_control, 
                                         count, lda, nombre_pregunta):
    n_palabras_tema = 6
    id_temas = []
    descripcion_temas = []
    numeros_control_respuestas_tema1 = []
    numeros_control_respuestas_tema2 = []

    # * obtencion de los temas recurrentes
    input_features = count.fit_transform(df_respuestas.values)
    input_features_name = count.get_feature_names_out()
    output = lda.fit_transform(input_features)

    # * despliegue de temas recurrentes
    print(f'{nombre_pregunta}\n')
    for tema_idx, tema in enumerate(lda.components_):
        palabras_tema = ' '.join([input_features_name[i]
                      for i in tema.argsort()\
                        [:-n_palabras_tema -1:-1]])
        if idx <= 9:
            label = f"p0{idx}_{tema_idx+1}"
            id_temas.append(label)
        else:
            label = f"p{idx}_{tema_idx+1}"
            id_temas.append(label)

        descripcion_temas.append(palabras_tema) 
        
        # * consulta de numeros de control por respuestas dentro de las tematicas
        tema = output[:, tema_idx].argsort()[::-1]
        print(f'Tema {tema_idx+1}: ')
        print(palabras_tema)
        for iter_idx, respuesta_idx in enumerate(tema):
            numero_control_respuesta = df_numeros_control[respuesta_idx]
            
            if tema_idx == 0:
                numeros_control_respuestas_tema1.append(numero_control_respuesta)
            if tema_idx == 1:
                numeros_control_respuestas_tema2.append(numero_control_respuesta)

    # * almancenamiento de los numeros de control por tema de respuesta
    numeros_control_por_tema = [numeros_control_respuestas_tema1, numeros_control_respuestas_tema2]

    summary = {
        'nombre_pregunta': nombre_pregunta,
        'id_tema': id_temas,
        'palabrasclave_tema': descripcion_temas,
        'descripcion_tema': '',
        'numero_control_respuestas' : numeros_control_por_tema,
    }
    
    json_summary = {
        'id_pregunta': idx,
        'summary': summary,
    }

    # * estructura json de temas recurrentes
    return json_summary

def getTemasDeRespuesta(df_csv, summary_file, count, lda):
    df_pregunta_abiertas = df_csv.iloc[:, 7:12]
    id_preguntas_abiertas = [8, 9, 10, 11, 12]
    nombre_preguntas_abiertas = df_pregunta_abiertas.columns.tolist()
    datos_parajson = []
    
    print("INICIO SUMMARY de temas recurrentes en preguntas abiertas de la Encuesta Preliminar")
    for idx, nombre_pregunta in enumerate(nombre_preguntas_abiertas):
       print(f"\nPREGUNTA NO. {id_preguntas_abiertas[idx]}")
       temas = getPalabrasRepresentativasRespuestas(id_preguntas_abiertas[idx], 
                                                    df_pregunta_abiertas.iloc[:, idx], 
                                                    df_csv['Número de control:'], 
                                                    count, lda, nombre_pregunta)
       datos_parajson.append(temas)
    with open(summary_file, 'w') as file:
        json.dump(datos_parajson, file, indent=2)
    print(f'\nSUMMARY {summary_file} generado con éxito')

def getDescripcionesCoherentesTemasRespuesta(summary_file):
    with open(summary_file, 'r') as file:
        data = json.load(file)
    
    # * PRIMER CICLO: Itera sobre los datos leidos del JSON
    for id_pregunta, pregunta in enumerate(data):
        descripciones = []
        nombre_pregunta = pregunta['summary']['nombre_pregunta']
        palabrasclave_tema = pregunta['summary']['palabrasclave_tema']

        # Prefacio
        prefacio = f"En relación a la pregunta: {nombre_pregunta}, las respuestas obtenidas se analizaron con un modelo NLP que detectó una de las siguientes tematicas en forma de una serie de palabras: "

        print(f'\nPregunta {id_pregunta+1}: {nombre_pregunta}')
        
        # * SEGUNDO CICLO: Genera oraciones para cada tema
        for id_palabras, palabrasclave in enumerate(palabrasclave_tema):
            # Combinación del prefacio y descripción del tema
            texto_entrada = f"{prefacio} {palabrasclave}; Generarme SOLO UNA oración breve que utilize esas palabras y que suene como un tema coherente y descriptivo acorde a la pregunta. SOLO DESPLEGA ESA ORACION Y ASEGURATE DE NO DESPLEGARME LA RESPUESTA TIPO: 'Claro, aquí tienes la oración breve que utiliza las palabras mencionadas y que suena como un tema coherente y descriptivo:'"
            
            # * inferencia por API de ChatGPT
            output = g4f.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                provider = g4f.Provider.You,
                messages = [{
                    "role": "user",
                    "content": texto_entrada
                }]
            )

            descripciones.append(output)

            # Imprime la respuesta generada
            print(f'\tTematica {id_palabras+1}:')
            print(f'{output}')
        
        # Actualiza la clave 'descripcion_tema' en el JSON directamente
        data[id_pregunta]['summary']['descripcion_tema'] = descripciones
                        
    # Guarda los datos actualizados en el JSON
    with open(summary_file, 'w') as file:
        json.dump(data, file, indent=4)
    
    print(f'\nSUMMARY {summary_file} actualizado con éxito')

def main():
    SUMMARY_FILE = '../results/summaries/PreguntasAbiertasEncuestaPreliminar.json'
    CSV_FILE = "../csv/EncuestaPreliminar.csv"

    df_csv = pandas.read_csv(CSV_FILE, encoding='utf-8')

    downloadStopWords()

    count = CountVectorizer(stop_words=getSpanishStopWords(),
                            max_df=0.1,
                            max_features=200)
    
    lda = LatentDirichletAllocation(n_components=2,
                                    random_state=123,
                                    learning_method='batch')

    print("\nFIN SUMMARY de temas recurrentes en preguntas abiertas de la Encuesta Preliminar")
    getTemasDeRespuesta(df_csv, SUMMARY_FILE, count, lda)
    print("INICIO DESCRIPCION COHERENTE de temas recurrentes con LLM")
    getDescripcionesCoherentesTemasRespuesta(SUMMARY_FILE)
    print("FIN DESCRIPCION COHERENTE de temas recurrentes con LLM")

if __name__ == '__main__':
    main()