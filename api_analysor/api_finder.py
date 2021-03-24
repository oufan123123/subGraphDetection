from method_generator import gen_call_graph
from apk import Apk
import os
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from pattern_find import find_three_point_pattern
from pattern_find import find_four_point_pattern
from pattern_find import find_five_point_pattern
import datetime
import fnmatch



# 查找所有的敏感API
def find_sen_api(apk_directory_path, api_dict):
    try:
        file = Path(apk_directory_path)
        my_abs_path = file.resolve()
    except FileNotFoundError:
        # 不存在
        print("file or dir not exist")
        return
    else:
        typeApkFiles = os.listdir(apk_directory_path)
        for typeApkFile in typeApkFiles:
            print(typeApkFile)
            smali_loc = apk_directory_path + '\\' + typeApkFile
            apk_name = typeApkFile[:-4]
            print(apk_name)
            apk = Apk(apk_name)
            # 生成FCG图
            start_time = datetime.datetime.now()
            api_set = find_apk_smali(smali_loc, apk, api_dict)
            for sen_api in api_set:
                api_dict[sen_api] = api_dict[sen_api] + 1
            end_time = datetime.datetime.now()
            print('{}:time:{}'.format(typeApkFile, (start_time - end_time).seconds))


# 查找所有apk反编译后的文件
def find_apk_smali(smali_loc, apk, api_dict):
    all_decode_file = os.listdir(smali_loc)
    api_set = set()
    for f in all_decode_file:
        if f == 'smali':
            path = smali_loc + '\\smali'
            for dirpath, dirs, files in os.walk(path):
                for filename in fnmatch.filter(files, '*.smali'):
                    find_api_smali(dirpath + '\\' + filename, api_set, api_dict)
    return api_set


# 查找一个smali文件的敏感API
def find_api_smali(smali_file, api_set, api_dict):
    try:
        f = open(smali_file, 'r', encoding='UTF-8')
        caller_class = ''
        for line in f:
            line = line.strip().replace("\n", "")
            line_list = line.strip().split(' ')
            # 找到类名
            if line.startswith(".class") and len(line_list)> 1:
                caller_class = line_list[len(line_list) - 1]
            # 找到函数
            elif line.startswith(".method") and len(line_list)> 1:
                caller_method = caller_class + "->" + line_list[len(line_list) - 1]
                if caller_method in api_dict:
                    api_set.add(caller_method)
                # print("caller_method:"+caller_method)
            # 找到调用类
            elif line.startswith("invoke-") and len(line_list) > 1:
                callee_method = line_list[len(line_list) - 1]
                # print("callee_method:" + callee_method)
                if callee_method in api_dict:
                    api_set.add(callee_method)
        f.close()
    except FileNotFoundError:
        pass