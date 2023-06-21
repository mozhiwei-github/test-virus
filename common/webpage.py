import os
import time
import importlib
from common.log import log
from urllib.parse import urlsplit
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

"""Selenium Web页面基类"""


class WebPage(object):
    PageUrl = None  # 页面Url
    PageName = None  # 页面描述名称

    def __init__(self, driver, do_pre_open=True):
        """
        @param driver: WebDriver实例
        @param do_pre_open: 是否执行预打开操作
        """
        self.driver = driver
        self.driver_wait_dict = {}
        # 子类类名
        self.page_name = self.__class__.__name__
        # 子类文件路径
        self.filepath = importlib.import_module(self.__module__).__file__
        self.file_dir, self.filename_with_ext = os.path.split(self.filepath)
        # 子类文件名与扩展名
        self.filename, self.file_ext = os.path.splitext(self.filename_with_ext)

        # 设置全局隐式等待时间
        self.implicitly_wait(5)

        # 是否执行预打开操作
        if do_pre_open:
            self.pre_open()

        self.wait_page_loaded()  # 等待页面加载完成

        if self.PageUrl:  # 是否校验页面Url
            current_url = urlsplit(self.get_current_url())._replace(query='').geturl()  # 去除Url的query部分
            assert current_url == self.PageUrl, self.log_error(f"{self.PageName}Url校验失败，实际Url：{current_url}")

        self.log_info(f"{self.PageName}打开成功", screenshot=True)

    def open(self):
        """打开页面"""
        self.open_url(self.PageUrl)

    def pre_open(self):
        """预打开操作"""
        self.open()

    def open_url(self, url, screenshot=False):
        """
        打开网页
        @param url: 网页地址
        @param screenshot: 是否添加截图附件
        @return:
        """
        self.driver.set_page_load_timeout(30)

        if screenshot:
            driver = self.driver
        else:
            driver = None

        try:
            self.driver.get(url)
            log.log_info(f"打开网页：{url}", driver=driver)
        except TimeoutException:
            log.log_error(f"打开 {url} 超时，请检查网络或网址服务器", driver=self.driver)

    def find_element(self, locator, element=None, multiple=False):
        """
        查找元素
        @param locator: 元素定位器
        @param element: 查找基准元素，为空时使用 self.driver
        @param multiple: 为True时返回包含多个元素的数组，默认为 False 返回单个元素
        @return:
        """
        if not element:
            element = self.driver

        try:
            if multiple:
                return element.find_elements(*locator)
            else:
                return element.find_element(*locator)
        except NoSuchElementException as e:
            return [] if multiple else None
        except Exception as e:
            assert not e

    def get_driver_wait(self, timeout=10):
        """
        获取 WebDriverWait 实例
        @param timeout: 等待超时时间（秒）
        @return:
        """
        _wait = self.driver_wait_dict.get(timeout, None)
        if not _wait:
            _wait = WebDriverWait(self.driver, timeout)
            self.driver_wait_dict[timeout] = _wait
        return _wait

    def wait_element(self, locator, timeout=10, multiple=False):
        """
        等待元素
        @param locator: 元素定位器
        @param timeout: 等待超时时间（秒）
        @param multiple: 为True时返回包含多个元素的数组，默认为 False 返回单个元素
        @return:
        """
        if multiple:
            method = EC.presence_of_all_elements_located(*locator)
        else:
            method = EC.presence_of_element_located(*locator)

        return self.wait_util(method, timeout, f"{locator}元素")

    def wait_page_loaded(self, timeout=10, message=''):
        """
        等待页面加载完成
        @param timeout: 等待超时时间（秒）
        @param message: 描述信息
        @return:
        """
        return self.wait_util(lambda driver: driver.execute_script('return document.readyState;') == "complete",
                              timeout, message)

    def wait_util(self, method, timeout=10, message=''):
        """
        根据提供的方法等待直至返回元素或超时
        @param method: 元素查找方法
        @param timeout: 等待超时时间（秒）
        @param message: 描述信息
        @return:
        """
        _wait = self.get_driver_wait(timeout)

        try:
            result = _wait.until(method, message)
            if message:
                log.log_info(f"等待 {message} 完成")
            return result
        except TimeoutException as e:
            assert not e, self.log_error(f"等待{message}超时")
        except Exception as e:
            assert not e, self.log_error(f"等待{message}出错，err: {e}")

    def input_text(self, locator, text, select_all=False, element_name=None):
        """
        元素输入文本
        (输入前会先清空)
        @param locator: 元素定位器
        @param text: 字符串
        @param select_all: 输入前先全选输入框内容
        @param element_name: 元素描述名称
        @return:
        """
        ele = self.find_element(locator)
        ele_name = element_name or locator
        assert ele, f"查找元素 {ele_name} 失败"

        if select_all:  # 使用 ctrl + a 全选输入框
            ele.send_keys(Keys.CONTROL + "a")
        else:  # 清除输入框内容（不适用于会自动设置默认值的输入框）
            ele.clear()
        self.sleep(1)

        ele.send_keys(text)
        log.log_info(f"输入文本：{text}")
        return ele

    def get_text(self, locator):
        """获取元素的文本"""
        _text = self.find_element(locator).text
        log.log_info(f"获取文本：{_text}")
        return _text

    def get_title(self):
        """获取网页标题"""
        title = self.driver.title
        log.log_info(f"获取网页标题：{title}")
        return title

    def get_current_url(self):
        """获取当前页面Url"""
        return self.driver.current_url

    def click(self, locator, element_name=None, element=None):
        """
        点击元素
        @param locator: 元素定位器
        @param element_name: 元素描述名称
        @param element: 页面元素对象
        @return:
        """
        element = self.find_element(locator, element)
        name = element_name or locator
        assert element, self.log_error(f"未找到元素：{name}")
        self.element_click(element, name)

    def element_click(self, element, element_name, move_to_element=False, screenshot=False):
        """
        点击传入的元素
        @return:
        @param element: 页面元素对象
        @param element_name: 元素描述名称
        @param move_to_element: 是否移动到元素位置
        @param screenshot: 是否添加截图附件
        """
        try:
            if move_to_element:
                self.move_to_element(element, element_name)
                self.sleep(0.5)

            element.click()
            log.log_info(f"点击{element_name}元素成功", screenshot=screenshot, shot_delay=1)
        except ElementClickInterceptedException as e:
            assert not e, self.log_error(f"点击{element_name}元素失败")
        except Exception as e:
            assert not e, self.log_error(f"点击{element_name}元素失败，err: {e}")

    def move_to_element(self, element, element_name):
        """
        移动到元素
        @param element: 页面元素对象
        @param element_name: 元素描述名称
        @return:
        """
        ActionChains(self.driver).move_to_element(element).perform()
        log.log_info(f"滚动到{element_name}元素位置")

    def get_element_attribute(self, element, attribute_name):
        """
        获取页面元素属性值
        @param element: 页面元素对象
        @param attribute_name: 属性名称
        @return:
        """
        return element.get_attribute(attribute_name)

    def refresh(self, wait_loaded=True):
        """
        浏览器刷新
        @param wait_loaded: 执行后等待页面加载完成
        @return:
        """
        self.driver.refresh()
        self.log_info("点击浏览器刷新")

        if wait_loaded:
            self.wait_page_loaded()

    def back(self, wait_loaded=True, expect_url=None):
        """
        浏览器返回
        @param wait_loaded: 执行后等待页面加载完成
        @param expect_url: 执行后预期Url
        @return:
        """
        self.driver.back()
        self.log_info("点击浏览器返回")

        if wait_loaded:
            self.wait_page_loaded()

        if expect_url:
            assert expect_url == self.get_current_url(), self.log_error(f"页面Url校验失败")
            self.log_info(f"浏览器返回后页面Url校验成功：{expect_url}")

    def forward(self, wait_loaded=True, expect_url=None):
        """
        浏览器前进
        @param wait_loaded: 执行后等待页面加载完成
        @param expect_url: 执行后预期Url
        @return:
        """
        self.driver.forward()
        self.log_info("点击浏览器前进")

        if wait_loaded:
            self.wait_page_loaded()

        if expect_url:
            assert expect_url == self.get_current_url(), self.log_error(f"页面Url校验失败")
            self.log_info(f"浏览器前进后页面Url校验成功：{expect_url}")

    @property
    def get_source(self):
        """获取页面源代码"""
        return self.driver.page_source

    @staticmethod
    def sleep(seconds=0):
        """
        强制等待
        （可能会导致脚本运行时间过长）
        @param seconds: 等待秒数
        @return:
        """
        time.sleep(seconds)

    def implicitly_wait(self, seconds=0):
        """
        隐式等待
        （隐式等待相比强制等待更智能，顾明思义，在脚本中我们一般看不到等待语句，但是它会在每个页面加载的时候自动等待；
        隐式等待只需要声明一次，一般在打开浏览器后进行声明。声明之后对整个 driver 的生命周期都有效，后面不用重复声明。）
        @param seconds: 等待秒数
        @return:
        """
        self.driver.implicitly_wait(seconds)

    def log_info(self, msg, log_only=False, screenshot=False, attach=True, compress_rate=0.7, shot_delay=0):
        """
        输出Info级别日志
        @param msg: 日志信息
        @param title: allure附件信息的title
        @param log_only: 是否仅打印日志
        @param screenshot: 是否添加截图附件
        @param attach: 是否添加到allure报告附件
        @param compress_rate: 截图附件压缩比率
        @param shot_delay: 截图延迟秒数
        @return:
        """
        if screenshot:
            driver = self.driver
        else:
            driver = None

        log.log_info(msg, log_only=log_only, attach=attach, driver=driver, compress_rate=compress_rate,
                     shot_delay=shot_delay)

    def log_error(self, msg, log_only=False, attach=True, need_assert=False):
        """
        输出Error级别日志
        @param msg: 日志信息
        @param log_only: 是否仅打印日志
        @param attach: 是否添加到allure报告附件
        @param need_assert: 是否需要断言
        @return:
        """
        log.log_error(msg, log_only=log_only, attach=attach, need_assert=need_assert, driver=self.driver)

    def log_pass(self, msg, screenshot=True, compress_rate=0.7):
        """
        输出Pass级别日志
        @param msg: 日志信息
        @param screenshot: 是否添加截图附件
        @param compress_rate: 截图附件压缩比率
        @return:
        """
        if screenshot:
            attach = True
            driver = self.driver
        else:
            attach = False
            driver = None

        log.log_pass(msg, attach=attach, driver=driver, compress_rate=compress_rate)

    def verify_link_info(self, link_desc, element, link_info, check_text=True, check_href=True):
        """
        校验链接信息
        @param link_desc: 链接描述
        @param element: 链接元素
        @param link_info: 预期链接信息
        @param check_text: 是否校验text属性
        @param check_href: 是否检验href属性
        @return:
        """

        if check_text:
            self.log_info(f"预期 {link_desc} 文本：{link_info['text']}")
            self.log_info(f"实际 {link_desc} 文本：{element.text}")
            assert element.text == link_info["text"], self.log_error(f"{link_desc} 名称校验失败")

        if check_href:
            self.log_info(f"预期 {link_desc} 链接：{link_info['href']}")
            self.log_info(f"实际 {link_desc} 链接：{element.get_attribute('href')}")
            assert element.get_attribute('href') == link_info["href"], self.log_error(f"{link_desc} 链接校验失败")

        self.log_info(f"{link_desc} 校验成功")

    def get_page_shot(self, shot_name):
        """
        根据文件名获取页面截图文件
        @param shot_name: 截图文件名
        @return:
        """
        page_shot_dir = os.path.join(os.path.dirname(self.file_dir), "PageShot", self.filename)
        assert os.path.exists(page_shot_dir), "读取页面截图文件夹失败"

        page_shot_path = os.path.join(page_shot_dir, shot_name)
        assert os.path.exists(page_shot_path), "获取页面截图文件路径失败"

        return page_shot_path
