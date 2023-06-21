# _*_ coding:UTF-8 _*_
import base64
import ctypes
import fileinput
import os
import subprocess
import time
import json
import shutil
import socket
import psutil
import hashlib
import random
import string
import allure
import colorsys
import importlib
from ctypes import *
from enum import Enum, unique
from common.log import log
from common.contants import logs_file
from common import start_cpu_percent


def try_import(module_name, element_name=None):
    """
    尝试引入模块（模块不存在时返回None）
    @param module_name: 模块名
    @param element_name: 模块内元素名称
    @return:
    """
    try:
        module_spec = importlib.util.find_spec(module_name)
    except Exception as e:
        return None
    if not module_spec:
        return module_spec

    module = importlib.import_module(module_name)

    if element_name:
        result = getattr(module, element_name)
    else:
        result = module

    return result


cv2 = try_import('cv2')
requests = try_import('requests')
win32api = try_import('win32api')
win32con = try_import('win32con')
win32gui = try_import('win32gui')
win32ui = try_import('win32ui')
win32clipboard = try_import('win32clipboard')
win32ui = try_import('win32ui')
pywintypes = try_import('pywintypes')
np = try_import('numpy')
ac = try_import('aircv')
np = try_import('numpy')
pyzbar = try_import('pyzbar.pyzbar')
Image = try_import('PIL.Image')
ImageGrab = try_import('PIL.ImageGrab')
unicode = try_import('idna', 'unicode')

"""常用功能函数"""

# 键位键值对
VK_CODE = {
    'backspace': 0x08,
    'tab': 0x09,
    'clear': 0x0C,
    'enter': 0x0D,
    'shift': 0x10,
    'ctrl': 0x11,
    'alt': 0x12,
    'pause': 0x13,
    'caps_lock': 0x14,
    'esc': 0x1B,
    'spacebar': 0x20,
    'page_up': 0x21,
    'page_down': 0x22,
    'end': 0x23,
    'home': 0x24,
    'left_arrow': 0x25,
    'up_arrow': 0x26,
    'right_arrow': 0x27,
    'down_arrow': 0x28,
    'select': 0x29,
    'print': 0x2A,
    'execute': 0x2B,
    'print_screen': 0x2C,
    'ins': 0x2D,
    'del': 0x2E,
    'help': 0x2F,
    '0': 0x30,
    '1': 0x31,
    '2': 0x32,
    '3': 0x33,
    '4': 0x34,
    '5': 0x35,
    '6': 0x36,
    '7': 0x37,
    '8': 0x38,
    '9': 0x39,
    'a': 0x41,
    'b': 0x42,
    'c': 0x43,
    'd': 0x44,
    'e': 0x45,
    'f': 0x46,
    'g': 0x47,
    'h': 0x48,
    'i': 0x49,
    'j': 0x4A,
    'k': 0x4B,
    'l': 0x4C,
    'm': 0x4D,
    'n': 0x4E,
    'o': 0x4F,
    'p': 0x50,
    'q': 0x51,
    'r': 0x52,
    's': 0x53,
    't': 0x54,
    'u': 0x55,
    'v': 0x56,
    'w': 0x57,
    'x': 0x58,
    'y': 0x59,
    'z': 0x5A,
    'numpad_0': 0x60,
    'numpad_1': 0x61,
    'numpad_2': 0x62,
    'numpad_3': 0x63,
    'numpad_4': 0x64,
    'numpad_5': 0x65,
    'numpad_6': 0x66,
    'numpad_7': 0x67,
    'numpad_8': 0x68,
    'numpad_9': 0x69,
    'multiply_key': 0x6A,
    'add_key': 0x6B,
    'separator_key': 0x6C,
    'subtract_key': 0x6D,
    'decimal_key': 0x6E,
    'divide_key': 0x6F,
    'F1': 0x70,
    'F2': 0x71,
    'F3': 0x72,
    'F4': 0x73,
    'F5': 0x74,
    'F6': 0x75,
    'F7': 0x76,
    'F8': 0x77,
    'F9': 0x78,
    'F10': 0x79,
    'F11': 0x7A,
    'F12': 0x7B,
    'F13': 0x7C,
    'F14': 0x7D,
    'F15': 0x7E,
    'F16': 0x7F,
    'F17': 0x80,
    'F18': 0x81,
    'F19': 0x82,
    'F20': 0x83,
    'F21': 0x84,
    'F22': 0x85,
    'F23': 0x86,
    'F24': 0x87,
    'num_lock': 0x90,
    'scroll_lock': 0x91,
    'left_shift': 0xA0,
    'right_shift ': 0xA1,
    'left_control': 0xA2,
    'right_control': 0xA3,
    'left_win': 0x5B,
    'right_win': 0x5C,
    'left_menu': 0xA4,
    'right_menu': 0xA5,
    'browser_back': 0xA6,
    'browser_forward': 0xA7,
    'browser_refresh': 0xA8,
    'browser_stop': 0xA9,
    'browser_search': 0xAA,
    'browser_favorites': 0xAB,
    'browser_start_and_home': 0xAC,
    'volume_mute': 0xAD,
    'volume_Down': 0xAE,
    'volume_up': 0xAF,
    'next_track': 0xB0,
    'previous_track': 0xB1,
    'stop_media': 0xB2,
    'play/pause_media': 0xB3,
    'start_mail': 0xB4,
    'select_media': 0xB5,
    'start_application_1': 0xB6,
    'start_application_2': 0xB7,
    'attn_key': 0xF6,
    'crsel_key': 0xF7,
    'exsel_key': 0xF8,
    'play_key': 0xFA,
    'zoom_key': 0xFB,
    'clear_key': 0xFE,
    '+': 0xBB,
    ',': 0xBC,
    '-': 0xBD,
    '.': 0xBE,
    '/': 0xBF,
    '`': 0xC0,
    ';': 0xBA,
    '[': 0xDB,
    '\\': 0xDC,
    ']': 0xDD,
    "'": 0xDE,
    '`': 0xC0}

screen_temp_pic_name = os.path.join(logs_file, "origin_pic.png")
CAPTURE_IMG_DATA_HISTORY = None


@unique
class Location(Enum):
    # 左上角为left_upper_corner，右上角为right_upper_corner，左下角left_bottom_corner， 右下角right_bottom_corner
    CENTER = "center"
    LEFT_UP = "left_upper_corner"
    RIGHT_UP = "right_upper_corner"
    LEFT_BOTTOM = "left_bottom_corner"
    RIGHT_BOTTOM = "right_bottom_corner"


