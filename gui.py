import tkinter as tk
from tkinter import simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data_handler import save_data, load_data, add_transaction, add_new_category, delete_category, edit_transaction, categories, transactions
from utils import animate_add_transaction, animate_new_category

def create_main_window():
    global balance_label, transaction_list, category_var, category_menu, fig, canvas

    root = tk.Tk()
    root.title("Учёт финансов")
    root.geometry("1200x900")
    root.configure(bg="#eaf5e0")

    main_frame = tk.Frame(root, bg="#eaf5e0", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    title_label = tk.Label(main_frame, text="Учёт финансов", font=("Helvetica", 20, "bold"), bg="#eaf5e0", fg="#4a773c")
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
    category_var.set(categories[0])

    category_menu = tk.OptionMenu(input_frame, category_var, *categories)
    category_menu.config(font=("Helvetica", 12), bg="#d8e8d0")
    category_menu.grid(row=1, column=1, padx=5, pady=5)

    description_label = tk.Label(input_frame, text="Описание:", font=("Helvetica", 12), bg="#ffffff")
    description_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    description_entry = tk.Entry(input_frame, font=("Helvetica", 12))
    description_entry.grid(row=2, column=1, padx=5, pady=5)

    button_frame = tk.Frame(main_frame, bg="#ffffff")
    button_frame.pack(fill=tk.X, pady=(0, 20))

    add_income_button = tk.Button(button_frame, text="Добавить доход", font=("Helvetica", 12), bg="#a1d99b",
                                  command=lambda: add_transaction(amount_entry.get(), category_var.get(),
                                                                  description_entry.get(), "доход"))
    add_income_button.pack(side=tk.LEFT, padx=5, pady=5)

    add_expense_button = tk.Button(button_frame, text="Добавить расход", font=("Helvetica", 12), bg="#fcba03",
                                   command=lambda: add_transaction(amount_entry.get(), category_var.get(),
                                                                   description_entry.get(), "расход"))
    add_expense_button.pack(side=tk.LEFT, padx=5, pady=5)

    add_category_button = tk.Button(button_frame, text="Добавить новую категорию", font=("Helvetica", 12), bg="#a1d99b",
                                    command=add_new_category)
    add_category_button.pack(side=tk.LEFT, padx=5, pady=5)

    delete_category_button = tk.Button(button_frame, text="Удалить категорию", font=("Helvetica", 12), bg="#fcba03",
                                       command=delete_category)
    delete_category_button.pack(side=tk.LEFT, padx=5, pady=5)

    edit_transaction_button = tk.Button(button_frame, text="Редактировать транзакцию", font=("Helvetica", 12),
                                        bg="#a1d99b", command=edit_transaction)
    edit_transaction_button.pack(side=tk.LEFT, padx=5, pady=5)

    balance_label = tk.Label(main_frame, text="Баланс: 0.00 руб.", font=("Helvetica", 16, "bold"), bg="#eaf5e0",
                             fg="#4a773c")
    balance_label.pack(pady=(0, 20))

    transaction_list = tk.Listbox(main_frame, width=80, height=10, font=("Helvetica", 12))
    transaction_list.pack(pady=(0, 20))

    fig = plt.Figure(figsize=(8, 6), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=main_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    load_data()
    update_balance()
    update_transactions_list()
    update_plot()

    root.mainloop()

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
    ax.axis('equal')
    canvas.draw()
