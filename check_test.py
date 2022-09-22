import numpy as np
import pandas as pd
import networkx as nx
import math
from itertools import product
import matplotlib.pyplot as plt
import random

def distance(x1, x2, y1, y2):
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return d


def Setting(FILENAME):
    mat = []
    with open('/Users/kurozumi ryouho/Desktop/benchmark2/' + FILENAME, 'r', encoding='utf-8') as fin:
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

def total_distance(loot):
    Total = np.zeros(len(loot))

    for i in range(len(loot)):
        if not loot[i] ==[]:
            kyori =Distance[loot[i][0][0]][0] + Distance[loot[i][-1][0]][n-1]
            Total[i] += kyori
            for j in range(len(loot[i])-1):
                kyori = Distance[loot[i][j][0]][loot[i][j+1][0]]
                Total[i] += kyori
    return Total



if __name__ == '__main__':
    FILENAME = 'darp01EX.txt'
    Setting_Info = Setting(FILENAME)
    Setting_Info_base = Setting_Info[0]

    Syaryo_max_time = Setting_Info_base[8]
    T = int(Setting_Info_base[5])  # 時間数
    n = int(Setting_Info[1]) + 1  # デポを含めた頂点数
    Request = int((n - 1) / 2)  # リクエスト数
    Distance = Setting_Info[3]  # 距離
    e = Setting_Info[4]  # early time
    l = Setting_Info[5]  # delay time
    d = 10  # 乗り降りにようする時間
    noriori = Setting_Info[6]

    loot =[[(9, 33), (9, 38), (17, 86), (17, 91), (41, 100), (41, 105), (33, 113), (33, 118), (3, 162), (3, 167), (10, 186), (10, 191), (27, 209), (27, 214), (7, 220), (7, 225), (31, 228), (31, 233), (34, 260), (34, 265), (2, 271), (2, 276), (12, 307), (12, 312), (26, 329), (26, 334), (36, 381), (36, 386), (19, 454), (19, 459), (43, 472), (43, 477), (23, 483), (23, 488), (47, 493), (47, 498)], [(14, 111), (14, 116), (38, 125), (38, 130), (20, 175), (20, 180), (44, 188), (44, 193), (11, 197), (11, 202), (35, 205), (35, 210), (5, 259), (5, 264), (29, 305), (29, 310), (13, 325), (13, 330), (37, 342), (37, 347), (15, 395), (15, 400), (39, 404), (39, 409), (6, 417), (6, 422), (4, 431), (4, 436), (28, 438), (28, 443), (30, 450), (30, 455)], [(22, 147), (22, 152), (46, 161), (46, 166), (8, 182), (8, 187), (1, 197), (1, 202), (32, 225), (32, 230), (25, 258), (25, 263), (24, 321), (24, 326), (48, 335), (48, 340), (21, 416), (21, 421), (45, 430), (45, 435)], [(16, 386), (16, 391), (40, 399), (40, 404), (18, 409), (18, 414), (42, 424), (42, 429)], [], [], [], [], [], []]

    print(loot[0][0][0])
    total = total_distance(loot)

    print(total,np.sum(total))

    a = [3,4,5,6]
    b=[5,6,7]
    c=list(set(a) & set(b))
    print(c)