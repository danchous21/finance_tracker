import tkinter as tk
from tkinter import messagebox, simpledialog
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
    root.minsize(600, 600)

    load_data()  # Загрузка данных из файла при старте

    input_frame = tk.Frame(root)
    input_frame.pack(pady=20)

    amount_label = tk.Label(input_frame, text="Сумма:")
    amount_label.grid(row=0, column=0)
    amount_entry = tk.Entry(input_frame)
    amount_entry.grid(row=0, column=1)

    category_label = tk.Label(input_frame, text="Категория:")
    category_label.grid(row=1, column=0)

    category_var = tk.StringVar(root)
    category_var.set(categories[0])  # Установить начальное значение

    category_menu = tk.OptionMenu(input_frame, category_var, *categories)
    category_menu.grid(row=1, column=1)

    description_label = tk.Label(input_frame, text="Описание:")
    description_label.grid(row=2, column=0)
    description_entry = tk.Entry(input_frame)
    description_entry.grid(row=2, column=1)

    add_income_button = tk.Button(input_frame, text="Добавить доход",
                                  command=lambda: add_transaction(amount_entry.get(),
                                                                  category_var.get(),
                                                                  description_entry.get(),
                                                                  "доход"))
    add_income_button.grid(row=3, column=0, pady=10)

    add_expense_button = tk.Button(input_frame, text="Добавить расход",
                                   command=lambda: add_transaction(amount_entry.get(),
                                                                   category_var.get(),
                                                                   description_entry.get(),
                                                                   "расход"))
    add_expense_button.grid(row=3, column=1, pady=10)

    add_category_button = tk.Button(input_frame, text="Добавить новую категорию", command=add_new_category)
    add_category_button.grid(row=4, column=0, pady=10)

    delete_category_button = tk.Button(input_frame, text="Удалить категорию", command=delete_category)
    delete_category_button.grid(row=4, column=1, pady=10)

    edit_transaction_button = tk.Button(input_frame, text="Редактировать транзакцию", command=edit_transaction)
    edit_transaction_button.grid(row=5, columnspan=2, pady=10)

    balance_label = tk.Label(root, text="Баланс: 0.00 руб.")
    balance_label.pack(pady=10)

    transaction_list = tk.Listbox(root, width=50)
    transaction_list.pack(pady=10)

    fig = plt.Figure(figsize=(5, 4), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    # Обновление интерфейса с загруженными данными
    update_balance()
    update_transactions_list()
    update_plot()

    root.mainloop()


if __name__ == "__main__":
    main()
