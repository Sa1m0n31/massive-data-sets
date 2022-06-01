import pandas as pd
import random
import math

data = pd.read_csv('./emzd/tags.csv', header=0, low_memory=False)


def get_number_of_unique_values(col_name):
    return data.groupby(by=col_name).first().shape[0]


def get_number_of_items_with_tag(tag, col_name):
    return data[data.tag == tag].groupby(by=col_name).first().shape[0]


def get_movies_with_tag(tag):
    return data[data.tag == tag].groupby(by='movieId').first().index.array


def get_all_movies():
    return data.groupby(by='movieId').first().index.array[:100]


def get_movie_tags(movie):
    return list(set(list(data[data.movieId == movie].tag)))


def tf_idf(tag, col_name, col_value):
    all_tags_for_item = data[data[col_name] == col_value].shape[0]
    tag_occurences_in_item = data[(data[col_name] == col_value) & (data.tag == tag)].shape[0]

    number_of_all_items = get_number_of_unique_values(col_name)
    number_of_items_with_tag = get_number_of_items_with_tag(tag, col_name)

    tf = tag_occurences_in_item / all_tags_for_item
    idf = math.log(number_of_all_items / number_of_items_with_tag)

    return tf * idf


def jaccarda_compare(set1, set2):
    doc_sum = set1.union(set2)
    doc_intersection = set1.intersection(set2)
    return len(doc_intersection) / len(doc_sum)


def get_similar_movies(userId, k):
    user_tags = data[data.userId == userId].tag
    user_tags_tf_idf = {}
    movie_tags_tf_idf = {}
    all_similarities = {}
    all_movies_profiles = []

    # Liczymy TF-IDF dla tagow uzytkownika
    for tag in list(set(user_tags)):
        user_tags_tf_idf[tag] = tf_idf(tag, 'userId', userId)

    # Tworzymy wektor reprezentujacy uzytkownika
    user_tags = list(user_tags_tf_idf.keys())
    user_tags_probabilities = list(user_tags_tf_idf.values())
    user_profile = random.choices(user_tags, weights=user_tags_probabilities, k=100)

    # Iterujemy po wszystkich tagach uzytkownika
    for user_tag in user_tags:
        for movie in get_movies_with_tag(user_tag):
            # Tworzymy wektor reprezentujacy film
            movie_tags = get_movie_tags(movie)

            # Liczymy podobienstwo miedzy profilami jako index jaccarda
            all_similarities[movie] = jaccarda_compare(set(user_tags), set(movie_tags))

    return list(dict(sorted(all_similarities.items(), key=lambda item: item[1], reverse=True)).keys())[:k]


print(get_similar_movies(19, 100))
print(get_similar_movies(3, 10))