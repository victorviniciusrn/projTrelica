import pandas as pd
import numpy as np


def calculate_angles(dados):
    L = np.zeros(len(dados.index))  # comprimento das barras
    C_theta = np.zeros(len(dados.index))  # cosseno
    S_theta = np.zeros(len(dados.index))  # seno
    C_alpha = np.zeros(len(dados.index))
    S_alpha = np.zeros(len(dados.index))

    for j, row in dados.iterrows():
        # calculo do Lj
        L[j] = (row['Xj'] ** 2 + row['Yj'] ** 2 + row['Zj'] ** 2) ** (1 / 2)

        # calculo da projeção da barra no plano XZ
        proj_xz = (row['Xj'] ** 2 + row['Zj'] ** 2) ** (1 / 2)
        # calculo do C_theta_j
        C_theta[j] = proj_xz / L[j]
        # calculo de S_theta_j
        S_theta[j] = (1 - C_theta[j] ** 2) ** (1 / 2)
        # calculo de C_alpha_j
        C_alpha[j] = proj_xz / row['Zj']
        # calculo de S_alpha_j
        S_alpha[j] = proj_xz / row['Xj']

    return L, C_theta, S_theta, C_alpha, S_alpha


def define_matrix(dados, len, C_theta, S_theta, C_alpha, S_alpha):
    A = np.zeros((len, len), dtype=np.float64)
    for j, row in dados.iterrows():
        if C_theta[j] * S_alpha[j] != 0:
            if row['N1'] != 0:
                A[int(row['N1']) - 1][j] = -C_theta[j] * S_alpha[j]
            if row['N3'] != 0:
                A[int(row['N3']) - 1][j] = C_theta[j] * S_alpha[j]
        else:
            if row['N1'] != 0:
                A[int(row['N1']) - 1][j] = 0
            if row['N3'] != 0:
                A[int(row['N3']) - 1][j] = 0

        if C_theta[j] * C_alpha[j] != 0:
            if row['N5'] != 0:
                A[int(row['N5']) - 1][j] = -C_theta[j] * C_alpha[j]
            if row['N6'] != 0:
                A[int(row['N6']) - 1][j] = C_theta[j] * C_alpha[j]
        else:
            if row['N5'] != 0:
                A[int(row['N5']) - 1][j] = 0
            if row['N6'] != 0:
                A[int(row['N6']) - 1][j] = 0

        if S_theta[j] != 0:
            if row['N2'] != 0:
                A[int(row['N2']) - 1][j] = -S_theta[j]
            if row['N4'] != 0:
                A[int(row['N4']) - 1][j] = S_theta[j]
        else:
            if row['N2'] != 0:
                A[int(row['N2']) - 1][j] = 0
            if row['N4'] != 0:
                A[int(row['N4']) - 1][j] = 0
    return A


def calculate_forces(A, V):
    det = np.linalg.det(A)
    inversa = np.linalg.inv(A)
    V_t = np.zeros((len(V), 1), dtype=np.float64)
    for j in range(len(V)):
        V_t[j][0] = V[j]
    F = np.dot(inversa, V_t)
    return F


if __name__ == '__main__':
    dados = pd.read_excel('dados.xlsx')
    L, C_theta, S_theta, C_alpha, S_alpha = calculate_angles(dados)
    A = define_matrix(dados, len(dados.index), C_theta, S_theta, C_alpha, S_alpha)
    array_dados = dados.to_numpy()
    V = array_dados[:, 10]

    F = calculate_forces(A, V)
    print(F)
