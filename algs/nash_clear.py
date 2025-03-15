# Поиск равновесия по Нэшу в чистых стратегиях

import numpy as np
from algs.maximin import find_maxmin
from algs.minimax import find_minmax

def nash_clear(matrix):
    """Поиск равновесий по Нэшу в чистых стратегиях

    Args:
        matrix (list): матрица в виде списка списков

    Returns:
        list: Список с кортежами из чистых стратегий, если их нет вернет пустой список 
    """
    # Преобразуем входную матрицу в numpy array для удобства вычислений
    matrix = np.array(matrix)
    
    # Находим максимальный элемент среди минимальных
    a_max_mins = find_maxmin(matrix)

    # Находим минимальный элемент среди максимальных
    b_min_maxs = find_minmax(matrix)

    #print("Платежная матрица:")
    #print(matrix)
    #print(f"a = {a_max_mins}")
    #print(f"b = {b_min_maxs}")

    strategies = []
    if (a_max_mins == b_min_maxs):
        #print(f"Равновесие по Нэшу среди чистых стратегий найдено: {a_max_mins}")
        strateg_idx = np.where(matrix == a_max_mins) # находим индексы где значения равны равновесию
        for i in range(len(strateg_idx[0])):  # Проходим по длине массива индексов
            row = strateg_idx[0][i]  
            col = strateg_idx[1][i]  
            strategies.append((row+1, col+1))  
    print(strategies)
    return strategies