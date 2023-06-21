# -*- coding: utf-8 -*-

import checkpe
#from pehash import get_pehash
import pehash
import os
import shutil
import pandas as pd
import hashlib
import time
import sys


def is_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False


def get_md5_of_file(filename):
    """
    get md5 of a file
    :param filename:
    :return:
    """
    if not os.path.isfile(filename):
        return None
    myhash = hashlib.md5()
    with open(filename, 'rb') as f:
        while True:
            b = f.read(8096)
            if not b:
                break
            myhash.update(b)
    return myhash.hexdigest()


def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            fullname = os.path.join(root, f)
            yield fullname

def mov_file(file_Path, out_file_dir, file_type, file_name):
    dir = out_file_dir + '\\' + file_type
    if not os.path.exists(dir):
        os.makedirs(dir)

    out_file_path = dir + '\\' + file_name
    shutil.copy(file_Path, out_file_path)


def check_file(file_dir, out_file_dir):
    if is_chinese(file_dir):
        print("'%s' 包含中包含中文，扫描文件目录不能包含中文，请更改！！！"%(file_dir))
        return

    fn, fmd5, fpeHash, finfo, ftype, packer = [], [], [], [], [], []
    fileType, fileInfo, filePEhash,packera = '', "", '', ""
    df = pd.DataFrame()

    for filePath in findAllFile(file_dir):
        fileName = os.path.basename(filePath)
        #print(filePath, fileName)
        file_Name = fileName
        fileType = 'un_file'
        md5 = ''
        try:
            tempPath = filePath
            filePEhash = ''
            packera = ''

            md5 = get_md5_of_file(filePath)
            if is_chinese(tempPath):
                mov_file(tempPath, out_file_dir, 'tempFile', md5)
                tempPath = out_file_dir + '\\tempFile\\' + md5

            fileType, fileInfo = checkpe.get_is_pefile(tempPath)
            if 'pe_' in fileType or 'net' in fileType:
                filePEhash = pehash.get_pehash(tempPath)
                file_Name = filePEhash + '___' + fileName

            if fileInfo:
                packera = fileInfo['packer']
        except Exception as e:
            print('check_file: ', e)

        mov_file(filePath, out_file_dir, fileType, file_Name)
        fpeHash.append(filePEhash)
        fn.append(fileName)
        ftype.append(fileType)
        finfo.append(fileInfo)
        fmd5.append(md5)
        packer.append(packera)
        print("name: %s\tmd5: %s\tpehash: %s\tftype: %s"%(fileName, md5, filePEhash, fileType))

    df["fileName"] = fn
    df["Md5"] = fmd5
    df["peHash"] = fpeHash
    df["ftype"] = ftype
    df["finfo"] = finfo
    df['packer'] = packer

    n = 'fRet.csv'
    try:
        if os.path.isfile(out_file_dir+'\\fRet.csv'):
            n = str(time.strftime("%Y%m%d_%H%M%S", time.localtime())) + '_fret.csv'
        else:
            n = 'fRet.csv'
    except Exception as e:
        print(e)

    df.to_csv(out_file_dir + '\\' + n)



if __name__ == "__main__":
    #print(get_md5_of_file(r'G:\999.dll'))
    scan_file_dir = r'D:\pe_before_201111\pe_before_201111_backup'
    out_file_dir = r'C:\Users\admin\Desktop\autotestresult'
    #check_file(r'E:\sample\sample', r'E:\sample\1')
    check_file(scan_file_dir, out_file_dir)