from common import utils
import os
import time


# 毒霸渠道下，将文件名改为g1r2a3y_ks，以使得其设置为灰文件
def change_file_name(file_path,current_name,change_name):
    old_name = os.path.join(file_path,current_name)
    new_name = os.path.join(file_path,change_name)
    dirs = os.listdir(file_path)
    for dir in dirs:
        if dir == current_name:
            os.rename(old_name,new_name)

# 恢复虚拟机镜像
def restore_vm_system(vm_system_manage_button_path,vm_chance_system_path,vm_besure_chance_system_path,vm_windows_desktop_path):
    ret, pos = utils.find_element_by_pic(vm_system_manage_button_path, sim=0.95, retry=1, sim_no_reduce=True)
    if ret:
        utils.mouse_click_tuple(pos)
        time.sleep(3)
    ret, pos = utils.find_element_by_pic(vm_chance_system_path, sim=0.95, retry=1, sim_no_reduce=True)
    if ret:
        utils.mouse_dclick_tuple(pos)
        time.sleep(3)
        ret, pos = utils.find_element_by_pic(vm_besure_chance_system_path, sim=0.95, retry=1, sim_no_reduce=True)
        if ret:
            pos = (1046, 573)
            utils.mouse_click_tuple(pos)
        else:
            pass
    else:
        print("system not existed")
    # 循环等待虚拟机切换镜像完成
    while True:
        ret, pos = utils.find_element_by_pic(vm_windows_desktop_path, sim=0.95, retry=1, sim_no_reduce=True)
        if ret:
            print("虚拟机恢复镜像完成")
            break

if __name__ == '__main__':
    test_picture_num = 1
    # 打开vmware workspace
    vmware_path = f'C:\\Program Files (x86)\\VMware\\VMware Workstation\\vmware.exe'
    utils.process_start(vmware_path,async_start=True)
    time.sleep(2)
    # 将vmwarestation窗口设置为最大化
    # filename = ".\\testpictures\\"+str(test_picture_num)+".jpg"
    # utils.screenshot(filename= filename)
    test_picture_num+=1
    # pic_picture = filename + ".jpg"
    vm_windowsize_picture_path = "vm/vm_windowsize.png"
    ret,pos = utils.find_element_by_pic(vm_windowsize_picture_path,sim=0.95, retry=1, sim_no_reduce=True)
    if ret:
        utils.mouse_click_tuple(pos)
    else:
        print("虚拟机窗口已经是最大化了")
    # 打开指定虚拟机操作系统
    vm_chance_operation_picture_path = ".\\vm\\vm_chance_operation.png"
    ret,pos = utils.find_element_by_pic(vm_chance_operation_picture_path,sim=0.95,retry=1,sim_no_reduce=True)
    if ret:
        print("存在该操作系统")
        utils.mouse_click_tuple(pos)
        time.sleep(3)
    vm_system_manage_button_path = ".\\vm\\vm_system_manage_button.png"
    vm_chance_system_path = ".\\vm\\vm_chance_system.png"
    vm_besure_chance_system_path = ".\\vm\\vm_besure_chance_system.png"
    vm_windows_desktop_path = ".\\vm\\vm_windows_desktop.png"
    restore_vm_system(vm_system_manage_button_path, vm_chance_system_path, vm_besure_chance_system_path,
                          vm_windows_desktop_path)




