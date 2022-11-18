import numpy as np
import pandas as pd
import networkx as nx
import math
from itertools import product
import matplotlib.pyplot as plt
import random
import time
import copy


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



def network_creat(Time_expand, kakucho):
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

"""
#現在地アップデートして大丈夫かどうか判定
"""


def check_node(next_location_id):
    '''
    移動先候補のノードが接続されているかどうかをチェックする関数
    :param next_location_id: tuple
        次の移動先候補のノード
    :return: 0-1変数
    '''
    flag = 1
    next_location_id = genzaichi_update(next_location_id)
    try:
        next_location_dic = G.adj[next_location_id]
    except KeyError as e:
        flag = 0

    return flag


def genzaichi_update(tup):
    '''
    現在地にサービス時間をプラスする関数
    :param tup: tuple
        現在地のノード
    :return: tuple
        次のノード
    '''
    tup_new = list(tup)
    tup_new[1] = tup_new[1] + d
    return tuple(tup_new)


def syaryo_time_check(Loot):
    '''
    車両の稼働時間を計算する関数
    :param Loot:list
        一台のルート
    :return: float
        車両の稼働時間
    '''
    syaryo_time = 0
    if not Loot == []:
        syaryo_time = Loot[-1][1] + Distance[0][Loot[-1][0]] - (Loot[0][1] - Distance[0][Loot[0][0]])
    return syaryo_time


def update_pick_node(next_node,pick_list):
    '''
    降ろさなければならないノードを管理しておく関数
    :param next_node: tuple
        現在のノード
    :param pick_list:list
         降ろさなければならないノードのリスト
    :return: list
        更新後の降ろさなければならないノードのリスト
    '''
    if noriori[next_node[0]] ==1:
        pick_list.append(next_node[0]+Request)
    else:
        pick_list.remove(next_node[0])

    return pick_list

"""
関数network_updateについて
現在地のノードを削除したらいけません→この関数は使えないかも
一台分のルートが完成してから削除しましょう
"""


def network_update(network, removenode):
    '''
    10/12 使っていない関数
    時空間ネットワークから指定のノードを削除するノード
    :param network: network.X
        時空間ネットワーク
    :param removenode: list
        消すべきノードリスト
    :return:
    '''
    for i in list(network.nodes()):
        for j in removenode:
            if i[0] == j:
                network.remove_node(i)




def return_kakuritsu(dic, now_location,capacity,picking_list):
    '''
    次のノードを確立で選択し、返す関数
    :param dic: G.adj[genzaichi]
        現在地から移動できるノードの一覧
    :param now_location: tuple
        現在地
    :param capacity: int
        キャパ
    :param picking_list:list
        降ろさなければならないノード
    :return: tuple
        次のノード
    '''
    idou_kanou = []
    idou_kanou_time=[]
    idou_kakuritsu = []
    next_limit = Setting_Info_base[9]
    capa_max =Setting_Info_base[4]
    saitan_drop_node = (n,T+1)
    random_return = (0, 0)
    if capacity < capa_max:
        if noriori[now_location[0]] ==0:
            for id, info in dic.items():
                if not id[0] == n and check_node(id) ==1 and id[0] not in kanryo_node:
                    if noriori[id[0]] ==1:
                        if id[0] in idou_kanou:
                            break
                        idou_kanou.append(id[0])
                        idou_kanou_time.append(id[1])
                        idou_kakuritsu.append(list(info.values())[2])
            if not idou_kanou==[]:
                random_return = saisyo(idou_kanou[idou_kanou_time.index(min(idou_kanou_time))],min(idou_kanou_time))

        elif noriori[now_location[0]] ==1:
            for id,info in dic.items():
                if id[1] < now_location[1] + next_limit and not id[0] == n and id[0] not in kanryo_node and check_node(id):
                    if id[0] in idou_kanou:
                        break
                    if noriori[id[0]] == 1:
                        idou_kanou.append(id[0])
                        idou_kanou_time.append(id[1])
                        idou_kakuritsu.append(list(info.values())[2])
                    else:
                        if id[0] in picking_list:
                            idou_kanou.append(id[0])
                            idou_kanou_time.append(id[1])
                            idou_kakuritsu.append(list(info.values())[2])

            random_return = probability_choice(now_location, idou_kanou, idou_kakuritsu, idou_kanou_time,picking_list)
        elif noriori[now_location[0]] == -1:
            for id,info in dic.items():
                if not picking_list ==[]:
                    if id[1] < now_location[1] + next_limit and not id[0] == n and id[0] not in kanryo_node and check_node(id):
                        if id[0] in idou_kanou:
                            break
                        if noriori[id[0]] == 1:
                            idou_kanou.append(id[0])
                            idou_kanou_time.append(id[1])
                            idou_kakuritsu.append(list(info.values())[2])
                        else:
                            if id[0] in picking_list:
                                idou_kanou.append(id[0])
                                idou_kanou_time.append(id[1])
                                idou_kakuritsu.append(list(info.values())[2])
                else:
                    if id[1] < now_location[1] + next_limit and id[0] not in kanryo_node and check_node(id):
                        if id[0] in idou_kanou:
                            break
                        if noriori[id[0]] == 1:
                            idou_kanou.append(id[0])
                            idou_kanou_time.append(id[1])
                            idou_kakuritsu.append(list(info.values())[2])
                        else:
                            if id[0] in picking_list:
                                idou_kanou.append(id[0])
                                idou_kanou_time.append(id[1])
                                idou_kakuritsu.append(list(info.values())[2])
            if picking_list ==[] and idou_kanou ==[]:
                for id, info in dic.items():
                    if not id[0] == n and id[0] not in kanryo_node and check_node(id):
                        if id[0] in idou_kanou:
                            break
                        if noriori[id[0]] == 1:
                            idou_kanou.append(id[0])
                            idou_kanou_time.append(id[1])
                            idou_kakuritsu.append(list(info.values())[2])
                        else:
                            if id[0] in picking_list:
                                idou_kanou.append(id[0])
                                idou_kanou_time.append(id[1])
                                idou_kakuritsu.append(list(info.values())[2])

            random_return = probability_choice(now_location, idou_kanou, idou_kakuritsu, idou_kanou_time,picking_list)
    else:
        pass

    if random_return ==(0,0):
        random_return =(n, T + 1)
    return random_return


