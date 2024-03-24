import subprocess
import os
import time
from pathlib import Path, WindowsPath
from winreg import *
import winapps
import pyautogui
import win32gui
import win32con
import re

# pyautogui.hotkey('win','d')
# pyautogui.hotkey('subtract')
# time.sleep(5)

class WindowMngr: 
    """Encapsulates some calls to the winapi for window management""" 
    def _init_ (self): 
        """Constructor""" 
        self._handle = None 
        
    def find_window(self, class_name, window_name=None): 
        """find a window by its class_name""" 
        self._handle = win32gui.FindWindow(class_name, window_name) 
        
    def _window_enum_callback(self, hwnd, wildcard): 
        """Pass to win32gui.EnumWindows() to check all the opened windows""" 
        # print(hwnd) 
        # 131802 
        print(str(win32gui.GetWindowText(hwnd))) 
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None: 
            self._handle = hwnd 
        
    def find_window_wildcard(self, wildcard): 
        """find a window whose title matches the wildcard regex""" 
        self._handle = None 
        win32gui.EnumWindows(self._window_enum_callback, wildcard) 
        
    def set_foreground(self): 
        """put the window in the foreground""" 
        print(self._handle) 
        # win32gui.ShowWindow(self._handle,win32con.SW_SHOW) 
        win32gui.ShowWindow(self._handle,win32con.SW_SHOWMAXIMIZED) 
        time.sleep(3)
        win32gui.SetForegroundWindow(self._handle) 

    def wrap(self):
        pyautogui.hotkey('win','d')

    def open_app(self, app_path: str):
        process = subprocess.Popen(app_path)

    

# files = glob.glob('F:/Super Bunny man/*.exe')
# p = WindowsPath('C:\Program Files (x86)\Fury Pro')
# print(p)
# print(p.name)
# print(str(p))
# for el in p.glob('*.exe'):
#     print(el)
#     print(el.name)
#     print(os.path.getsize(el))
    
# files = glob.glob(Path('C:\Program Files (x86)\Fury Pro\*.exe'))
# for file in files:
#     print(file)

# for root, dirs, files in os.walk("F:/Super Bunny man"):
#     print(files)
    
# w = WindowMgr()
# w.find_window_wildcard(".*Chrome.*")
# w.set_foreground()
# for app in winapps.list_installed():
#     if "Rockstar" in app.name:
#         print(app)
#     if app.install_location:
#         if type(app.install_location) is str:
#             print(type(app.install_location))
#             print(app,'\n')

# ##################### 
# for app in winapps.search_installed('Google Chrome'): 
#     g_app = app 
#     print(app)

# print(type(g_app))
# print(g_app.install_location)
# g_path = g_app.install_location
# process = subprocess.Popen(f"{g_path}/chrome.exe")
# process = subprocess.Popen(f"notepad")