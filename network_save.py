import numpy as np
import pandas as pd
import networkx as nx
import math
from itertools import product
import matplotlib.pyplot as plt
import random
import time
import copy
import pickle


def distance(x1, x2, y1, y2):
    '''
    距離を計算する関数
    Perameters
    :param x1,x2,y1,y2: float
        点1の座標（x1,y1）と点2の座標（x2,y2）
    :return: float
        距離
    '''
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return d


def Setting(FILENAME):
    '''
    ファイルから各種情報を取り出す関数

    :param FILENAME: str
            ファイル名（拡張子含めて）
    :return:
        Setting_Info：list
            0:車両数、4:キャパ、8:タクシー車両の最大走行時間、9:顧客一人の最大乗車時間
        request_number ：int
            デポを含めた頂点数
        depo_zahyo：list
            デポの座標
        c:list
            各頂点間の距離
        e:list
            最早時間窓
        l:list
            最遅時間窓
        noriori:list
            乗り降り決定変数
    '''
    mat = []
    with open('/home/kurozumi/デスクトップ/shin_darpbench/' + FILENAME, 'r', encoding='utf-8') as fin:
        for line in fin.readlines():
            row = []
            toks = line.split()
            for tok in toks:
                try:
                    num = float(tok)
                except ValueError:
                    continue
                row.append(num)
            mat.append(row)
    # インスタンスの複数の行（問題設定）を取り出す
    Setting_Info = mat.pop(0)  # 0:車両数、4:キャパシティ、8:一台あたりの最大移動時間(min)、9:一人あたりの最大移動時間(min)

    # デポの座標を取り出す
    depo_zahyo = np.zeros(2)  # デポ座標配列
    x = mat.pop(-1)
    depo_zahyo[0] = x[1]
    depo_zahyo[1] = x[2]

    request_number = len(mat) - 1

    # 各距離の計算
    c = np.zeros((len(mat), len(mat)), dtype=float, order='C')

    # eがtime_windowの始、lが終
    e = np.zeros(len(mat), dtype=int, order='C')
    l = np.zeros(len(mat), dtype=int, order='C')

    # テキストファイルからtime_windowを格納 & 各ノードの距離を計算し格納
    for i in range(len(mat)):
        e[i] = mat[i][5]
        l[i] = mat[i][6]
        for j in range(len(mat)):
            c[i][j] = distance(mat[i][1], mat[j][1], mat[i][2], mat[j][2])

    # 乗り降りの0-1情報を格納
    noriori = np.zeros(len(mat), dtype=int, order='C')
    for i in range(len(mat)):
        noriori[i] = mat[i][4]

    return Setting_Info, request_number, depo_zahyo, c, e, l, noriori

