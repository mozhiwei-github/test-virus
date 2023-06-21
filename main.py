import os
from common import utils
import time
pop_sample_path = os.path.join(os.getcwd(), "popsample")


def do_virus_test(product_name,sample_path,wait_time):
    file_title_list = []
    file_top_list = []
    file_sample_list = []  #sample_path
    for root,dirs,files in os.walk(sample_path): #查询样本
        for name in files:
            path = os.path.join(root,name)
            file_sample_list.append([name,path])  #样本list [['2.jpg.exe', 'C:\\Users\\admin\\Desktop\\安全组\\autotest\\2.jpg.exe'], ['防黑墙.bat', 'C:\\Users\\admin\\Desktop\\安全组\\autotest\\防黑墙.bat']]
        print("file_sample_list:  ")
        print(file_sample_list)

    for root, dirs, files in os.walk(pop_sample_path+'\\'+product_name, topdown=False): #弹泡类型列表
        for name in files:
            filename = os.path.join(root, name)
            if filename.find("title") > 0:
                file_title_list.append(filename)   #弹泡样式title
            else:
                file_top_list.append(filename)    #弹泡样式top
    for i in file_sample_list:      #遍历list获取样本
        utils.process_start(i[1],async_start=True)    #执行样本
        starttime = time.time()
        #while utils.is_process_exists(i[0]):
        while True:
            endtime = time.time()
            if endtime< starttime + wait_time:
                #return example:(680, 371) C:\project\virustest\popsample\duba\XiTongBaoHu\XiTongBaoHu.png
                ret, pos, picname = utils.find_element_by_pics(file_top_list, sim=0.95, retry=1, sim_no_reduce=True,
                                                               use_history_capture=False)
                if ret:    #命中拦截类型
                    print("识别到标签图片")
                    print(pos, picname)
                    utils.screenshot(filename = ".\\screen_pictures\\"+i[0]) # 若不是黑名单泡泡则截图记录
                    ret, pos, picname = utils.find_element_by_pics(file_title_list, sim=0.95, retry=1, sim_no_reduce=True,
                                                                use_history_capture=True)
                    if ret: # 命中拦截类型
                        print("识别到title图片")
                        print(pos, picname)
                    else:
                        print("未识别到title")
                else:
                    print("未识别到对应类型")
                utils.perform_sleep(1)
                pass
            else:
                print("该进程该次判断已结束")
                #cmdshell = 'taskkill /im '+i[0]+' /F'
                #os.system(cmdshell)
                break

if __name__ == '__main__':
    sample_path = r"C:\Users\admin\Desktop\安全组\autotest"
    product_name = 'duba'
    wait_time = 60
    do_virus_test(product_name, sample_path,wait_time)
