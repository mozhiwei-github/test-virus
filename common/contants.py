import os
from common import file_process
from enum import unique, Enum
from selenium.webdriver.common.by import By

base_dir = os.path.dirname(os.path.dirname(__file__))

# 日志目录
make_dir = file_process.DirOperation()
make_dir.makedir(os.path.join(base_dir, 'logs'))
logs_file = os.path.join(base_dir, "logs")


@unique
class ServerHost(Enum):
    """服务器地址"""
    CDS = "http://10.12.36.155:8080"  # 容器调度服务地址


@unique
class InputLan(Enum):
    """
    输入法语言
    https://msdn.microsoft.com/en-us/library/cc233982.aspx
    """
    EN = 0x4090409
    ZH = 0x8040804
