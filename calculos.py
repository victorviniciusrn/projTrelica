from sympy import *

if __name__ == '__main__':
    f = Symbol('f')
    Re = 128000
    relative_roughness = 0.0013
    eq = f ** (-0.5) + 2 * log(relative_roughness / 3.7 + 2.51 / (Re * (f) ** (0.5)), 10)
    r = nsolve(eq, f, 0.025, maxsteps=1000)
    print(r)
