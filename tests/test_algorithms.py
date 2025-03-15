import pytest
import numpy as np
from algs import find_maxmin, find_minmax, nash_mixed, nash_clear

##############################################################

def test_maxmin():
    """Тест для функции поиска максимина"""
    ### Тест 1: Матрица с седловой точкой
    matrix1 = [
        [4, 0, 6, 2],
        [3, 8, 4, 4],
        [1, 2, 5, 6]
    ]
    assert find_maxmin(matrix1) == 3  # Минимум в строках: [0,3,1], максимин = 3

    ### Тест 2: Матрица 2x2
    matrix2 = [
        [3, 1],
        [2, 4]
    ]
    assert find_maxmin(matrix2) == 2  # Минимум в строках: [1,2], максимин = 2

    ### Тест 3: Матрица с отрицательными числами
    matrix3 = [
        [-1, -3],
        [0, -2]
    ]
    assert find_maxmin(matrix3) == -2  # Минимум в строках: [-3,-2], максимин = -2

##############################################################

def test_minmax():
    """Тест для функции поиска минимакса"""
    ### Тест 1: Матрица с седловой точкой
    matrix1 = [
        [4, 0, 6, 2],
        [3, 8, 4, 4],
        [1, 2, 5, 6]
    ]
    assert find_minmax(matrix1) == 4  # Максимум в столбцах: [4,8,6,6], минимакс = 4

    ### Тест 2: Матрица 2x2
    matrix2 = [
        [3, 1],
        [2, 4]
    ]
    assert find_minmax(matrix2) == 3  # Максимум в столбцах: [3,4], минимакс = 3

    ### Тест 3: Матрица с отрицательными числами
    matrix3 = [
        [-1, -3],
        [0, -2]
    ]
    assert find_minmax(matrix3) == -2  # Максимум в столбцах: [0,-2], минимакс = -2

##############################################################

def test_nash_clear():
    """Тест для функции поиска равновесия Нэша в чистых стратегиях"""
    ### Тест 1: Матрица с одним равновесием
    matrix1 = [
        [1, 2],
        [0, 3]
    ]
    equilibria1 = nash_clear(matrix1)
    assert len(equilibria1) == 1


    equilibria1_tuples = [(int(row), int(col)) for row, col in equilibria1]
    assert (1, 1) in equilibria1_tuples  

    ### Тест 2: Матрица без равновесий
    matrix2 = [
        [0, 1],
        [1, 0]
    ]
    equilibria2 = nash_clear(matrix2)
    assert len(equilibria2) == 0  # Нет равновесий

    ### Тест 3: Матрица с несколькими равновесиями
    matrix3 = [
        [1, 0],
        [0, 1]
    ]
    equilibria3 = nash_clear(matrix3)
    assert len(equilibria3) == 0

    ### Тест 4: "Дилемма заключенного"
    matrix4 = [
        [-1, -3],
        [0, -2]
    ]
    equilibria4 = nash_clear(matrix4)
    assert len(equilibria4) == 1
    equilibria4_tuples = [(int(row), int(col)) for row, col in equilibria4]
    assert (2, 2) in equilibria4_tuples  

##############################################################

def test_nash_mixed():
    """Тест для функции поиска равновесия Нэша в смешанных стратегиях"""
    ### Тест 1: Матрица с равновесием в смешанных стратегиях
    matrix1 = [
        [4, 1],
        [2, 3]
    ]
    result = nash_mixed(matrix1)
    assert result is not None
    p1, p2 = result
    assert len(p1) == 2 and len(p2) == 2
    # Проверяем, что вероятности в допустимом диапазоне
    assert all(0 <= p <= 1 for p in p1)
    assert all(0 <= p <= 1 for p in p2)
    # Проверяем, что сумма вероятностей равна 1
    assert abs(sum(p1) - 1.0) < 1e-10
    assert abs(sum(p2) - 1.0) < 1e-10

    ### Тест 2: Проверка на некорректный размер матрицы
    matrix2 = [
        [1, 2, 3],
        [4, 5, 6]
    ]
    result2 = nash_mixed(matrix2)
    assert result2 is None  # Для некорректного размера возвращаем None

    ### Тест 3: Матрица с нулевым определителем
    matrix3 = [
        [1, 1],
        [1, 1]
    ]
    result3 = nash_mixed(matrix3)
    assert result3 is None  # Для нулевого определителя возвращаем None

    ### Тест 4: Матрица с равновесием в смешанных стратегиях (1/3, 2/3)
    matrix4 = [
        [4, 0],
        [0, 2]
    ]
    result4 = nash_mixed(matrix4)
    assert result4 is not None
    p1, p2 = result4


    assert abs(p1[0] - 1/3) < 1e-10 and abs(p1[1] - 2/3) < 1e-10
    assert abs(p2[0] - 1/3) < 1e-10 and abs(p2[1] - 2/3) < 1e-10

##############################################################

def test_matrix_conversion():

    """Тест для проверки преобразования матриц для  разных вх данных"""
    matrix_list = [[1, 2], [3, 4]]
    matrix_np = np.array([[1, 2], [3, 4]])

    # список
    maxmin_list = find_maxmin(matrix_list)
    minmax_list = find_minmax(matrix_list)

    # numpy array
    maxmin_np = find_maxmin(matrix_np)
    minmax_np = find_minmax(matrix_np)

    #должны быть одинаковыми
    assert int(maxmin_list) == int(maxmin_np)
    assert int(minmax_list) == int(minmax_np) 

##############################################################