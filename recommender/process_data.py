import re
import pandas as pd
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

okt = Okt()


def sub_special(text):
    return re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣0-9a-zA-Z]', '', text)


def tokenize(text):
    tokens = okt.morphs(text)
    return ' '.join(tokens)


def generate_tfidf_matrix(books):
    tfidf = TfidfVectorizer()
    books["description"] = books["description"].fillna('')
    books["reviews"] = books["reviews"].fillna('')
    books["description"] = books["description"].apply(sub_special)
    books["reviews"] = books["reviews"].apply(sub_special)
    books["description"] = books["description"].apply(tokenize)

    books["content"] = books["title"] + " " + books["author"] + " " + books["publisher"] + " " + books["description"] + " " + books["reviews"]

    tfidf_matrix = tfidf.fit_transform(books["content"])
    return tfidf_matrix, tfidf


def generate_cosine_sim(tfidf_matrix):
    return linear_kernel(tfidf_matrix, tfidf_matrix)


def generate_indices(books):
    return pd.Series(books.index, index=books['title']).drop_duplicates()


def prepare_data(file_path):
    books = pd.read_csv(file_path)
    tfidf_matrix, tfidf = generate_tfidf_matrix(books)
    cosine_sim = generate_cosine_sim(tfidf_matrix)
    indices = generate_indices(books)

    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf.get_feature_names_out())
    cosine_sim_df = pd.DataFrame(cosine_sim, index=books.index, columns=books.index)

    tfidf_df.to_pickle('tfidf_matrix.pkl')
    cosine_sim_df.to_pickle('cosine_sim.pkl')
    indices.to_pickle('indices.pkl')
    books.to_pickle('books.pkl')

    return tfidf_matrix, cosine_sim, indices, books


def load_data():
    tfidf_matrix = pd.read_pickle('tfidf_matrix.pkl')
    cosine_sim = pd.read_pickle('cosine_sim.pkl')
    indices = pd.read_pickle('indices.pkl')
    books = pd.read_pickle('books.pkl')

    return tfidf_matrix, cosine_sim, indices, books
