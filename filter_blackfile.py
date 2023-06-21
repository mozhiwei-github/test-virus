import os
from common import utils
import time

pop_sample_path = os.path.join(os.getcwd(), "blacksample")
button_path = os.path.join(os.getcwd(),"button")
clear_button_360_path = "./button/360/clear_button_360.png"
clear_button_duba_path = "./button/duba/clear_button_duba.png"
clear_and_more_360_path = f"./button/360/button_360/clear_and_more_360.png"
more_360_path = f"./button/360/button_360/more_360.png"
more_clear_path = f"./button/360/button_360/more_clear.png"


def do_virus_test(product_name,sample_path,wait_time):
    file_sample_list = []  # sample_path
    for root,dirs,files in os.walk(sample_path): # 查询样本
        for name in files:
            path = os.path.join(root,name)
            file_sample_list.append([name,path])  # 样本list [['2.jpg.exe', 'C:\\Users\\admin\\Desktop\\安全组\\autotest\\2.jpg.exe'], ['防黑墙.bat', 'C:\\Users\\admin\\Desktop\\安全组\\autotest\\防黑墙.bat']]

    black_file_sample_list = [] # black_file_sample
    for root, dirs, files in os.walk(pop_sample_path+'\\'+product_name, topdown=False): #弹泡类型列表
        for name in files:
            filename = os.path.join(root, name)
            black_file_sample_list.append(filename)   # 弹泡样式

    button_list = []
    for root, dirs,files in os.walk(button_path+'\\'+product_name+'\\button_'+product_name,topdown=False):
        for name in files:
            filename = os.path.join(root,name)
            button_list.append(filename)

    for i in file_sample_list:      # 遍历list获取样本
        utils.process_start(i[1],async_start=True)    # 执行样本
        # 一般黑样本在程序调起后会立即弹出拦截
        time.sleep(1)
        #return example:(680, 371) C:\project\virustest\popsample\duba\XiTongBaoHu\XiTongBaoHu.png
        ret, pos, picname = utils.find_element_by_pics(black_file_sample_list, sim=0.95, retry=1, sim_no_reduce=True,
                                                        use_history_capture=False)
        if ret:    #命中黑名单
            print("this file is a virus")
            if product_name =="duba":
                utils.click_element_by_pic(clear_button_duba_path, sim=0.8, retry=1, hwnd=None, sim_no_reduce=False)
            else:
                utils.click_element_by_pic(clear_button_360_path, sim=0.8, retry=1, hwnd=None, sim_no_reduce=False)
                ret2, pos, picname = utils.find_element_by_pic(clear_and_more_360_path, sim=0.95, retry=1,
                                                              sim_no_reduce=True,
                                                              use_history_capture=False)
                if ret2:
                    utils.click_element_by_pic(more_360_path, sim=0.8, retry=1, hwnd=None, sim_no_reduce=False)
                    utils.click_element_by_pic(more_clear_path, sim=0.8, retry=1, hwnd=None, sim_no_reduce=False)
            # 关闭弹窗后将该文件进程删除
            if utils.is_process_exists(i[1]):
                cmdshell = 'taskkill /im ' + i[0] + ' /F'
                os.system(cmdshell)
                print("该样本进程已退出")
            else:
                print("该样本进程不存在")
            # 关闭进程后将该文件删除
            utils.remove_path(i[0])
            print("该样本已成功删除")

        else:# 如果不是黑名单文件，有可能弹出了其他弹窗，需要将其他弹窗均关闭避免对接下来的样本验证造成误差
            for num in range(5):
                ret, pos, picname = utils.find_element_by_pics(button_list, sim=0.95, retry=1,
                                                               sim_no_reduce=True,use_history_capture=False)
                if ret:
                    print("此文件不是黑文件且弹出了其他弹窗/一定时间内没有任何拦截行为弹窗")
                    # 阻止该样本进行其他的行为
                    utils.mouse_click_tuple(pos)
                time.sleep(1)
            # 不删除该文件,将其进程退出，避免造成其他样本的干扰
            if utils.is_process_exists(i[1]):
                cmdshell = 'taskkill /im ' + i[0] + ' /F'
                os.system(cmdshell)
                print("该样本进程已退出")
            else:
                print("该样本进程不存在")

if __name__ == '__main__':
    sample_path = r"C:\Users\admin\Desktop\安全组\autotest"
    product_name = 'duba'
    wait_time = 60
    do_virus_test(product_name, sample_path,wait_time)
