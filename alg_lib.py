import numpy as np

def maxmin(matrix):
    max_in_rows = np.min(matrix, axis=1)
    return max(max_in_rows)

def minmax(matrix):
    max_in_rows = np.max(matrix, axis=0)
    return min(max_in_rows)

def nash_clear(matrix):
    """Поиск равновесий по нешу в чистых стратегиях

    Args:
        matrix (np.array): матрица

    Returns:
        list: Список с кортежами из чистых стратегий, если их нет вернет пустой список 
    """
    # Находим максимальный элемент среди минимальных
    a_max_mins = maxmin(matrix)

    # Находим минимальный элемент среди максимальных
    b_min_maxs = minmax(matrix)

    #print("Платежная матрица:")
    #print(matrix)
    #print(f"a = {a_max_mins}")
    #print(f"b = {b_min_maxs}")

    strategies = []
    if (a_max_mins == b_min_maxs):
        #print(f"Равновесие по Нэшу среди чистых стратегий найдено: {a_max_mins}")
        strateg_idx = np.where(matrix == a_max_mins) # находим индексы где значения равны равновесию
        for i in range(len(strateg_idx[0])):  # Проходим по длине массива индексов
            row = strateg_idx[0][i]  # Индекс строки
            col = strateg_idx[1][i]  # Индекс столбца
            strategies.append((row+1, col+1)) # добавляем единицу так как индексы с начинаются с нуля
    
    return strategies

def nash_mixed(matrix):
    """Поиск равновесий по нешу в смешанных стратегиях 2x2

    Args:
        matrix (np.array): матрица

    Returns:
        list: список с 2 картежами:
            1 - вероятности первого игрока
            2 - вероятности второго игрока
    """
    # создаем вектора - полный набор вероятностей выбора стратегий (должны в сумме быть равны единице)
    p = np.zeros(2) # для первого игрока
    q = np.zeros(2) # для второго игрока

    # ищем оптимальную смешананую стратегию 
    D = (matrix[0,0] + matrix[1,1]) - (matrix[1,0] + matrix[0,1]) # определитель матрицы
    #print(D)
    p[0] = (matrix[1,1] - matrix[1,0]) / D 
    p[1] = (matrix[0,0] - matrix[0,1]) / D 

    q[0] = (matrix[1,1] - matrix[0,1]) / D #((matrix[0,0] + matrix[1,1]) - (matrix[0,1] + matrix[1, 0]))
    q[1] = 1 - q[0]

    strategies = []
    strategies.append(tuple(p))
    strategies.append(tuple(q))

    return strategies
    #print("Вероятности стратегий игроков при равновесии по Нешу для смешанных стратегий")
    #print("Вероятности 1 игрока")
    #print(p)
    #print("Вероятности 2 игрока")
    #print(q)

# Создаем платёжную матрицу
# matrix1 = np.array([[2, 4, 7, 5],
#                    [7, 6, 8, 7],
#                    [5, 3, 4, 1]])

# matrix2 = np.array([[3, 8],
#                    [7, 4]])


# print(maxmin(matrix1))
# print(minmax(matrix1))

# print(nash_clear(matrix1))
# print(nash_mixed(matrix2))

#print(maxmin(matrix2))
#print(minmax(matrix2))

#nash_clear(matrix2)
#nash_mixed(matrix2)