def saisyo(saisyo_kyaku,saisyo_time):
    '''
    移動可能な最小ノードをタプル型で返す関数
    :param saisyo_kyaku:int
        移動先のノード番号
    :param saisyo_time:int
        移動先のノード時間
    :return:tuple
        ノード
    '''
    re_saisyo = [saisyo_kyaku,saisyo_time]
    re_saisyo =tuple(re_saisyo)
    return re_saisyo


def total_distance(loot):
    '''
    総車両の移動距離を返す関数
    :param loot: list
        タクシーすべてのルート
    :return:float
        距離
    '''
    Total = np.zeros(len(loot))

    for i in range(len(loot)):
        if not loot[i] ==[]:
            kyori =Distance[loot[i][0][0]][0] + Distance[loot[i][-1][0]][n-1]
            Total[i] += kyori
            for j in range(len(loot[i])-1):
                kyori = Distance[loot[i][j][0]][loot[i][j+1][0]]
                Total[i] += kyori
    return Total



def probability_choice(now_location,idou_list,idou_probability,idou_kanou_time,picking_list):
    '''
    return_kakuritsu関数  →   probability_choice関数  →   cal_kakuritsu関数
    橋渡し的な関数
    :param now_location:tuple
        現在地
    :param idou_list:list
        移動候補ノードリスト
    :param idou_probability:list
        移動候補ノードの移動しやすさリスト、中身は1/(移動先の時間ー現在の時間)
    :param idou_kanou_time:list
        移動候補ノードの時間リスト
    :param picking_list:list
        降ろさなければならないリスト
    :return:tuple
        次のノード
    '''
    if not idou_list == []:
        re_random =[]
        kakuritsu_list = cal_kakuritsu(now_location,idou_list,idou_probability)

        random=np.random.choice(idou_list,p=kakuritsu_list)
        index = idou_list.index(random)
        re_random.append(random)
        re_random.append(idou_kanou_time[index])
        re_random =tuple(re_random)
    else:
        re_random =(n,T+1)
    return re_random

