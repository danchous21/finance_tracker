import json
import os

# Путь к файлу для сохранения данных
DATA_FILE = "transactions_data.json"

# Список транзакций и категорий
transactions = []
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
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            transactions = data.get("transactions", [])
            categories = data.get("categories", ["Еда", "Транспорт", "Развлечения", "Коммунальные услуги", "Прочее"])
    else:
        save_data()  # Создать файл, если его нет
