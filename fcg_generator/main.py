'''
第一个模块的启动py文件
完成对apk的fcg图构造，根据敏感API选择子图
'''
from fcg_generate import generate_all_apks_method_graph


if __name__ == '__main__':
    goodApkDir = "F:\\apkSampleMin\\decodeGoodApk"
    badApkDir = "F:\\apkSampleMin\\decodeBadApk"
    generate_all_apks_method_graph(goodApkDir, "benign")
    generate_all_apks_method_graph(badApkDir, "malware")