class POINT(Structure):
    _fields_ = [("x", c_ulong), ("y", c_ulong)]


# 模拟键盘输入按键指令，key为VK_CODE的键值
def keyboardInputByCode(key):
    win32api.keybd_event(VK_CODE.get(key), 0, 0, 0)
    win32api.keybd_event(VK_CODE.get(key), 0, win32con.KEYEVENTF_KEYUP, 0)


# 模拟键盘输入按键指令带上打键--shift，key为VK_CODE的键值
def keyboardInputByCode_shift(key):
    win32api.keybd_event(VK_CODE.get("left_shift"), 0, 0, 0)
    time.sleep(0.01)
    win32api.keybd_event(VK_CODE.get(key), 0, 0, 0)
    time.sleep(0.01)
    win32api.keybd_event(VK_CODE.get(key), 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.01)
    win32api.keybd_event(VK_CODE.get("left_shift"), 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.01)


# 模拟键盘输入按键指令--alt_tab，key为VK_CODE的键值
def keyboardInputByCode_alt_tab(key):
    win32api.keybd_event(VK_CODE.get("alt"), 0, 0, 0)
    time.sleep(0.01)
    win32api.keybd_event(VK_CODE.get(key), 0, 0, 0)
    time.sleep(0.01)
    win32api.keybd_event(VK_CODE.get(key), 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.01)
    win32api.keybd_event(VK_CODE.get("alt"), 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.01)


