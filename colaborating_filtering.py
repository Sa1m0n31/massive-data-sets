import pandas as pd
import numpy as np
from scipy import stats
import math
from random import randrange


def get_average_rating(matrix):
    ratings = []

    for ind in index:
        for col in columns:
            v = matrix.loc[ind, col]
            if v != 0:
                ratings.append(v)

    if len(ratings):
        return sum(ratings) / len(ratings)
    else:
        return 0


def get_average_rating_for_user(user, matrix):
    all_user_ratings = matrix.loc[user]
    user_non_zero_ratings = []

    for rating in all_user_ratings:
        if rating != 0:
            user_non_zero_ratings.append(rating)

    if len(user_non_zero_ratings) != 0:
        return sum(user_non_zero_ratings) / len(user_non_zero_ratings)
    else:
        return 0


def get_average_rating_for_movie(movie, matrix):
    all_movie_ratings = matrix.loc[:, movie]
    movie_non_zero_ratings = []

    for rating in all_movie_ratings:
        if rating != 0:
            movie_non_zero_ratings.append(rating)

    if len(movie_non_zero_ratings) != 0:
        return sum(movie_non_zero_ratings) / len(movie_non_zero_ratings)
    else:
        return 0


def calculate_bias(user, movie):
    user_average = get_average_rating_for_user(user, utility_matrix)
    movie_average = get_average_rating_for_movie(movie, utility_matrix)

    return user_average + movie_average - average_rating


# Liczymy wspolczynnik korelacji Pearsona miedzy dwoma filmami
def calculate_similarity(matrix):
    i = 0
    for ind in columns:
        for col in columns:
            c = stats.pearsonr(matrix.loc[:, ind], matrix.loc[:, col])[0]
            corelation_matrix.loc[ind, col] = c
            i += 1


def get_similarity(movie_1, movie_2):
    return corelation_matrix.loc[movie_1, movie_2]


def get_user_rating(user, movie):
    return utility_matrix.loc[user, movie]


# Znajdz filmy najblizsze do movie ocenione przez uzytkownika user
def get_similar_movies(movie, user, k):
    user_movies = utility_matrix.loc[user]
    movies_rated_by_user = []

    # Zbieramy filmy ocenione przez uzytkownika
    for movie_id, movie_rating in user_movies.items():
        if movie_rating != 0:
            movies_rated_by_user.append(movie_id)

    # Wybieramy z nich k filmow najbardziej podobnych do danego filmu
    movie_corelations = corelation_matrix.filter(items=movies_rated_by_user).loc[movie]
    knn = movie_corelations.sort_values(ascending=False).head(k)
    return list(knn.index.array)


# Szacowanie oceny produktu i przez uzytkownika x
def estimate_rating(movie, user):
    similar_movies = get_similar_movies(movie, user, 10)
    bias = calculate_bias(user, movie)

    numerator, denominator = 0, 0

    for mv in similar_movies:
        sim = get_similarity(movie, mv)
        rat = get_user_rating(user, movie)
        b = calculate_bias(user, mv)

        numerator += sim * (rat - b)
        denominator += abs(sim)

    if denominator != 0:
        return bias + (numerator / denominator)
    else:
        return 0


def normalize_matrix_to_rating_range(matrix):
    normalized_matrix = matrix

    matrix_cols = [int(c) for c in matrix.columns]

    max_value = matrix.to_numpy().max()
    min_value = matrix.to_numpy().min()

    for row in matrix.index:
        for col in matrix_cols:
            if [row, col] not in fixed_values_indexes:
                normalized_matrix.loc[row, col] = (5 - 0) * (matrix.loc[row, col] - min_value) / (max_value - min_value)

    return normalized_matrix


def get_random_value_from_array(arr):
    return arr[randrange(len(arr))]


def get_test_set(matrix):
    # Przechodzimy po filmach i zerujemy ocene jesli film ma inne oceny
    for i in range(100):
        movie_ratings = list(matrix.iloc[:, i])
        real_movie_ratings = [i for i, e in enumerate(movie_ratings) if e != 0]
        if len(real_movie_ratings) > 1:
            random_rating_index = get_random_value_from_array(real_movie_ratings)
            val = matrix.iloc[random_rating_index, i]
            new_test_set_item = {
                'user_index': random_rating_index, 'movie_index': i, 'rating': val
            }
            test_set.append(new_test_set_item)
            matrix.iloc[random_rating_index, i] = 0


# Wczytujemy dane
all_data = pd.read_csv('./emzd/netflix.txt', names=['movie', 'user', 'rating'])
test_set = []

# Pobieramy uzytkownikow z liczba ocenionych filmow > 10
v = all_data.user.value_counts()
data = all_data[all_data.user.isin(v.index[v.gt(10)])]
data = data.loc[:, (data != 0).any(axis=0)]

utility_matrix = pd.pivot_table(data, values='rating', index='user', columns='movie')
utility_matrix = utility_matrix.fillna(0)

# Wycinamy zbior testowy
get_test_set(utility_matrix)

# Zerujemy elementy, ktore pobralismy do zbioru testowego
for dic in test_set:
    utility_matrix.iloc[dic['user_index'], dic['movie_index']] = 0

columns = [int(c) for c in utility_matrix.columns]
index = [int(i) for i in utility_matrix.index]

corelation_matrix = pd.DataFrame(index=columns, columns=columns)

# Obliczamy srednia wszystkich ocen
average_rating = get_average_rating(utility_matrix)

# Obliczamy podobienstwo miedzy produktami jako wspolczynnik korelacji Pearsona
calculate_similarity(utility_matrix)

# Szacujemy oceny dla filmow nieocenionych
current_user = 0

result_matrix = utility_matrix.copy()
fixed_values_indexes = []

for user, matrix_index in zip(index, utility_matrix.index):
    for movie in columns:
        rating = utility_matrix.loc[user, movie]
        if rating == 0:
            e = estimate_rating(movie, user)
            result_matrix.loc[user, movie] = e
        else:
            fixed_values_indexes.append([matrix_index, movie])

    current_user += 1

# Normalizacja wartosci do przedzialu 0-5
result_matrix = normalize_matrix_to_rating_range(result_matrix)

# Test
RMSE = 0
for test_dict in test_set:
    RMSE += (test_dict['rating'] - result_matrix.iloc[test_dict['user_index'], test_dict['movie_index']]) ** 2

RMSE /= len(test_set)
RMSE = math.sqrt(RMSE)
print(RMSE)

print(result_matrix)
result_matrix.to_csv('training_result.csv')