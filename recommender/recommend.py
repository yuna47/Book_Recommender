import re
import pandas as pd
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

books = pd.read_csv('../crawler/books_.csv')
okt = Okt()
tfidf = TfidfVectorizer()


def sub_special(text):
    return re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣0-9a-zA-Z]', '', text)


def tokenize(text):
    tokens = okt.morphs(text)
    return ' '.join(tokens)


books["description"] = books["description"].apply(sub_special)
books["review"] = books["review"].apply(sub_special)
books["description"] = books["description"].apply(tokenize)

description_tfidf_matrix = tfidf.fit_transform(books["description"])
review_tfidf_matrix = tfidf.fit_transform(books["review"])
print("description")
print(description_tfidf_matrix.shape)
print()
print("review")
print(review_tfidf_matrix.shape)

cosine_sim = linear_kernel(description_tfidf_matrix, review_tfidf_matrix)
