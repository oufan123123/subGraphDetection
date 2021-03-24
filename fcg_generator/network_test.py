'''
测试一些特殊情况
'''
import networkx as nx
from networkx.algorithms import isomorphism
import networkx.classes.digraph as dddd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import sklearn.ensemble as es
from sklearn.metrics import accuracy_score

if __name__ == '__main__':
    apk_array = np.zeros((4, 4))
    print(apk_array)
    apk_array[0, 1] = 1
    apk_array[2, 3] = 1
    apk_array[0, 1] = 1
    apk_array[1, 2] = 1
    # 开始训练
    x = apk_array[:, :-1]
    y = apk_array[:, -1:]
    print(x)
    print(y)
    train_size = int(len(x) * 0.7)
    train_x, test_x, train_y, test_y = x[:train_size], x[train_size:], y[:train_size], y[train_size:]

    # 训练模型
    model = RandomForestClassifier(n_estimators = 10)
    model.fit(train_x, train_y.ravel())

    # 模型测试
    pred_test_y = model.predict(test_x)

    # 模型评估
    print('bike_day的r2_score得分：', accuracy_score(test_y, pred_test_y))