def cal_kakuritsu(now_location, idou_list, idou_probability):
    '''
    確率を計算する関数
    :param now_location:tuplw
        現在地
    :param idou_list: list
        移動候補リスト
    :param idou_probability:list
        移動候補ノードの移動しやすさリスト、中身は1/(移動先の時間ー現在の時間)
    :return: list
        確率リスト
    '''
    kakuritsu_list =[]
    sum=0
    sum_sum =0
    for i in range(len(idou_probability)):
        if noriori[idou_list[i]]==-1:
            #p = (pheromon[i]**alpha)*((Q/Distance[idou_list[i]][now_location[0]]+1/(l[idou_list[i]]-e[idou_list[i]]))**beta)#時間窓がヒューリスティック値
            #p = round(idou_probability[i] ** alpha,5) * round(((Q / Distance[idou_list[i]][now_location[0]]) ** beta,5) * round((1 / (l[idou_list[i]] - now_location[0])) ** ganma,5) * round((pheromon[now_location[0]][idou_list[i]]) ** delta,5) #現在の時刻からの∆がヒューリスティック値
            #p = ((Q / Distance[idou_list[i]][now_location[0]]) ** beta) * (1 / (l[idou_list[i]] - now_location[0])) ** ganma
            Probability = round(idou_probability[i] ** alpha,5)
            kyori= round((Q / Distance[idou_list[i]][now_location[0]]) ** beta,5)
            simekiri = round((1 / (l[idou_list[i]] - now_location[1])) ** ganma,5)
            phe=round((pheromon[now_location[0]][idou_list[i]]) ** delta, 5)
            p=Probability*kyori*simekiri*phe
            kakuritsu_list.append(p)
            sum +=p
        else:
            #p = ((idou_probability[i]*100) ** alpha) * (Q / Distance[idou_list[i]][now_location[0]]) ** beta * ((1 / (l[idou_list[i]] - now_location[0]))*100 ** theta) * (pheromon[now_location[0]][idou_list[i]]*100)**delta
            #p = (Q / Distance[idou_list[i]][now_location[0]]) ** beta * (1 / (l[idou_list[i]] - now_location[0])) ** theta
            Probability = round(idou_probability[i] ** alpha, 5)
            kyori = round((Q / Distance[idou_list[i]][now_location[0]]) ** beta, 5)
            simekiri = round((1 / (l[idou_list[i]] - now_location[1])) ** theta, 5)
            phe = round((pheromon[now_location[0]][idou_list[i]]) ** delta, 5)
            p = Probability * kyori * simekiri * phe
            kakuritsu_list.append(p)
            sum += p
    for i in range(len(kakuritsu_list)):
        if i ==0:
            kakuritsu_list[i] = kakuritsu_list[i]/sum
            sum_sum += kakuritsu_list[i]
        elif i == range(len(kakuritsu_list)):
            kakuritsu_list[i] = 1-sum_sum
        else:
            kakuritsu_list[i] = kakuritsu_list[i]/sum
            sum_sum += kakuritsu_list[i]


    return kakuritsu_list





def route_k_cost_sum(route_k):
    '''
    一台のルートの距離コストを計算
    :param route_k:list
        タクシー1台のルート
    :return:float
        タクシー1台の距離コスト
    '''
    route_k_sum = 0
    for i in range(len(route_k) - 1):
        route_k_sum = route_k_sum + Distance[route_k[i]][route_k[i + 1]]
    route_k_sum = route_k_sum + Distance[0][route_k[0]]
    route_k_sum = route_k_sum + Distance[0][route_k[i + 1]]

    return route_k_sum

def capacity_route_k(route_k):
    '''
    タクシー1台のキャパシティオーバーを計算
    :param route_k: list
        タクシー1台のルート
    :return: int
        タクシー1台のキャパオーバー数
    '''
    capacity_over = 0
    q = 0
    for i in range(len(route_k)):
        q = q + noriori[route_k[i]]
        if q > Setting_Info_base[4]:
            capacity_over += 1
    return capacity_over

def time_caluculation(Route_k):
    '''
    タクシー１台の各タイム計算
    :param Route_k:list
        タクシー1台のルート
    :return: list
        タクシー1台のルートに関しての各タイム計算
    '''
    B = np.zeros(n + 2, dtype=float, order='C')  # サービス開始時間（e.g., 乗せる時間、降ろす時間)
    A = np.zeros(n + 2, dtype=float, order='C')  # ノード到着時間
    D = np.zeros(n + 2, dtype=float, order='C')  # ノード出発時間
    W = np.zeros(n + 2, dtype=float, order='C')  # 車両待ち時間
    L = np.zeros(Request, dtype=float, order='C')  # リクエストiの乗車時間
    if not len(Route_k) == 0:
        for i in range(len(Route_k)):
            if i == 0:
                A[Route_k[i]] = D[i] + Distance[i][Route_k[i]]
                B[Route_k[i]] = max(e[Route_k[i]], A[Route_k[i]])
                D[Route_k[i]] = B[Route_k[i]] + d
                W[Route_k[i]] = B[Route_k[i]] - A[Route_k[i]]
            else:
                A[Route_k[i]] = D[Route_k[i - 1]] + Distance[Route_k[i - 1]][Route_k[i]]
                B[Route_k[i]] = max(e[Route_k[i]], A[Route_k[i]])
                D[Route_k[i]] = B[Route_k[i]] + d
                W[Route_k[i]] = B[Route_k[i]] - A[Route_k[i]]
        A[-1] = D[Route_k[-1]] + Distance[0][Route_k[-1]]
        B[-1] = A[-1]
        for i in range(len(Route_k)):
            if Route_k[i] <= Request:
                L[Route_k[i] - 1] = B[Route_k[i] + Request] - D[Route_k[i]]
    return A, B, D, W, L

