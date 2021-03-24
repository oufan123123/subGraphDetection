'''
得到dapasa的敏感API，pscout的敏感API
'''

def get_api_list(api_path):
    api_list = list()
    f = open(api_path, "r")
    for line in f:
        line = line.strip().replace("\n", "")
        api_list.append(line)
    return api_list