import pandas as pd
import math

data = pd.read_csv('./emzd/tags.csv', header=0, low_memory=False)


def get_number_of_unique_values(col_name):
    return data.groupby(by=col_name).first().shape[0]


def get_number_of_items_with_tag(tag, col_name):
    return data[data.tag == tag].groupby(by=col_name).first().shape[0]


def get_movies_with_tag(tag):
    return data[data.tag == tag].groupby(by='movieId').first().index.array


def tf_idf(tag, col_name, col_value):
    all_tags_for_item = data[data[col_name] == col_value].shape[0]
    tag_occurences_in_item = data[(data[col_name] == col_value) & (data.tag == tag)].shape[0]

    number_of_all_items = get_number_of_unique_values(col_name)
    number_of_items_with_tag = get_number_of_items_with_tag(tag, col_name)

    tf = tag_occurences_in_item / all_tags_for_item
    idf = math.log(number_of_all_items / number_of_items_with_tag)

    return tf * idf


def get_similar_movies(userId, k, support):
    user_tags = data[data.userId == userId].tag
    user_tags_tf_idf = {}
    movies_tags_tf_idf = {}
    for tag in user_tags:
        # Liczymy TF-IDF dla tagow uzytkownika
        current_tag_tf_idf = tf_idf(tag, 'userId', userId)
        movies_tf_idf_for_current_tag = {}

        # Jesli TF-IDF tego tagu u uzytkownika jest > support to szukaj TF-IDF tego tagu dla wszystkich filmow
        if current_tag_tf_idf > support:
            user_tags_tf_idf[tag] = current_tag_tf_idf
            for movie in get_movies_with_tag(tag):
                current_movie_tf_idf = tf_idf(tag, 'movieId', movie)
                # Jesli TF-IDF tego tagu dla danego filmu jest > support to zapisz
                if current_movie_tf_idf > support:
                    movies_tf_idf_for_current_tag[movie] = current_movie_tf_idf

        # Dodajemy informacje jakie filmy maja duzy TF-IDF dla danego tagu
        movies_tags_tf_idf[tag] = movies_tf_idf_for_current_tag

    # Liczymy iloczyn TF-IDF tagow wsrod wszystkich tagow usera i TF-IDF tagow dla danego filmu
    similar_movies = {}
    for user_tag, user_tf_idf in user_tags_tf_idf.items():
        for movie_id, movie_tf_idf in movies_tags_tf_idf[user_tag].items():
            val = user_tf_idf * movie_tf_idf
            similar_movies[movie_id] = val

    most_similar_movies = list(dict(sorted(similar_movies.items(), key=lambda item: item[1], reverse=True)).keys())[:k]
    return most_similar_movies


print(get_similar_movies(87, 100, 0.3))
# odleglosc cosinusowa miedzy filmem a userem