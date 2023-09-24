import pandas
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

def main():
    CSV_FILE = "../csv/EncuestaPreliminar.csv"
    df_csv = pandas.read_csv(CSV_FILE, encoding='utf-8')


if __name__ == '__main__':
    main()