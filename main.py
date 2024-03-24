import os
import config
import stt
import tts
from fuzzywuzzy import fuzz
import datetime
import webbrowser
import random
import winapps
from set_wind import BotSetting, VOICES_M_NAMES
from fingers import MouseThread
from sql import DBManager
from window_manage import WindowMngr

import logging

logging.basicConfig(level=logging.INFO, filename="assistant.log",filemode="a")


class BotV1:

    def __init__(self):
        self.name = "Олег"
        self.voice = VOICES_M_NAMES[0]
        self.gender = "male"
        self.mouse_control = False
        self.wind_manager = WindowMngr()
        self.db_manage = DBManager()
        self.update_programs()
        print(f"{config.VA_NAME} начал свою работу ...")

    def va_respond(self, voice: str):
        print(voice)
        if voice.startswith(self.name.lower()):
            # обращаются к ассистенту
            cmd = self.recognize_cmd(self.filter_cmd(voice))

            if cmd['cmd'] not in config.VA_CMD_LIST.keys():
                tts.va_speak("Повторите команду", self.voice)
            else:
                print(f"Выполнение команды {cmd['cmd']}")
                self.execute_cmd(cmd['cmd'])


    def filter_cmd(self, raw_voice: str):
        cmd = raw_voice

        # for x in config.VA_ALIAS:
        cmd = cmd.replace(self.name, "").strip()

        for x in config.VA_TBR:
            cmd = cmd.replace(x, "").strip()

        return cmd


    def recognize_cmd(self, cmd: str):
        rc = {'cmd': '', 'percent': 0}
        for c, v in config.VA_CMD_LIST.items():

            for x in v:
                vrt = fuzz.ratio(cmd, x)
                if vrt > rc['percent']:
                    rc['cmd'] = c
                    rc['percent'] = vrt

        return rc


    def execute_cmd(self, cmd: str):
        if cmd == 'help':
            # help
            text = "Я умею: ..."
            text += "произносить время ..."
            text += "рассказывать анекдоты ..."
            text += "и открывать браузер"
            tts.va_speak(text, self.voice)
            pass
        elif cmd == 'ctime':
            # current time
            now = datetime.datetime.now()
            # text = "Сейч+ас " + num2text(now.hour) + " " + num2text(now.minute)
            tts.va_speak(text, self.voice)

        elif cmd == 'joke':
            jokes = ['Как смеются программисты? ... ехе ехе ехе',
                    'ЭсКьюЭль запрос заходит в бар, подходит к двум столам и спрашивает .. «м+ожно присоединиться?»',
                    'Программист это машина для преобразования кофе в код']

            tts.va_speak(random.choice(jokes), self.voice)

        elif cmd == 'open_browser':
            chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            webbrowser.get(chrome_path).open("http://python.org")

        elif cmd == 'open_settings':
            print(f"До гуи - Пол: {self.gender}, Голос: {self.voice}, Имя: {self.name}")
            tts.va_speak("Открываю настройки", self.voice)
            sql_data = self.db_manage.data_for_gui()
            gui = BotSetting(self.name, self.gender, self.voice, sql_data)
            gui.run()
            self.name = gui.bot_name.get()
            self.gender = gui.cur_gender.get()
            self.voice = gui.voice
            print(f"После гуи - Пол: {self.gender}, Голос: {self.voice}, Имя: {self.name}")

        elif cmd == 'mouse_control':
            if not self.mouse_control:
                self.ms = MouseThread()
                self.ms.start()
                self.mouse_control = True
                print("Start control")
            else:
                self.ms.need_term.set()
                self.ms.join()
                print("End control")
                self.mouse_control = False

        elif cmd == 'wrap':
            self.wind_manager.wrap()
        
        elif cmd == 'open':
            self.wind_manager.open_app()

        elif cmd == 'foreground':
            self.wind_manager.find_window_wildcard()
            self.wind_manager.set_foreground()

    def update_programs(self):
        def compare_names(app_name: str, exe_name: str):
            norm_app_name = app_name.lower().replace(" ", "")
            norm_exe_name = exe_name.lower().replace(" ", "")
            return (norm_app_name in norm_exe_name or norm_exe_name in norm_app_name)

        for app in winapps.list_installed():
            if app.install_location:
                if self.db_manage.is_exist_by_name(app.name):
                    continue
                # print(app.name, app.install_location,)
                need_exe = None
                size = 0
                try:
                    for el in app.install_location.glob('*.exe'):
                        low_name = el.name.lower()
                        if not ("unins" in low_name or "setup" in low_name or "install" in low_name):
                            # print(el.name)
                            # if app.name in el.name:
                            if compare_names(app.name, el.name):
                                need_exe = el
                                break
                            if os.path.getsize(el) > size:
                                need_exe = el
                                size = os.path.getsize(el)
                except:
                    pass
                if need_exe:
                    print(f"Data for DB - name: {app.name}; path: {str(need_exe)}")
                    self.db_manage.insert_data(app.name, str(need_exe))

    # начать прослушивание команд
    def start(self):
        stt.va_listen(self.va_respond)

if __name__ == "__main__":
    bt = BotV1()
    bt.start()