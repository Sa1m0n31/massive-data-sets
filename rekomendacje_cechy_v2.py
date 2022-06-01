import pandas as pd
from scipy.spatial import distance
from collections import Counter

data = pd.read_csv('./emzd/tags.csv', header=0, low_memory=False)


def get_number_of_unique_values(col_name):
    return data.groupby(by=col_name).first().shape[0]


def get_number_of_items_with_tag(tag, col_name):
    return data[data.tag == tag].groupby(by=col_name).first().shape[0]


def get_movies_with_tag(tag):
    return data[data.tag == tag].groupby(by='movieId').first().index.array


def get_all_movies():
    return data.groupby(by='movieId').first().index.array


def hash_tags(tag):
    return hash(tag) % 10000

def sort_arrays_by_length(arr1, arr2):
    if len(arr1) > len(arr2):
        return [arr1, arr2]
    else:
        return [arr2, arr1]

def get_similar_movies(user_id, k):
    user_tags = list(map(hash_tags, list(data[data.userId == user_id].tag)))
    # user_tags = list(data[data.userId == user_id].tag)
    similar_movies = Counter()

    for movie in get_all_movies():
        print(movie)
        movie_tags = list(map(hash_tags, list(data[data.movieId == movie].tag)))
        # movie_tags = list(data[data.movieId == movie].tag)

        sorted_arrays = sort_arrays_by_length(user_tags, movie_tags)
        longer_array = sorted_arrays[0]
        shorter_array = sorted_arrays[1]

        while len(shorter_array) < len(longer_array):
            shorter_array += list(map(lambda x : 0, shorter_array))

        shorter_array = shorter_array[:len(longer_array)]

        similar_movies[movie] = distance.cosine(shorter_array, longer_array)

    print(dict(sorted(similar_movies.items(), key=lambda item: item[1])))
    top_k_movies = list(dict(sorted(similar_movies.items(), key=lambda item: item[1])).keys())[:k]
    return top_k_movies


print(get_similar_movies(87, 100))