def time_window_penalty(route_k, b):  # 論文でのw(s)
    '''
    時間窓制約違反の合計を返す関数
    :param route_k:list
        タクシー1台のルート
    :param b:list
        サービス開始時間
    :return: flaot
        時間窓制約違反の合計
    '''
    sum = 0
    for i in range(len(route_k)):
        a = b[route_k[i]] - l[route_k[i]]
        if a > 0:
            sum = sum + a
    a = b[-1] - l[0]
    if a > 0:
        sum = sum + a
    return sum


def ride_time_penalty(L):  # 論文でのt_s
    '''
    顧客一人の乗車時間違反を返す関数
    :param L:list
        乗客の乗車時間リスト
    :return: flaot
        顧客一人の乗車時間違反の合計
    '''
    sum = 0
    for i in range(len(L)):
        a = L[i] - Setting_Info_base[9]
        if a > 0:
            sum = sum + a
    return sum

def penalty_sum_route_k(route_k):
    '''
    タクシー１台のルートの各ペナルティコスト計算関数
    :param route_k: list
        タクシー1台のルート
    :return: list
        各ペナルティーをリストにしたもの
    '''
    c_s = route_k_cost_sum(route_k)
    q_s = capacity_route_k(route_k)
    d_s = 0
    w_s = 0
    t_s = 0
    if not len(route_k) == 0:
        ROUTE_TIME_info = time_caluculation(route_k)
        d_s_s = (ROUTE_TIME_info[1][-1] - ROUTE_TIME_info[1][route_k[1]] + Distance[0][route_k[1]]) - Setting_Info_base[8]
        if d_s_s < 0:
            d_s_s = 0
        d_s = d_s + d_s_s
        w_s = time_window_penalty(route_k, ROUTE_TIME_info[1])
        t_s = ride_time_penalty(ROUTE_TIME_info[4])
    #penalty = c_s + keisu[0] * q_s + keisu[1] * d_s + keisu[2] * w_s + keisu[3] * t_s
    penalty =[c_s,q_s,d_s,w_s,t_s]
    return penalty

def insert_route_ver2(route, riyoukyakunumber, new_vehiclenumber):
    '''
    ルートに挿入する関数
    :param route:list
        すべてのルート
    :param riyoukyakunumber:int
        挿入する顧客の番号
    :param new_vehiclenumber:int
        挿入先の車両番号
    :return:list
        挿入した１台のルート
    '''
    new_route_k = copy.deepcopy(route[new_vehiclenumber])
    route_k_node = len(route[new_vehiclenumber])
    riyoukyakunumber = int(riyoukyakunumber)
    new_route_k.insert(0, riyoukyakunumber)
    new_route_k.insert(1, riyoukyakunumber + Request)
    penalty = sum(penalty_sum_route_k(new_route_k))
    check_route = copy.deepcopy(route[new_vehiclenumber])
    for i in range(route_k_node):
        j = i + 1
        while j <= route_k_node:
            check_route = copy.deepcopy(route[new_vehiclenumber])
            check_route.insert(i, riyoukyakunumber)
            check_route.insert(j, riyoukyakunumber + Request)
            check_penalty = sum(penalty_sum_route_k(check_route))
            if check_penalty < penalty:
                penalty = check_penalty
                new_route_k = copy.deepcopy(check_route)
            j = j + 1
        if j == route_k_node + 1:
            check_route = copy.deepcopy(route[new_vehiclenumber])
            check_route.insert(i, riyoukyakunumber)
            check_route.append(riyoukyakunumber + Request)
            check_penalty = sum(penalty_sum_route_k(check_route))
            if check_penalty < penalty:
                penalty = check_penalty
                new_route_k = copy.deepcopy(check_route)
    check_route = copy.deepcopy(route[new_vehiclenumber])
    check_route.append(riyoukyakunumber)
    check_route.append(riyoukyakunumber + Request)
    check_penalty = sum(penalty_sum_route_k(check_route))
    if check_penalty < penalty:
        penalty = check_penalty
        new_route_k = copy.deepcopy(check_route)

    return new_route_k

