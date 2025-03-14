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

        # Главное меню
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Меню "Файл"
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Загрузить из файла", command=self.load_matrix)
        self.file_menu.add_command(label="Выгрузить в файл", command=self.save_matrix)
        self.menu_bar.add_cascade(label="Файл", menu=self.file_menu)

        # Меню "Модель"
        self.model_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Модель", menu=self.model_menu)
        self.model_menu.add_command(label="Создать матрицу", command=self.create_new_matrix)
        self.model_menu.add_command(label="Просмотреть матрицу", command=self.see_matrix)

        # Меню "Алгоритмы"
        self.algorithms_menu = Menu(self.menu_bar, tearoff=0)
        self.algorithms_menu.add_command(label="Поиск максимина/минимакса", command=self.run_minimax)
        self.algorithms_menu.add_command(label="Поиск равновесия Нэша (чистые стратегии)", command=self.run_nash_pure)
        self.algorithms_menu.add_command(label="Поиск равновесия Нэша (смешанные стратегии 2x2)", command=self.run_nash_mixed)
        self.menu_bar.add_cascade(label="Алгоритмы", menu=self.algorithms_menu)

        # Меню "Помощь"
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Помощь", menu=self.help_menu)
        self.help_menu.add_command(label="Описание функционала", command=self.show_help)

        # Надпись о состоянии
        self.status_label = tk.Label(self.root, text="Готово к работе", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)

    def load_matrix(self):
        """Загрузка матрицы из файла"""
        matrix = load_matrix_from_file(self.root)
        if matrix is not None:
            self.open_matrix_window(matrix)

    def open_matrix_window(self, matrix):
        """Открытие окна с матрицей"""
        self.matrix_window = MatrixInputWindow(self.root, matrix=matrix)
        self.matrix_window.show()

    def save_matrix(self):
        """Сохранение матрицы в файл"""
        if hasattr(self, "matrix_window") and self.matrix_window:
            save_matrix_to_file(self.matrix_window.get_matrix(), self.root)
        else:
            show_error("Ошибка", "Нет открытой матрицы для сохранения.")

    def create_new_matrix(self):
        """Создание новой матрицы 2x2 с помощью окна ввода"""
        self.matrix_window = MatrixInputWindow(self.root, matrix=[[0, 0], [0, 0]])  # Изначально 2x2
        self.matrix_window.show()

    def see_matrix(self):
        """Просмотр текущей матрицы"""
        if hasattr(self, "matrix_window") and self.matrix_window:
            # Если матрица уже существует, показываем окно просмотра с текущими значениями
            self.matrix_window.show()
        else:
            show_error("Ошибка", "Нет матрицы для редактирования.")

    def run_minimax(self):
        # Алгоритм минимакс/максимин
        pass

    def run_nash_pure(self):
        # Алгоритм поиска равновесия по Нэшу в чистых стратегиях
        pass

    def run_nash_mixed(self):
        # Алгоритм поиска равновесия по Нэшу в смешанных стратегиях
        pass

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
