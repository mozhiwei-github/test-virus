import os
import re
import pandas as pd
from chardet.universaldetector import UniversalDetector

"""
1. 将各杀软日志转换编码为‘utf-8’
2. 读取日志信息
3. 统计日志数据表格输出
"""


###################################
# 以下为修改文件编码功能函数
#####################################
def get_encode_info(file):
    with open(file, 'rb') as f:
        detector = UniversalDetector()
        for line in f.readlines():
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        return detector.result['encoding']


def read_file(file):
    with open(file, 'rb') as f:
        return f.read()


def write_file(content, file):
    with open(file, 'wb') as f:
        f.write(content)


def convert_encode2utf8(file, original_encode, des_encode, outfile):
    file_content = read_file(file)
    file_decode = file_content.decode(original_encode, 'ignore')
    file_encode = file_decode.encode(des_encode)
    write_file(file_encode, outfile)


###############################
# 读取修改日志编码
###############################
def get360LogInfo(fileName, filePath):
    ret = ''
    try:
        r = r"\[(.*?)\]"
        with open(filePath, 'r', encoding='utf8') as f:
            line = f.readline()
            while line:
                line = str(line)
                if fileName in line:
                    temp = re.findall(r, line, re.DOTALL)
                    ret = temp[1]
                    print(fileName, ret)
                    break
                line = f.readline()
        # print(fileName, ret)
    except Exception as e:
        print('ERROR get360LogInfo: ', e)
    return ret


def getDUBALogInfo(fileName, filePath):
    ret = ''
    # Bcode = get_encoding(filePath)
    # fileName = os.path.basename(fileName)
    try:
        r = r"类型：(.*)"
        with open(filePath, 'r', encoding='utf8') as f:
            line = f.readline()
            while line:
                line = str(line.encode('utf8').decode('utf8'))
                # print(line)
                if fileName in line:
                    for i in (1, 2, 3):
                        line = f.readline().encode('utf8').decode('utf8')
                        temp = len(re.findall(r, line))
                        if temp > 0:
                            ret = re.findall(r, line)[0]
                            break
                    print(fileName, ret)
                    break
                line = f.readline()
    except Exception as e:
        print('ERROR getDubaLogInfo: ', e)
    return ret


def getkbloginfo(fileName, filePath, bcase):
    ret = ''
    try:
        if bcase == 1:
            r = r".*\t(.*)\n"
        else:
            r = r".*\t(.*)\t"

        with open(filePath, 'r', encoding='utf8') as f:
            line = f.readline()
            while line:
                line = str(line.encode('utf8').decode('utf8'))
                # print(line)
                if fileName in line:
                    ret = re.findall(r, line)[0]
                    #print(fileName, ret)
                line = f.readline()
    except Exception as e:
        print('getKbLoginfo: ', e)
    return ret


def get_huortong_log(fileName, filePath):
    ret = ''
    #na = ''
    try:
        r = r"病毒名：(.*?),"
        with open(filePath, 'r', encoding='utf-8') as f:
            line = f.readline()
            while line:
                line = str(line)
                if fileName in line:
                    ret = re.findall(r, line)[0]
                    #cl = re.findall(r'处理结果：(.*?)\n',line)[0]
                    #k = re.split('/', ret)
                    #ret = k[0] + ',' + k[1] + ', ' + cl
                    print(fileName, ret)
                    break
                line = f.readline()
        # print(fileName, ret)
    except Exception as e:
        print('get_huortong_log: ',fileName, e)
    return ret


def get_kaspersky_log(fileName, filePath):
    ret = ''
    try:
        with open(filePath, 'r', encoding='utf-8') as f:
            line = f.readline()
            while line:
                line = str(line)
                if fileName in line:
                    ret = line.split('\t')[4]
                    print(fileName, ret)
                    break
                line = f.readline()
        # print(fileName, ret)
    except Exception as e:
        print('get_huortong_log: ', e)

    return ret


def qq_log(fileName, filePath):
    ret = ''
    try:
        r = r"\[(.*?)\]"
        with open(filePath, 'r', encoding='utf8') as f:
            line = f.readline()
            while line:
                line = str(line)
                if fileName in line:
                    ret = re.findall(r, line)[0]
                    break
                line = f.readline()
        # print(fileName, ret)
    except Exception as e:
        print('getqqLogInfo: ', e)
    return ret


def log_file_check(av_n, index, index1, file_name, home):
    ret = False
    log_file_path = ''
    if (av_n in file_name) and (index in file_name) and (index1 in file_name):
        if len(index1) == 2:
            index1 = index1[0]
        log_file_path = home + '\\' + av_n + '-' + index + '-' + index1
        if os.path.isfile(log_file_path):
            ret = True
            print(log_file_path)
            return ret
        # file_content = read_file(os.path.join(home, file_name))
        encode_info = get_encode_info(os.path.join(home, file_name))
        file_path = os.path.join(home, file_name)
        if encode_info != 'utf-8':
            convert_encode2utf8(file_path, encode_info, 'utf-8', log_file_path)
        else:
            log = read_file(file_path)
            write_file(log, log_file_path)
        ret = True
    if ret:
        print(log_file_path)
    return ret


