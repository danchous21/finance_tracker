from gui import create_main_window
from data_handler import load_data, save_data
from logger import log_message

def main():
    load_data()
    log_message("INFO", "Приложение запущено.")
    create_main_window()

if __name__ == "__main__":
    main()
