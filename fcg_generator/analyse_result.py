'''
这个py文件完成任务：
对analyse的结果进行分析
'''
import networkx as nx
import matplotlib.pyplot as plt

'''
函数：目前还没有
基本分析：
analyse_graph_type: 分析子图和apk类型的关系，证明子图在恶意和良性apk中的出现频率不一样
分析apk的分析时间与apk包的大小关系(整个算法(图解析，模式查找)的复杂度)
分析apkfcg图大小(节点数目，边数目)和图解析时间的关系(图解析算法的复杂度)
分析apkfcg图大小(节点数目，边数目)和模式查找时间的关系(模式查找算法的复杂度)
恶意apk和良性apk的dapasaaapi数目和pscoutapi数目随fcg图大小发生的变化(证明相同条件下敏感api在恶意和良性apk中的出现的频率不同)
'''

def analyse_graph_type():
    pattern_dir = '..\\data\\pattern_single'
    benign_top_path = pattern_dir + '\\' + 'benign_top_20.txt'
    malware_top_path = pattern_dir + '\\' + 'malware_top_20.txt'
    benign_dict = dict()
    malware_dict = dict()
    f_benign = open(benign_top_path, 'r')
    f_malware = open(malware_top_path, 'r')
    for i in f_benign:
        i = i.strip().replace("\n", "")
        i_split = i.split(',')
        if i.startswith('graph'):
            continue
        if float(i_split[3]) == 0.0:
            score = float(i_split[2]) / (float(i_split[2]) + 2)
        else:
            score = float(i_split[2]) / (float(i_split[2]) + float(i_split[3]))
        benign_dict[i_split[0] + ',' + i_split[1]] = score
    for i in f_malware:
        i = i.strip().replace("\n", "")
        i_split = i.split(',')
        if i.startswith('graph'):
            continue
        if float(i_split[3]) == 0.0:
            score = float(i_split[2]) / (float(i_split[2]) + 2)
        else:
            score = float(i_split[2]) / (float(i_split[2]) + float(i_split[3]))
        malware_dict[i_split[0] + ',' + i_split[1]] = score
    sorted_benign_dict = sorted(benign_dict.items(), key=lambda item: item[1], reverse=True)
    sorted_malware_dict = sorted(malware_dict.items(), key=lambda item: item[1], reverse=True)

    benign_index = 1
    for index, value in list(sorted_benign_dict):
        index_list = index.split(',')
        path = pattern_dir + '\\benign\\{}\\{}.gexf'.format(index_list[0], index_list[1])
        print("benign:" + str(value))
        graph = nx.read_gexf(path)
        plt.subplot(3, 4, benign_index)
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=False)
        benign_index += 1
        if benign_index > 11:
            break
    plt.show()
    malware_index = 1
    for index, value in list(sorted_malware_dict):
        index_list = index.split(',')
        path = pattern_dir + '\\malware\\{}\\{}.gexf'.format(index_list[0], index_list[1])
        graph = nx.read_gexf(path)
        print("malware:" + str(value))
        plt.subplot(3, 4, malware_index)
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=False)
        malware_index += 1
        if malware_index > 11:
            break
    plt.show()


if __name__ == '__main__':
    analyse_graph_type()