# 模拟键盘输入alt +F4
def keyboardInputAltF4():
    log.log_info("键盘输入 alt + F4")
    win32api.keybd_event(0x12, 0, 0, 0)
    win32api.keybd_event(0x73, 0, 0, 0)
    win32api.keybd_event(0x73, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(0x12, 0, win32con.KEYEVENTF_KEYUP, 0)


# 模拟键盘输入ctrl + a
def keyboardInputCtrlA():
    log.log_info("键盘输入 ctrl + a")
    win32api.keybd_event(0x11, 0, 0, 0)
    win32api.keybd_event(0x41, 0, 0, 0)
    win32api.keybd_event(0x41, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)


# 模拟键盘输入快捷键
def keyboardInputHotkey(*key_name_list):
    log.log_info(f"按下快捷键 {' + '.join(key_name_list)}")
    for key_name in key_name_list:
        code = VK_CODE.get(key_name)
        win32api.keybd_event(code, 0, 0, 0)
    for key_name in key_name_list:
        code = VK_CODE.get(key_name)
        win32api.keybd_event(code, 0, win32con.KEYEVENTF_KEYUP, 0)


# 模拟键盘输入回车
def keyboardInputEnter():
    # 回车
    log.log_info("键盘输入 回车")
    win32api.keybd_event(0x0D, 0, 0, 0)
    win32api.keybd_event(0x0D, 0, win32con.KEYEVENTF_KEYUP, 0)


# 模拟键盘输入dlt+D
def keyboardInputAltD():
    # alt + d
    log.log_info("键盘输入 Alt + D 切换到地址栏")
    win32api.keybd_event(0x12, 0, 0, 0)
    win32api.keybd_event(0x44, 0, 0, 0)
    win32api.keybd_event(0x44, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(0x12, 0, win32con.KEYEVENTF_KEYUP, 0)


# 获取鼠标坐标
def get_mouse_point():
    po = POINT()
    windll.user32.GetCursorPos(byref(po))
    return int(po.x), int(po.y)


# 鼠标点击方法
def mouse_click_int(x=None, y=None, click_seconds=0):
    if not x is None and not y is None:
        mouse_move(x, y)
        time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(click_seconds)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


# 重写鼠标点击方法传入元组
def mouse_click_tuple(t_position):
    x = t_position[0]
    y = t_position[1]
    mouse_click_int(x, y)


# 重写鼠标点击方法入口
def mouse_click(*parm):
    time.sleep(0.1)
    if len(parm) == 1:
        mouse_click_tuple(parm[0])
    elif len(parm) == 2:
        mouse_click_int(parm[0], parm[1])


# 鼠标双击方法
def mouse_dclick(x=None, y=None):
    if not x is None and not y is None:
        mouse_move(x, y)
        time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


# 鼠标右键方法
def mouse_right_click(x=None, y=None):
    if not x is None and not y is None:
        mouse_move(x, y)
        time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

# 鼠标右键方法-坐标元组
def mouse_right_click_tuple(t_position):
    x = t_position[0]
    y = t_position[1]
    mouse_right_click(x,y)


# 鼠标移动方法
def mouse_move(x, y):
    windll.user32.SetCursorPos(x, y)


# 鼠标滚动方法
def mouse_scroll(distance):
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -distance, win32con.WHEEL_DELTA)


def mouse_drag(start_pos, other_pos, cost_seconds=1):
    """
    鼠标点击拖动
    @param start_pos: 开始点击坐标
    @param other_pos: 拖动坐标（传坐标元组时为拖动直线，传元组列表时为逐步拖动到多个坐标位置）
    @param cost_seconds: 拖动耗时（秒）
    @return:
    """
    from common.bezier_curve import bezier_curve_gen

    mouse_move(start_pos[0], start_pos[1])
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(1)

    assert other_pos, "拖动坐标参数错误"
    if isinstance(other_pos, tuple):
        other_pos_list = [other_pos]
    else:
        other_pos_list = other_pos

    for index, other_pos_tuple in enumerate(other_pos_list):
        if index == 0:
            last_pos = start_pos
        else:
            last_pos = other_pos_list[index - 1]

        if cost_seconds > 0:
            # 拖动耗时大于0秒时，使用贝塞尔曲线计算拖动坐标
            for p in bezier_curve_gen(last_pos, other_pos_tuple, int(cost_seconds * 10)):
                mouse_move(p[0], p[1])
                time.sleep(0.1)
        else:
            mouse_move(other_pos_tuple[0], other_pos_tuple[1])

    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def change_input_lan(lan):
    """
    # 切换系统输入法
    @param lan: 输入法类型枚举 InputLan
    @return:
    """
    # 获取系统输入法列表
    hwnd = win32gui.GetForegroundWindow()
    im_list = win32api.GetKeyboardLayoutList()
    im_list = list(map(hex, im_list))

    if hex(lan.value) not in im_list:
        # 加载输入法
        win32api.LoadKeyboardLayout('0000' + hex(lan.value)[-4:], 1)

    # 切换输入法
    res = win32api.SendMessage(
        hwnd,
        win32con.WM_INPUTLANGCHANGEREQUEST,
        0,
        lan.value
    )

    result = res == 0

    if result:
        log.log_info(f"设置输入法成功，lan：{lan.name}")
    else:
        log.log_error(f"设置输入法失败，lan：{lan.name}")

    return result


# 键位输入方法
def key_input(s=''):
    special_word_dict = {"~": "`", "!": "1", "@": "2", "#": "3", "$": "4", "%": "5", "^": "6", "&": "7", "*": "8",
                         "(": "9", ")": "0", "_": "-", "+": "=", "L": "l", "I": "i", "E": "e", "B": "b", "A": "a",
                         "O": "o"}
    for c in s:
        time.sleep(0.01)
        if c in special_word_dict.keys():
            keyboardInputByCode_shift(special_word_dict.get(c))
            continue
        win32api.keybd_event(VK_CODE[c], 0, 0, 0)
        win32api.keybd_event(VK_CODE[c], 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.01)


def key_copy():
    """按下ctrl + c"""
    win32api.keybd_event(VK_CODE["ctrl"], 0, 0, 0)
    time.sleep(0.01)
    win32api.keybd_event(VK_CODE["c"], 0, 0, 0)
    win32api.keybd_event(VK_CODE["c"], 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(VK_CODE["ctrl"], 0, win32con.KEYEVENTF_KEYUP, 0)


def key_paste():
    """按下ctrl + v"""
    win32api.keybd_event(VK_CODE["ctrl"], 0, 0, 0)
    time.sleep(0.01)
    win32api.keybd_event(VK_CODE["v"], 0, 0, 0)
    win32api.keybd_event(VK_CODE["v"], 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(VK_CODE["ctrl"], 0, win32con.KEYEVENTF_KEYUP, 0)


def copy_to_clipboard(text):
    """
    将文本复制到剪切板
    @param text: 待复制文本
    @return:
    """
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text)
    win32clipboard.CloseClipboard()


def get_clipboard_text():
    """获取剪切板文字"""
    win32clipboard.OpenClipboard()
    copy_data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()

    try:
        text_data = str(copy_data)
    except Exception as e:
        log.log_error("转换剪切板数据为字符串时异常")
        return None
    else:
        return text_data


def clear_clipboard():
    """清空剪切板"""
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()


# 图像对比方法
def get_pic_coordinates(target_pic_path, similarity, location="center"):
    """
    :param target_pic_path:目标图片的路径，需要无缩放的打开图片进行截图保存，推荐使用Windows自带的画板打开
    :param similarity:相似度阈值（范围：0-1），低于Similarity则表示相似图片
    :param location 返回坐标点的位置，默认中间点center，左上角为left_upper_corner
    :return:有高于阈值的图片返回坐标百分比（保留两位小数,类型为float），否则返回0,0，异常则返回-1,-1
    """
    # 截取当前的屏幕作为原图

    # try:
    #     window_capture(screen_temp_pic_name)
    # except:
    #     screenshot(screen_temp_pic_name)
    #
    # img_src = cv2.imread(screen_temp_pic_name)

    img_src = window_capture2()
    assert img_src is not None, f"找不到原始图片，path：{screen_temp_pic_name}"
    template = cv2.imread(target_pic_path)
    assert template is not None, f"找不到目标图片，path：{target_pic_path}"

    # 获取当前设备的宽高
    screenw = img_src.shape[1]
    screenh = img_src.shape[0]

    if (img_src is not None) and (template is not None):
        # 获取小图片的高和宽
        imgtmh = template.shape[0]
        imgtmw = template.shape[1]
        # 获取大图片的高和宽
        img_srch = img_src.shape[0]
        img_srcw = img_src.shape[1]
        # 匹配图片
        res = cv2.matchTemplate(img_src, template, cv2.TM_CCOEFF_NORMED)

        # 最小匹配度，最大匹配度，最小匹配度的坐标，最大匹配度的坐标
        min_md, max_md, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_md >= similarity:
            # 计算屏幕中坐标,max_loc为左上角的坐标点
            if location == Location.CENTER.value:
                position = (int(max_loc[0] + imgtmw / 2), int(max_loc[1] + imgtmh / 2))
            elif location == Location.LEFT_UP.value:
                position = [int(max_loc[0]), int(max_loc[1])]
            elif location == Location.LEFT_BOTTOM.value:
                position = [int(max_loc[0]), int(max_loc[1] + imgtmh)]
            elif location == Location.RIGHT_UP.value:
                position = [int(max_loc[0] + imgtmw), int(max_loc[1])]
            elif location == Location.RIGHT_BOTTOM.value:
                position = [int(max_loc[0] + imgtmw), int(max_loc[1] + imgtmh)]
            else:
                raise Exception("get_pic_coordinates location error")
            return position
        else:
            return (0, 0)


def get_more_pic_coordinates(target_pic_path, similarity, location=Location.CENTER.value):
    """
    :param target_pic_path: 截图资源的路径
    :param similarity: 相似度阈值，返回相似度高于此阈值的坐标
    :param location 返回坐标点的位置，默认中间点center，左上角为left_upper_corner
    :return: 高于阈值的坐标列表，异常则返回-1，无则返回0
    """
    # 截取当前的屏幕作为原图
    # try:
    #     window_capture(screen_temp_pic_name)
    # except:
    #     screenshot(screen_temp_pic_name)
    try:
        # img_src = cv2.imread(screen_temp_pic_name)
        img_src = window_capture2()
        template = cv2.imread(target_pic_path)
    except Exception as e:
        raise Exception(f"图片读取异常 path：{target_pic_path}")

    if (img_src is not None) and (template is not None):
        # 获取小图片的高和宽
        imgtmh = template.shape[0]
        imgtmw = template.shape[1]
        # 获取大图片的高和宽
        img_srch = img_src.shape[0]
        img_srcw = img_src.shape[1]
        # 匹配图片
        res = cv2.matchTemplate(img_src, template, cv2.TM_CCOEFF_NORMED)

        loc = np.where(res >= similarity)
        pic_list_x = []
        pic_list_y = []
        for i in range(loc[0].size):
            position = [(loc[1][i] + (imgtmw / 2)), (loc[0][i] + (imgtmh / 2))]
            # 计算屏幕中坐标,position为中间坐标点
            if location == Location.CENTER.value:
                position = position
            elif location == Location.LEFT_UP.value:
                position = [position[0] - imgtmw / 2, position[1] - imgtmh / 2]
            elif location == Location.LEFT_BOTTOM.value:
                position = [position[0] - imgtmw / 2, position[1] + imgtmh / 2]
            elif location == Location.RIGHT_UP.value:
                position = [position[0] + imgtmw / 2, position[1] - imgtmh / 2]
            elif location == Location.RIGHT_BOTTOM.value:
                position = [position[0] + imgtmw / 2, position[1] + imgtmh / 2]
            else:
                raise Exception("get_pic_coordinates location error")

            pic_list_x.append(int(position[0]))
            pic_list_y.append(int(position[1]))
        pic_position_zip = zip(pic_list_x, pic_list_y)
        if len(list(pic_list_x)):
            return list(pic_position_zip)
        else:
            return None


def compress_pic(compress_rate=1.0, pic_path=screen_temp_pic_name):
    """
    压缩图片
    @param compress_rate: 压缩比率（影响清晰度）
    @param pic_path: 图片路径
    @return:
    """
    path, name = os.path.split(pic_path)
    filename, extension = os.path.splitext(name)
    new_name = f"{filename}_compress_{compress_rate}{extension}"
    new_path = os.path.join(path, new_name)

    if cv2:  # 安装了 opencv 时优先使用 cv2 压缩
        pic = cv2.imread(pic_path)
        height, width = pic.shape[:2]
        pic_resize = cv2.resize(pic, (int(width * compress_rate), int(height * compress_rate)),
                                interpolation=cv2.INTER_AREA)
        cv2.imwrite(new_path, pic_resize)
    else:  # 使用 Pillow 压缩
        img = Image.open(pic_path)
        if img.format == 'PNG':
            img = img.convert('RGB')

        img.save(new_path, quality=int(compress_rate * 100), optimize=True)

    return new_path


def compare_picture_similarity(image1_path, image2_path, sim=0.8):
    """
    比较图片相似度
    @param image1_path: 图1文件路径
    @param image2_path: 图2文件路径
    @param sim: 相似度 数值范围：0~1.0
    @return:
    """
    try:
        image1 = ac.imread(image1_path)
        image2 = ac.imread(image2_path)
    except Exception as e:
        raise Exception(f"图片读取异常 path：{image1_path}, {image2_path}")

    match_result = ac.find_template(image1, image2, sim)

    return match_result is not None


def get_pic_coordinates_aircv(pic, confidence=0.8, location=Location.CENTER.value, use_history_capture=False):
    """
    :param pic: 截图资源的路径
    :param confidence: 相似度阈值，返回相似度高于此阈值的坐标
    :param location: 返回坐标点的位置，默认中间点center，左上角为left_upper_corner，右上角为right_upper_corner，左下角left_bottom_corner， 右下角right_bottom_corner
    :return: 高于阈值的坐标列表，异常则返回-1，无则返回0
    """
    # 截取当前的屏幕作为原图
    # try:
    #     window_capture(screen_temp_pic_name)
    # except:
    #     screenshot(screen_temp_pic_name)
    #
    # imsrc = ac.imread(screen_temp_pic_name)
    global CAPTURE_IMG_DATA_HISTORY
    if use_history_capture and CAPTURE_IMG_DATA_HISTORY is not None:
        imsrc = CAPTURE_IMG_DATA_HISTORY
    else:
        imsrc = window_capture2()

    try:
        imobj = ac.imread(pic)
    except Exception as e:
        raise Exception(f"图片读取异常 path：{pic}")

    match_result = ac.find_template(imsrc, imobj, confidence)
    # {'confidence': 0.5435812473297119, 'rectangle': ((394, 384), (394, 416), (450, 384), (450, 416)), 'result': (422.0, 400.0)}

    if match_result is not None:
        # print(match_result.get("confidence", 0), confidence)
        # if match_result.get("confidence", 0) < confidence:
        #     return None
        if location == Location.CENTER.value:
            return int(match_result["result"][0]), int(match_result["result"][1])
        elif location == Location.LEFT_UP.value:
            return int(match_result["rectangle"][0][0]), int(match_result["rectangle"][0][1])
        elif location == Location.LEFT_BOTTOM.value:
            return int(match_result["rectangle"][1][0]), int(match_result["rectangle"][1][1])
        elif location == Location.RIGHT_UP.value:
            return int(match_result["rectangle"][2][0]), int(match_result["rectangle"][2][1])
        elif location == Location.RIGHT_BOTTOM.value:
            return int(match_result["rectangle"][3][0]), int(match_result["rectangle"][3][1])
    return None


def find_element_by_pic(pic, sim=0.8, location=Location.CENTER.value, retry=10, sim_no_reduce=False, hwnd=None):
    """
    根据图片查找元素位置
    @param pic: 图片地址
    @param sim: 相似度
    @param location: 图片位置
    @param retry: 重试次数
    @param sim_no_reduce: 重试时是否降低相似度
    @param hwnd: 指定窗口内寻图的窗口句柄
    @return:
    """

    position = (0, 0)
    if not hwnd:
        for i in range(0, retry, 1):
            position = get_pic_coordinates_aircv(pic, confidence=sim, location=location)
            import traceback
            log.log_debug(f"pic:{pic} sim:{sim} i:{i}, stack: {traceback.extract_stack(limit=5)}")
            # log.log_debug(f"pic:{pic} sim:{sim} i:{i}, stack: \n{os.linesep.join([str(stack) for stack in traceback.extract_stack(limit=5)])}\n")
            if position and position != (0, 0):
                return True, position
            if not sim_no_reduce:
                sim -= 0.1
            perform_sleep(1)
        return False, position
    else:
        if is_hwnd_exist(hwnd):
            x1, y1, x2, y2 = get_pos_by_hwnd(hwnd)
            log.log_debug(f"x1:{x1} y1:{y1}, x2: {x2}, y2: {y2}")
        else:
            return find_element_by_pic(pic, sim=sim, location=location, retry=retry, sim_no_reduce=sim_no_reduce,
                                       hwnd=None)  # 取不到句柄，用回上一种方法
        find_result, positions = find_elements_by_pic(pic, sim=sim, location=location, retry=retry,
                                                      sim_no_reduce=sim_no_reduce)
        log.log_debug(f"pic:{pic} sim:{sim}, hwnd: {hwnd}")
        if find_result:
            log.log_debug(f"positions:{positions}")
            for position_a in positions:
                if x2 >= position_a[0] >= x1 and y2 >= position_a[1] >= y1:
                    position = position_a
                    return True, position

        return False, position


def find_element_by_pics(pics: list, sim=0.8, location=Location.LEFT_UP.value, retry=10, sim_no_reduce=False,
                         use_history_capture=False):
    """
    根据图片查找元素位置
    @param pics: 图片列表地址
    @param sim: 相似度
    @param location: 图片位置
    @param retry: 重试次数
    @param sim_no_reduce: 重试时是否降低相似度
    @param hwnd: 指定窗口内寻图的窗口句柄
    @return:
    """
    global CAPTURE_IMG_DATA_HISTORY
    if not use_history_capture:
        CAPTURE_IMG_DATA_HISTORY = None
    position = (0, 0)

    for i in range(0, retry, 1):
        for pic in pics:
            position = get_pic_coordinates_aircv(pic, confidence=sim, location=location, use_history_capture=True)
            import traceback
            log.log_debug(f"pic:{pic} sim:{sim} i:{i}, stack: {traceback.extract_stack(limit=5)}")
            if position and position != (0, 0):
                return True, position, pic
            if not sim_no_reduce:
                sim -= 0.1
            # perform_sleep(1)
    return False, position, None


def find_elements_by_pic(pic, sim=0.8, location=Location.CENTER.value, retry=10, sim_no_reduce=False):
    """
    根据图片返回符合相似度的元素（一个或者多个）位置
    @param pic: 图片地址
    @param sim: 相似度
    @param location: 返回坐标点的位置，默认中间点center，左上角为left_upper_corner，右上角为right_upper_corner，左下角left_bottom_corner， 右下角right_bottom_corner
    @param retry: 重试次数
    @param sim_no_reduce: 重试时是否降低相似度
    @return:
    """
    positions = []
    for i in range(1, retry, 1):
        positions = get_more_pic_coordinates(pic, sim, location=location)
        if positions:
            return True, positions
        if not sim_no_reduce:
            sim -= 0.1
        time.sleep(1)

    return False, positions


# 点击图片
def click_element_by_pic(pic, sim=0.8, retry=10, hwnd=None, sim_no_reduce=False):
    """
    :param pic 图片路径
    :param sim 图片相似度
    :param retry 对比重试次数
    :param hwnd 指定窗口内寻图的窗口句柄
    :param sim_no_reduce: 重试时是否降低相似度
    :return 找到图片并点击返回True, 找不到图片返回False
    """
    find_result, pic_position = find_element_by_pic(pic, sim, location=Location.CENTER.value, retry=retry, hwnd=hwnd,
                                                    sim_no_reduce=sim_no_reduce)
    if find_result:
        log.log_debug(f"click_element_by_pic: {pic_position}")
        mouse_click(pic_position)
        return True
    else:
        return False

# 鼠标右键点击图片
def click_right_element_by_pic(pic, sim=0.8, retry=10, hwnd=None, sim_no_reduce=False):
    """
    :param pic 图片路径
    :param sim 图片相似度
    :param retry 对比重试次数
    :param hwnd 指定窗口内寻图的窗口句柄
    :param sim_no_reduce: 重试时是否降低相似度
    :return 找到图片并点击返回True, 找不到图片返回False
    """
    find_result, pic_position = find_element_by_pic(pic, sim, location=Location.CENTER.value, retry=retry, hwnd=hwnd,
                                                    sim_no_reduce=sim_no_reduce)
    if find_result:
        log.log_debug(f"click_element_by_pic: {pic_position}")
        mouse_right_click_tuple(pic_position)
        return True
    else:
        return False


# 依次查找点击队列里的查找到的图片
def click_element_by_pics(pics=list, sim=0.8, retry=10, sim_no_reduce=False):
    """
    :param pics 图片路径列表
    :param sim 图片相似度
    :param retry 对比重试次数
    :param sim_no_reduce 重试时是否降低相似度
    :return 找到图片并点击返回True, 找不到图片返回False
    """
    for pic in pics:
        find_result, pic_position = find_element_by_pic(pic, sim, location=Location.CENTER.value, retry=retry,
                                                        sim_no_reduce=sim_no_reduce)
        if find_result:
            mouse_click(pic_position)
            return True
    return False


# 屏幕截图方法
def window_capture(filename):
    hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)
    # 释放内存
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)


