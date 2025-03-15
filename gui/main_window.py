# Главное окно приложения

import tkinter as tk
from tkinter import Menu
from gui.matrix_input_window import MatrixInputWindow
from gui.message_boxes import show_error, show_info
from gui.file_operations import load_matrix_from_file, save_matrix_to_file
from algs import find_minimax, find_nash_pure, find_nash_mixed


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Решение матричных теоретико-игровых моделей")
        self.root.geometry("600x400")

        self.matrix_data = None  # Хранение текущей матрицы

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

        # Меню "Помощь"
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Помощь", menu=self.help_menu)
        self.help_menu.add_command(label="Описание функционала", command=self.show_help)

        # Статус
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
        MatrixInputWindow(self.root, matrix, self.save_matrix_data)

    def save_matrix_data(self, matrix):
        """Сохранение изменений после редактирования"""
        self.matrix_data = matrix

    def run_minimax(self):
        # Алгоритм минимакс/максимин
        if self.matrix_data is None:
            show_error("Ошибка", "Нет матрицы для анализа")
            return
        result = find_minimax(self.matrix_data)
        show_info("Результат", f"Минимаксное значение: {result}")

    def run_nash_pure(self):
        # Алгоритм поиска равновесия по Нэшу в чистых стратегиях
        if self.matrix_data is None:
            show_error("Ошибка", "Нет матрицы для анализа")
            return
        result = find_nash_pure(self.matrix_data)
        show_info("Результат", f"Равновесие Нэша: {result}")

    def run_nash_mixed(self):
        # Алгоритм поиска равновесия по Нэшу в смешанных стратегиях
        if self.matrix_data is None:
            show_error("Ошибка", "Нет матрицы для анализа")
            return
        result = find_nash_mixed(self.matrix_data)
        show_info("Результат", f"Смешанные стратегии: {result}")

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
