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

    loot = [[(9, 33), (9, 43), (33, 102), (33, 112), (20, 175), (20, 185), (8, 188), (8, 198), (44, 207), (44, 217), (32, 225), (32, 235), (1, 241), (1, 251), (25, 258), (25, 268), (24, 321), (24, 331), (48, 340), (48, 350), (15, 395), (15, 405), (39, 409), (39, 419), (4, 427), (4, 437), (28, 439), (28, 449), (19, 455), (19, 465), (23, 475), (23, 485), (47, 490), (47, 500), (43, 502), (43, 512)], [(17, 86), (17, 96), (41, 105), (41, 115), (11, 125), (11, 135), (22, 147), (22, 157), (46, 166), (46, 176), (35, 183), (35, 193), (7, 195), (7, 205), (31, 208), (31, 218), (3, 225), (3, 235), (27, 237), (27, 247), (2, 271), (2, 281), (26, 329), (26, 339), (6, 368), (6, 378), (18, 409), (18, 419), (42, 429), (42, 439), (30, 445), (30, 455)], [(14, 111), (14, 121), (38, 130), (38, 140), (10, 186), (10, 196), (34, 260), (34, 270), (5, 281), (5, 291), (29, 305), (29, 315), (12, 326), (12, 336), (36, 381), (36, 391), (21, 416), (21, 426), (45, 435), (45, 445)], [(13, 325), (13, 335), (37, 347), (37, 357), (16, 386), (16, 396), (40, 404), (40, 414)], [], [], [], [], [], []]

    print(loot[0][0][0])
    total = total_distance(loot)

    print(total,np.sum(total))