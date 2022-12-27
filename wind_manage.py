import win32gui
import win32con
import re
import time

class WindowMgr: 
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