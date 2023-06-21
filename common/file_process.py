#!/usr/bin/evn python
# --coding = 'utf-8' --
# Author An hongyun
# Python Version 3.8
import os
import sys
import platform
import configparser

if platform.system() == "Windows":
    import winreg


# print(os.name)
# print(sys.getdefaultencoding())
# print(sys.version)
# print(sys.version_info)

class FileOperation:
    def __init__(self, file):
        self.file = file
        self.conf = configparser.ConfigParser()
        self.conf.read(file)

    def get_appdata(self):
        return os.getenv('APPDATA')

    def get_desktop(self):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return winreg.QueryValueEx(key, "Desktop")[0]

    # 获取ini配置文件中section名称
    def get_sessions(self):
        return self.conf.sections()

    # 获取ini配置文件中section下所有字段内容
    def get_items(self, sec):
        return self.conf.items(section=sec)

    # 获取某一个section下所有option字段
    def get_options(self, sec):
        return self.conf.options(section=sec)

    # 获取某一个section下，某一个option下的值
    def get_option(self, sec, opt):
        result = None
        if self.conf.has_option(sec, opt):
            result = self.conf.get(sec, opt)
        return result

    # 修改某一个section下，某一option下的值
    def set_option(self, sec, opt, new_value):
        self.conf.set(sec, opt, new_value)
        f = open(self.file, 'w')
        self.conf.write(f)
        f.close()

    # 删除某一个section下，某一个option下的值
    def del_option(self, sec, opt):
        if self.conf.has_option(sec, opt):
            self.conf.remove_option(sec, opt)
            f = open(self.file, 'w')
            self.conf.write(f)
            f.close()


class DirOperation():
    # 判断目录是否存在，若不存在，则创建
    def makedir(self, filepath):
        if not os.path.exists(path=filepath):
            os.makedirs(filepath)
