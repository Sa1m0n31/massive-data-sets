import pandas as pd
import numpy as np
import math
import sys
from random import randrange


def get_random_value_from_array(arr):
    return arr[randrange(len(arr))]


def get_test_set(matrix):
    # Przechodzimy po trackach i pobieramy ocene jesli track ma inne oceny
    for i in range(100):
        track_ratings = list(matrix.iloc[:, i])
        real_track_ratings = [i for i, e in enumerate(track_ratings) if e != 0]
        if len(real_track_ratings) > 1:
            random_rating_index = get_random_value_from_array(real_track_ratings)
            val = matrix.iloc[random_rating_index, i]
            new_test_set_item = {
                'user_index': random_rating_index, 'track_index': i, 'rating': val
            }
            test_set.append(new_test_set_item)
            matrix.iloc[random_rating_index, i] = 0


def normalize_matrix_to_rating_range(matrix):
    normalized_matrix = matrix

    max_value = matrix.max()
    min_value = matrix.min()

    non_zero_matrix = matrix[np.where(matrix != 0)]
    print(non_zero_matrix)

    q1 = np.quantile(non_zero_matrix, 0.2)
    q2 = np.quantile(non_zero_matrix, 0.4)
    q3 = np.quantile(non_zero_matrix, 0.6)
    q4 = np.quantile(non_zero_matrix, 0.8)

    print(q1, q2, q3, q4)

    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row, col] != 0:
                print(matrix[row, col])
            normalized_matrix[row, col] = round((5 - 1) * (matrix[row, col] - min_value) / (max_value - min_value))

    return normalized_matrix


def error(R, P, Q):
    err = 0
    for i in range(len(R)):
        for j in range(len(R[0])):
            if R[i][j] > 0:
                err = err + (R[i][j] - np.dot(P[i, :], Q[:, j])) ** 2
    return err


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


users_data = pd.read_csv('./emzd/projekt/data/kaggle_visible_evaluation_triplets.txt',
                         names=['user_id', 'track_id', 'play_count'], delim_whitespace=True)
test_set = []

# Pobieramy uzytkownikow z liczba odsluchanych piosenek > 10
v = users_data.user_id.value_counts()
data = users_data[users_data.user_id.isin(v.index[v.gt(50)])]
data = data.loc[:, (data != 0).any(axis=0)]

utility_matrix = pd.pivot_table(data, values='play_count', index='user_id', columns='track_id')
utility_matrix = utility_matrix.fillna(0)

# Wycinamy zbior testowy i zerujemy go
get_test_set(utility_matrix)

# Tworzymy oceny uzytkownikow na podstawie liczby odsluchan
R = normalize_matrix_to_rating_range(utility_matrix.to_numpy())
with np.printoptions(threshold=np.inf):
    print(R)


# SVD
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
    RMSE += (test_dict['rating'] - S[test_dict['user_index'], test_dict['track_index']]) ** 2

RMSE /= len(test_set)
RMSE = math.sqrt(RMSE)

# print('Wynik:')
# print(S)
# print(RMSE)