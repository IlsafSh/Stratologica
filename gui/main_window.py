# Главное окно приложения

import tkinter as tk
from tkinter import Menu
from PIL import Image, ImageTk
import os
from gui.matrix_input_window import MatrixInputWindow
from gui.message_boxes import show_error, show_info
from gui.file_operations import load_matrix_from_file, save_matrix_to_file

from algs import find_minmax, find_maxmin, nash_mixed, nash_clear


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Решение матричных теоретико-игровых моделей")
        self.root.geometry("600x500")  # Увеличим высоту окна для размещения всех элементов

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
        """Алгоритм минимакс/максимин"""
        if not hasattr(self, "matrix_window") or not self.matrix_window:
            show_error("Ошибка", "Сначала создайте или загрузите матрицу")
            return
            
        matrix = self.matrix_window.get_matrix()
        maximin = find_maxmin(matrix)
        minimax = find_minmax(matrix)
        
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
        if not hasattr(self, "matrix_window") or not self.matrix_window:
            show_error("Ошибка", "Сначала создайте или загрузите матрицу")
            return
            
        matrix = self.matrix_window.get_matrix()
        nash_equilibria = nash_clear(matrix)
        
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
        if not hasattr(self, "matrix_window") or not self.matrix_window:
            show_error("Ошибка", "Сначала создайте или загрузите матрицу")
            return
            
        matrix = self.matrix_window.get_matrix()
        
     
        if len(matrix) != 2 or len(matrix[0]) != 2:
            show_error("Ошибка", "Для поиска смешанных стратегий необходима матрица 2x2")
            return
            
        try:
            strategies = nash_mixed(matrix)
            p1_probs, p2_probs = strategies
            
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
