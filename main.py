import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkthemes import ThemedTk
import os
import datetime

# Путь к файлу для сохранения данных
DATA_FILE = "transactions_data.json"
# Путь к файлу для логов
LOG_FILE = "application_log.txt"

# Список транзакций
transactions = []

# Изначальные категории
categories = ["Еда", "Транспорт", "Развлечения", "Коммунальные услуги", "Прочее"]


def log_message(level, message):
    """Записывает сообщение в файл лога с указанным уровнем."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(f"{timestamp} [{level}] {message}\n")


def save_data():
    """Сохраняет транзакции и категории в файл."""
    data = {
        "transactions": transactions,
        "categories": categories
    }
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        log_message("INFO", "Данные сохранены.")
    except Exception as e:
        log_message("ERROR", f"Ошибка при сохранении данных: {e}")


def load_data():
    """Загружает транзакции и категории из файла."""
    global transactions, categories
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                transactions = data.get("transactions", [])
                categories = data.get("categories",
                                      ["Еда", "Транспорт", "Развлечения", "Коммунальные услуги", "Прочее"])
            log_message("INFO", "Данные загружены из файла.")
        else:
            save_data()  # Создать файл, если его нет
            log_message("INFO", "Файл данных не найден. Создан новый файл.")
    except Exception as e:
        log_message("ERROR", f"Ошибка при загрузке данных: {e}")


def add_transaction(amount, category, description, transaction_type):
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной.")
    except ValueError as e:
        messagebox.showerror("Некорректный ввод", f"Ошибка: {e}")
        log_message("ERROR", f"Не удалось добавить транзакцию: {e}")
        return

    transaction = {
        "amount": amount if transaction_type == "доход" else -amount,
        "category": category,
        "description": description
    }
    transactions.append(transaction)
    save_data()
    log_message("INFO", f"Добавлена транзакция: {transaction}")
    update_balance()
    animate_add_transaction()
    update_plot()


def animate_add_transaction():
    """Плавная анимация добавления транзакции в список."""

    def animate():
        for i in range(10):
            transaction_list.after(i * 100, lambda i=i: transaction_list.insert(tk.END, " "))
        transaction_list.after(1000, lambda: transaction_list.delete(0, tk.END))
        update_transactions_list()

    transaction_list.delete(0, tk.END)
    animate()


def update_balance():
    total_balance = sum([t["amount"] for t in transactions])
    balance_label.config(text=f"Баланс: {total_balance:.2f} руб.")
    log_message("INFO", f"Баланс обновлен: {total_balance:.2f} руб.")


def update_transactions_list():
    transaction_list.delete(0, tk.END)
    for i, transaction in enumerate(transactions):
        transaction_list.insert(tk.END,
                                f"{i + 1}. {transaction['category']}: {transaction['description']} ({transaction['amount']:.2f} руб.)")
    log_message("INFO", "Список транзакций обновлен.")


def update_plot():
    """Обновляет диаграмму расходов по категориям."""
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

    fig.clear()  # Очищаем предыдущий график
    ax = fig.add_subplot(111)
    ax.pie(amounts_plot, labels=categories_plot, autopct='%1.1f%%', startangle=140)
    ax.set_title('Расходы по категориям')

    canvas.draw()  # Обновляем диаграмму на экране


def add_new_category():
    new_category = simpledialog.askstring("Новая категория", "Введите название новой категории:")
    if new_category:
        categories.append(new_category)
        category_var.set(new_category)  # Выбрать новую категорию
        category_menu['menu'].add_command(label=new_category, command=tk._setit(category_var, new_category))
        save_data()
        log_message("INFO", f"Добавлена новая категория: {new_category}")
        animate_new_category()


def animate_new_category():
    """Плавная анимация добавления новой категории в меню."""

    def animate():
        for i in range(10):
            category_menu.after(i * 100, lambda i=i: category_menu.config(bg="#eaf5e0"))
        category_menu.after(1000, lambda: category_menu.config(bg="#d8e8d0"))

    category_menu.config(bg="#eaf5e0")
    animate()


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
        log_message("INFO", f"Удалена категория: {category_to_delete}")
    else:
        messagebox.showwarning("Предупреждение", "Должна остаться хотя бы одна категория!")
        log_message("WARNING", "Попытка удалить последнюю категорию.")


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
        log_message("INFO", f"Отредактирована транзакция: {transaction}")

    except IndexError:
        messagebox.showwarning("Ошибка", "Выберите транзакцию для редактирования")
        log_message("WARNING", "Попытка редактирования несуществующей транзакции.")


def main():
    global balance_label, transaction_list, category_var, category_menu, fig, canvas

    root = ThemedTk(theme="breeze")  # Используем библиотеку ttkthemes
    root.title("Учёт финансов")
    root.geometry("1200x900")  # Увеличиваем размер окна
    root.configure(bg="#eaf5e0")

    load_data()  # Загрузка данных из файла при старте

    # Основной фрейм
    main_frame = tk.Frame(root, bg="#eaf5e0", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Заголовок
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
    category_var.set(categories[0])  # Установить начальное значение

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

    # Обновление интерфейса с загруженными данными
    update_balance()
    update_transactions_list()
    update_plot()

    root.mainloop()


if __name__ == "__main__":
    main()
