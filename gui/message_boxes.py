# Всплывающие уведомления

import tkinter as tk
from tkinter import messagebox

def show_info(title, message):
    """Отображает информационное сообщение."""
    messagebox.showinfo(title, message)

def show_error(title, message):
    """Отображает сообщение об ошибке."""
    messagebox.showerror(title, message)

def show_warning(title, message):
    """Отображает предупреждающее сообщение."""
    messagebox.showwarning(title, message)

def ask_question(title, message):
    """Отображает диалог подтверждения и возвращает True, если пользователь нажал 'Да'."""
    return messagebox.askyesno(title, message)
