from common import utils
import os
import time


def clear_button_click(button_list,product_name):
    clear_and_more_360_path = f"./button/360/button_360/clear_and_more_360.png"
    more_360_path = f"./button/360/button_360/more_360.png"
    more_clear_path = f"./button/360/button_360/more_clear.png"
    ret,pos,picname = utils.find_element_by_pic(clear_and_more_360_path,sim=0.95, retry=1, sim_no_reduce=True,
                                                        use_history_capture=False)
    if ret:
            utils.click_element_by_pic(more_360_path, sim=0.8, retry=1, hwnd=None, sim_no_reduce=False)
            utils.click_element_by_pic(more_clear_path, sim=0.8, retry=1, hwnd=None, sim_no_reduce=False)
            print("")