def min_route(route,riyoukokyaku_number,penalty_sum_list):
    '''
    挿入して総コストが最小となるルートをつくる関数
    :param route: list
        すべてのルート
    :param riyoukokyaku_number: int
        挿入する顧客番号
    :param penalty_sum_list:list
        各ルートのペナルティをまとめたlist
    :return: list
        新たなルート
    '''
    check_route=copy.deepcopy(route)
    penalty=sum(penalty_sum_list)
    new_route=copy.deepcopy(route)
    count=0
    for i in range(len(route)):
        check_route=copy.deepcopy(route)
        new_penalty_sum_list = copy.deepcopy(penalty_sum_list)
        check_route[i] = insert_route_ver2(route,riyoukokyaku_number,i)
        new_penalty_sum_list[i] =sum(penalty_sum_route_k(check_route[i]))
        if count==0:
            penalty = sum(new_penalty_sum_list)
            new_route = copy.deepcopy(check_route)
            count+=1
        elif sum(new_penalty_sum_list) < penalty:
             penalty=sum(new_penalty_sum_list)
             new_route = copy.deepcopy(check_route)
    return new_route

def insert_remaining_node(route,drop_remaining_node,remaining_node,loot_without_time):#remaining_node:取り残されたノードのこと、drop_remaining_node:降ろすポイントだけ挿入できなかったノード
    '''
    残ったノードを挿入する関数
    :param route: list
        総ルート
    :param drop_remaining_node:list
        残っている降ろすノード
    :param remaining_node: list
        残っているpick_upノード
    :param loot_without_time: list
        総ルート(時間情報がない)
    :return:
        loot_without_time,penalty_list,penalty_sum_list
    '''
    diff_remaining_node = sorted(list(set(remaining_node)^set(sum(drop_remaining_node,[]))))
    print(diff_remaining_node)
    penalty_sum_list =[]
    penalty_list=[]
    for i in range(len(drop_remaining_node)):
        if not drop_remaining_node[i] ==[]:
            for j in drop_remaining_node[i]:
                sort_index = loot_out_time[i].index(j-Request) +1
                loot_out_time[i].insert(sort_index,j)
        penalty_list.append(penalty_sum_route_k(loot_out_time[i]))
        penalty_sum_list.append(sum(penalty_list[i]))
    print(loot_out_time)
    print(penalty_list,penalty_sum_list)
    for i in remaining_node:
        if i <=Request:
            loot_without_time = min_route(route=loot_without_time,riyoukokyaku_number=i,penalty_sum_list=penalty_sum_list)
    for j in range(len(loot_without_time)):
        penalty_list[j] = penalty_sum_route_k(loot_without_time[j])
        penalty_sum_list[j] = sum(penalty_list[j])
    print(loot_without_time)
    print(penalty_list)
    print(penalty_sum_list)
    return loot_without_time,penalty_list,penalty_sum_list

def pheromon_upgrade(route,pheromon,penalty_sum_list):
    pheromon=pheromon*rou
    for i in range(len(route)):
        for j in range(len(route[i])-1):
            pheromon[route[i][j]][route[i][j+1]] +=1/penalty_sum_list[i]

    print(1)
    return pheromon

def penalty_check(penalty_list):
    flag=0
    sum=0
    for i in range(len(penalty_list)):
        sum += penalty_list[i][1]+penalty_list[i][2]+penalty_list[i][3]+penalty_list[i][4]
    if not sum == 0:
        flag=1
    return flag

if __name__ == '__main__':
    FILENAME = 'darp01EX.txt'
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
    kokyaku_node = range(1, n)

    time_expand = 1

    FILENAME = FILENAME.replace('.txt', '')
    G = nx.read_gpickle('time_network' + FILENAME)

    G_copy = copy.deepcopy(G)
