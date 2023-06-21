import win32con
import win32gui
import win32api

def get_window_handle(lpClassName=None,lpWindowTitle=None):
    try:
        handle = win32gui.FindWindow(lpClassName,lpWindowTitle)
    except:
        print("Something Error")
    return handle

def get_window_title(handle):
    try:
        title = win32gui.GetWindowText(handle)
    except:
        print("Something Error")
    return title

def get_window_classname(handle):
    try:
        class_name = win32gui.GetClassName(handle)
    except:
        print("Something Error")
    return class_name


