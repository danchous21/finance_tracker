import tkinter as tk

def animate_add_transaction(transaction_list):
    """Анимация добавления транзакции в список."""
    transaction_list.insert(tk.END, "Новая транзакция добавлена")
    transaction_list.after(2000, lambda: transaction_list.delete(tk.END))

def animate_new_category(category_menu):
    """Анимация добавления новой категории."""
    category_menu.config(text="Новая категория добавлена")
    category_menu.after(2000, lambda: category_menu.config(text="Выберите категорию"))
