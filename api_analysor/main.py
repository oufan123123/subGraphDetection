'''
第二个模块的启动py文件
完成对apk的语义特征分析，找到其中的敏感API，并进行统计，计算权重值。
'''
from api_finder import find_sen_api
from sen_api_generator import get_api_dict


# 根据api的权重计算公式计算敏感分数,逆序排列，输出字典结果
def compute_score(benign_api_dict, malware_api_dict):
    api_dict = dict()
    for benign_api, benign_number in benign_api_dict.items():
        malware_number = malware_api_dict[benign_api]
        if malware_number > 0 or benign_number > 0:
            score = malware_number / (malware_number + benign_number)
            api_dict[benign_api] = score
    sorted_api_dict = sorted(api_dict.items(), key=lambda item: item[1], reverse=True)
    return sorted_api_dict


if __name__ == '__main__':

    benign_api_dict, malware_api_dict = get_api_dict("..\data\sensitiveApiFromDAPASA.txt", "..\data\sensitiveApiFromPscout.txt")
    goodApkDir = "F:\\apkSampleMin\\decodeGoodApk"
    badApkDir = "F:\\apkSampleMin\\decodeBadApk"
    find_sen_api(goodApkDir, benign_api_dict)
    find_sen_api(badApkDir, malware_api_dict)
    sorted_api_dict = compute_score(benign_api_dict, malware_api_dict)

    # 输出到文件
    output_path = '..\data\senApiScore.txt'
    f = open(output_path, 'w+')
    for api, score in sorted_api_dict:
        line = '{},{},{},{}'.format(api, score, benign_api_dict[api], malware_api_dict[api])
        f.write(line)
        f.write('\n')
    f.close()