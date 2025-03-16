# Главное окно приложения

import tkinter as tk
from tkinter import Menu
from PIL import Image, ImageTk
import os
from gui.matrix_input_window import MatrixInputWindow
from gui.message_boxes import show_error, show_info
from gui.file_operations import load_matrix_from_file, save_matrix_to_file

from algs import find_minmax, find_maxmin, nash_mixed, nash_clear
from algs.ml_strategies import analyze_matrix_patterns, suggest_strategy, StrategyPredictor


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Решение матричных теоретико-игровых моделей")
        self.root.geometry("600x500")  # Увеличим высоту окна для размещения всех элементов

        # Инициализация ML-модели
        self.strategy_predictor = StrategyPredictor()
        self.game_history = []  # История игр для обучения

        # Главное меню
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Меню "Файл"
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Загрузить из файла", command=self.load_matrix)
        self.file_menu.add_command(label="Выгрузить в файл", command=self.save_matrix)
        self.menu_bar.add_cascade(label="Файл", menu=self.file_menu)

        # Меню "Модель"
        self.model_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Модель", menu=self.model_menu)
        self.model_menu.add_command(label="Создать матрицу", command=self.create_new_matrix)
        self.model_menu.add_command(label="Редактировать матрицу", command=self.edit_matrix)

        # Меню "Алгоритмы"
        self.algorithms_menu = Menu(self.menu_bar, tearoff=0)
        self.algorithms_menu.add_command(label="Поиск максимина/минимакса", command=self.run_minimax)
        self.algorithms_menu.add_command(label="Поиск равновесия Нэша (чистые стратегии)", command=self.run_nash_pure)
        self.algorithms_menu.add_command(label="Поиск равновесия Нэша (смешанные стратегии 2x2)", command=self.run_nash_mixed)
        self.menu_bar.add_cascade(label="Алгоритмы", menu=self.algorithms_menu)

        # Добавляем меню ML-анализа
        self.ml_menu = Menu(self.menu_bar, tearoff=0)
        self.ml_menu.add_command(label="Анализ паттернов матрицы", command=self.analyze_patterns)
        self.ml_menu.add_command(label="Предложить стратегию", command=self.get_strategy_suggestion)
        self.ml_menu.add_command(label="История игр", command=self.show_history)
        self.menu_bar.add_cascade(label="ML анализ", menu=self.ml_menu)

        # Меню "Помощь"
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Помощь", menu=self.help_menu)
        self.help_menu.add_command(label="Описание функционала", command=self.show_help)

        # Приветственное сообщение
        welcome_text = """Добро пожаловать в Стратологику!

Для начала работы:
1. Создайте новую матрицу через меню "Модель" -> "Создать матрицу"
2. Введите значения в матрицу
3. Используйте алгоритмы из меню "Алгоритмы" для анализа
4. Доступны операции в файлами

"""
        
        self.welcome_label = tk.Label(
            self.root,
            text=welcome_text,
            justify=tk.LEFT,
            font=("Arial", 12),
            padx=20,
            pady=20
        )
        self.welcome_label.pack(fill=tk.X)

        try:
           
            image = Image.open("cat.jpeg")
            
            basewidth = 300
            wpercent = (basewidth / float(image.size[0]))
            hsize = int((float(image.size[1]) * float(wpercent)))
            image = image.resize((basewidth, hsize), Image.Resampling.LANCZOS)
            
            self.cat_photo = ImageTk.PhotoImage(image)
            self.cat_label = tk.Label(self.root, image=self.cat_photo)
            self.cat_label.pack(pady=10)
        except Exception as e:
            print(f"Ошибка при загрузке изображения: {e}")

        self.status_label = tk.Label(self.root, text="Готово к работе", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)

    def load_matrix(self):
        """Загрузка матрицы"""
        matrix = load_matrix_from_file(self.root)
        if matrix is not None:
            self.matrix_data = matrix
            show_info("Успех", "Матрица загружена")

    def save_matrix(self):
        """Сохранение матрицы"""
        if self.matrix_data is not None:
            save_matrix_to_file(self.matrix_data, self.root)
        else:
            show_error("Ошибка", "Нет матрицы для сохранения")

    def create_new_matrix(self):
        """Создание новой матрицы 2x2"""
        self.open_matrix_window([[0, 0], [0, 0]])

    def edit_matrix(self):
        """Просмотр текущей матрицы"""
        if self.matrix_data is not None:
            self.open_matrix_window(self.matrix_data)
        else:
            show_error("Ошибка", "Нет матрицы для просмотра")

    def open_matrix_window(self, matrix):
        """Создание окна ввода матрицы"""
        self.matrix_window = MatrixInputWindow(self.root, matrix, self.save_matrix_data)

    def save_matrix_data(self, matrix):
        """Сохранение изменений после редактирования"""
        self.matrix_data = matrix
        self.matrix_window = None  # Очищаем ссылку после закрытия окна

    def get_matrix_data(self):
        """Получение текущей матрицы"""
        if hasattr(self, "matrix_data") and self.matrix_data is not None:
            return self.matrix_data
        return None

    def add_to_history(self, strategy_type, result):
        """Добавление результата в историю игр
        
        Args:
            strategy_type (str): тип использованной стратегии
            result (dict): результат применения стратегии
        """
        if hasattr(self, "matrix_data") and self.matrix_data is not None:
            history_entry = {
                'matrix': [row[:] for row in self.matrix_data],  # Копия матрицы
                'strategy_type': strategy_type,
                'result': result,
                'size': f"{len(self.matrix_data)}x{len(self.matrix_data[0])}"
            }
            self.game_history.append(history_entry)

    def show_history(self):
        """Отображение истории игр"""
        if not self.game_history:
            show_info("История игр", "История пуста")
            return
            
        result_text = "История игр:\n\n"
        for i, entry in enumerate(self.game_history, 1):
            result_text += f"Запись {i}:\n"
            result_text += f"Размер матрицы: {entry['size']}\n"
            result_text += f"Тип стратегии: {entry['strategy_type']}\n"
            
            if isinstance(entry['result'], dict):
                for key, value in entry['result'].items():
                    result_text += f"{key}: {value}\n"
            else:
                result_text += f"Результат: {entry['result']}\n"
            
            result_text += "\n"
            
        show_info("История игр", result_text)

    def run_minimax(self):
        """Алгоритм минимакс/максимин"""
        if not hasattr(self, "matrix_data") or self.matrix_data is None:
            show_error("Ошибка", "Сначала создайте или загрузите матрицу")
            return
            
        matrix = self.matrix_data
        maximin = find_maxmin(matrix)
        minimax = find_minmax(matrix)
        
        result = {
            'максимин': maximin,
            'минимакс': minimax,
            'седловая_точка': maximin == minimax
        }
        
        # Добавляем в историю
        self.add_to_history('Максимин/Минимакс', result)
        
        result_text = (
            f"Результаты анализа:\n\n"
            f"Максимин (гарантированный выигрыш первого игрока): {maximin}\n"
            f"Минимакс (гарантированный проигрыш второго игрока): {minimax}\n"
        )
        
        if maximin == minimax:
            result_text += f"\nНайдена седловая точка со значением {maximin}"
        else:
            result_text += "\nСедловая точка отсутствует"
            
        show_info("Результаты", result_text)

    def run_nash_pure(self):
        """Алгоритм поиска равновесия по Нэшу в чистых стратегиях"""
        if not hasattr(self, "matrix_data") or self.matrix_data is None:
            show_error("Ошибка", "Сначала создайте или загрузите матрицу")
            return
            
        matrix = self.matrix_data
        nash_equilibria = nash_clear(matrix)
        
        result = {
            'количество_равновесий': len(nash_equilibria) if nash_equilibria else 0,
            'равновесия': nash_equilibria
        }
        
        # Добавляем в историю
        self.add_to_history('Равновесие Нэша (чистые)', result)
        
        if nash_equilibria:
            result_text = "Найдены следующие равновесия в чистых стратегиях:\n\n"
            for i, (row, col) in enumerate(nash_equilibria, 1):
                result_text += f"Равновесие {i}:\n"
                result_text += f"Первый игрок: стратегия {row}\n"
                result_text += f"Второй игрок: стратегия {col}\n"
                result_text += f"Значение: {matrix[row-1][col-1]}\n\n"
        else:
            result_text = "Равновесий в чистых стратегиях не найдено"
            
        show_info("Результаты", result_text)

    def run_nash_mixed(self):
        """Алгоритм поиска равновесия по Нэшу в смешанных стратегиях"""
        if not hasattr(self, "matrix_data") or self.matrix_data is None:
            show_error("Ошибка", "Сначала создайте или загрузите матрицу")
            return
            
        matrix = self.matrix_data
        
        if len(matrix) != 2 or len(matrix[0]) != 2:
            show_error("Ошибка", "Для поиска смешанных стратегий необходима матрица 2x2")
            return
            
        try:
            strategies = nash_mixed(matrix)
            p1_probs, p2_probs = strategies
            
            result = {
                'стратегии_p1': p1_probs,
                'стратегии_p2': p2_probs
            }
            
            # Добавляем в историю
            self.add_to_history('Равновесие Нэша (смешанные)', result)
            
            result_text = "Найдено равновесие в смешанных стратегиях:\n\n"
            result_text += "Первый игрок:\n"
            for i, prob in enumerate(p1_probs, 1):
                result_text += f"Стратегия {i}: {prob:.3f}\n"
                
            result_text += "\nВторой игрок:\n"
            for i, prob in enumerate(p2_probs, 1):
                result_text += f"Стратегия {i}: {prob:.3f}\n"
                
        except Exception as e:
            result_text = f"Ошибка при поиске равновесия: {str(e)}"
            
        show_info("Результаты", result_text)

    def analyze_patterns(self):
        """Анализ паттернов в текущей матрице"""
        if not hasattr(self, "matrix_data") or self.matrix_data is None:
            show_error("Ошибка", "Сначала создайте или загрузите матрицу")
            return
            
        analysis = analyze_matrix_patterns(self.matrix_data)
        
        # Форматируем результат анализа
        result_text = "Результаты анализа матрицы:\n\n"
        for key, value in analysis.items():
            result_text += f"{key}: {value}\n"
            
        show_info("Анализ матрицы", result_text)
        
    def get_strategy_suggestion(self):
        """Получение предложения по стратегии"""
        if not hasattr(self, "matrix_data") or self.matrix_data is None:
            show_error("Ошибка", "Сначала создайте или загрузите матрицу")
            return
            
        row_strategy, col_strategy, confidence = suggest_strategy(self.matrix_data, self.game_history)
        
        result_text = (
            f"Рекомендуемые стратегии (уверенность: {confidence:.2%}):\n\n"
            f"Первый игрок: стратегия {row_strategy + 1}\n"
            f"Второй игрок: стратегия {col_strategy + 1}\n\n"
            f"Примечание: Рекомендации основаны на анализе паттернов в матрице"
        )
        
        show_info("Рекомендация стратегий", result_text)

    def show_help(self):
        help_text = (
            "Описание функционала:\n"
            "- Загрузка и выгрузка матриц из файлов.\n"
            "- Создание матриц вручную.\n"
            "- Применение различных алгоритмов теории игр:\n"
            "  - Алгоритм минимакса.\n"
            "  - Поиск равновесий Нэша в чистых и смешанных стратегиях.\n"
        )
        show_info("Помощь", help_text)
