import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Путь к файлу для сохранения данных
DATA_FILE = "transactions_data.json"

# Список транзакций
transactions = []

# Изначальные категории
categories = ["Еда", "Транспорт", "Развлечения", "Коммунальные услуги", "Прочее"]


def save_data():
    """Сохраняет транзакции и категории в файл."""
    data = {
        "transactions": transactions,
        "categories": categories
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_data():
    """Загружает транзакции и категории из файла."""
    global transactions, categories
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            transactions = data.get("transactions", [])
            categories = data.get("categories", ["Еда", "Транспорт", "Развлечения", "Коммунальные услуги", "Прочее"])
    except FileNotFoundError:
        save_data()  # Создать файл, если его нет


def add_transaction(amount, category, description, transaction_type):
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Некорректный ввод", "Пожалуйста, введите корректную сумму.")
        return

    transaction = {
        "amount": amount if transaction_type == "доход" else -amount,
        "category": category,
        "description": description
    }
    transactions.append(transaction)
    save_data()
    update_balance()
    update_transactions_list()
    update_plot()


def update_balance():
    total_balance = sum([t["amount"] for t in transactions])
    balance_label.config(text=f"Баланс: {total_balance:.2f} руб.")


def update_transactions_list():
    transaction_list.delete(0, tk.END)
    for i, transaction in enumerate(transactions):
        transaction_list.insert(tk.END,
                                f"{i + 1}. {transaction['category']}: {transaction['description']} ({transaction['amount']:.2f} руб.)")


def update_plot():
    expenses = {}
    for transaction in transactions:
        if transaction['amount'] < 0:
            category = transaction['category']
            amount = abs(transaction['amount'])
            if category in expenses:
                expenses[category] += amount
            else:
                expenses[category] = amount

    categories_plot = list(expenses.keys())
    amounts_plot = list(expenses.values())

    fig.clear()
    ax = fig.add_subplot(111)
    ax.pie(amounts_plot, labels=categories_plot, autopct='%1.1f%%', startangle=140)
    ax.set_title('Расходы по категориям')
    canvas.draw()


def add_new_category():
    new_category = simpledialog.askstring("Новая категория", "Введите название новой категории:")
    if new_category:
        categories.append(new_category)
        category_var.set(new_category)  # Выбрать новую категорию
        category_menu['menu'].add_command(label=new_category, command=tk._setit(category_var, new_category))
        save_data()


def delete_category():
    if len(categories) > 1:
        category_to_delete = category_var.get()
        categories.remove(category_to_delete)
        category_var.set(categories[0])  # Установить начальное значение
        category_menu['menu'].delete(0, 'end')

        for cat in categories:
            category_menu['menu'].add_command(label=cat, command=tk._setit(category_var, cat))

        # Обновление категорий в транзакциях
        for transaction in transactions:
            if transaction['category'] == category_to_delete:
                transaction['category'] = categories[0]

        update_transactions_list()
        update_plot()
        save_data()
    else:
        messagebox.showwarning("Предупреждение", "Должна остаться хотя бы одна категория!")


def edit_transaction():
    try:
        selected_index = transaction_list.curselection()[0]
        transaction = transactions[selected_index]

        new_amount = simpledialog.askfloat("Редактировать сумму", "Введите новую сумму:",
                                           initialvalue=abs(transaction["amount"]))
        if new_amount is not None:
            transaction["amount"] = new_amount if transaction["amount"] > 0 else -new_amount

        new_category = simpledialog.askstring("Редактировать категорию", "Введите новую категорию:",
                                              initialvalue=transaction["category"])
        if new_category is not None and new_category in categories:
            transaction["category"] = new_category

        new_description = simpledialog.askstring("Редактировать описание", "Введите новое описание:",
                                                 initialvalue=transaction["description"])
        if new_description is not None:
            transaction["description"] = new_description

        update_transactions_list()
        update_balance()
        update_plot()
        save_data()

    except IndexError:
        messagebox.showwarning("Ошибка", "Выберите транзакцию для редактирования")


def main():
    global balance_label, transaction_list, category_var, category_menu, fig, canvas

    root = tk.Tk()
    root.title("Учёт финансов")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")

    load_data()  # Загрузка данных из файла при старте

    # Основной фрейм
    main_frame = tk.Frame(root, bg="#f0f0f0")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Заголовок
    title_label = tk.Label(main_frame, text="Учёт финансов", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
    title_label.pack(pady=(0, 20))

    input_frame = tk.Frame(main_frame, bg="#ffffff", padx=10, pady=10, relief=tk.RAISED, borderwidth=1)
    input_frame.pack(fill=tk.X, pady=(0, 20))

    amount_label = tk.Label(input_frame, text="Сумма:", font=("Helvetica", 12), bg="#ffffff")
    amount_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    amount_entry = tk.Entry(input_frame, font=("Helvetica", 12))
    amount_entry.grid(row=0, column=1, padx=5, pady=5)

    category_label = tk.Label(input_frame, text="Категория:", font=("Helvetica", 12), bg="#ffffff")
    category_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

    category_var = tk.StringVar(root)
    category_var.set(categories[0])  # Установить начальное значение

    category_menu = tk.OptionMenu(input_frame, category_var, *categories)
    category_menu.config(font=("Helvetica", 12))
    category_menu.grid(row=1, column=1, padx=5, pady=5)

    description_label = tk.Label(input_frame, text="Описание:", font=("Helvetica", 12), bg="#ffffff")
    description_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    description_entry = tk.Entry(input_frame, font=("Helvetica", 12))
    description_entry.grid(row=2, column=1, padx=5, pady=5)

    button_frame = tk.Frame(main_frame, bg="#ffffff")
    button_frame.pack(fill=tk.X, pady=(0, 20))

    add_income_button = tk.Button(button_frame, text="Добавить доход", font=("Helvetica", 12),
                                  command=lambda: add_transaction(amount_entry.get(), category_var.get(),
                                                                  description_entry.get(), "доход"))
    add_income_button.pack(side=tk.LEFT, padx=5, pady=5)

    add_expense_button = tk.Button(button_frame, text="Добавить расход", font=("Helvetica", 12),
                                   command=lambda: add_transaction(amount_entry.get(), category_var.get(),
                                                                   description_entry.get(), "расход"))
    add_expense_button.pack(side=tk.LEFT, padx=5, pady=5)

    add_category_button = tk.Button(button_frame, text="Добавить новую категорию", font=("Helvetica", 12),
                                    command=add_new_category)
    add_category_button.pack(side=tk.LEFT, padx=5, pady=5)

    delete_category_button = tk.Button(button_frame, text="Удалить категорию", font=("Helvetica", 12),
                                       command=delete_category)
    delete_category_button.pack(side=tk.LEFT, padx=5, pady=5)

    edit_transaction_button = tk.Button(button_frame, text="Редактировать транзакцию", font=("Helvetica", 12),
                                        command=edit_transaction)
    edit_transaction_button.pack(side=tk.LEFT, padx=5, pady=5)

    balance_label = tk.Label(main_frame, text="Баланс: 0.00 руб.", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
    balance_label.pack(pady=(0, 20))

    transaction_list = tk.Listbox(main_frame, width=80, height=10, font=("Helvetica", 12))
    transaction_list.pack(pady=(0, 20))

    fig = plt.Figure(figsize=(8, 6), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=main_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Обновление интерфейса с загруженными данными
    update_balance()
    update_transactions_list()
    update_plot()

    root.mainloop()


if __name__ == "__main__":
    main()
