import csv
import os

# 将CSV文件数据转换为list存储
def get_csvfile_result(filepath):
    result_list = []
    with open(filepath, 'r', encoding='UTF-8', errors='ignore') as f:
        reader = csv.reader(f)
        for row in reader:
            result_list.append(row)
    return result_list


def handle_ai_list(ai_result_list):
    blackvirus_list = []
    for i in ai_result_list[1:]:
        if i[3] > 0:
            blackvirus_list.append(i)
    return blackvirus_list

"""
software_num_list:
AI,offline_old_360_num,offline_new_360_num,online_1_360_num,online_2_360_num,offline_old_duba_num,offline_new_duba_num,
offline_old_kb_duba_num,offline_new_kb_duba_num,online_1_duba_num,online_2_duba_num,offline_old_huorong_num ,
offline_new_huorong_num,offline_old_kabasiji_num,offline_new_kabasiji_num ,
online_1_kabasiji_num,online_2_kabasiji_num,offline_old_QQ_num,offline_new_QQ_num,online_1_QQ_num,online_2_QQ_num

"""

def analy_result(final_list):
    all_num = len(final_list)
    software_num_list = [0] * 22
    num = 2
    for i in final_list:
        if int(i[2]) > 0:
            software_num_list[0] += 1
        num = 2
        for status in i[num:]:
            if status != '':
                if num > 22:
                    break
                else:
                    software_num_list[num - 1] += 1
                    num += 1
    return software_num_list

def handle_list(recent_list):
    filename_list = []
    for element in recent_list[1:]:
        if '___' in element[1]:
            element[1] = element[1].split('___')[1]
        filename_list.append(element[1])
    return recent_list,filename_list

"""
result_list:filename,2360旧库离线,3360新库离线,4360一扫,5360二扫,6毒霸旧库离线,7毒霸新库离线，8毒霸KB旧库离线,9毒霸KB新库离线，10毒霸一扫,11毒霸二扫，
                    12火绒旧库，13火绒新库，14卡巴旧库离线，15卡巴新库离线，16卡巴一扫，17卡巴二扫，18Q管旧库离线，19Q管新库离线，20Q管一扫，21Q管二扫
"""

# 获取机器学习和杀软扫描结果中相同数据
def handle_final(ai_result_list, others_result_list,malgbm_result_list):
    final_list = []
    result_list = []
    ai_result_list = handle_list(ai_result_list)[0]
    others_result_list = handle_list(others_result_list)[0]
    malgbm_result_list = handle_list(malgbm_result_list)[0]
    for element_ai in ai_result_list[1:]:
        for element_malgbm in malgbm_result_list[1:]:
            for element_others in others_result_list[1:]:
                if element_ai[1] == element_others[1]:
                    if element_ai[1] == element_malgbm[1]:
                        result_list.append(element_ai[1])
                        result_list.append(element_others[4])
                        result_list.append(element_ai[3])
                        result_list.append(element_malgbm[3])
                        for other in element_others[7:]:
                            result_list.append(other)
                        final_list.append(result_list)
                        result_list = []
    return final_list

def handle_final(ai_result_list, others_result_list,malgbm_result_list):
    final_list = []
    result_list = []
    ai_result_list = handle_list(ai_result_list)[0]
    others_result_list = handle_list(others_result_list)[0]
    malgbm_result_list = handle_list(malgbm_result_list)[0]
    for element_ai in ai_result_list[1:]:
        for element_others in others_result_list[1:]:
            if element_ai[1] == element_others[1]:
                for element_malgbm in malgbm_result_list[1:] :
                    if element_ai[1] == element_malgbm[1]:
                        result_list.append(element_ai[1])
                        result_list.append(element_others[4])
                        result_list.append(element_ai[3])
                        result_list.append(element_malgbm[3])
                        for other in element_others[7:]:
                            result_list.append(other)
                        final_list.append(result_list)
                        result_list = []
    return final_list

