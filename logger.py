import datetime

LOG_FILE = "app.log"

def log_message(level, message):
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{timestamp} - {level} - {message}\n")
