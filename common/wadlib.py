# _*_ coding:UTF-8 _*_
# window application driver类实现库方法

import os
import requests, time
from appium import webdriver
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from common.contants import InputLan
from common.log import log
from common import utils
from selenium.webdriver import ActionChains
from common.utils import is_process_exists


# app调用wad方法类
class wadlib(object):
    def __init__(self, app_path=None, appArguments=None, appTopLevelWindow=None, appWorkingDir=None,
                 platformName="Windows", platformVersion=1.0, execute_url="http://127.0.0.1:4723"):
        if not is_process_exists("WinAppDriver.exe"):
            assert "WinAppDriver.exe is not running"

        self.app_path = app_path
        self.appArguments = appArguments
        self.appTopLevelWindow = appTopLevelWindow
        self.appWorkingDir = appWorkingDir
        self.platformName = platformName
        self.platformVersion = platformVersion
        self.execute_url = execute_url
        self.desired_caps = {
            "platformName": self.platformName,
            "platformVersion": self.platformVersion
        }
        if app_path:
            self.desired_caps["app"] = self.app_path
        if appArguments:
            self.desired_caps["appArguments"] = self.appArguments
        if appTopLevelWindow:
            self.desired_caps["appTopLevelWindow"] = self.appTopLevelWindow
        if appWorkingDir:
            self.desired_caps["appWorkingDir"] = self.appWorkingDir

        # wad driver 驱动对象
        self.driver: WebDriver()
        self.load(self.execute_url, self.desired_caps)

    # def __del__(self):
    #     self.session_close()

    # 重新加载页面元素，返回给driver
    def load(self, execute_url=None, desired_caps=None):
        if not execute_url and not desired_caps:
            execute_url = self.execute_url
            desired_caps = self.desired_caps
        self.driver = webdriver.Remote(command_executor=execute_url, desired_capabilities=desired_caps)
        return self.driver

    # 重新(多次)加载页面元素，返回给driver
    def new_load(self, execute_url=None, desired_caps=None):
        sign, count = 2, 1
        if not execute_url and not desired_caps:
            execute_url = self.execute_url
            desired_caps = self.desired_caps
        while True:
            try:
                self.driver = webdriver.Remote(command_executor=execute_url, desired_capabilities=desired_caps)
            except WebDriverException:
                sign = 1
                log.log_info("刷新失败，当前失败次数:%s" % count)
            if sign == 2:
                return self.driver
            sign += 1
            count += 1
            if count > 3:
                return False
            utils.perform_sleep(2)

    # 返回系统信息,系统版本等
    def status(self):
        r = requests.get(self.execute_url + "/status").json()
        return r

    # 关闭session对象
    def session_close(self):
        r = requests.post(self.execute_url + "/session/" + self.driver.session_id + "/appium/app/close").json()
        if r.get("status", None) == 0:
            return True
        else:
            return False

    def session_post_operation(self, api_name, pdata={}):
        r = requests.post(self.execute_url + "/session/" + self.driver.session_id + api_name, json=pdata).json()
        print(r)
        if r.get("status", None) == 0:
            return r
        else:
            return None

    def session_get_operation(self, api_name):
        r = requests.get(self.execute_url + "/session/" + self.driver.session_id + api_name).json()
        print(r)
        if r.get("status", None) == 0:
            return r
        else:
            return None

    # 获取窗口句柄
    def get_window_handle(self):
        ret = self.session_get_operation("/window_handle")
        if ret.get("status", None) == 0:
            return ret.get("value")
        else:
            return None

    # 获取元素相对屏幕的坐标，实际上相对的是父窗体
    def get_element_position(self, by_type, value):
        # pos = None
        window_position = self.driver.get_window_position()
        try:
            el = self.driver.find_element(by_type, value)
            el_position = el.location
            pos = (el_position["x"] + window_position["x"], el_position["y"] + window_position["y"])
        except:
            self.load()
            try:
                el = self.driver.find_element(by_type, value)
                el_position = el.location
                pos = (el_position["x"] + window_position["x"], el_position["y"] + window_position["y"])
            except:
                pos = None
        return pos

    # 根据name属性点击，并输入日志
    def click_find_by_name(self, name):
        try:
            self.driver.find_element_by_name(name).click()
            utils.perform_sleep(2)
            log.log_info("***点击【%s】***" % name)
        except NoSuchElementException:
            utils.attach_screenshot("失败原因")
            log.log_error("根据name找不到【%s】按钮位置" % name)

    # 根据name属性定位，模拟键盘回车
    def send_keys_enter(self, name):
        self.driver.find_element_by_name(name).send_keys(Keys.ENTER)

    # 根据xpath路径点击按钮
    def click_find_by_xpath(self, path):
        try:
            self.driver.find_element_by_xpath(path).click()
            utils.perform_sleep(2)
            log.log_info("***点击【%s】***" % path)
        except NoSuchElementException:
            utils.attach_screenshot("失败原因")
            log.log_error("根据【%s】路径找不到按钮位置" % path)

    # 根据classname属性找到输入框并输入对应内容
    def input_find_by_classname(self, name, text):
        try:
            box = self.driver.find_element_by_class_name(name)
            box.clear()
            utils.perform_sleep(1)
            box.send_keys(text)
            utils.perform_sleep(1)
            log.log_info("在输入框【%s】内输入内容：%s" % (name, text))
        except NoSuchElementException:
            utils.attach_screenshot("失败原因")
            log.log_error("找不到【%s】输入框位置，操作失败！" % name)

    # 根据name属性找到输入框并输入对应内容
    def input_find_by_name(self, name, text):
        try:
            box = self.driver.find_element_by_name(name)
            box.clear()
            utils.perform_sleep(1)
            box.send_keys(text)
            utils.perform_sleep(1)
            log.log_info("在输入框【%s】内输入内容：%s" % (name, text))
        except NoSuchElementException:
            log.log_error("找不到【%s】输入框位置，操作失败！" % name)

    # 通用点击方法，根据传入属性值找到对应的对象或对象集进行点击操作
    """
    所有的type类型请看by.py文件
    @"id"
    @"xpath"
    @"name"
    @"tag name"
    @"class name"
    """
    def click_find_elements_by_property(self, object_type, value, site, object_name=None):
        try:
            element = self.driver.find_elements(by=object_type, value=value)
            element[site].click()
            utils.perform_sleep(2)
            if object_name is None:
                log.log_info("***点击第[%s]个[%s]对象***" % (site, value))
            else:
                log.log_info("***点击[%s]***" % object_name)
        except NoSuchElementException:
            utils.attach_screenshot("失败原因")
            log.log_error("根据[%s]找不到值为[%s]的对象集" % (object_type, value))
        except NoSuchWindowException:
            utils.attach_screenshot("失败原因")
            log.log_error("窗口已关闭")

    # 查找子元素集
    def find_elements_by_property(self, father_type, father_value, child_type, child_value):
        try:
            father_element = self.driver.find_element(by=father_type, value=father_value)
            child_element = father_element.find_elements(by=child_type, value=child_value)
            return child_element
        except NoSuchElementException:
            utils.attach_screenshot("失败原因")
            log.log_error("根据父对象值[%s]找不到下属子对象为[%s]的对象集" % (father_value, child_value))
        except NoSuchWindowException:
            utils.attach_screenshot("失败原因")
            log.log_error("窗口已关闭")

    # 支持对象集点击
    def click_element_by_list(self, father_type, father_value, child_type, child_value, site=None, object_name=None):
        try:
            father_element = self.driver.find_element(by=father_type, value=father_value)
            child_element = father_element.find_elements(by=child_type, value=child_value)
            child_element[site].click()
            utils.perform_sleep(2)
            log.log_info("***点击[%s]***" % object_name)
        except NoSuchElementException:
            utils.attach_screenshot("失败原因")
            log.log_error("根据父对象值[%s]找不到下属子对象为[%s]的对象集" % (father_value, child_value))
        except NoSuchWindowException:
            utils.attach_screenshot("失败原因")
            log.log_error("窗口已关闭")

    # 实现对象的右键点击
    def right_click_by_path(self, element, element_name=None):
        try:
            ActionChains(self.driver).context_click(element).perform()
            utils.perform_sleep(2)
            if element_name is None:
                log.log_info("右键点击对象【%s】" % element)
            else:
                log.log_info("右键点击对象【%s】" % element_name)
        except AttributeError:
            utils.attach_screenshot("失败原因")
            log.log_error("找不到对象坐标")

    # 判断元素是否存在，返回结果
    def isElementPresent(self, by, value):
        try:
            element = self.driver.find_element(by=by, value=value)
        except NoSuchElementException:
            log.log_info("未找到该元素")
            return False
        except NoSuchWindowException:
            log.log_info("未找到该元素，当前窗口已关闭")
            return False
        else:
            return True

    # 获取当前窗口标题比较
    def file_open(self, name):
        title = self.driver.title
        if title == name:
            return True
        else:
            return False

    # 通过获取窗口标题时抛出的异常，判断当前窗口是否关闭
    def driver_exist(self):
        try:
            page = self.driver.title
        except NoSuchWindowException:
            log.log_info("当前对象已关闭")
            return True
        except WebDriverException:
            log.log_info("当前对象已关闭")
            return True
        else:
            log.log_info("当前对象未关闭")
            return False

    # 获取新的driver，支持多次尝试
    @staticmethod
    def new_driver(exe_path):
        global file_menu
        refresh_time, count = 2, 1
        while True:
            try:
                log.log_info("初始化次数:【%s】" % count)
                file_menu = wadlib(app_path=exe_path)
            except WebDriverException:
                refresh_time = 1
                log.log_info("初始化失败，当前失败次数:【%s】" % count)
            if refresh_time == 2:
                log.log_info("初始化对象成功！")
                return file_menu
            refresh_time += 1
            count += 1
            if count > 3:
                utils.attach_screenshot("失败原因")
                log.log_info("超出重试次数")
                return False
            utils.perform_sleep(3)

    # 切换窗口
    def switch_windows(self, title):
        try:
            all_handles = self.driver.window_handles
            if len(all_handles) == 1:
                self.driver.switch_to.window(all_handles[0])
                log.log_info("当前窗口切换->[%s]" % self.driver.title)
            else:
                for window_handle in all_handles:
                    self.driver.switch_to.window(window_handle)
                    if self.driver.title == title:
                        log.log_info("当前窗口切换->[%s]" % title)
                        break
        except NoSuchWindowException:
            utils.attach_screenshot("切换窗口失败")
            return False

    # 存在多个同名窗口时，根据窗口特定内容切换至对应窗口
    def switch_windows_to_condition(self, condition, value):
        try:
            for win_handle in self.driver.window_handles:
                self.driver.switch_to.window(win_handle)
                if self.isElementPresent(condition, value):
                    log.log_info("根据[%s]切换到对应窗口" % value)
                    break
        except NoSuchWindowException:
            utils.attach_screenshot("切换窗口失败")
            return False

    # 获取所有窗口标题
    def find_all_win_title(self):
        win_title_list = []
        for window_handle in self.driver.window_handles:
            self.driver.switch_to.window(window_handle)
            win_title_list.append(self.driver.title)
        return win_title_list


# 集成wadlib，系统桌面类
class windesktop(wadlib):
    def __init__(self):
        super().__init__(app_path="Root")
