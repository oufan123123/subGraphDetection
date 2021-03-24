'''
寻找apk中的三点，四点，五点模式
'''
import networkx as nx
from networkx.algorithms import isomorphism
import os

# 根据已知点造子图
def make_graph(fcg, adj):
    H = nx.DiGraph()
    if len(adj) == 1:
        H.add_node(adj[0])
        return H
    for i in range(0, len(adj)):
        for j in range(i + 1, len(adj)):
            if not H.has_node(adj[i]):
                H.add_node(adj[i])
            if not H.has_node(adj[j]):
                H.add_node(adj[j])
            if fcg.has_edge(adj[i], adj[j]):
                H.add_edge(adj[i], adj[j])
            if fcg.has_edge(adj[j], adj[i]):
                H.add_edge(adj[j], adj[i])
    return H


# 判断这个模式是否是与模式字典中的键异构
def judge_is_Iso(graph, pattern_dict, apk, index, apk_type, graph_type):
    if not pattern_dict:
        nx.write_gexf(graph, '..\data\{}\{}\{}-{}.gexf'.format(apk_type, apk.apk_name, graph_type, index))
        return False
    for pattern in list(pattern_dict.keys()):
        matcher = isomorphism.DiGraphMatcher(graph, pattern)
        # if isomorphism add number 1
        if matcher.is_isomorphic():
            pattern_dict[pattern] = pattern_dict[pattern] + 1
            return True
    nx.write_gexf(graph, '..\data\{}\{}\{}-{}.gexf'.format(apk_type, apk.apk_name, graph_type, index))
    return False

# 找到这个apk中的所有三点模式
def find_three_point_pattern(apk, graph, apk_type):
    # 对每个dapasa api进行遍历
    #print(len(apk.apk_name))
    #print("dapasa_api_list")
    #print(len(apk.dapasa_api_list))
    index = 0
    for dapasa_api in apk.dapasa_api_list:
        first_neigh_list = list(graph.successors(dapasa_api))
        first_neigh_list.extend(list(graph.predecessors(dapasa_api)))
        # print("first_neigh_list")
        # print(len(first_neigh_list))
        if first_neigh_list is None or not first_neigh_list:
            continue
        # 先找dapasa节点第一层邻居
        for first_neigh in first_neigh_list:
            if first_neigh == dapasa_api:
                continue
            second_neigh_list = list(graph.successors(first_neigh))
            second_neigh_list.extend(list(graph.predecessors(first_neigh)))
            # print("second_neigh_list")
            # print(len(second_neigh_list))
            if second_neigh_list is None or not second_neigh_list:
                continue
            # 再找dapasa节点第二层邻居
            for second_neigh in second_neigh_list:
                if second_neigh == first_neigh or second_neigh == dapasa_api:
                    continue
                three_point = [dapasa_api, first_neigh, second_neigh]
                subgraph = make_graph(graph, three_point)
                # 判断是否异构
                if not judge_is_Iso(subgraph, apk.three_graph_dict, apk, index, apk_type, 3):
                    # print("find three point pattern:dapasa")
                    apk.three_graph_dict[subgraph] = 1
                    apk.three_graph_id_dict[index] = subgraph
                index += 1


    # 对每个pscout api进行遍历
    for pscout_api in apk.pscout_api_list:
        first_neigh_list = list(graph.predecessors(pscout_api))
        if first_neigh_list is None or not first_neigh_list:
            continue
        # 先找pscout节点第一层邻居
        for first_neigh in first_neigh_list:
            if first_neigh == pscout_api:
                continue
            second_neigh_list = list(graph.successors(first_neigh))
            second_neigh_list.extend(list(graph.predecessors(first_neigh)))
            if second_neigh_list is None or not second_neigh_list:
                continue
            # 再找pscout节点第二层邻居
            for second_neigh in second_neigh_list:
                if second_neigh == first_neigh or second_neigh == pscout_api:
                    continue
                three_point = [pscout_api, first_neigh, second_neigh]
                subgraph = make_graph(graph, three_point)
                # 判断是否异构
                if not judge_is_Iso(subgraph, apk.three_graph_dict, apk, index, apk_type, 3):
                    #print("find three point pattern:pscout")
                    apk.three_graph_dict[subgraph] = 1
                    apk.three_graph_id_dict[index] = subgraph
                index += 1
    print("three-graph index:"+str(index))