# 屏幕截图方法
def screenshot(filename):
    try:
        ImageGrab.grab().save(filename)
    except Exception as e:
        # 出现 OSError: screen grab failed 时尝试使用 window_capture 方法截屏
        log.log_error(e, log_only=True)
        window_capture(filename)


# 新截图方法,提升截图速度,把图片返回到内存,没有硬盘文件IO操作
def window_capture2():
    hwin = win32gui.GetDesktopWindow()
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    # signedIntsArray = bmp.GetBitmapBits(False)
    # img = np.array(signedIntsArray).astype(dtype="uint8")  # This is REALLY slow!
    img.shape = (height, width, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())
    global CAPTURE_IMG_DATA_HISTORY
    CAPTURE_IMG_DATA_HISTORY = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    return CAPTURE_IMG_DATA_HISTORY


# 获取屏幕中二维码，返回字符串
def decode_qrcode():
    screenshot(screen_temp_pic_name)
    if not os.path.exists(screen_temp_pic_name):
        return None
    try:
        r = pyzbar.decode(Image.open(screen_temp_pic_name), symbols=[pyzbar.ZBarSymbol.QRCODE])
        return bytes(r[0][0]).decode('utf-8')
    except:
        return None


# 获取传入图片二维码，返回字符串
def decode_qrcode_by_img(img):
    if not os.path.exists(img):
        return None
    try:
        r = pyzbar.decode(Image.open(img), symbols=[pyzbar.ZBarSymbol.QRCODE])
        return bytes(r[0][0]).decode('utf-8')
    except:
        return None


