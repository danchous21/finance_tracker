from gui import create_main_window
from data_handler import load_data, save_data
from logger import log_message

def main():
    global transactions, categories

    load_data()  # Загрузка данных из файла при старте
    log_message("INFO", "Приложение запущено.")

    create_main_window()  # Создание главного окна

if __name__ == "__main__":
    main()
