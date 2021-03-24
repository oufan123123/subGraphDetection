'''
得到dapasa的敏感API，pscout的敏感API
分别用两个字典存储，良性API字典存储其在良性apk中出现的次数，恶意API字典存储其在恶意apk中出现的次数
首先还是存储其在某个apk中出现的总数，后续根据需要统计某个API在apk的总数，或者只是计1次(更好，因为需要消除apk大小带来的偏差)，

'''

def get_api_dict(dapasa_api_path, pscout_api_path):
    benign_api_dict = dict()
    malware_api_dict = dict()
    f_dapasa = open(dapasa_api_path, "r")
    for line in f_dapasa:
        line = line.strip().replace("\n", "")
        benign_api_dict[line] = 0
        malware_api_dict[line] = 0

    f_pscout = open(pscout_api_path, "r")
    for line in f_pscout:
        line = line.strip().replace("\n", "")
        benign_api_dict[line] = 0
        malware_api_dict[line] = 0
    return benign_api_dict, malware_api_dict