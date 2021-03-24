import fnmatch
import os
import networkx as nx
from sen_api_generate import get_api_list

'''
生成函数调用图
'''
dapasa_api_list = get_api_list("..\data\sensitiveApiFromDAPASA.txt")
pscout_api_list = get_api_list("..\data\sensitiveApiFromPscout.txt")


def gen_call_graph(smali_loc, apk):
    graph = nx.DiGraph()
    all_decode_file = os.listdir(smali_loc)
    for f in all_decode_file:
        if f == 'smali':
            path = smali_loc + '\\smali'
            for dirpath, dirs, files in os.walk(path):
                for filename in fnmatch.filter(files, '*.smali'):
                    save_call(dirpath + '\\' + filename, graph, apk)
    apk.node_number = len(graph.nodes())
    apk.edge_number = len(graph.edges())
    print('Total Nodes = {}', format(len(graph.nodes())))
    print('Total Edges = {}', format(len(graph.edges())))
    return graph


# 将调用关系加到图
def save_call(smali_file, graph, apk):
    try:
        f = open(smali_file, 'r', encoding='UTF-8')
        caller_class = ''
        caller_method = ''
        for line in f:
            line = line.strip().replace("\n", "")
            line_list = line.strip().split(' ')
            # 找到类名
            if line.startswith(".class") and len(line_list)> 1:
                caller_class = line_list[len(line_list) - 1]
            # 找到函数
            elif line.startswith(".method") and len(line_list)> 1:
                caller_method = caller_class + "->" + line_list[len(line_list) - 1]
                # print("caller_method:"+caller_method)
            elif line.startswith(".end method"):
                caller_method = ''
            # 找到调用类
            elif line.startswith("invoke-") and len(line_list) > 1:
                callee_method = line_list[len(line_list) - 1]
                # print("callee_method:" + callee_method)
                if caller_method != '':
                    if callee_method in dapasa_api_list and callee_method not in apk.dapasa_api_list:
                        apk.dapasa_api_list.append(callee_method)
                    if caller_method in pscout_api_list and caller_method not in apk.pscout_api_list:
                        apk.pscout_api_list.append(caller_method)
                    graph.add_edge(caller_method, callee_method)
        f.close()
    except FileNotFoundError:
        pass
