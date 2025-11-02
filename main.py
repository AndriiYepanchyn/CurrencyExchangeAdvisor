import sys
import subprocess
import os
import DataBaseApi
from time import sleep
# from data_collector import DataCollector
# from ui_app import UiApp

class MainApp:
    @staticmethod
    def run():
        args = sys.argv[1:]

        if "-collect-mode" in args:
            # Реальний збір даних
            # collector = DataCollector()
            # collector.run_silent()
            sleep(5)
            
        else:
            # Якщо запущено без аргументів — запускаємо UI
            print("Запуск графічного інтерфейсу...")
            
            database_connector = DataBaseApi.DataBaseApi("sqlite")
            database_connector.connect()
            # database_connector.execute("INSERT INTO banks VALUES ('NBU', 'National bank of Ukraine', 'https://bank.gov.ua/')")
            rows = database_connector.fetchall("SELECT bank_name FROM banks")
            
            for r in rows:
                print(r, '\n')
            
            # app = UiApp()
            # app.run()

    @staticmethod
    def run_background():
        """
        Запускає цей же скрипт у фоновому режимі без консолі (Windows).
        """
        python_exe = sys.executable.replace("python.exe", "pythonw.exe")

        if not os.path.exists(python_exe):
            # Якщо pythonw.exe не знайдено — fallback
            python_exe = sys.executable

        subprocess.Popen(
            [python_exe, __file__, "-collect-mode"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW
        )
        print("Фоновий процес збору даних запущено.")

if __name__ == "__main__":
    # Якщо викликати main.py без аргументів — відкриється UI
    # але можна з нього запустити збір даних у фоні
    args = sys.argv[1:]
    if "-collect-mode" in args:
        MainApp.run()
    else:
        # Приклад: можна викликати MainApp.run_background() прямо з UI
        MainApp.run()
