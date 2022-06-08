import numpy as np
import pandas as pd


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


test_data = pd.read_csv('./emzd/netflix.txt', names=['movie', 'user', 'rating']).sample(frac=0.001)

# zamiast randoma wybrac tych userow, ktorzy maja duzo ocen > 20

utility_matrix = pd.pivot_table(test_data, values='rating', index='user', columns='movie')
utility_matrix = utility_matrix.fillna(0)

R = utility_matrix.to_numpy()

#
N = len(R)
M = len(R[0])
K = 2
P = np.random.rand(N, K)
Q = np.random.rand(K, M)


P1, Q1 = matrix_factorization_with_regularisation(R, P, Q)

S = np.dot(P1, Q1)
null_indexes = np.where(np.array(R) == 0)

# Obliczanie bledu
nindx = zip(null_indexes[0], null_indexes[1])
err = 0.0
for ni in range(len(R)):
    for nj in range(len(R[0])):
        if (ni, nj) not in nindx:
            err += (R[ni][nj] - S[ni][nj]) ** 2


print('Wynik:')
print(S)