def change_av_log_encode(file_dir):
    """
    1. 直接将指定目录里面的txt文件修改编码
    2. 通过文件名匹配确定是那家杀软日志
    """
    kb_log_path = ''
    # 获取指定杀软日志路径
    for home, dirs, files in os.walk(file_dir + '\\log'):
        for filename in files:
            if 'kboost' in filename:
                kb_log_path = os.path.join(home, filename)
            log_file_check('360', 'new', 'offline', filename, home)
            log_file_check('360', 'old', 'offline', filename, home)
            log_file_check('360', 'online', '1-', filename, home)
            log_file_check('360', 'online', '2-', filename, home)
            log_file_check('duba', 'new-', 'offline', filename, home)
            log_file_check('duba', 'old-', 'offline', filename, home)
            log_file_check('duba', 'online', '1-', filename, home)
            log_file_check('duba', 'online', '2-', filename, home)
            log_file_check('duba', 'old_kb', 'offline', filename, home)
            log_file_check('duba', 'new_kb', 'offline', filename, home)
            log_file_check('huorong', 'old', 'offline', filename, home)
            log_file_check('huorong', 'new', 'offline', filename, home)
            log_file_check('kaba', 'new', 'offline', filename, home)
            log_file_check('kaba', 'old', 'offline', filename, home)
            log_file_check('kaba', 'online', '1-', filename, home)
            log_file_check('kaba', 'online', '2-', filename, home)
            log_file_check('qq', 'new', 'offline', filename, home)
            log_file_check('qq', 'old', 'offline', filename, home)
            log_file_check('qq', 'online', '1-', filename, home)
            log_file_check('qq', 'online', '2-', filename, home)
    return kb_log_path


def get_av_log_info_to_csv(file_dir, date, kb):
    big360offlinenew = file_dir + '\\log' + '\\360-new-offline'
    big360online2 = file_dir + '\\log' + '\\360-online-2'
    big360offlineold = file_dir + '\\log' + '\\360-old-offline'
    big360online1 = file_dir + '\\log' + '\\360-online-1'
    bigdubaofflinenew = file_dir + '\\log' + '\\duba-new--offline'
    bigdubaonline2 = file_dir + '\\log' + '\\duba-online-2'
    bigdubaofflineold = file_dir + '\\log' + '\\duba-old--offline'
    bigdubaonline1 = file_dir + '\\log' + '\\duba-online-1'
    bigdubaofflineoldkb = file_dir + '\\log' + '\\duba-old_kb-offline'
    bigdubaofflinenewkb = file_dir + '\\log' + '\\duba-new_kb-offline'
    huorongold = file_dir + '\\log' + '\\huorong-old-offline'
    huorongnew = file_dir + '\\log' + '\\huorong-new-offline'
    kaspersky_off_new = file_dir + '\\log' + '\\kaba-new-offline'
    kaspersky_on2 = file_dir + '\\log' + '\\kaba-online-2'
    kaspersky_off_old = file_dir + '\\log' + '\\kaba-old-offline'
    kaspersky_on1 = file_dir + '\\log' + '\\kaba-online-1'
    qq_off_new = file_dir + '\\log' + '\\qq-new-offline'
    qq_on2 = file_dir + '\\log' + '\\qq-online-2'
    qq_off_old = file_dir + '\\log' + '\\qq-old-offline'
    qq_on1 = file_dir + '\\log' + '\\qq-online-1'
    kboost = kb
    fret = file_dir + '\\' + date + '\\fRet.csv'
    df = pd.read_csv(fret)
    df['360旧库离线'] = df['fileName'].apply(get360LogInfo, args=(big360offlineold,))
    df['360新库离线'] = df['fileName'].apply(get360LogInfo, args=(big360offlinenew,))
    df['360一扫'] = df['fileName'].apply(get360LogInfo, args=(big360online1,))
    df['360二扫'] = df['fileName'].apply(get360LogInfo, args=(big360online2,))
    df['毒霸旧库离线'] = df['fileName'].apply(getDUBALogInfo, args=(bigdubaofflineold,))
    df['毒霸新库离线'] = df['fileName'].apply(getDUBALogInfo, args=(bigdubaofflinenew,))
    df['毒霸KB旧库离线'] = df['fileName'].apply(getDUBALogInfo, args=(bigdubaofflineoldkb,))
    df['毒霸KB新库离线'] = df['fileName'].apply(getDUBALogInfo, args=(bigdubaofflinenewkb,))
    df['KB_score'] = df['fileName'].apply(getkbloginfo, args=(kboost, 1,))
    df['KB_packer_score'] = df['fileName'].apply(getkbloginfo, args=(kboost, 2,))
    df['毒霸一扫'] = df['fileName'].apply(getDUBALogInfo, args=(bigdubaonline1,))
    df['毒霸二扫'] = df['fileName'].apply(getDUBALogInfo, args=(bigdubaonline2,))
    df['火绒旧库'] = df['fileName'].apply(get_huortong_log, args=(huorongold,))
    df['火绒新库'] = df['fileName'].apply(get_huortong_log, args=(huorongnew,))
    df['卡巴旧库离线'] = df['fileName'].apply(get_kaspersky_log, args=(kaspersky_off_old,))
    df['卡巴新库离线'] = df['fileName'].apply(get_kaspersky_log, args=(kaspersky_off_new,))
    df['卡巴一扫'] = df['fileName'].apply(get_kaspersky_log, args=(kaspersky_on1,))
    df['卡巴二扫'] = df['fileName'].apply(get_kaspersky_log, args=(kaspersky_on2,))
    df['Q管旧库离线'] = df['fileName'].apply(qq_log, args=(qq_off_old,))
    df['Q管新库离线'] = df['fileName'].apply(qq_log, args=(qq_off_new,))
    df['Q管一扫'] = df['fileName'].apply(qq_log, args=(qq_on1,))
    df['Q管二扫'] = df['fileName'].apply(qq_log, args=(qq_on2,))
    df.to_csv(file_dir + '\\' + date + '\\fRet_log_info.csv', index=False)


