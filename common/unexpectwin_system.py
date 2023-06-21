import requests
import json

from idna import unicode

from common import utils
from common.log import log


class UnExpectWin_System(object):
    def __init__(self):
        utils.screenshot(utils.screen_temp_pic_name)
        self.img_screen = utils.screen_temp_pic_name

    def find_closepos_by_screen(self):
        file = open(self.img_screen, "rb")
        files = {"file_name": file}
        response = requests.request("post", "http://autotest.cf.com/interface/findunexpectwin", files=files)
        r = json.loads(unicode(response.content, "utf-8"))
        if r["ret"] == "success" and r["result"]["sid"] != 0:
            log.log_info("查找弹窗信息成功返回 " + str(r["result"]))
            return int(r["result"]["closepos_by_screen"][0]), int(r["result"]["closepos_by_screen"][1])
        elif r["ret"] == "success" and r["result"]["sid"] == 0:
            log.log_info("查找弹窗信息失败返回 " + str(r["result"]))
            return int(r["result"]["closepos_by_screen"][0]), int(r["result"]["closepos_by_screen"][1])
        elif r["ret"] == "failed":
            log.log_info("查找弹窗信息出错" + str(r))
            return None
        else:
            return None


if __name__ == '__main__':
    unwinsys = UnExpectWin_System()
    unwinclosepos = unwinsys.find_closepos_by_screen()
    utils.mouse_click(unwinclosepos)
