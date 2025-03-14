# Окна ввода/редактирования матрицы

import tkinter as tk
from tkinter import messagebox

class MatrixInputWindow:
    def __init__(self, root, matrix):
        self.root = root
        self.matrix = matrix
        self.window = tk.Toplevel(root)
        self.window.title("Создание/Редактирование матрицы")

        # Сетка для отображения и ввода значений
        self.entries = []

        # Строки и столбцы для таблицы
        self.rows = len(matrix)
        self.cols = len(matrix[0])

        # Кнопки для добавления строк и столбцов, с ограничениями
        self.add_row_button = tk.Button(self.window, text="Добавить строку", command=self.add_row)
        self.add_row_button.grid(row=self.rows, column=0, columnspan=self.cols, sticky="ew")

        self.add_col_button = tk.Button(self.window, text="Добавить столбец", command=self.add_col)
        self.add_col_button.grid(row=0, column=self.cols, sticky="ns")

        # Кнопка для применения изменений
        self.apply_button = tk.Button(self.window, text="Применить", command=self.apply_changes)
        self.apply_button.grid(row=self.rows + 1, column=0, columnspan=self.cols, sticky="ew")

        # Отображение матрицы в виде таблицы
        self.show()

    def show(self):
        """Отображение окна ввода матрицы"""
        # Если окно уже существует и не закрыто, перерисовываем элементы
        if self.window.winfo_exists():
            # Очистить старые записи, если они есть
            for widget in self.window.winfo_children():
                widget.grid_forget()

            self.entries = []  # Список для новых записей

        else:
            # Если окно закрыто, создаем новое окно
            self.window = tk.Toplevel(self.root)
            self.window.title("Создание/Редактирование матрицы")

        # Создание новой таблицы для ввода
        for i in range(self.rows):
            row_entries = []
            for j in range(self.cols):
                entry = tk.Entry(self.window)
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(tk.END, str(self.matrix[i][j]))  # Заполнить текущими значениями
                row_entries.append(entry)
            self.entries.append(row_entries)

        # Кнопки добавления строк и столбцов
        self.add_row_button.grid(row=self.rows, column=0, columnspan=self.cols, sticky="ew")
        self.add_col_button.grid(row=0, column=self.cols, sticky="ns")

        # Кнопка "Применить"
        self.apply_button.grid(row=self.rows + 1, column=0, columnspan=self.cols, sticky="ew")

    def add_row(self):
        """Добавить новую строку, если количество строк меньше 10"""
        if self.rows < 10:
            self.rows += 1
            self.matrix.append([0] * self.cols)  # Новая строка с нулями
            self.show()
        else:
            messagebox.showwarning("Предупреждение", "Максимальное количество строк — 10.")

    def add_col(self):
        """Добавить новый столбец, если количество столбцов меньше 10"""
        if self.cols < 10:
            self.cols += 1
            for row in self.matrix:
                row.append(0)  # Добавить ноль в каждую строку
            self.show()
        else:
            messagebox.showwarning("Предупреждение", "Максимальное количество столбцов — 10.")

    def apply_changes(self):
        """Применить изменения и закрыть окно"""
        for i in range(self.rows):
            for j in range(self.cols):
                value = self.entries[i][j].get()
                try:
                    self.matrix[i][j] = float(value)
                except ValueError:
                    messagebox.showerror("Ошибка", f"Неверное значение в ячейке {i + 1}, {j + 1}.")
                    return
        self.window.destroy()

    def get_matrix(self):
        return self.matrix