# 识别屏幕中指定文字
# 此接口用的腾讯在线接口，多次连续调用大概率会出现500错误，多次、连续、批量识别尽量使用tcreadimgtxt方法
def tcocr(text):
    screenshot(screen_temp_pic_name)
    file = open(screen_temp_pic_name, "rb")
    files = {"file": file, "text": text}
    response = requests.request("post", "http://autotest.cf.com/interface/tcocr?text=" + text, files=files)
    res_json = json.loads(unicode(response.content, "utf-8"))
    return res_json


# 识别图片中的所有文字返回
def tcreadimgtxt(picfilename):
    file = open(picfilename, "rb")
    files = {"file": file}
    response = requests.request("post", "http://autotest.cf.com/interface/tcreadimgtxt", files=files)
    return unicode(response.content, "utf-8")


# 识别图片中的所有数字返回
def tcreadimgnum(picfilename):
    file = open(picfilename, "rb")
    files = {"file": file}
    response = requests.request("post", "http://autotest.cf.com/interface/tcreadimgnum", files=files)
    return unicode(response.content, "utf-8")


# paddle ocr文字识别接口
def paddleocr(picfile):
    def cv2_to_base64(image):
        data = cv2.imencode('.png', image)[1]
        return base64.b64encode(data.tobytes()).decode('utf8')

    # 获取图片的base64编码格式
    img1 = cv2_to_base64(cv2.imread(picfile))
    data = {'images': [img1]}
    # 指定content-type
    headers = {"Content-type": "application/json"}
    # 发送HTTP请求
    url = "http://autotest.cf.com:8866/predict/ocr_system"
    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    # 返回预测结果
    return r.json()["results"]


