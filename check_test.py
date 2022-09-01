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
    with open('/home/kurozumi/デスクトップ/benchmark2/' + FILENAME, 'r', encoding='utf-8') as fin:
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
            kyori =Distance[loot[i][0][0]][0] + Distance[loot[i][-1][0]][0]
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

    loot =[[(9, 33), (9, 38), (33, 102), (33, 107), (24, 321), (24, 326), (5, 316), (5, 321), (2, 313), (2, 318), (26, 329), (26, 334), (12, 327), (12, 332), (48, 341), (48, 346), (6, 368), (6, 373), (30, 432), (30, 437), (21, 434), (21, 439), (4, 428), (4, 433), (28, 435), (28, 440), (45, 447), (45, 452), (19, 461), (19, 466), (43, 479), (43, 484), (23, 478), (23, 483), (47, 488), (47, 493)], [(10, 186), (10, 191), (8, 180), (8, 185), (1, 197), (1, 202), (7, 208), (7, 213), (3, 208), (3, 213), (27, 215), (27, 220), (31, 228), (31, 233), (32, 234), (32, 239), (34, 260), (34, 265), (25, 273), (25, 278), (15, 395), (15, 400), (18, 409), (18, 414), (42, 424), (42, 429), (39, 425), (39, 430)], [(14, 111), (14, 116), (17, 108), (17, 113), (41, 122), (41, 127), (11, 132), (11, 137), (35, 178), (35, 183), (38, 190), (38, 195), (20, 184), (20, 189), (44, 197), (44, 202), (13, 325), (13, 330), (37, 342), (37, 347), (16, 386), (16, 391), (40, 399), (40, 404)], [(22, 147), (22, 152), (46, 161), (46, 166)], [], [], [], [], [], []]

    print(loot[0][0][0])
    total = total_distance(loot)

    print(total,np.sum(total))