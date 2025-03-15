# Поиск максимина/минимакса

import numpy as np

def find_minmax(matrix):
    max_in_rows = np.max(matrix, axis=0)
    return min(max_in_rows)
