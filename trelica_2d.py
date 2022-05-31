import pandas as pd
import numpy as np

def calculate_angles(dados):
    #calculo dos senos e cossenos necessários
    L = np.zeros(len(dados.index))  # comprimento das barras
    C = np.zeros(len(dados.index))  # cosseno
    S = np.zeros(len(dados.index))  # seno

    for j, row in dados.iterrows():
        # calculo do Lj
        L[j] = (row['Hj'] * row['Hj'] + row['Vj'] * row['Vj']) ** (1 / 2)
        # calculo do Cj
        C[j] = row['Hj'] / L[j]
        # calculo de Sj
        S[j] = row['Vj'] / L[j]

    return L, C, S


def define_matrix(dados, len, C, S):
    # definição da matriz A
    A = np.zeros((len, len), dtype=np.float64)
    for j, row in dados.iterrows():
        if C[j] != 0:
            if row['N1'] != 0:
                A[int(row['N1']) - 1][j] = -C[j]
            if row['N3'] != 0:
                A[int(row['N3']) - 1][j] = C[j]
        else:
            if row['N1'] != 0:
                A[int(row['N1']) - 1][j] = 0
            if row['N3'] != 0:
                A[int(row['N3']) - 1][j] = 0
        if S[j] != 0:
            if row['N2'] != 0:
                A[int(row['N2']) - 1][j] = -S[j]
            if row['N4'] != 0:
                A[int(row['N4']) - 1][j] = S[j]
        else:
            if row['N2'] != 0:
                A[int(row['N2']) - 1][j] = 0
            if row['N4'] != 0:
                A[int(row['N4']) - 1][j] = 0

    return A


def calculate_forces(A, V):
    # resolução do sistema
    det = np.linalg.det(A)
    inversa = np.linalg.inv(A)
    V_t = np.zeros((len(V), 1), dtype=np.float64)
    for j in range(len(V)):
        V_t[j][0] = V[j]
    F = np.dot(inversa, V_t)
    return F


if __name__ == '__main__':
    # ler dados do arquivo excel com modelo segundo o dados.xlsx ou dados_2.xlsx
    dados = pd.read_excel('dados_2.xlsx')
    L, C, S = calculate_angles(dados)
    A = define_matrix(dados, len(dados.index), C, S)
    array_dados = dados.to_numpy()
    V = array_dados[:, 7]

    F = calculate_forces(A, V)
    print(F)