def get_pic_coordinates_color(x, y, path=None, rgb=False, use_history_capture=False):
    """
    获取图片指定坐标的颜色
    @param x: x坐标
    @param y: y坐标
    @param path: 图片路径
    @param rgb: 是否返回rgb颜色值，否则返回hex
    @param use_history_capture: 是否使用内存中的历史截图
    @return:
    """

    try:
        # 传入图片路径参数时，读取相应路径的图片
        if path:
            img = Image.open(path)
            img_rgb = img.convert("RGB")
            img_array = img_rgb.load()
            data = img_array[x, y]
        else:
            global CAPTURE_IMG_DATA_HISTORY
            if use_history_capture and CAPTURE_IMG_DATA_HISTORY is not None:
                img = CAPTURE_IMG_DATA_HISTORY
            else:
                img = window_capture2()
            data = img[y, x]

        if rgb:
            return data

        return rgb_to_hex(data)

    except Exception as e:
        log.log_error(e)
        return None


def rgb_to_hex(rgb):
    """rgb转hex"""
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def is_admin():
    """是否有管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def query_reg_value(regroot=None, regpath="", keyname=""):
    """
    查询注册表中的值
    @param regroot:
    @param regpath:
    @param keyname:
    @return:
    """
    if not is_admin():
        log.log_error("请尝试以管理员权限启动")
        return

    if regroot == None:
        regroot = win32con.HKEY_LOCAL_MACHINE

    try:
        regflags = win32con.WRITE_OWNER | win32con.KEY_WOW64_64KEY | win32con.KEY_ALL_ACCESS
        key = win32api.RegOpenKeyEx(regroot, regpath, 0, regflags)
        value, key_type = win32api.RegQueryValueEx(key, keyname)
        win32api.RegCloseKey(key)
    except pywintypes.error as e:
        log.log_info("找不到指定的注册表数据", attach=False)
        return
    except Exception as e:
        log.log_error(str(e))
        return

    return value


# 删除注册表中的值
def remove_reg_value(regroot=None, regpath="", value=""):
    if regroot == None:
        regroot = win32con.HKEY_LOCAL_MACHINE

    try:
        regflags = win32con.WRITE_OWNER | win32con.KEY_WOW64_64KEY | win32con.KEY_ALL_ACCESS
        key = win32api.RegOpenKeyEx(regroot, regpath, 0, regflags)
        win32api.RegDeleteValue(key, value)
        win32api.RegCloseKey(key)
    except:
        return False
    return True


# 删除注册表中的键
def remove_reg_key(regroot=None, regpath=""):
    if regroot == None:
        regroot = win32con.HKEY_LOCAL_MACHINE

    try:
        reg_parent, subkey_name = os.path.split(regpath)
        regflags = win32con.WRITE_OWNER | win32con.KEY_WOW64_64KEY | win32con.KEY_ALL_ACCESS
        key = win32api.RegOpenKeyEx(regroot, reg_parent, 0, regflags)
        win32api.RegDeleteKeyEx(key, subkey_name)
        win32api.RegCloseKey(key)
    except:
        return False
    return True


# 创建注册表中的键
def create_reg_key(regroot=None, regpath=""):
    if regroot == None:
        regroot = win32con.HKEY_LOCAL_MACHINE

    try:
        regflags = win32con.WRITE_OWNER | win32con.KEY_WOW64_64KEY | win32con.KEY_ALL_ACCESS
        key, _ = win32api.RegCreateKeyEx(regroot, regpath, regflags)
        win32api.RegCloseKey(key)
    except:
        return False
    return True


# 修改注册表中的值
def set_reg_value(regroot=None, regpath="", keyname="", value_type=None, value=""):
    # 修改参数默认值设置方式，避免其他项目未装pywin32库时报错
    if regroot == None:
        regroot = win32con.HKEY_LOCAL_MACHINE
    if value_type == None:
        value_type = win32con.REG_SZ

    try:
        regflags = win32con.WRITE_OWNER | win32con.KEY_WOW64_64KEY | win32con.KEY_ALL_ACCESS
        key = win32api.RegOpenKeyEx(regroot, regpath, 0, regflags)
        win32api.RegSetValueEx(key, keyname, 0, value_type, value)
        win32api.RegCloseKey(key)
    except:
        return False
    return True


# 删除指定目录
def remove_path(p):
    if not os.path.exists(p):
        return
    if os.path.isfile(p):
        os.remove(p)
        return

    for f in os.listdir(p):
        remove_path(os.path.join(p, f))
    os.rmdir(p)


# 获取字符中所有的数字内容
def renum(ss):
    ss = str(ss).replace(" ", "")
    import re
    num = re.findall(r'\d+', ss)
    if len(num) > 0:
        return int(num[0])
    else:
        return None


# 裁剪屏幕截图中的某个位置
def cutscreen_img(x, y, x1, y1):
    try:
        window_capture(screen_temp_pic_name)
    except:
        screenshot(screen_temp_pic_name)
    img = Image.open(screen_temp_pic_name)
    cropped = img.crop((x, y, x1, y1))  # (left, upper, right, lower)
    cut_png = screen_temp_pic_name.replace(".png", "_cut.png")
    cropped.save(cut_png)
    return cut_png


# 判断指定进程是否存在
def is_process_exists(procname):
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess:
            pass
        if pinfo["name"] == procname:
            return True
    return False


def process_start(process_path, async_start=False, param=None):
    """
    打开进程
    @param process_path: 进程地址
    @param async_start: 是否异步打开（非阻塞）
    @param param: 命令行参数
    @return:
    """
    if not param is None:
        cmdline = "\"" + process_path + "\" " + param
    else:
        cmdline = process_path

    if async_start:
        os.popen(cmdline)
    else:
        os.system(cmdline)
    for i in range(1, 10, 1):
        if is_process_exists(os.path.basename(process_path)):
            return True
        time.sleep(1)
    return False


# 发送http请求
def send_request(url, params=None, data=None, json=None, files=None, headers=None, timeout=10, method='post',
                 proxy=None, num_retries=1, _is_retry=False):
    """
    :param dict url: 请求地址
    :param dict params: 请求查询参数
    :param dict data: 提交表单数据
    :param dict json: 提交json字符串数据
    :param dict files: 提交文件数据
    :param dict headers: 请求头
    :param int timeout: 超时时间，单位秒
    :param str method: 请求方法，get、post、put、delete
    :param str proxy: 设置代理服务器
    :param int num_retries: 超时重试次数
    :param bool _is_retry: 判定为重试请求，这不应该由用户发出
    """
    headers = headers or {}

    method = method.lower()
    if method == 'get':
        method_func = requests.get
    elif method == 'post':
        method_func = requests.post
    elif method == 'put':
        method_func = requests.put
    elif method == 'delete':
        method_func = requests.delete
    else:
        method_func = requests.post
    try:
        resp = method_func(url, params=params, headers=headers, data=data, json=json, files=files, timeout=timeout,
                           proxies=proxy if _is_retry is True and proxy else None)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        if num_retries > 0:
            return send_request(
                url,
                params=params,
                headers=headers,
                data=data,
                json=json,
                files=files,
                timeout=timeout,
                method=method,
                proxy=proxy,
                num_retries=num_retries - 1,
                _is_retry=True,
            )
        else:
            raise
    except (requests.exceptions.RequestException, Exception):
        raise
    else:
        return resp


def create_server_id():
    """随机生成server_id"""
    m = hashlib.md5()  # 创建Md5对象
    m.update(''.join(random.sample(string.ascii_letters + string.digits, 32)).encode('utf-8'))  # 生成加密串，其中n是要加密的字符串
    return m.hexdigest()  # 经过md5加密的字符串赋值


def get_hwnd_by_mouse_pos():
    """函数检索包含指定点的窗口的句柄，即鼠标点所在位置窗口的句柄。返回句柄~"""
    x, y = win32api.GetCursorPos()
    hwnd = win32gui.WindowFromPoint((x, y))
    return hwnd
    # while hwnd != 0:
    #     pev_hwnd = hwnd
    #     hwnd = windll.user32.GetParent(pev_hwnd)
    # return pev_hwnd


def get_hwnd_class_name(hwnd):
    try:
        return win32gui.GetClassName(hwnd)
    except:
        return None


def is_hwnd_exist(hwnd):
    if win32gui.IsWindowVisible(hwnd):
        if get_hwnd_class_name(hwnd):
            return True
    return False


def get_hwnd_by_class(class_name, title):
    hwnd = win32gui.FindWindow(class_name, title)
    if hwnd != 0:
        return hwnd
    else:
        return None


def focus_window_by_hwnd(hwnd):
    if is_hwnd_exist(hwnd):
        win32gui.SetForegroundWindow(hwnd)


def get_hwnd_by_foreground():
    """函数返回前台窗口的句柄（用户当前正在使用的窗口）。系统为创建前台窗口的线程分配比其他线程稍高的优先级。返回句柄~"""
    return win32gui.GetForegroundWindow()


# 获取句柄的父句柄
def get_parent_hwnd(hwnd):
    return win32gui.GetParent(hwnd)


# 获取句柄的子句柄，返回列表
def get_childs_hwnd(hwnd):
    child_handlers = []
    parent_handler = hwnd

    def all_ok(hwnd, param):
        child_handlers.append(hwnd)

    try:
        win32gui.EnumChildWindows(parent_handler, all_ok, None)
    except:
        pass
    return child_handlers


def get_all_hwnd_info():
    hwnd_dict = dict()

    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_dict.update({hwnd: win32gui.GetWindowText(hwnd)})

    win32gui.EnumWindows(get_all_hwnd, 0)
    return hwnd_dict


def get_pos_by_hwnd(hwnd):
    try:
        x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd)
    except:
        return None
    return x1, y1, x2, y2


def attach_screenshot(name, compress_rate=0.7, image_path=None):
    """
    添加截图至allure报告中
    @param name: allure附件标题
    @param compress_rate: 压缩比率
    @param image_path: 图片路径，缺省时使用当前屏幕截图
    @return:
    """
    if image_path is None:
        try:
            window_capture(screen_temp_pic_name)
        except:
            screenshot(screen_temp_pic_name)

        image_path = screen_temp_pic_name

    # 压缩图片
    compress_png = compress_pic(pic_path=image_path, compress_rate=compress_rate)

    allure.attach.file(compress_png, name=name, attachment_type=allure.attachment_type.PNG)


def attach_driver_screenshot(driver, name, compress_rate=0.7, image_path=screen_temp_pic_name):
    """
    添加浏览器截图至allure报告中
    @param driver: selenium浏览器驱动
    @param name: allure附件标题
    @param compress_rate: 压缩比率
    @param image_path: 截图存储路径
    @return:
    """
    driver.get_screenshot_as_file(image_path)

    # 压缩图片
    compress_png = compress_pic(pic_path=image_path, compress_rate=compress_rate)

    # 添加到allure报告中
    allure.attach.file(compress_png, name=name, attachment_type=allure.attachment_type.PNG)


# 返回给予图片的主要颜色值
def get_dominant_color(object_pic):
    image = Image.open(object_pic)
    max_score = 0.0001
    dominant_color = None
    for count, (r, g, b) in image.getcolors(image.size[0] * image.size[1]):
        # 转为HSV标准
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
        y = (y - 16.0) / (235 - 16)

        # 忽略高亮色
        if y > 0.9:
            continue
        score = (saturation + 0.1) * count
        if score > max_score:
            max_score = score
            dominant_color = (r, g, b)
    return dominant_color


def perform_sleep(sec):
    # v_mem_info = psutil.virtual_memory()
    # v_mem_percent = v_mem_info.percent
    # v_mem_free_g = v_mem_info.free / 1024 / 1024 / 1024
    time.sleep(sec)
    index = 0
    while True:
        v_cpu_percent = psutil.cpu_percent(0.3)
        # 判断cpu平均使用率超过启动前的50%，20次以内，则sleep 1秒，最大为10秒
        if v_cpu_percent > (start_cpu_percent * 3) / 2 and index < 10:
            index += 1
            time.sleep(1)
            log.log_debug(f"性能延迟，开始cpu使用率：{start_cpu_percent}，cpu使用率：{v_cpu_percent}")
        else:
            break


def get_host_ip():
    """
    获取本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def copytree(src, dst, symlinks=False, ignore=None):
    """
    复制目录数
    @param src: 源目录
    @param dst: 目标目录
    @param symlinks:
    @param ignore:
    @return:
    """
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
            log.log_info(f"已复制文件: {d}")