def log_info(file_dir, date):
    def kblog(df):
        temp = 0
        for i in list(df['KB_score']):
            if i:
                if float(i) >= 0.5:
                    temp += 1
        return temp

    file_info = file_dir + '\\' + date + '\\fRet_log_info.csv'
    df = pd.read_csv(file_info, encoding='utf-8')

    # pe32
    pe32 = df[df['ftype'] == 'pe_32']
    pe32_total = (len(pe32['Md5'].tolist()))
    pe32_duba_off = (pe32['毒霸离线'].notna().tolist().count(True))
    pe32_duba_on = (pe32['毒霸在线'].notna().tolist().count(True))
    pe32_hr = (pe32['火绒'].notna().tolist().count(True))
    pe32_ks_off = (pe32['卡巴离线'].notna().tolist().count(True))
    pe32_ks_on = (pe32['卡巴在线'].notna().tolist().count(True))
    pe32_360_off = (pe32['360离线'].notna().tolist().count(True))
    pe32_360_on = (pe32['360在线'].notna().tolist().count(True))
    pe32_kb = kblog(pe32)

    # pe64
    pe64 = df[df['ftype'] == 'pe_64']
    pe64_total = (len(pe64['Md5'].tolist()))
    pe64_duba_off = (pe64['毒霸离线'].notna().tolist().count(True))
    pe64_duba_on = (pe64['毒霸在线'].notna().tolist().count(True))
    pe64_hr = (pe64['火绒'].notna().tolist().count(True))
    pe64_ks_off = (pe64['卡巴离线'].notna().tolist().count(True))
    pe64_ks_on = (pe64['卡巴在线'].notna().tolist().count(True))
    pe64_360_off = (pe64['360离线'].notna().tolist().count(True))
    pe64_360_on = (pe64['360在线'].notna().tolist().count(True))
    pe64_kb = kblog(pe64)

    # netf
    netf = df[df['ftype'] == 'net_file']
    netf_total = (len(netf['Md5'].tolist()))
    netf_duba_off = (netf['毒霸离线'].notna().tolist().count(True))
    netf_duba_on = (netf['毒霸在线'].notna().tolist().count(True))
    netf_hr = (netf['火绒'].notna().tolist().count(True))
    netf_ks_off = (netf['卡巴离线'].notna().tolist().count(True))
    netf_ks_on = (netf['卡巴在线'].notna().tolist().count(True))
    netf_360_off = (netf['360离线'].notna().tolist().count(True))
    netf_360_on = (netf['360在线'].notna().tolist().count(True))
    netf_kb = kblog(netf)

    # olef
    olef = df[df['ftype'] == 'ole_file']
    olef_total = (len(olef['Md5'].tolist()))
    olef_duba_off = (olef['毒霸离线'].notna().tolist().count(True))
    olef_duba_on = (olef['毒霸在线'].notna().tolist().count(True))
    olef_hr = (olef['火绒'].notna().tolist().count(True))
    olef_ks_off = (olef['卡巴离线'].notna().tolist().count(True))
    olef_ks_on = (olef['卡巴在线'].notna().tolist().count(True))
    olef_360_off = (olef['360离线'].notna().tolist().count(True))
    olef_360_on = (olef['360在线'].notna().tolist().count(True))
    olef_kb = kblog(olef)

    # notpe
    notpe = df[(df['ftype'] != 'ole_file') & (df['ftype'] != 'net_file') & (df['ftype'] != 'pe_64') &
               (df['ftype'] != 'pe_32') & (df['ftype'] != 'elf_32') & (df['ftype'] != 'elf_64')]
    notpe_total = (len(notpe['Md5'].tolist()))
    notpe_duba_off = (notpe['毒霸离线'].notna().tolist().count(True))
    notpe_duba_on = (notpe['毒霸在线'].notna().tolist().count(True))
    notpe_hr = (notpe['火绒'].notna().tolist().count(True))
    notpe_ks_off = (notpe['卡巴离线'].notna().tolist().count(True))
    notpe_ks_on = (notpe['卡巴在线'].notna().tolist().count(True))
    notpe_360_off = (notpe['360离线'].notna().tolist().count(True))
    notpe_360_on = (notpe['360在线'].notna().tolist().count(True))
    notpe_kb = kblog(notpe)

    sample_total = pe32_total + pe64_total + netf_total + olef_total + notpe_total
    duba_off_total = pe32_duba_off + pe64_duba_off + netf_duba_off + notpe_duba_off + olef_duba_off
    s_off_total = pe32_360_off + pe64_360_off + netf_360_off + notpe_360_off + olef_360_off
    ks_off_total = pe32_ks_off + pe64_ks_off + netf_ks_off + notpe_ks_off + olef_ks_off
    hr_total = pe32_hr + pe64_hr + netf_hr + notpe_hr + olef_hr
    kb_total = pe32_kb + netf_kb + notpe_kb + olef_kb + pe64_kb
    s_on_total = pe32_360_on + pe64_360_on + netf_360_on + notpe_360_on + olef_360_on
    duba_on_total = pe32_duba_on + pe64_duba_on + netf_duba_on + notpe_duba_on + olef_duba_on
    ks_on_total = pe32_ks_on + pe64_ks_on + netf_ks_on + notpe_ks_on + olef_ks_on

    print(date)
    print('类型', '\t', '总量', '\t', '毒霸离线', '\t', '360离线', '\t', '卡巴离线', '\t', '火绒',
          '\t', 'kboost', '\t', '360在线', '\t', '毒霸在线', '\t', '卡巴在线')
    print('pe_32', '\t', pe32_total, "\t", pe32_duba_off, "\t", pe32_360_off, "\t", pe32_ks_off, "\t", pe32_hr, "\t",
          pe32_kb, "\t", pe32_360_on, "\t", pe32_duba_on, "\t", pe32_ks_on)
    print('pe_64', '\t', pe64_total, "\t", pe64_duba_off, "\t", pe64_360_off, "\t", pe64_ks_off, "\t", pe64_hr, "\t",
          pe64_kb, "\t", pe64_360_on, "\t", pe64_duba_on, "\t", pe64_ks_on)
    print('net_file', '\t', netf_total, "\t", netf_duba_off, "\t", netf_360_off, "\t", netf_ks_off, "\t", netf_hr, "\t",
          netf_kb, "\t", netf_360_on, "\t", netf_duba_on, "\t", netf_ks_on)
    print('ole_file', '\t', olef_total, "\t", olef_duba_off, "\t", olef_360_off, "\t", olef_ks_off, "\t", olef_hr, "\t",
          olef_kb, "\t", olef_360_on, "\t", olef_duba_on, "\t", olef_ks_on)
    print('not_pe', '\t', notpe_total, "\t", notpe_duba_off, "\t", notpe_360_off, "\t", notpe_ks_off, "\t", notpe_hr,
          "\t",
          notpe_kb, "\t", notpe_360_on, "\t", notpe_duba_on, "\t", notpe_ks_on)
    print('ALL', '\t', sample_total, '\t', duba_off_total, '\t', s_off_total, '\t', ks_off_total, "\t", hr_total, "\t",
          kb_total, '\t', s_on_total, '\t', duba_on_total, '\t', ks_on_total)


def get_av_log(file_dir, date):
    kb = change_av_log_encode(file_dir)
    get_av_log_info_to_csv(file_dir, date, kb)
    #log_info(file_dir, date)


if __name__ == "__main__":
    #get_kaspersky_log('ffb754f38c5d363e203e48279bfe779ad8a1e4d546c1a1650912e9fb0385430b', r'E:\sample\virusmodel-20210907\log\big-kabasiji-new-offline-20210907.txt')
    get_av_log(r'C:\Users\admin\Desktop\virusmodel-20211206', '20211206')
    #qq_log('0631de7652344b360019ee273589f1adc811e2511bfd80d77e45ce6203815e74', r'E:\sample\virusmodel-20210921\log\qq-online-1')
