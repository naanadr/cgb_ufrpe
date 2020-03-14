from mathcgb import MatrizOperations, SpaceOperations


def letter_a():
    print('Letra A - Multiplicação de matrizes')
    print('[1.5  2.5  3.5]\t   \t[7.5    8.5]')
    print('[4.5  5.5  6.5]\t * \t[9.5   10.5]')
    print('               \t   \t[11.5  12.5]')
    value_a = [
        [1.5, 2.5, 3.5],
        [4.5, 5.5, 6.5]
    ]
    value_b = [
        [7.5, 8.5],
        [9.5, 10.5],
        [11.5, 12.5]
    ]
    math = MatrizOperations(value_a, value_b)
    print('Resultado = ', math.multiplication())


def letter_b():
    pass


def letter_c():
    print('Letra C - Produto escalar de dois vetores 3D')
    print('\t(3.5, 1.5, 2) * (1.0, 2.0, 1.5)')
    vetor_a = [3.5, 1.5, 2]
    vetor_b = [1.0, 2.0, 1.5]
    op = SpaceOperations(vetor_a, vetor_b)
    print('Resultado = ', op.produto_escalar())


def letter_d():
    print('Letra D - Produto vetorial de dois vetores 3D')
    print('\t(3.5, 1.5, 2) X (1.0, 2.0, 1.5)')
    vetor_a = [3.5, 1.5, 2]
    vetor_b = [1.0, 2.0, 1.5]
    op = SpaceOperations(vetor_a, vetor_b)
    print('Resultado = ', op.produto_vetorial())


def letter_e():
    print('Letra E - Norma de um vetor 3D')
    print('\t ||(3.5, 1.5, 2.0)||')
    op = SpaceOperations()
    print('Resultado = ', op.normal([3.5, 1.5, 2.0]))


def letter_f():
    pass


def letter_g():
    pass


def letter_h():
    pass