def get_pid(pname):
    for proc in psutil.process_iter():
        try:
            if proc.name() == pname:
                return proc.pid
        except:
            continue
    return None


def kill_process_by_name(process_name):
    os.system("taskkill /f /im " + process_name)
    if is_process_exists(process_name):
        process_id = get_pid(process_name)
        os.system("taskkill /PID %s /F /T" % (process_id))


def is_symlink_dir(path):
    """
    是否为符号链接（软链接）目录
    @param path: 目录路径
    @return:
    """
    attributes = win32api.GetFileAttributes(path)
    flag = (attributes & win32con.FILE_ATTRIBUTE_REPARSE_POINT) == win32con.FILE_ATTRIBUTE_REPARSE_POINT
    return flag


def get_domain_ip(domain):
    """
    获取域名指向ip
    @param domain: 域名
    @return:
    """
    result = None
    try:
        address = socket.getaddrinfo(domain, 'http')
        result = address[0][4][0]
    except Exception as e:
        log.log_error("解析域名失败", attach=False)
    return result


# 获取进程名的命令行参数
def get_cmdline(pname):
    for proc in psutil.process_iter():
        try:
            if proc.name() == pname:
                return psutil.Process(proc.pid).cmdline()
        except:
            continue
    return None


# 对比命令行参数是否包含了预期的命令行字段（用于判断进程启动为对应产品所启动）
def compare_cmdline(pname, target_pname):
    """
    @param pname:当前进程名
    @param target_pname:预期进程名（如kingsoft，Clean Master）
    """
    a = get_cmdline(pname)
    if a == None:  # 不存在这个进程，所以取到的命令行为空
        return False
    if target_pname in a[0]:
        return True
    else:
        return False