#----------------------パラメータ-------------------------------------
    alpha =1    #1/(移動先の時刻𝑡)ー（現在の時刻𝑡）移動先の時間を優先
    beta=0.7  #ノード間の距離を優先
    theta = 1   #1/(ノード𝑗の最遅時間窓)ー(現在の時刻𝑡）移動先(pick-up)の締め切り時間を優先
    ganma =0.7  #1/(ノード𝑗の最遅時間窓)ー(現在の時刻𝑡）移動先(drop)の締め切り時間を優先
    delta =1    #フェロモンを優先
    keisu=np.ones(4)
    Q =1
    pheromon = np.ones((n,n))
    rou=0.9
#-----------------------------------------------------------------
    print(FILENAME)
    print(time_expand)
    print(nx.number_of_edges(G))
    print(nx.number_of_nodes(G))
    roop =0
    opt = 10000
    kinbo=10000
    opt_loot =[]
    opt_info =[]

    LOOP=1
    data =np.zeros((LOOP,2))


    loop_nukedashi = np.zeros(Syaryo)


    while True:
        G = copy.deepcopy(G_copy)
        main_loop = 0
        misounyu = []
        misounyu_2 = []
        loot = [[] * 1 for i in range(Syaryo)]
        loot_out_time =[[] * 1 for i in range(Syaryo)]
        genzaichi_list =[(0,0) * 1 for i in range(Syaryo)]
        old_genzaichi_list =[(0,0) * 1 for i in range(Syaryo)]
        capa_list =[0 * 1 for i in range(Syaryo)]
        syaryo_number =0
        kanryo_node = []
        pick_now_node_list =[[] * 1 for i in range(Syaryo)]
        while True:
            if syaryo_number >= Syaryo:
                syaryo_number = 0
            while True:
                if syaryo_number >= Syaryo:
                    syaryo_number = 0
                setuzoku_Node = return_kakuritsu(G.adj[genzaichi_list[syaryo_number]], genzaichi_list[syaryo_number],capa_list[syaryo_number],pick_now_node_list[syaryo_number])
                if not setuzoku_Node[0] ==n:
                    pick_now_node_list[syaryo_number] = update_pick_node(setuzoku_Node,pick_now_node_list[syaryo_number])
                    if noriori[setuzoku_Node[0]] ==1:
                        capa_list[syaryo_number] +=1
                    else:
                        capa_list[syaryo_number]-=1
                if pick_now_node_list[syaryo_number] == [] and syaryo_time_check(loot[syaryo_number]) >=Syaryo_max_time:
                    loop_nukedashi[syaryo_number] =1
                    break
                if setuzoku_Node == (n, T + 1):
                    loop_nukedashi[syaryo_number] =1
                    break

                kanryo_node.append(setuzoku_Node[0])

                old_genzaichi_list[syaryo_number] = genzaichi_list[syaryo_number]
                genzaichi_list[syaryo_number] = setuzoku_Node

                loot[syaryo_number].append(genzaichi_list[syaryo_number])
                loot_out_time[syaryo_number].append(genzaichi_list[syaryo_number][0])
                genzaichi_list[syaryo_number] = genzaichi_update(genzaichi_list[syaryo_number])
                loot[syaryo_number].append(genzaichi_list[syaryo_number])

                syaryo_number += 1

            if loop_nukedashi.sum() ==Syaryo:
                break
            syaryo_number +=1



        misounyu_2.append(kanryo_node)

        insert_ROUTE = insert_remaining_node(loot, pick_now_node_list, list(set(kokyaku_node) ^ set(sum(misounyu_2, []))),loot_out_time)
        route_without_time = insert_ROUTE[0]
        penalty_list=insert_ROUTE[1]
        penalty_sum_list=insert_ROUTE[2]

        if sum(penalty_sum_list) < kinbo:
            kinbo=sum(penalty_sum_list)
            kinbo_loot=route_without_time
            kinbo_info =penalty_list
            data[roop][0] = kinbo
        if sum(penalty_sum_list) < opt and penalty_check(penalty_list)==0:
            opt = sum(penalty_sum_list)
            opt_loot= route_without_time
            opt_info = penalty_list
            data[roop][1] = opt
        pheromon = pheromon_upgrade(route_without_time,pheromon,penalty_sum_list)
        roop +=1
        if roop ==LOOP:
            break
    print(pheromon)
    print(opt)
    print(opt_loot)
    print(opt_info)
    np.savetxt('/Users/kurozumi ryouho/Desktop/benchmark2/kekka/' + FILENAME + 'ans.csv', data, delimiter=",")