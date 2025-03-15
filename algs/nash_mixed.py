import numpy as np

def nash_mixed(matrix):
    """Поиск равновесия по Нэшу в смешанных стратегиях для 2×2-игры.

    Args:
        matrix (list): матрица 2x2 в виде списка списков.

    Returns:
        list: [(p1, p2), (q1, q2)] - вероятности первого и второго игроков
              или None если нет смешанного равновесия или матрица неправильного размера
    """
   
    matrix = np.array(matrix)

    if matrix.shape != (2, 2):
        return None  #  неправильны размер

  
    D = (matrix[0, 0] + matrix[1, 1]) - (matrix[1, 0] + matrix[0, 1])

    if abs(D) < 1e-10:  
        return None  # нет смешанного равновесия если 0

    # Вычисление вероятностей
    p1 = (matrix[1, 1] - matrix[1, 0]) / D
    q1 = (matrix[1, 1] - matrix[0, 1]) / D

    # Проверка границ вероятностей -- если у нас вероятность выходит за пределы 0 1 то пусть будет чистая стратегия
    if not (0 <= p1 <= 1):
        p1 = 1 if matrix[0, 0] > matrix[1, 0] else 0 

    if not (0 <= q1 <= 1):
        q1 = 1 if matrix[0, 1] > matrix[1, 1] else 0  

    p2 = 1 - p1
    q2 = 1 - q1

    return [(p1, p2), (q1, q2)]
