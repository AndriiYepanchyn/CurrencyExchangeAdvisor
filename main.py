import sys
import subprocess
import os
import DataBaseApi
from ui.CurrencyUI import CurrencyUI
from Parser import Parser 

class MainApp:
    @staticmethod
    def run():
        args = sys.argv[1:]
        database_connector = DataBaseApi.DataBaseApi("sqlite")
        database_connector.connect()

        if "-collect-mode" in args:
            # Реальний збір даних
            parser = Parser()
            parser.collect()
            
        else:
            # Якщо запущено без аргументів — запускаємо UI
            # database_connector.execute("INSERT INTO banks VALUES ('NBU', 'National bank of Ukraine', 'https://bank.gov.ua/')")
            # rows = database_connector.execute("SELECT * FROM BANKS_INFO;")
            # for r in rows:
            #     print(r, '\n')
            app = CurrencyUI(database_connector)
            app.mainloop()   

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

if __name__ == "__main__":
    MainApp.run()