# 找到所有apk中的所有四点模式
def find_four_point_pattern(apk, graph, apk_type):
    # 遍历dapasa api的每个节点
    index = 0
    for dapasa_api in apk.dapasa_api_list:
        first_neigh_list = list(graph.successors(dapasa_api))
        first_neigh_list.extend(list(graph.predecessors(dapasa_api)))
        if first_neigh_list is None or not first_neigh_list:
            continue
        # 找dapasa节点第一层邻居
        first_index = 0
        for first_neigh in first_neigh_list:
            if first_neigh == dapasa_api:
                continue
            second_neigh_list = list(graph.successors(first_neigh))
            second_neigh_list.extend(list(graph.predecessors(first_neigh)))
            if second_neigh_list is None or not second_neigh_list:
                continue
            # 找dapasa节点第二层邻居
            second_index = 0
            for second_neigh in second_neigh_list:
                if second_neigh == first_neigh or second_neigh == dapasa_api:
                    continue
                third_neigh_list = list(graph.successors(second_neigh))
                third_neigh_list.extend(list(graph.predecessors(second_neigh)))
                if third_neigh_list is None or not third_neigh_list:
                    continue
                # 找dapasa节点第三层邻居
                third_index = 0
                for third_neigh in third_neigh_list:
                    if third_neigh == second_neigh or third_neigh == first_neigh or third_neigh == dapasa_api:
                        continue
                    four_point = [dapasa_api, first_neigh, second_neigh, third_neigh]
                    subgraph = make_graph(graph, four_point)
                    if not judge_is_Iso(subgraph, apk.four_graph_dict, apk, index, apk_type, 4):
                        # print("find four point pattern:dapasa")
                        apk.four_graph_dict[subgraph] = 1
                        apk.four_graph_id_dict[index] = subgraph
                    index += 1
                    third_index += 1
                    if third_index > 10:
                        break
                second_index += 1
                if second_index > 10:
                    break
            first_index += 1
            if first_index > 10:
                break
    # 遍历pscout api的每个节点
    for pscout_api in apk.pscout_api_list:
        first_neigh_list = list(list(graph.predecessors(pscout_api)))
        if first_neigh_list is None or not first_neigh_list:
            continue
        # 找pscout节点第一层邻居
        first_index = 0
        for first_neigh in first_neigh_list:
            if first_neigh == pscout_api:
                continue
            second_neigh_list = list(graph.successors(first_neigh))
            second_neigh_list.extend(list(graph.predecessors(first_neigh)))
            if second_neigh_list is None or not second_neigh_list:
                continue
            # 找pscout节点第二层邻居
            second_index = 0
            for second_neigh in second_neigh_list:
                if second_neigh == first_neigh or second_neigh == pscout_api:
                    continue
                third_neigh_list = list(graph.successors(second_neigh))
                third_neigh_list.extend(list(graph.predecessors(second_neigh)))
                if third_neigh_list is None or not third_neigh_list:
                    continue
                # 找pscout节点第三层邻居
                third_index = 0
                for third_neigh in third_neigh_list:
                    if third_neigh == second_neigh or third_neigh == first_neigh or third_neigh == pscout_api:
                        continue
                    four_point = [pscout_api, first_neigh, second_neigh, third_neigh]
                    subgraph = make_graph(graph, four_point)
                    if not judge_is_Iso(subgraph, apk.four_graph_dict, apk, index, apk_type, 4):
                        # print("find four point pattern:pscout")
                        apk.four_graph_dict[subgraph] = 1
                        apk.four_graph_id_dict[index] = subgraph
                    index += 1
                    third_index += 1
                    if third_index > 10:
                        break
                second_index += 1
                if second_index > 10:
                    break
            first_index += 1
            if first_index > 10:
                break
    print("four-graph index:" + str(index))
