import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

class StrategyPredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def _prepare_features(self, matrix):
        """Подготовка признаков из матрицы"""
        # Извлекаем базовые характеристики матрицы
        features = []
        matrix = np.array(matrix)
        
        # Статистические характеристики
        features.extend([
            np.mean(matrix),  # среднее значение
            np.std(matrix),   # стандартное отклонение
            np.min(matrix),   # минимум
            np.max(matrix),   # максимум
            np.mean(matrix, axis=0).mean(),  # среднее по столбцам
            np.mean(matrix, axis=1).mean(),  # среднее по строкам
        ])
        
        # Добавляем элементы матрицы
        features.extend(matrix.flatten())
        return np.array(features).reshape(1, -1)
        
    def train(self, matrices, optimal_strategies):
        """Обучение модели на исторических данных
        
        Args:
            matrices: список матриц
            optimal_strategies: список оптимальных стратегий (индексы)
        """
        X = np.vstack([self._prepare_features(m) for m in matrices])
        y = np.array(optimal_strategies)
        
        # Нормализация данных
        X = self.scaler.fit_transform(X)
        
        # Обучение модели
        self.model.fit(X, y)
        self.is_trained = True
        
    def predict(self, matrix):
        """Предсказание оптимальной стратегии для новой матрицы
        
        Args:
            matrix: матрица игры
            
        Returns:
            tuple: (predicted_row, predicted_col) - предсказанные индексы стратегий
        """
        if not self.is_trained:
            raise ValueError("Модель не обучена. Сначала выполните train()")
            
        X = self._prepare_features(matrix)
        X = self.scaler.transform(X)
        
        # Предсказание индексов оптимальных стратегий
        prediction = self.model.predict(X)
        return tuple(map(int, prediction))

def analyze_matrix_patterns(matrix):
    """Анализ паттернов в матрице
    
    Args:
        matrix: матрица игры
        
    Returns:
        dict: словарь с различными метриками и характеристиками матрицы
    """
    matrix = np.array(matrix)
    
    analysis = {
        'размерность': matrix.shape,
        'среднее_значение': np.mean(matrix),
        'медиана': np.median(matrix),
        'стандартное_отклонение': np.std(matrix),
        'асимметрия': bool(np.any(matrix != matrix.T)),  # проверка на симметричность
        'доминирующие_строки': [],
        'доминирующие_столбцы': []
    }
    
    # Поиск доминирующих стратегий
    for i in range(matrix.shape[0]):
        if np.all(matrix[i] >= matrix):
            analysis['доминирующие_строки'].append(i)
            
    for j in range(matrix.shape[1]):
        if np.all(matrix[:, j] >= matrix):
            analysis['доминирующие_столбцы'].append(j)
            
    return analysis

def suggest_strategy(matrix, history=None):
    """Предложение стратегии на основе анализа матрицы и истории игр
    
    Args:
        matrix: текущая матрица
        history: список кортежей (матрица, выбранная_стратегия, результат)
        
    Returns:
        tuple: (row_strategy, col_strategy, confidence) - предлагаемые стратегии и уверенность
    """
    analysis = analyze_matrix_patterns(matrix)
    
    # Если есть доминирующие стратегии, рекомендуем их
    if analysis['доминирующие_строки']:
        row_strategy = analysis['доминирующие_строки'][0]
        confidence = 0.9
    else:
        # Используем смешанную стратегию
        row_strategy = np.argmax(np.mean(matrix, axis=1))
        confidence = 0.7
        
    if analysis['доминирующие_столбцы']:
        col_strategy = analysis['доминирующие_столбцы'][0]
        confidence = 0.9
    else:
        col_strategy = np.argmin(np.mean(matrix, axis=0))
        confidence = 0.7
        
    return row_strategy, col_strategy, confidence 