def download_file(url, save_path=screen_temp_pic_name):
    """
    下载文件
    @param url: 文件下载链接
    @param save_path: 文件保存路径
    @return:
    """
    res = send_request(url, method='get')
    if res.status_code != 200:
        return

    with open(save_path, 'wb') as f:
        f.write(res.content)

    return save_path


# 删除文件中某行内容
def remove_file_line(file_name, keyword):
    """
    @param file_name:文件目录
    @param keyword:想要删除的行中，包含的关键字。会将包含此关键字的行删除
    """
    for line in fileinput.input(files=file_name, backup='.bak', inplace=True):
        # 删除含有某一关键词的行
        if keyword in line:
            pass  # 跳过此次循环，此处删除，inplace此时标准输出的结果不写回文件?所以删除了？
        else:
            print(line.rstrip())  # 在文件中重新输入该行（line）内容，且会将该行内容字段中后面的空格删除
            # 由于line结果会带空行，所以要rstrip()


# 替换文件中的某一关键词
def replace_file_keyword(file_name, keyword, target_word):
    """
    @param file_name:文件目录
    @param keyword:想要替换的关键字
    @param target_word:替换后的字段
    """
    for line in fileinput.input(files=file_name, backup='.bak', inplace=True):
        print(line.rstrip().replace(keyword, target_word))


# 删除文件中某一关键字
def delete_file_keyword(file_name, keyword):
    """
    @param file_name:文件目录
    @param keyword:想要删除的关键字
    """
    for line in fileinput.input(files=file_name, backup='.bak', inplace=True):
        print(line.rstrip().replace(keyword, ''))


# 在文件中某关键字所在行后添加一行
def add_file_keyword_in_line(file_name, keyword, target_word):
    """
    @param file_name:文件目录
    @param keyword:关键字,在此关键字所在行的下一行，新增一行内容
    @param target_word:新增一行内容
    """
    no = ""
    for line in fileinput.input(files=file_name, backup='.bak', inplace=True):
        if keyword in line:
            no = fileinput.filelineno()  # 获取关键字行号
        if fileinput.lineno() == no:
            print(line.rstrip())
            print(target_word)  # 在第一行中新增此内容。在文件中print？
        else:
            print(line.rstrip())


def get_gbk2312(length=1):
    """
    获取随机中文字符串
    @param length: 字符串长度
    @return:
    """
    gbk_str = ""
    for i in range(length):
        head = random.randint(0xb0, 0xf7)
        body = random.randint(0xa1, 0xf9)
        val = f'{head:x} {body:x}'
        gbk_str += bytes.fromhex(val).decode('gb2312')
    return gbk_str


def get_random_mobile(prefix_numb=None):
    """
    获取随机手机号
    @param prefix_numb: 手机号前缀
    @return:
    """
    # 没有传手机号前缀时随机选择
    if not prefix_numb:
        prefix_numb_list = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151",
                            "152", "153", "155", "156", "157", "158", "159", "173", "177", "178", "186", "187", "188",
                            "189"]
        prefix_numb = random.choice(prefix_numb_list)
    # 随机生成尾号
    suffix_len = 11 - len(prefix_numb)
    suffix_numb = "".join(random.choice("0123456789") for i in range(suffix_len))
    return prefix_numb + suffix_numb


def get_random_email(min_len=5, max_len=15, email_suffix=None):
    """
    获取随机邮箱
    @param min_len: 邮箱前缀字符的最小长度
    @param max_len: 邮箱前缀字符的最大长度
    @param email_suffix: 邮箱后缀（不包含@符号，不传时在常用邮箱后缀中随机选择）
    @return:
    """
    prefix_len = random.randint(min_len, max_len)
    chars = "0123456789qbcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPWRSTUVWXYZ"
    email_prefix = "".join(random.choice(chars) for i in range(prefix_len))

    if not email_suffix:
        suffix_list = ["qq.com", "gmail.com", "163.com", "126.com", "189.com", "hotmail.com", "outlook.com",
                       "yahoo.com"]
        email_suffix = random.choice(suffix_list)

    return f"{email_prefix}@{email_suffix}"
