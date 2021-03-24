'''
定义apk的属性
'''
import networkx as nx

class Apk:
    def __init__(self, apk_name):
        # apk的基本信息统计
        self.apk_name = apk_name
        self.node_number = 0
        self.edge_number = 0
        self.fcg_graph_time = 0
        self.pattern_find_time = 0
        self.dapasa_api_list = list()
        self.pscout_api_list = list()

        # 存储3,4,5个点下的各种子图的总数，键值对为:子图--数目
        self.three_graph_dict= dict()
        self.four_graph_dict = dict()
        self.five_graph_dict = dict()

        # 存储3,4,5个点下的各种子图的存在磁盘上的路径名称，键值对为:id--子图
        # 可以存储到文件，方便后期的信息统计
        self.three_graph_id_dict = dict()
        self.four_graph_id_dict = dict()
        self.five_graph_id_dict = dict()



