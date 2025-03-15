# Главное окно приложения

import sys
import os
import tkinter as tk
from tkinter import Menu
from PIL import Image, ImageTk
from gui.matrix_input_window import MatrixInputWindow
from gui.message_boxes import show_error, show_info
from gui.file_operations import load_matrix_from_file, save_matrix_to_file

from algs import find_minmax, find_maxmin, nash_mixed, nash_clear


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Решение матричных теоретико-игровых моделей")
        self.root.geometry("800x500")  # Размеры главного окна

        # Карусель изображений
        self.carousel = ImageCarousel(root, "assets")

        self.matrix_data = None     # Хранение текущей модели

        # Главное меню
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Меню "Файл"
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Загрузить модель из файла", command=self.load_matrix)
        self.file_menu.add_command(label="Выгрузить модель в файл", command=self.save_matrix)
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

        # Приветственное сообщение
        welcome_text = (
            'Добро пожаловать в Стратологику!\n'
            'Для начала работы:\n'
            '1. Создайте новую матрицу через меню "Модель" -> "Создать матрицу"\n'
            '2. Введите значения в матрицу\n'
            '3. Используйте алгоритмы из меню "Алгоритмы" для анализа\n'
            '4. Доступны операции с файлами .txt, .xlsx\n'
        )

        self.welcome_label = tk.Label(
            self.root,
            text=welcome_text,
            justify=tk.LEFT,
            font=("Times New Roman", 12),
            padx=20,
            pady=20
        )
        self.welcome_label.pack(fill=tk.X)

        try:
            image = Image.open("assets/cat.jpeg")

            basewidth = 300
            wpercent = (basewidth / float(image.size[0]))
            hsize = int((float(image.size[1]) * float(wpercent)))
            image = image.resize((basewidth, hsize), Image.Resampling.LANCZOS)

            self.cat_photo = ImageTk.PhotoImage(image)
            self.cat_label = tk.Label(self.root, image=self.cat_photo)
            self.cat_label.pack(pady=10)
        except Exception as e:
            print(f"Ошибка при загрузке изображения: {e}")

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
            show_error("Ошибка", "Сначала создайте или загрузите матрицу")

    def create_new_matrix(self):
        """Создание новой матрицы 2x2"""
        self.open_matrix_window([[0, 0], [0, 0]])

    def edit_matrix(self):
        """Просмотр текущей матрицы"""
        if self.matrix_data is not None:
            self.open_matrix_window(self.matrix_data)
        else:
            show_error("Ошибка", "Сначала создайте или загрузите матрицу")

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

    def run_minimax(self):
        """Алгоритм минимакс/максимин"""
        if not hasattr(self, "matrix_data") or self.matrix_data is None:
            show_error("Ошибка", "Сначала создайте или загрузите матрицу")
            return

        matrix = self.matrix_data

        try:
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

        except Exception as e:
            result_text = f"Ошибка при поиске максимина/минимакса: {str(e)}"

        show_info("Результаты", result_text)

    def run_nash_pure(self):
        """Алгоритм поиска равновесия по Нэшу в чистых стратегиях"""
        if not hasattr(self, "matrix_data") or self.matrix_data is None:
            show_error("Ошибка", "Сначала создайте или загрузите матрицу")
            return

        matrix = self.matrix_data

        try:
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

        except Exception as e:
            result_text = f"Ошибка при поиске равновесия: {str(e)}"

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

# Определяем путь к папке assets
def get_assets_path(filename=""):
    """Возвращает путь к файлу внутри папки assets"""
    if getattr(sys, 'frozen', False):
        # Если приложение запущено из .exe
        base_path = sys._MEIPASS
    else:
        # Если запущено в режиме отладки (из Python)
        base_path = os.path.abspath(".")

    return os.path.join(base_path, "assets", filename)

class ImageCarousel:
    def __init__(self, parent, image_folder, interval=10000):
        self.parent = parent
        self.image_folder = image_folder
        self.image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if not self.image_files:
            raise ValueError("В папке assets нет изображений.")

        self.current_index = 0
        self.interval = interval
        self.image_label = tk.Label(parent)
        self.image_label.pack(expand=True, fill=tk.BOTH)
        self.prev_button = tk.Button(parent, text="◀", command=self.prev_image)
        self.prev_button.place(relx=0.02, rely=0.5, anchor=tk.CENTER)
        self.next_button = tk.Button(parent, text="▶", command=self.next_image)
        self.next_button.place(relx=0.98, rely=0.5, anchor=tk.CENTER)
        self.parent.bind("<Configure>", self.resize_image)
        self.load_image()
        self.start_auto_scroll()

    def load_image(self):
        image_path = get_assets_path(self.image_files[self.current_index])
        self.original_image = Image.open(image_path)
        self.resize_image()

    def resize_image(self, event=None):
        width = self.parent.winfo_width()
        height = self.parent.winfo_height()
        if width > 1 and height > 1:
            resized_image = self.original_image.resize((width, height), Image.Resampling.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(resized_image)
            self.image_label.config(image=self.tk_image)

    def next_image(self):
        self.current_index = (self.current_index + 1) % len(self.image_files)
        self.load_image()

    def prev_image(self):
        self.current_index = (self.current_index - 1) % len(self.image_files)
        self.load_image()

    def start_auto_scroll(self):
        self.next_image()
        self.parent.after(self.interval, self.start_auto_scroll)