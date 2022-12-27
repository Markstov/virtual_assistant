import subprocess
import os
import time
from pathlib import Path
from winreg import *
import winapps
import pyautogui
import sqlite3
from wind_manage import WindowMgr


class Assistant:
    
    def __init__(self):
        self.w = WindowMgr()
        self.conn = sqlite3.connect("apps.db")
        self.cursor = self.conn.cursor()

    def minimize_winds(self):
        pyautogui.hotkey('win','d')
        time.sleep(1)

    def set_wind_foreground(self, app_name):
        self.w.find_window_wildcard(f".*{app_name}.*")
        self.w.set_foreground()
        
    def open_app(self, app_name):
        self.cursor.execute(f"SELECT app_path FROM applications WHERE app_name LIKE '%{app_name}%'")
        app_path = self.cursor.fetchone()[0]
        subprocess.Popen(f"{app_path}/{app_name}")
        # subprocess.Popen(f"{app_name}")

    def update_db_apps(self):
        for app in winapps.list_installed():
            if app.name and app.install_location:
                print(app.name)
                self.cursor.execute(f"INSERT INTO applications(app_name, app_path) VALUES('{app.name}', '{app.install_location}')")
        self.conn.commit()

    def show_apps(self):
        self.cursor.execute("SELECT * FROM applications")
        print(self.cursor.fetchall())

    def exec_command(self, command:str):
        command_list = command.split()
        comm = command_list[0].lower()

        if "открыть" in comm:
            self.open_app(" ".join(command_list[1:]))
        elif "свернуть" in comm:
            self.minimize_winds()
        elif "развернуть" in comm:
            self.set_wind_foreground(" ".join(command_list[1:]))
        elif "help" in comm:
            self.help()
        else:
            print("Unknown command")
            return None

    def help(self):
        print("""Список команд:
        1. Открыть 'Имя программы'
        2. Развернуть 'Имя программы'
        3. Свернуть
        """)


if __name__ == "__main__":
    assist = Assistant()
    assist.exec_command("Свернуть")
    assist.exec_command("Открыть notepad")
    # assist.help()
    # assist.update_db_apps()
    # assist.show_apps()

    # assist.cursor.execute("""Drop table applications
    # """)

    # assist.cursor.execute("""CREATE TABLE IF NOT EXISTS applications(
    #     app_id INTEGER PRIMARY KEY,
    #     app_name VARCHAR,
    #     app_path VARCHAR);
    # """)
    # assist.conn.commit()
    # assist.minimize_winds()
    # time.sleep(5)
    # assist.set_wind_foreground("Chrome")
    # assist.open_app("notepad")

    # for app in winapps.list_installed():
    #     print(app,'\n')

    # # ##################### 
    # for app in winapps.search_installed('Google Chrome'): 
    #     g_app = app 
    #     print(app)

    # # print(type(g_app))
    # # print(g_app.install_location)
    # g_path = g_app.install_location
    # print(g_path)
    # process = subprocess.Popen(f"{g_path}/chrome.exe")