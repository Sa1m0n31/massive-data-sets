import numpy as np
import pandas as pd
import math
from random import randrange


def error(R, P, Q):
    err = 0
    for i in range(len(R)):
        for j in range(len(R[0])):
            if R[i][j] > 0:
                err = err + (R[i][j] - np.dot(P[i, :], Q[:, j])) ** 2
    return err


def get_random_value_from_array(arr):
    return arr[randrange(len(arr))]


def normalize_matrix_to_rating_range(matrix):
    normalized_matrix = matrix

    max_value = matrix.max()
    min_value = matrix.min()

    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            normalized_matrix[row, col] = round((5 - 1) * (matrix[row, col] - min_value) / (max_value - min_value))

    return normalized_matrix


def get_test_set(matrix):
    # Przechodzimy po filmach i pobieramy ocene jesli film ma inne oceny
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


def matrix_factorization_with_regularisation(R, P, Q):
    steps = 10000
    alpha = 0.002
    beta = 0.02
    for st in range(steps):
        for i in range(len(R)):
            for j in range(len(R[0])):
                if R[i][j] > 0:
                    for m in range(len(P[0])):
                        Jij = -2 * (R[i][j] - np.dot(P[i, :], Q[:, j]))
                        P[i][m] = P[i][m] - alpha * (Jij * Q[m][j] + beta * P[i][m])
                        Q[m][j] = Q[m][j] - alpha * (Jij * P[i][m] + beta * Q[m][j])

        e = error(R, P, Q)
        if e < 0.1:
            break
    return P, Q


def matrix_factorization_without_regularisation(R, P, Q):
    steps = 10000
    for st in range(steps):
        for i in range(len(R)):
            for j in range(len(R[0])):
                if R[i][j] > 0:
                    for m in range(len(P[0])):
                        Jij = -2 * (R[i][j] - np.dot(P[i, :], Q[:, j]))
                        P[i][m] = P[i][m] - (Jij * Q[m][j] + P[i][m])
                        Q[m][j] = Q[m][j] - (Jij * P[i][m] + Q[m][j])

        e = error(R, P, Q)
        if e < 0.1:
            break
    return P, Q


# Wczytujemy dane
all_data = pd.read_csv('./emzd/netflix.txt', names=['movie', 'user', 'rating'])
test_set = []

# Pobieramy uzytkownikow z liczba ocenionych filmow > 10
v = all_data.user.value_counts()
data = all_data[all_data.user.isin(v.index[v.gt(12)])]
data = data.loc[:, (data != 0).any(axis=0)]

utility_matrix = pd.pivot_table(data, values='rating', index='user', columns='movie')
utility_matrix = utility_matrix.fillna(0)

utility_matrix = utility_matrix / 5

# Wycinamy zbior testowy i zerujemy go
get_test_set(utility_matrix)

# SVD
R = utility_matrix.to_numpy()
N = len(R)
M = len(R[0])
K = 2
P = np.random.rand(N, K)
Q = np.random.rand(K, M)

P1, Q1 = matrix_factorization_with_regularisation(R, P, Q)

S = np.dot(P1, Q1) * 5

result_matrix = normalize_matrix_to_rating_range(S)

# Obliczanie bledu
RMSE = 0
for test_dict in test_set:
    RMSE += (test_dict['rating'] - S[test_dict['user_index'], test_dict['movie_index']]) ** 2

RMSE /= len(test_set)
RMSE = math.sqrt(RMSE)

print('Wynik:')
print(S)
print(RMSE)