# 找到所有apk中的所有五点模式
def find_five_point_pattern(apk, graph, apk_type):
    # 遍历dapasa api的每个节点
    index = 0
    for dapasa_api in apk.dapasa_api_list:
        first_neigh_list = list(graph.successors(dapasa_api))
        first_neigh_list.extend(list(graph.predecessors(dapasa_api)))
        if first_neigh_list is None or not first_neigh_list:
            continue
        # 找dapasa节点第一层邻居
        first_index = 0
        for first_neigh in first_neigh_list:
            if first_neigh == dapasa_api:
                continue
            second_neigh_list = list(graph.successors(first_neigh))
            second_neigh_list.extend(list(graph.predecessors(first_neigh)))
            if second_neigh_list is None or not second_neigh_list:
                continue
            # 找dapasa节点第二层邻居
            second_index = 0
            for second_neigh in second_neigh_list:
                if second_neigh == first_neigh or second_neigh == dapasa_api:
                    continue
                third_neigh_list = list(graph.successors(second_neigh))
                third_neigh_list.extend(list(graph.predecessors(second_neigh)))
                if third_neigh_list is None or not third_neigh_list:
                    continue
                # 找dapasa节点第三层邻居
                third_index = 0
                for third_neigh in third_neigh_list:
                    if third_neigh == second_neigh or third_neigh == first_neigh or third_neigh == dapasa_api:
                        continue
                    four_neigh_list = list(graph.successors(third_neigh))
                    four_neigh_list.extend(list(graph.predecessors(third_neigh)))
                    if four_neigh_list is None or not four_neigh_list:
                        continue
                    # 找dapasa第四层邻居
                    four_index = 0
                    for four_neigh in four_neigh_list:
                        if four_neigh == third_neigh or four_neigh == second_neigh or four_neigh == first_neigh or four_neigh == dapasa_api:
                            continue
                        five_point = [four_neigh, third_neigh, second_neigh, first_neigh, dapasa_api]
                        subgraph = make_graph(graph, five_point)
                        if not judge_is_Iso(subgraph, apk.five_graph_dict, apk, index, apk_type, 5):
                            # print("find five point pattern:dapasa")
                            apk.five_graph_dict[subgraph] = 1
                            apk.five_graph_id_dict[index] = subgraph
                        index += 1
                        four_index += 1
                        if four_index > 5:
                            break
                    third_index += 1
                    if third_index > 5:
                        break
                second_index += 1
                if second_index > 5:
                    break
            first_index += 1
            if first_index > 5:
                break
    # 遍历pscout api的每个节点
    for pscout_api in apk.pscout_api_list:
        first_neigh_list = list(graph.successors(pscout_api))
        first_neigh_list.extend(list(graph.predecessors(pscout_api)))
        if first_neigh_list is None or not first_neigh_list:
            continue
        # 找pscout节点第一层邻居
        first_index = 0
        for first_neigh in first_neigh_list:

            if first_neigh == pscout_api:
                continue
            second_neigh_list = list(graph.successors(first_neigh))
            second_neigh_list.extend(list(graph.predecessors(first_neigh)))
            if second_neigh_list is None or not second_neigh_list:
                continue
            # 找pscout节点第二层邻居
            second_index = 0
            for second_neigh in second_neigh_list:
                if second_neigh == first_neigh or second_neigh == pscout_api:
                    continue
                third_neigh_list = list(graph.successors(second_neigh))
                third_neigh_list.extend(list(graph.predecessors(second_neigh)))
                if third_neigh_list is None or not third_neigh_list:
                    continue
                # 找dapasa节点第三层邻居
                third_index = 0
                for third_neigh in third_neigh_list:
                    if third_neigh == second_neigh or third_neigh == first_neigh or third_neigh == dapasa_api:
                            continue
                    four_neigh_list = list(graph.successors(third_neigh))
                    four_neigh_list.extend(list(graph.predecessors(third_neigh)))
                    if four_neigh_list is None or not four_neigh_list:
                        continue
                    # 找dapasa第四层邻居
                    four_index = 0
                    for four_neigh in four_neigh_list:
                        if four_neigh == third_neigh or four_neigh == second_neigh or four_neigh == first_neigh or four_neigh == dapasa_api:
                            continue
                        five_point = [four_neigh, third_neigh, second_neigh, first_neigh, dapasa_api]
                        subgraph = make_graph(graph, five_point)
                        if not judge_is_Iso(subgraph, apk.five_graph_dict, apk, index, apk_type, 5):
                            #print("find five point pattern:pscout ")
                            apk.five_graph_dict[subgraph] = 1
                            apk.five_graph_id_dict[index] = subgraph
                        index += 1
                        four_index += 1
                        if four_index > 5:
                            break
                    third_index += 1
                    if third_index > 5:
                        break
                second_index += 1
                if second_index > 5:
                    break
            first_index += 1
            if first_index > 5:
                break
    print("five-graph index:" + str(index))















