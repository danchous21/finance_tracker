import json
import os
from tkinter import simpledialog
import tkinter as tk
from utils import animate_add_transaction, animate_new_category

DATA_FILE = "transactions_data.json"
transactions = []
categories = ["Еда", "Транспорт", "Развлечения", "Коммунальные услуги", "Прочее"]

def save_data():
    data = {
        "transactions": transactions,
        "categories": categories
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data():
    global transactions, categories
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            transactions = data.get("transactions", [])
            categories = data.get("categories", ["Еда", "Транспорт", "Развлечения", "Коммунальные услуги", "Прочее"])
    else:
        save_data()

def add_transaction(amount, category, description, type):
    amount = float(amount)
    if type == "расход":
        amount = -amount
    transactions.append({"amount": amount, "category": category, "description": description})
    save_data()

def add_new_category():
    new_category = simpledialog.askstring("Новая категория", "Введите название новой категории:")
    if new_category and new_category not in categories:
        categories.append(new_category)
        save_data()

def delete_category():
    category_to_delete = simpledialog.askstring("Удаление категории", "Введите название категории для удаления:")
    if category_to_delete in categories:
        categories.remove(category_to_delete)
        save_data()

def edit_transaction():
    transaction_id = simpledialog.askinteger("Редактировать транзакцию", "Введите ID транзакции для редактирования:")
    if transaction_id is not None and 0 < transaction_id <= len(transactions):
        transaction = transactions[transaction_id - 1]
        new_amount = simpledialog.askfloat("Изменить сумму", "Введите новую сумму:", initialvalue=transaction['amount'])
        new_description = simpledialog.askstring("Изменить описание", "Введите новое описание:", initialvalue=transaction['description'])
        if new_amount is not None and new_description is not None:
            transactions[transaction_id - 1]['amount'] = new_amount
            transactions[transaction_id - 1]['description'] = new_description
            save_data()
