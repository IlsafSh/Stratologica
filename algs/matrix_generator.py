import numpy as np

def generate_random_matrix(rows=2, cols=2, min_val=-5, max_val=5):
    """Генерация случайной матрицы с заданными параметрами.
    
    Args:
        rows (int): количество строк (по умолчанию 2)
        cols (int): количество столбцов (по умолчанию 2)
        min_val (int): минимальное значение элементов (по умолчанию -5)
        max_val (int): максимальное значение элементов (по умолчанию 5)
        
    Returns:
        list: Сгенерированная матрица в виде списка списков
    """
    matrix = np.random.randint(min_val, max_val + 1, size=(rows, cols))
    return matrix.tolist() 