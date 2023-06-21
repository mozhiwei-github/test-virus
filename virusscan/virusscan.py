from common.utils import *
from commonmethod import *
from pywinauto.application import Application


if __name__ == '__main__':
    # virusmodel_path
    virusmodel_path = r"C:\project\virustest\virusscan\virusmodel\virusmodel.png"
    # duba
    duba_kismainexe_path = r"C:\Program Files (x86)\kingsoft\kingsoft antivirus\kismain.exe"
    if not is_process_exists("kxescore.exe"):
        # 启动duba
        app = Application().start(duba_kismainexe_path)
        while True:
            if is_process_exists("kxescore.exe"):
                break
        print("duba process start success")
    else:
        print("duba process existed")
    # 打开样本右键菜单
    click_right_element_by_pic(virusmodel_path,sim=0.8,retry=1)
    time.sleep(1)
    # 选择右键菜单duba扫描
    duba_rightmenu_path = r"C:\project\virustest\virusscan\duba\duba_rightmenu.png"
    click_element_by_pic(duba_rightmenu_path,sim=0.7,retry=2)
    time.sleep(1)
    # 判断是否进入扫描界面
    duba_scaning_page_path = r"C:\project\virustest\virusscan\duba\duba_scaning.png"
    duba_finish_page_path = r"C:\project\virustest\virusscan\duba\duba_finish_scan.png"
    while True:
        if page_exist_judge(duba_scaning_page_path):
            # 每隔5s判断一次
            time.sleep(5)
        elif page_exist_judge(duba_finish_page_path):
            print("*****Virusmodel Scan Finished*****")
            break





