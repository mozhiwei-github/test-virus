#!/usr/bin/evn python
# --coding = 'utf-8' --
# Author An hongyun
# Python Version 3.8


import win32api
import win32con
import os
import winreg

#权限设置
REG_FLAGS = win32con.WRITE_OWNER|win32con.KEY_WOW64_64KEY|win32con.KEY_ALL_ACCESS
#root (根节点)
HKEY_CLASSES_ROOT = winreg.HKEY_CLASSES_ROOT
HKEY_CURRENT_USER = winreg.HKEY_CURRENT_USER
HKEY_LOCAL_MACHINE = winreg.HKEY_LOCAL_MACHINE
HKEY_USERS = winreg.HKEY_USERS
HKEY_CURRENT_CONFIG = winreg.HKEY_CURRENT_CONFIG

#value type (值类型)
REG_SZ = winreg.REG_SZ
REG_BINARY = winreg.REG_BINARY
REG_DWORD = winreg.REG_DWORD
REG_QWORD = winreg.REG_QWORD
REG_MULTI_SZ = winreg.REG_MULTI_SZ
REG_EXPAND_SZ = winreg.REG_EXPAND_SZ

class RegEdit:
    def __init__(self,root,path):
        '''init method (key root,key path)'''
        self.root = root
        self.path = path

    # 获取值
    def get_value(self,value_name):
        """get key object"""
        key = winreg.OpenKey(self.root,self.path)
        value, value_type = winreg.QueryValueEx(key, value_name)
        winreg.CloseKey(key)
        return value,value_type

    # 获取键
    def get_key(self):
        """get key object"""
        pass

    # 获取子键名称
    def get_sub_keys(self):
        """get key's sub keys"""
        key = winreg.OpenKey(self.root,self.path)
        count_key = winreg.QueryInfoKey(key)[0]
        keylist=[]
        for i in range(int(count_key)):
            name = winreg.EnumKey(key,i)
            keylist.append(name)
        winreg.CloseKey(key)
        return keylist

    # 删除当前键
    def delete_current_key(self,sub_key):
        '''delete current key'''
        key = winreg.OpenKey(self.root, self.path,0,winreg.KEY_ALL_ACCESS)
        winreg.DeleteKey(key,sub_key)
        winreg.CloseKey(key)
    # 删除键值
    def delete_current_value(self,sub_value):
        key = winreg.OpenKey(self.root, self.path,0,winreg.KEY_ALL_ACCESS)
        winreg.DeleteValue(key, sub_value)
        winreg.CloseKey(key)
    # 修改键值
    def edit_current_value(self,sub_key,key_type,value):
        key = winreg.OpenKey(self.root, self.path,0,winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key,sub_key,0,key_type,value)
        winreg.CloseKey(key)




# test = RegEdit(HKEY_CURRENT_USER,'Software\Kingsoft\KVip')
# test.delete_current_value('vip_version')
# test.delete_current_key('10001')

# key = winreg.OpenKey(HKEY_CURRENT_USER, 'Software\Kingsoft\KVip',0,winreg.KEY_ALL_ACCESS)
# winreg.DeleteKey(key,'user_info')
# winreg.CloseKey(key)








