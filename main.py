import tkinter as tk
from tkinter import messagebox

# Список транзакций
transactions = []

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
        transaction_list.insert(tk.END, f"{transaction['category']}: {transaction['description']} ({transaction['amount']:.2f} руб.)")

def main():
    global balance_label, transaction_list

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
    category_entry = tk.Entry(input_frame)
    category_entry.grid(row=1, column=1)

    description_label = tk.Label(input_frame, text="Описание:")
    description_label.grid(row=2, column=0)
    description_entry = tk.Entry(input_frame)
    description_entry.grid(row=2, column=1)

    add_income_button = tk.Button(input_frame, text="Добавить доход",
                                  command=lambda: add_transaction(amount_entry.get(),
                                                                  category_entry.get(),
                                                                  description_entry.get(),
                                                                  "доход"))
    add_income_button.grid(row=3, column=0, pady=10)

    add_expense_button = tk.Button(input_frame, text="Добавить расход",
                                   command=lambda: add_transaction(amount_entry.get(),
                                                                   category_entry.get(),
                                                                   description_entry.get(),
                                                                   "расход"))
    add_expense_button.grid(row=3, column=1, pady=10)

    balance_label = tk.Label(root, text="Баланс: 0.00 руб.")
    balance_label.pack(pady=10)

    transaction_list = tk.Listbox(root, width=50)
    transaction_list.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
