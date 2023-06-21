from common.utils import *
from commonmethod import *
from pywinauto.application import Application
import win32gui
import win32con
import win32api


if __name__ == '__main__':

    # 判断是否进入扫描界面
    # duba_scaning_page_path = r"C:\project\virustest\virusscan\duba\duba_scaning.png"
    # duba_finish_page_path = r"C:\project\virustest\virusscan\duba\duba_finish_scan.png"
    # duba_log_exe_path = r"C:\project\virustest\virusscan\duba\log_exe_operate.png"
    # duba_kavlog_path = r"c:\Program Files (x86)\kingsoft\kingsoft antivirus\kavlog2.exe"
    # duba_logexe_refresh_path = r"C:\project\virustest\virusscan\duba\log_exe_operate.png"
    # duba_logexe_cancel_path = r"C:\project\virustest\virusscan\duba\logexe_cancel.png"

    # while True:
    #     ret, pos = find_element_by_pic(duba_log_output_button_path, sim=0.9, retry=1, sim_no_reduce=True)
    #     if ret:
    #         print(f"pos = {pos}")
    #         mouse_click(pos)
    #         break
    #     else:
    #         print("no such element")


    handle = win32gui.FindWindow(None,"另存为")
    print(handle)
    classname = win32gui.GetClassName(handle)
    print(classname)
    handle2 = win32gui.FindWindow("ComboBoxEx32",None)
    print(handle2)
    hwndChildList = []
    win32gui.EnumChildWindows(handle,lambda hwnd,param:param.append(hwnd),hwndChildList)
    print(hwndChildList)
    subHandle = win32gui.FindWindowEx(handle,0,"ComboBoxEx32",None)
    print(subHandle)
    subHandle2 = win32gui.FindWindowEx(subHandle, 0, "ComboBox", None)
    print(subHandle2)
    subHandle3 = win32gui.FindWindowEx(subHandle2, 0, "Edit", None)
    print(subHandle3)

    # s = "444"
    win32api.SendMessage(subHandle3,win32con.WM_SETTEXT,0,"dkjfh".encode('utf-8'))
    # win32api.SendMessage(subHandle, win32con.WM_SETTEXT, 0, s.encode('gbk'))



    #get_duba_log(duba_kavlog_path,duba_log_exe_path,duba_logexe_cancel_path)






