import tkinter as tk
from tkinter import messagebox
from algs import generate_random_matrix

class MatrixInputWindow:
    def __init__(self, root, matrix, save_callback):
        """
        Окно ввода и редактирования матрицы
        :param root: Основное окно
        :param matrix: Исходная матрица
        :param save_callback: Функция для сохранения матрицы в MainWindow
        """
        self.root = root
        self.matrix = [row[:] for row in matrix]  # Копия матрицы
        self.save_callback = save_callback  # Сохранение данных
        self.window = tk.Toplevel(root)
        self.window.title("Создание/Редактирование матрицы")

        self.entries = []
        self.rows = len(matrix)
        self.cols = len(matrix[0])

        self.create_widgets()
        self.show()

    def create_widgets(self):
        """Создание интерфейса"""
        self.entries = [[None] * self.cols for _ in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.cols):
                entry = tk.Entry(self.window, width=5)
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(tk.END, str(self.matrix[i][j]))
                self.entries[i][j] = entry

        tk.Button(self.window, text="Добавить строку", command=self.add_row).grid(row=self.rows, column=0, columnspan=self.cols, sticky="ew")
        tk.Button(self.window, text="Добавить столбец", command=self.add_col).grid(row=0, column=self.cols, sticky="ns")
        tk.Button(self.window, text="Применить", command=self.apply_changes).grid(row=self.rows + 1, column=0, columnspan=self.cols, sticky="ew")

    def show(self):
        """Отображение окна ввода матрицы"""
        # Если окно уже существует и не закрыто, перерисовываем элементы
        if hasattr(self, 'window') and self.window.winfo_exists():
            # Очистить старые записи, если они есть
            for widget in self.window.winfo_children():
                widget.grid_forget()
        else:
            # Если окно закрыто, создаем новое окно
            self.window = tk.Toplevel(self.root)
            self.window.title("Создание/Редактирование матрицы")

        self.entries = []  # Очищаем список для новых записей

        # Создание новой таблицы для ввода
        for i in range(self.rows):
            row_entries = []
            for j in range(self.cols):
                entry = tk.Entry(self.window, width=8)
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(tk.END, str(self.matrix[i][j]))  # Заполнить текущими значениями
                row_entries.append(entry)
            self.entries.append(row_entries)

        # Кнопки добавления строк и столбцов
        self.add_row_button = tk.Button(self.window, text="Добавить строку", command=self.add_row)
        self.add_row_button.grid(row=self.rows, column=0, columnspan=self.cols//2, sticky="ew")

        self.add_col_button = tk.Button(self.window, text="Добавить столбец", command=self.add_col)
        self.add_col_button.grid(row=self.rows, column=self.cols//2, columnspan=self.cols//2, sticky="ew")

        # Кнопка генерации случайной матрицы
        self.generate_button = tk.Button(self.window, text="Сгенерировать случайную матрицу", command=self.generate_random)
        self.generate_button.grid(row=self.rows + 1, column=0, columnspan=self.cols, sticky="ew")

        # Кнопка "Применить"
        self.apply_button = tk.Button(self.window, text="Применить", command=self.apply_changes)
        self.apply_button.grid(row=self.rows + 2, column=0, columnspan=self.cols, sticky="ew")

    def add_row(self):
        """Добавление строки (максимум 10)"""
        if self.rows < 10:
            self.matrix.append([0] * self.cols)
            self.rows += 1
            self.show()
        else:
            messagebox.showwarning("Предупреждение", "Максимальное количество строк — 10")

    def add_col(self):
        """Добавление столбца (максимум 10)"""
        if self.cols < 10:
            for row in self.matrix:
                row.append(0)
            self.cols += 1
            self.show()
        else:
            messagebox.showwarning("Предупреждение", "Максимальное количество столбцов — 10")

    def apply_changes(self):
        """Сохранение изменений"""
        for i in range(self.rows):
            for j in range(self.cols):
                value = self.entries[i][j].get()
                try:
                    self.matrix[i][j] = float(value)
                except ValueError:
                    messagebox.showerror("Ошибка", f"Неверное значение в ячейке ({i + 1};{j + 1})")
                    return
        self.save_callback(self.matrix)  # Передача в MainWindow
        self.window.destroy()

    def generate_random(self):
        """Генерация случайной матрицы с текущими размерами"""
        try:
            self.matrix = generate_random_matrix(self.rows, self.cols)
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.entries[i][j].winfo_exists():
                        self.entries[i][j].delete(0, tk.END)
                        self.entries[i][j].insert(0, str(self.matrix[i][j]))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сгенерировать матрицу: {str(e)}")
