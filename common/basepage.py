#!/usr/bin/evn python
# --coding = 'utf-8' --
import os
import atexit
import importlib
from common import utils
from common.log import log
from common.unexpectwin_system import UnExpectWin_System
from common.utils import Location, perform_sleep

"""所有页面基本操作，打开页面，关闭页面"""


def page_method_record(info):
    def wrapper(func):
        def dec(self, *args, **kwargs):
            if self.open_result:
                log.log_info(str(info))
                result = func(self, *args, **kwargs)
                return result

            log.log_error("failed " + str(info))

        return dec

    return wrapper


class BasePage:
    # 初始化函数，可传入进程路径进行打开进程，可传入进程名用于判断进程存在
    def __init__(self, do_pre_open=True, page_desc=None, delay_sec=0):
        perform_sleep(delay_sec)
        # 子类类名
        self.page_name = self.__class__.__name__
        # 子类文件路径
        self.filepath = importlib.import_module(self.__module__).__file__
        self.file_dir, self.filename_with_ext = os.path.split(self.filepath)
        # 子类文件名与扩展名
        self.filename, self.file_ext = os.path.splitext(self.filename_with_ext)
        # 关闭窗口允许执行变量，True为可执行，False为不可执行
        self.is_allow_close = True
        # 返回窗口允许执行变量，True为可执行，False为不可执行
        self.is_allow_back = True
        # 计算page_close的操作次数
        self.count_page_close = 0
        # 计算page_back的操作次数
        self.count_page_back = 0
        # 窗口句柄
        self.hwnd = None
        # 窗口对角坐标
        self.rect_pos = None
        # 启用尝试点击句柄窗口右上角坐标关闭
        self.enable_rect_pos_close = True

        class_resource_dict = self.get_init_by_name(self.file_dir, self.page_name)
        if class_resource_dict:
            self.page_desc = page_desc or class_resource_dict.get("page_desc", None)
            self.process_name = class_resource_dict.get("process_name", None)
            self.process_path = class_resource_dict.get("process_path", None)
            self.entry_pic = class_resource_dict.get("entry_pic", None)
            self.tab_pic = self.get_page_resource_pic(class_resource_dict.get("tab_pic", None))
            self.exit_pic = self.get_page_resource_pic(class_resource_dict.get("exit_pic", None))
            self.back_pic = self.get_page_resource_pic(class_resource_dict.get("back_pic", None))
            self.page_class = class_resource_dict.get("page_class", None)
            self.page_title = class_resource_dict.get("page_title", None)
        else:
            self.page_desc = page_desc
            self.process_name = None
            self.process_path = None
            self.entry_pic = None
            self.tab_pic = None
            self.exit_pic = None
            self.back_pic = None
            self.page_class = None
            self.page_title = None

        # 是否执行预打开操作
        self.do_pre_open = do_pre_open
        if self.do_pre_open:
            self.pre_open()

        self.open_result, self.position = self.get_pos(self)

        # 接入弹窗规避系统
        if not self.open_result:
            if self.unexpectwin_detect():
                if self.do_pre_open:
                    self.pre_open()
                self.open_result, self.position = self.get_pos(self)

        log.log_debug(f"{self.page_desc} open_result: {self.open_result}, position: {self.position}")
        assert self.open_result, log.log_error(f"{self.page_desc}页初始化失败")
        log.log_info(f"{self.page_desc}页初始化成功", screenshot=True)

        log.log_debug(f"{self.page_desc} hwnd = {self.hwnd}")

        # 注册析构函数
        atexit.register(self.page_del)

    def get_page_resource_pic(self, data):
        """
        获取页面标识图数据
        @param data: 页面资源文件中的 tab_pic
        @return:
        """
        if not data:
            return None

        pic_data_list = []

        if type(data) == str:
            pic_data_list.append(data)
        elif type(data) == list:
            pic_data_list = data

        for index, pic_data in enumerate(pic_data_list):
            if os.path.exists(pic_data):
                continue

            pic_data_list[index] = self.get_page_shot(pic_data)

        return pic_data_list

    # 此函数重载预打开界面的逻辑
    def pre_open(self):
        # TODO：执行打开动作
        pass

    # 打开界面函数，可传入点击入口图片进行点击打开操作，可传入标记图片判断界面打开成功与否
    def page_open(self):
        process_open_success = 0
        process_name_exists_success = 0
        click_entry_pic_success = 0

        self.open_result, self.position = False, (0, 0)
        # 通过进程路径打开界面
        if self.process_open(self) and self.do_pre_open:
            process_open_success = 1

        # 检查进程是否存在
        if self.process_name:
            if utils.is_process_exists(self.process_name):
                process_name_exists_success = 1
            else:
                process_name_exists_success = 2

        # 点击入口图片位置
        if self.entry_pic:
            find_result, click_position = self.get_resourse_pic(self.entry_pic, 5, Location.LEFT_UP.value)
            if find_result:
                utils.mouse_click(click_position)
                click_entry_pic_success = 1

        # 检查标记图片判断界面打开情况
        if self.tab_pic:
            find_result, self.position = self.get_resourse_pic(self.tab_pic, 5, Location.LEFT_UP.value)

            # 再次判断检查进程是否存在，防止进程启动缓慢问题
            if self.process_name:
                if utils.is_process_exists(self.process_name):
                    process_name_exists_success = 1
                else:
                    process_name_exists_success = 2

            if find_result:
                if process_open_success == 1:
                    self.open_result = True
                if process_name_exists_success != 2:
                    self.open_result = True

        elif click_entry_pic_success == 1:
            self.open_result = True

        # 返回处理
        if process_open_success == 1 and process_name_exists_success == 1:
            self.open_result = True

        return self.open_result, self.position

    def page_back(self):
        if not self.is_allow_back or not self.page_is_exist():
            return True

        if self.back_pic and self.page_is_exist():  # 使用exit图来进行关闭窗口
            find_result, back_position = self.get_resourse_pic(self.back_pic, 3, Location.CENTER.value,
                                                               sim_no_reduce=True, hwnd=self.hwnd)
            if not find_result:
                log.log_info(f"{self.page_desc}页无需返回")
            else:
                log.log_info(f"{self.page_desc}找到返回按钮")
                utils.mouse_click(back_position)
                utils.mouse_move(0, 0)
                perform_sleep(1)

        return True

    def page_close(self):
        if not self.is_allow_close or not self.page_is_exist():
            return True

        # 先使用坐标点进行关闭窗口，重试的话就不再使用pos关闭了，避免误操作其它窗口关闭。
        if self.enable_rect_pos_close and self.rect_pos and self.count_page_close < 1:
            exit_position = self.rect_pos[2] - 10, self.rect_pos[1] + 10
            utils.mouse_click(exit_position)
            utils.mouse_move(0, 0)
            perform_sleep(1)
        elif self.exit_pic and self.page_is_exist():  # 使用exit图来进行关闭窗口
            find_result, exit_position = self.get_resourse_pic(self.exit_pic, 3, Location.CENTER.value,
                                                               sim_no_reduce=True, hwnd=self.hwnd)
            if not find_result:
                log.log_error(f"查找{self.page_desc}页关闭按钮失败")
                return False
            utils.mouse_click(exit_position)
            utils.mouse_move(0, 0)
            perform_sleep(1)

        # 页面二次确认关闭
        if self.page_is_exist():
            self.page_confirm_close()
            perform_sleep(1)

        # 接入弹窗规避系统
        if self.page_is_exist():
            self.unexpectwin_detect()
            perform_sleep(1)

        if self.count_page_close < 1 and self.page_is_exist():  # 这里控制page_close只进来重试执行一次
            self.count_page_close += 1
            log.log_info(f"重试{self.page_desc}页关闭按钮")
            return self.page_close()
        log.log_info(f"点击{self.page_desc}页关闭按钮成功")
        self.is_allow_close = False

        utils.attach_screenshot(f"{self.page_desc}页关闭")
        return True

    # 规避弹窗系统检测
    def unexpectwin_detect(self):
        unwinsys = UnExpectWin_System()
        unwinclosepos = unwinsys.find_closepos_by_screen()
        if unwinclosepos and unwinclosepos != (0, 0):
            log.log_info("点击关闭弹窗关闭按钮坐标 " + str(unwinclosepos))
            utils.mouse_click(unwinclosepos)
            return True
        return False

    def page_del(self, unregister=False):
        """
        页面析构函数（解决__del__中使用open报错的问题）
        @param unregister: 是否注销 __init__ 时注册的页面析构函数
        @return:
        """
        if unregister:
            atexit.unregister(self.page_del)

        self.page_close()

    def page_confirm_close(self):
        """页面二次确认关闭（用于关闭点击关闭按钮后二次确认关闭弹窗，默认为空）"""
        # TODO：执行二次关闭动作
        pass

    def page_is_exist(self):
        # 先判断tab标识存在
        if self.tab_pic and \
                self.get_resourse_pic(self.tab_pic, location=Location.LEFT_UP.value, retry=2, sim_no_reduce=True)[0]:
            return True

        # 万一tab被挡的话就判断句柄
        if self.hwnd and utils.is_hwnd_exist(self.hwnd):
            return True

        return False

    def get_page_shot(self, shot_name):
        """
        根据文件名获取页面截图
        @param shot_name: 截图文件名
        @return:
        """
        page_shot_dir = os.path.join(os.path.dirname(self.file_dir), "PageShot", self.filename)
        assert os.path.exists(page_shot_dir), f"读取页面截图文件夹失败: {page_shot_dir}"

        page_shot_path = os.path.join(page_shot_dir, shot_name)
        assert os.path.exists(page_shot_path), f"获取页面截图文件路径失败: {page_shot_path}"

        return page_shot_path

    @staticmethod
    def process_open(self):
        if self.process_path:
            if not str(self.process_path).endswith(".exe"):
                return False
            if utils.process_start(self.process_path):
                return True
        return False

    @staticmethod
    def get_init_by_name(file_dir, page_name):
        page_resource_path = os.path.join(os.path.dirname(file_dir), "page_resource.py")
        assert os.path.exists(page_resource_path), "读取page_resource.py文件失败"

        # 动态引入项目目录下的page_resource.py
        module_name = ".".join([os.path.basename(os.path.dirname(file_dir)), "page_resource"])
        page_resource_module = importlib.import_module(module_name)
        page_resource = getattr(page_resource_module, "page_resource")

        return page_resource.get(page_name, None)

    @staticmethod
    def get_pos(self, retry=5):
        """
        获取窗口左上角tab坐标
        """
        open_result = False  # 打开窗口成功返回参数
        tab_position = None  # 左上角tab坐标返回参数

        # 先使用通过tab图获取坐标
        if self.tab_pic:
            open_result, tab_position = self.get_resourse_pic(self.tab_pic, retry, Location.LEFT_UP.value)
            if not self.hwnd and tab_position:  # 通过移动鼠标到窗口位置查找句柄
                utils.mouse_move(tab_position[0] + 2, tab_position[1] + 2)
                perform_sleep(0.5)
                new_hwnd = utils.get_hwnd_by_mouse_pos()
                new_rect_pos = utils.get_pos_by_hwnd(new_hwnd)
                # 通过鼠标位置获取到句柄后计算窗口坐标与tab图位置，差值大时则不使用此句柄（当tab图不是左上角的图时，也会不满足此条件）
                if abs(tab_position[0] - new_rect_pos[0]) < 10 and abs(tab_position[1] - new_rect_pos[1]) < 10:
                    self.hwnd = new_hwnd
                    self.rect_pos = new_rect_pos

        # 如果上面方法失败，则使用类名获取句柄和坐标
        if self.page_class and not self.hwnd:
            for i in range(0, 3, 1):
                self.hwnd = utils.get_hwnd_by_class(self.page_class, self.page_title)
                if self.hwnd:
                    self.rect_pos = utils.get_pos_by_hwnd(self.hwnd)
                    if self.rect_pos:
                        tab_position = self.rect_pos[0] + 2, self.rect_pos[1] + 2  # 多加2个像素避免太靠边缘
                        if tab_position != (2, 2):
                            open_result = True
                            return open_result, tab_position

                if not self.do_pre_open:
                    perform_sleep(2)  # 如果是通过第三方打开页面初始化的，通过句柄获取窗口坐标的方法，等待2秒重试3次

        return open_result, tab_position

    @staticmethod
    def get_resourse_pic(pic, retry, location, sim_no_reduce=True, hwnd=None):
        open_result = False

        pic_list = []
        if type(pic) == str:
            pic_list.append(pic)
        elif type(pic) == list:
            pic_list = pic

        for p in pic_list:
            open_result, tab_position = utils.find_element_by_pic(p, 0.8, retry=retry, location=location,
                                                                  sim_no_reduce=sim_no_reduce, hwnd=hwnd)
            if open_result:
                return open_result, tab_position

        return open_result, None

# if __name__ == '__main__':
#     bp = BasePage()
#     tab_baibaoxiang = os.path.join(os.getcwd(), "cutpic", "tab_baibaoxiang.png")
#     entry_baibaoxiang = os.path.join(os.getcwd(), "cutpic", "entry_baibaoxiang.png")
#     r, p = bp.page_open(entry_baibaoxiang, tab_baibaoxiang)
#     log.log_debug(r, p)
