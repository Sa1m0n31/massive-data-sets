import pandas as pd
import numpy as np
from scipy import stats

data = pd.read_csv('./emzd/netflix.txt', names=['movie', 'user', 'rating'])
utility_matrix = pd.pivot_table(data, values='rating', index='user', columns='movie')
utility_matrix = utility_matrix.fillna(0)

columns = [int(c) for c in utility_matrix.columns]
index = [int(i) for i in utility_matrix.index]

coleration_matrix = pd.DataFrame(index=columns, columns=columns)

# Liczymy wspolczynnik korelacji Pearsona miedzy dwoma filmami
for ind in columns:
    for col in columns:
        c = stats.pearsonr(utility_matrix.loc[:, ind], utility_matrix.loc[:, col])[0]
        coleration_matrix.loc[ind, col] = c


# Znajdz filmy najblizsze do movie ocenione przez uzytkownika user
def knn_for_movie(movie, user):
    print(data[data.user == user])


knn_for_movie(1, 769643)