def network_creat(Time_expand):
    '''

    :param Time_expand: int
        時空間ネットワークの間隔 T
    :param kakucho: int
        最遅時間窓にプラスするノードの数
    :return: G
        時空間ネットワーク
    '''
    G = nx.DiGraph()  # ノード作成
    for i in range(n):
        early_time = e[i]
        late_time = l[i]
        if e[i] == 0:
            early_time = 0
        add_node = range(early_time, late_time)
        if i == 0:
            G.add_node((0, 0))
        else:
            for j in add_node:
                if j % Time_expand == 0:
                    G.add_node((i, j))
    G.add_node((n, T + 1))
    # G.add_edge((0,0),(1,5),weight=Setting_Info[3][0][1])

    for a in range(n):
        early_time = e[a]
        late_time = l[a]

        add_node = range(early_time, late_time)
        for j in add_node:
            if j % Time_expand == 0:
                b = 0
                for i in range(n - 1):  # 各ノードからdepoに帰るエッジがつくられていない & ここのループだとdepoのノード同士がつながらないので改善が必要
                    if a == 0 and noriori[i + 1] > 0:
                        next_early_time = e[i + 1]
                        next_late_time = l[i + 1]

                        next_add_node = range(next_early_time, next_late_time)
                        for k in next_add_node:
                            if k % Time_expand == 0:
                                distance_check = math.ceil(Distance[a][i + 1])
                                if distance_check + j <= k:  # このedgeを追加するコードは無駄な処理を含んでいます。直す必要アリ(5/10)
                                    b = 1
                                    if a == i + 1:
                                        if k - j == 1:
                                            G.add_edge((0, 0), (i + 1, k), weight=Distance[a][i + 1])
                                            G.edges[(0, 0), (i + 1, k)]['penalty'] = 0
                                            G.edges[(0, 0), (i + 1, k)]['ph'] = 1/k

                                    else:
                                        G.add_edge((0, 0), (i + 1, k), weight=Distance[a][i + 1])
                                        G.edges[(0, 0), (i + 1, k)]['penalty'] = 0
                                        G.edges[(0, 0), (i + 1, k)]['ph'] = 1/k

                                if b == 1:
                                    break
                    elif not a == 0 and not a-(i+1) == Request:
                        if noriori[a] > 0:
                            next_early_time = e[i + 1]
                            next_late_time = l[i + 1]
                            connect_abs = l[a] - next_late_time
                            if abs(connect_abs) <= Setting_Info_base[9]:
                                next_add_node = range(next_early_time, next_late_time)
                                for k in next_add_node:
                                    if k > j:
                                        if k % Time_expand == 0:
                                            distance_check = math.ceil(Distance[a][i + 1])
                                            if distance_check + j <= k:  # このedgeを追加するコードは無駄な処理を含んでいます。直す必要アリ(5/10)
                                                b = 1
                                                if not a ==i+1:
                                                    G.add_edge((a, j), (i + 1, k), weight=Distance[a][i + 1])
                                                    G.edges[(a, j), (i + 1, k)]['penalty'] = 0
                                                    G.edges[(a, j), (i + 1, k)]['ph'] = 1/abs(j - k)

                                            if b == 1:
                                                b = 0
                                                break
                        else:
                            next_early_time = e[i + 1]
                            next_late_time = l[i + 1]

                            next_add_node = range(next_early_time, next_late_time)
                            for k in next_add_node:
                                if k >j:
                                    if k % Time_expand == 0:
                                        distance_check = math.ceil(Distance[a][i + 1])
                                        if distance_check + j <= k:  # このedgeを追加するコードは無駄な処理を含んでいます。直す必要アリ(5/10)
                                            b = 1
                                            if not a == i + 1:

                                                G.add_edge((a, j), (i + 1, k), weight=Distance[a][i + 1])
                                                G.edges[(a, j), (i + 1, k)]['penalty'] = 0
                                                G.edges[(a, j), (i + 1, k)]['ph'] = 1/abs(j - k)
                                        if b == 1:
                                            b = 0
                                            break

    for i in range(n - 1):
        if noriori[i + 1] < 0:
            early_time = e[i + 1]
            late_time = l[i + 1]

            add_node = range(early_time, late_time)
            for j in add_node:
                if j % Time_expand == 0:
                    b = 0
                    depo_repeat = range(early_time, l[0])
                    for k in depo_repeat:
                        if k % Time_expand == 0:
                            distance_check = math.ceil(Distance[i + 1][0])
                            if j + distance_check <= k:
                                b = 1
                                G.add_edge((i + 1, j), (n, T + 1), weight=Distance[i + 1][0])
                                G.edges[(i + 1, j), (n, T + 1)]['penalty'] = 0
                                G.edges[(i + 1, j), (n, T + 1)]['ph'] = 1/(T + 1 - j)
                            if b == 1:
                                break

    pos = {n: (n[1], -n[0]) for n in G.nodes()}  # ノードの座標に注意：X座標がノード番号、Y座標が時刻t

    return G

if __name__ == '__main__':
    FILENAME = 'darp05EX.txt'
    Setting_Info = Setting(FILENAME)
    Setting_Info_base = Setting_Info[0] #ベンチマーク問題の１行目（設定情報）を抜き出した変数
    Syaryo =int(Setting_Info_base[0]) #車両数
    Syaryo_max_time = Setting_Info_base[8] #車両の最大稼働時間
    T = int(Setting_Info_base[5])  # 時間数
    n = int(Setting_Info[1]) + 1  # デポを含めた頂点数
    Request = int((n - 1) / 2)  # リクエスト数
    Distance = Setting_Info[3]  # 距離
    e = Setting_Info[4]  # early time
    l = Setting_Info[5]  # delay time
    d = 5  # 乗り降りにようする時間
    noriori = Setting_Info[6] #乗り降り0-1決定変数

    time_expand = 1
    t1 = time.time()
    G = network_creat(Time_expand=time_expand)
    t2= time.time()
    print(t2-t1)
    FILENAME=FILENAME.replace('.txt','')
    nx.write_gpickle(G,'time_network2'+FILENAME)