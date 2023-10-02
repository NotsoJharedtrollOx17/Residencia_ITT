import pandas
import json
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

    print("INICIO SUMMARY de temas recurrentes en preguntas abiertas de la Encuesta Preliminar")
    
    for idx, nombre_pregunta in enumerate(nombre_preguntas_abiertas):
        temas = getTemasDeRespuestas(idx, df_pregunta_abiertas.iloc[:, idx], count, lda, nombre_pregunta, SUMMARY_FILE)
        datos_parajson.append(temas)
    
    with open(SUMMARY_FILE, 'w') as file:
        json.dump(datos_parajson, file, indent=2)
    
    print(f'\nSUMMARY {SUMMARY_FILE} generado con éxito')
    print("\nFIN SUMMARY de temas recurrentes en preguntas abiertas de la Encuesta Preliminar")

if __name__ == '__main__':
    main()