def handle_file_type(filetype):
    if filetype == 'un_file':
        statics_list_num = 0
    elif filetype == 'pe_32':
        statics_list_num = 1
    elif filetype == 'pe_64':
        statics_list_num = 2
    else:
        statics_list_num = 3
    return statics_list_num


def write_result_file(final_list, out_file_path):
    normal_list = ["filename", "ftype", "AI", "malgbm", "360旧库离线", "360新库离线", "360一扫", "360二扫", "毒霸旧库离线", "毒霸新库离线", "毒霸KB旧库离线", "毒霸KB新库离线",
         "KB_score", "KB_packer_score", "毒霸一扫","毒霸二扫",
         "火绒旧库", "火绒新库", "卡巴旧库离线", "卡巴新库离线", "卡巴一扫", "卡巴二扫", "Q管旧库离线", "Q管新库离线", "Q管一扫", "Q管二扫"]
    null_list = []
    statistics_num = 0  #max=23 sum=24
    # not_file pe_32 pe_64 net_file
    statistics_list=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],]
    f = open(out_file_path, 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(normal_list)
    for final_list_element in final_list:
        print(final_list_element)
        file_type = final_list_element[1]
        for i in final_list_element[2:]:
            if statistics_num < 2:
                if int(i) >=70:
                    statistics_list[handle_file_type(file_type)][statistics_num]+=1
            elif i!='':
                statistics_list[handle_file_type(file_type)][statistics_num]+=1
            statistics_num+=1
        statistics_num = 0
        csv_writer.writerow(final_list_element)

    for i in range(len(statistics_list)):
        for j in range(len(statistics_list[i])):
            statistics_list[i][j] = str(statistics_list[i][j])
    csv_writer.writerow(null_list)
    csv_writer.writerow(normal_list)

    statistics_list[0].insert(0, "")
    statistics_list[0].insert(1,"not_file")
    statistics_list[1].insert(0, "")
    statistics_list[1].insert(1, "pe_32")
    statistics_list[2].insert(0, "")
    statistics_list[2].insert(1,"pe_64")
    statistics_list[3].insert(0, "")
    statistics_list[3].insert(1, "net_file")

    for element in statistics_list:
        csv_writer.writerow(element)
    f.close()


"""
ai_result_list:sha256,filename,predtype,score,malConfidence0新库离
others_result_list:0unnamed,1filename,2md5,3pehash,4ftype,5finfo,6packer,7360旧库离线,836线,9360一扫,10360二扫,11毒霸旧库离线,12毒霸新库离线，13毒霸KB旧库离线,14毒霸KB新库离线，15KB_score,16KB_packer_score,
16毒霸一扫,17毒霸二扫，18火绒旧库，19火绒新库，20卡巴旧库离线，21卡巴新库离线，22卡巴一扫，23卡巴二扫，24Q管旧库离线，25Q管新库离线，26Q管一扫，27Q管二扫
"""
if __name__ == '__main__':
    # 机器学习分析结果
    ai_csv_path = f'C:\\Users\\admin\Desktop\\virustest\\ai_results.csv'
    # malgbm分析结果
    malgbm_csv_path = f'C:\\Users\\admin\Desktop\\virustest\\ai_results_malgbm.csv'
    # 所有杀软扫描结果
    others_csv_path = f'C:\\Users\\admin\Desktop\\virustest\\fRet_log_info.csv'
    # 输出结果
    out_file_path = f'C:\\Users\\admin\\Desktop\\virustest\\result.csv'
    # 获取所有文件数据
    ai_result_list = get_csvfile_result(ai_csv_path)
    others_result_list = get_csvfile_result(others_csv_path)
    malgbm_result_list = get_csvfile_result(malgbm_csv_path)
    final_list = handle_final(ai_result_list, others_result_list,malgbm_result_list)
    software_num_list = analy_result(final_list)
    write_result_file(final_list, out_file_path)

