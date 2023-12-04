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


books["description"] = books["description"].fillna('')
books["reviews"] = books["reviews"].fillna('')
books["description"] = books["description"].apply(sub_special)
books["reviews"] = books["reviews"].apply(sub_special)
books["description"] = books["description"].apply(tokenize)

books["content"] = books["title"] + " " + books["author"] + " " + books["publisher"] + " " + books[
    "description"] + " " + books["reviews"]

tfidf_matrix = tfidf.fit_transform(books["content"])

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

indices = pd.Series(books.index, index=books['title']).drop_duplicates()


def recommend(title, cosine_sim=cosine_sim):
    recomm = []
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:11]

    movie_indices = [i[0] for i in sim_scores]

    for i in range(10):
        recomm.append(books['title'][movie_indices[i]])

    print('< 도서 추천 >')
    for i in range(10):
        print(str(i + 1) + ' : ' + recomm[i])


recommend('황금종이 1')
