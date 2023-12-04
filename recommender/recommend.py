from process_data import prepare_data, load_data


def prepare():
    try:
        tfidf_matrix, cosine_sim, indices, books = load_data()
    except FileNotFoundError:
        print("Preparing data...")
        tfidf_matrix, cosine_sim, indices, books = prepare_data('../crawler/books.csv')
    return cosine_sim, indices, books


def recommend(title):
    cosine_sim, indices, books = prepare()
    recomm = []
    idx = indices[title]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:11]

    movie_indices = [i[0] for i in sim_scores]

    for i in range(10):
        recomm.append(books['title'][movie_indices[i]])

    print('< 『' + title + '』 관련 도서 추천 >')
    for i in range(10):
        print(str(i + 1) + ' : ' + recomm[i])


if __name__ == "__main__":
    recommend('리팩터링')
