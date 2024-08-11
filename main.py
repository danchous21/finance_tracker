import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt

# Список транзакций
transactions = []

# Изначальные категории
categories = ["Еда", "Транспорт", "Развлечения", "Коммунальные услуги", "Прочее"]


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
    messagebox.showinfo("Транзакция добавлена", f"{transaction_type.capitalize()} успешно добавлен!")
    update_balance()
    update_transactions_list()


def update_balance():
    total_balance = sum([t["amount"] for t in transactions])
    balance_label.config(text=f"Баланс: {total_balance:.2f} руб.")


def update_transactions_list():
    transaction_list.delete(0, tk.END)
    for transaction in transactions:
        transaction_list.insert(tk.END,
                                f"{transaction['category']}: {transaction['description']} ({transaction['amount']:.2f} руб.)")


def plot_expenses():
    expenses = {}
    for transaction in transactions:
        if transaction['amount'] < 0:
            category = transaction['category']
            amount = abs(transaction['amount'])
            if category in expenses:
                expenses[category] += amount
            else:
                expenses[category] = amount

    if expenses:
        categories = list(expenses.keys())
        amounts = list(expenses.values())

        plt.figure(figsize=(8, 6))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title('Расходы по категориям')
        plt.show()
    else:
        messagebox.showinfo("Нет данных", "Пока нет расходов для отображения.")


def add_new_category():
    new_category = simpledialog.askstring("Новая категория", "Введите название новой категории:")
    if new_category:
        categories.append(new_category)
        category_var.set(new_category)  # Выбрать новую категорию
        category_menu['menu'].add_command(label=new_category, command=tk._setit(category_var, new_category))


def main():
    global balance_label, transaction_list, category_var, category_menu

    root = tk.Tk()
    root.title("Учёт финансов")
    root.minsize(400, 400)

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
    add_category_button.grid(row=4, columnspan=2, pady=10)

    plot_button = tk.Button(root, text="Показать график расходов", command=plot_expenses)
    plot_button.pack(pady=10)

    balance_label = tk.Label(root, text="Баланс: 0.00 руб.")
    balance_label.pack(pady=10)

    transaction_list = tk.Listbox(root, width=50)
    transaction_list.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
