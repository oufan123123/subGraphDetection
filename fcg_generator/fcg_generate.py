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

# 测试生成的apk是否有敏感api
def test_api(apk):
    for api in apk.dapasa_api_list:
        print(api)
    for api in apk.pscout_api_list:
        print(api)

# 输出apk的信息到文件
def write_apk_message(apk, path):
    with open(path, "a") as f:
        f.write("apk_name:" + apk.apk_name)
        f.write("\n")
        f.write("node_number:" + str(apk.node_number))
        f.write("\n")
        f.write("edge_number:" + str(apk.edge_number))
        f.write("\n")
        f.write("fcg_graph_time:" + str(apk.fcg_graph_time))
        f.write("\n")
        f.write("pattern_find_time:" + str(apk.pattern_find_time))
        f.write("\n")
        f.write("dapasa_number:" + str(len(apk.dapasa_api_list)))
        f.write("\n")
        f.write("pscout_number:" + str(len(apk.pscout_api_list)))
        f.write("\n")

        for index,graph in apk.three_graph_id_dict.items():
            number = apk.three_graph_dict.get(graph)
            f.write("3:{}:{}".format(index, number))
            f.write("\n")
        for index,graph in apk.four_graph_id_dict.items():
            number = apk.four_graph_dict.get(graph)
            f.write("4:{}:{}".format(index, number))
            f.write("\n")
        for index,graph in apk.five_graph_id_dict.items():
            number = apk.five_graph_dict.get(graph)
            f.write("5:{}:{}".format(index, number))
            f.write("\n")

# 生成所有apk的函数调用图,指定apk所在目录，表明这个目录下的apk类型
def generate_all_apks_method_graph(apk_directory_path, apk_type):
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
            fcg_start_time = datetime.datetime.now()
            graph = generate_apk_method_graph(smali_loc, apk)
            print("generate apk fcg successfully")
            fcg_end_time = datetime.datetime.now()
            apk.fcg_graph_time = (fcg_end_time - fcg_start_time).seconds
            # test_api(apk)

            # 先创建一个存储apk信息的目录
            os.makedirs('..\data\{}\{}'.format(apk_type, apk_name))
            pattern_start_time = datetime.datetime.now()

            # 寻找三点子图的模式
            find_three_point_pattern(apk, graph, apk_type)
            # 寻找四点子图的模式
            find_four_point_pattern(apk, graph, apk_type)
            # 寻找五点子图的模式
            find_five_point_pattern(apk, graph, apk_type)
            pattern_end_time = datetime.datetime.now()
            apk.pattern_find_time = (pattern_end_time - pattern_start_time).seconds

            print("find apk pattern successfully")

            # 统计信息，输出到文件
            message_path = '..\data\{}\{}\message.txt'.format(apk_type, apk_name)
            write_apk_message(apk, message_path)
            # 展示一下生成的子图
            print_opcode_graph(apk)



# 生成单个apk的函数调用图
def generate_apk_method_graph(smali_loc, apk):
    # 生成函数调用图
    sfcg = gen_call_graph(smali_loc, apk)
    # nx.write_gexf(sfcg, '.\\data\\' + type + 'ApkGexf\\{}.gexf'.format(typeApkFile))
    print("generating fcg graph over")
    return sfcg


# 生成的子图展示代码
def print_opcode_graph(apk):
    index = 1
    sorted_three_list = sorted(apk.three_graph_dict.items(), key=lambda item:item[1], reverse=True)
    sorted_four_list = sorted(apk.four_graph_dict.items(), key=lambda item: item[1], reverse=True)
    sorted_five_list = sorted(apk.five_graph_dict.items(), key=lambda item: item[1], reverse=True)
    three_index= 0
    for graph,value in list(sorted_three_list):
        plt.subplot(3, 3, index)
        print("three-graph-sorted:"+str(value))
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True)
        index += 1
        three_index += 1
        if three_index > 2:
            break
    four_index = 0
    for graph,value in list(sorted_four_list):
        plt.subplot(3, 3, index)
        print("four-graph-sorted:"+str(value))
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True)
        index += 1
        four_index += 1
        if four_index > 2:
            break
    five_index = 0
    for graph,value in list(sorted_five_list):
        plt.subplot(3, 3, index)
        print("five-graph-sorted:"+str(value))
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True)
        index += 1
        five_index += 1
        if five_index > 2:
            break
    plt.show()


