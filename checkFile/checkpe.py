# -*- coding: utf-8 -*-
import subprocess
import ast
import os
import sys
import re
import json

pecheck = r'checkpe.exe'
DIEC_PATH = r'base\diec.exe'
print(pecheck,DIEC_PATH)

def run_pe_tool(sample_dir_os_file_path):
    # proc = subprocess.run([pecheck, sample_dir_os_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    # output = proc.stdout

    #sample_dir_os_file_path = str(sample_dir_os_file_path.encode('utf-8'))
    #print(sample_dir_os_file_path)
    cmd = '%s "%s"' % (pecheck, sample_dir_os_file_path)

    p = subprocess.Popen([pecheck, sample_dir_os_file_path], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #print(p.stdout)
    out, err = p.communicate()
    out = str(out)
    if err or p.returncode != 0:
        return False, out
    else:
        return True, out


def scan_diec(fpath):
    info = {}
    try:
        proc = subprocess.run([DIEC_PATH, "-j", fpath], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        output = proc.stdout.decode('utf-8')

        json_data = json.loads(output)
        info = {
            "compiler": "", "linker": "", "protector": "", "packer": "", "library": "",
            "sfx": "", "overlay": "", "archive": "", "installer": "", "filetype": "",
            "converter": "", "patcher": "", "player": "", "format": "", "joiner": "", "other": "",
        }

        for r in json_data['detects']:
            if r["type"] in info.keys():
                if info[r["type"]] == "":
                    info[r["type"]] = r["name"]
                else:
                    info[r["type"]] += "#{}".format(r["name"])

        info['filetype'] = json_data['filetype']

        return info
    except Exception as e:
        print(e)
        pass
    return info


def file_Check(file_path, file_type):
    info = scan_diec(file_path)
    if info:
        if info['filetype'] == 'ELF32':
            file_type = 'elf_32'
        elif info['filetype'] == 'ELF64':
            file_type = 'elf_64'
        elif 'Windows Shortcut' in info['format']:
            file_type = 'lnk_file'
        elif info['library'] == '.NET':
            file_type = 'net_file'

    return file_type, info



def get_is_pefile(file_path):
    fileType, fileInfo = 'un_file', ''
    try:
        ret, out = run_pe_tool(file_path)
        if not out:
            print("run_pe_tool返回为空")
            return fileType, fileInfo
        if not ret:
            raise Exception("pe_tool:%s" % out)

        if 'is_not_pe' in out:
            fileType, fileInfo = file_Check(file_path, 'not_pe')

        elif 'is_pe_32' in out:
            fileType, fileInfo = file_Check(file_path, 'pe_32')
        elif 'is_pe_64' in out:
            fileType, fileInfo = file_Check(file_path, 'pe_64')
        elif 'is_pe_other' in out:
            fileType, fileInfo = file_Check(file_path, 'pe_other')
        elif 'is_msi_file' in out:
            fileType = 'msi_file'
        elif 'is_ole_file' in out:
            fileType = 'ole_file'
        elif 'is_apk_file' in out:
            fileType = 'apk_file'
        elif 'is_zip_file' in out:
            fileType = 'zip_file'
        elif 'is_rar_file' in out:
            fileType = 'rar_file'
        elif 'is_sis_file' in out:
            fileType = 'sis_file'
        elif 'is_ace_file' in out:
            fileType = 'ace_file'
        elif 'is_bad_en_package' in out:
            fileType = 'bad_en_package'
        elif 'is_ne_file' in out:
            fileType = 'ne_file'
        elif 'is_le_file' in out:
            fileType = 'le_file'
        elif 'is_jar_file' in out:
            fileType = 'jar_file'
        else:
            fileType, fileInfo = file_Check(file_path, 'pe_32')
    except Exception as e:
        print('get_is_pefile error: ', e)
    return fileType, fileInfo

if __name__ == "__main__":
    import sys
    print(get_is_pefile(sys.argv[1]))
    # ret = scan_diec(r'E:\sample\test\not_pe\1c46c881c00a6fecd8ec2f5546802ccad62cdebe824e1ebbd77c9bd87c700771.lnk')
    # print(ret)
    #ret = get_is_pefile(r'E:\sample\sample\pe_64_file')
    #print(ret)

