from common.utils import *
import time
from pywinauto.application import Application
import os

# 启动进程并等待进程/服务起来
def process_started(process_name,process_path):
    pass

def page_exist_judge(page_path):
    ret,pos = find_element_by_pic(page_path,sim=0.9,retry=1,sim_no_reduce=False)
    return ret

def duba_log_operate(operation):
    output = r""

    duba_log_clear_button_path = r"C:\project\virustest\virusscan\duba\duba_log_clear_button.png"
    duba_log_close_button_path = r"C:\project\virustest\virusscan\duba\duba_log_close_button.png"
    duba_log_output_button_path = r"C:\project\virustest\virusscan\duba\duba_log_output_button.png"
    duba_log_clear_sure_form_path = r"C:\project\virustest\virusscan\duba\duba_log_clear_sure_form.png"
    duba_log_clear_sure_button_path = r"C:\project\virustest\virusscan\duba\duba_log_clear_sure_button.png"
    duba_log_clear_finish_path = r"C:\project\virustest\virusscan\duba\duba_log_clear_finish.png"

    if operation == "clear":
        click_element_by_pic(duba_log_clear_button_path,sim=0.95,retry=1)
        time.sleep(0.5)
        while True:
            if page_exist_judge(duba_log_clear_sure_form_path):
                break
        click_element_by_pic(duba_log_clear_sure_button_path,sim=0.95,retry=1)
        time.sleep(1)
        # 验证清理完成
        click_element_by_pic(duba_log_output_button_path, sim=0.95, retry=1)
        while True:
            if page_exist_judge(duba_log_clear_finish_path):
                print("log clear finished")
                click_element_by_pic(duba_log_clear_sure_button_path, sim=0.95, retry=1)
                break

    elif operation == "output":
        click_element_by_pic(duba_log_output_button_path,sim=0.95,retry=1)
        time.sleep(0.5)
        app = Application().connect(title="另存为")


    else:  # operation == "close"
        click_element_by_pic(duba_log_close_button_path,sim=0.95,retry=1)



# 封装duba 获取日志
def get_duba_log(duba_kavlog_path,log_exe_path,duba_logexe_cancel_path):
    os.popen(duba_kavlog_path)
    while True:
        ret,pos1 = find_element_by_pic(log_exe_path,sim=0.9,retry=1,sim_no_reduce=False)
        if ret:
            break
    while True:
        ret,pos2 = find_element_by_pic(duba_logexe_cancel_path,sim=0.99,retry=1,sim_no_reduce=False)
        if ret:
            time.sleep(1)
        else:
            break
    duba_log_operate("clear")




