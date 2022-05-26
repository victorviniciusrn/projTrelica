import numpy as np

if __name__ == '__main__':
    n = int(input("Número de Barras:"))

    M = np.zeros((n, n))
    P = np.zeros((n, 1))

    for i in range(n):
        j = i + 1
        print("Para a {}ª barra, digite:".format(j))
        n1 = int(input("Coordenada N1:"))
        n2 = int(input("Coordenada N2:"))
        n3 = int(input("Coordenada N3:"))
        n4 = int(input("Coordenada N4:"))
        H = float(input("Comprimento horizontal:"))
        V = float(input("Comprimento vertical:"))
        L = (H ** 2 + V ** 2) ** (1 / 2)
        C = H / L
        S = V / L
        M[n1][j] += -C
        M[n2][j] += -S
        M[n3][j] += C
        M[n4][j] += S

    for i in range(n):
        j = i + 1
        P[j][1] = float(input("Digite a {}ª força externa".format(j)))

    M_inversa = np.linalg.inv(M)

    F = np.dot(M_inversa, P)

    print(F)



