import util
from client import Client
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd


# 2×2のウィンドウで3種類のトピックを持つアニメーションの生成
def create_animation(index_file, out_file, FPS):
    # インデックスファイルの読み込み
    df_index = pd.read_csv(index_file, index_col=0)

    config_file = df_index.at['data', 'config_file']
    data_file = df_index.at['data', 'assign_file']
    edge_file = df_index.at['data', 'edge_file']

    # 設定ファイルからパラメーターの取り出し
    parameter = util.read_config(config_file)

    min_x = parameter['min_x']
    max_x = parameter['max_x']
    min_y = parameter['min_y']
    max_y = parameter['max_y']
    num_edge = parameter['num_edge']
    num_client = parameter['num_client']
    num_topic = parameter['num_topic']
    simulation_time = parameter['simulation_time']
    time_step = parameter['time_step']

    # トピック情報付きのトラッキングデータを読み込み
    data_set = util.read_data_set_topic(data_file, num_topic)

    # 描画領域の設定
    fig = plt.figure()
    wind1 = fig.add_subplot(2, 2, 1)
    wind2 = fig.add_subplot(2, 2, 2)
    wind3 = fig.add_subplot(2, 2, 3)
    wind4 = fig.add_subplot(2, 2, 4)
    wind1.grid()
    wind2.grid()
    wind3.grid()
    wind4.grid()
    wind1.set_xlim(min_x, max_x)
    wind1.set_ylim(min_y, max_y)
    wind2.set_xlim(min_x, max_x)
    wind2.set_ylim(min_y, max_y)
    wind3.set_xlim(min_x, max_x)
    wind3.set_ylim(min_y, max_y)
    wind4.set_xlim(min_x, max_x)
    wind4.set_ylim(min_y, max_y)
    wind1.set_xticks(np.arange(0, 13, 4))
    wind1.set_yticks(np.arange(0, 13, 4))
    wind2.set_xticks(np.arange(0, 13, 4))
    wind2.set_yticks(np.arange(0, 13, 4))
    wind3.set_xticks(np.arange(0, 13, 4))
    wind3.set_yticks(np.arange(0, 13, 4))
    wind4.set_xticks(np.arange(0, 13, 4))
    wind4.set_yticks(np.arange(0, 13, 4))

    # エッジサーバの読み込み
    all_edge = util.read_edge(edge_file)
    edge_x = np.zeros(num_edge)
    edge_y = np.zeros(num_edge)

    for edge in all_edge:
        edge_x[edge.id] = edge.x
        edge_y[edge.id] = edge.y

    imgs = []

    # アニメーションの作成準備
    for t in range(0, simulation_time, time_step):
        # 各タイムステップにおけるクライアントの座標を格納
        # クラアント全体の分布
        x_list = []
        y_list = []
        # 各トピックの分布
        pub_x_list = [[] for i in range(3)]
        pub_y_list = [[] for i in range(3)]
        sub_x_list = [[] for i in range(3)]
        sub_y_list = [[] for i in range(3)]
        pub_sub_x_list = [[] for i in range(3)]
        pub_sub_y_list = [[] for i in range(3)]

        for id in range(num_client):
            data = data_set.pop(0)
            x_list.append(data.x)
            y_list.append(data.y)

            # トピックの割り当て状況を元に各分布の座標変数に追加
            for i in range(3):
                if data.pub_topic[i] == True and data.sub_topic[i] == True:
                    pub_sub_x_list[i].append(data.x)
                    pub_sub_y_list[i].append(data.y)
                elif data.pub_topic[i] == True:
                    pub_x_list[i].append(data.x)
                    pub_y_list[i].append(data.y)
                elif data.sub_topic[i] == True:
                    sub_x_list[i].append(data.x)
                    sub_y_list[i].append(data.y)


        # 各タイムステップでの描画情報の作成
        my_title = wind1.text(11.5, 14, 'time : {}'.format(t))
        img1_client = wind1.scatter(x_list, y_list, c="blue")
        img1_edge = wind1.scatter(edge_x, edge_y, s=20, c="green", marker="s")
        img2_pub = wind2.scatter(pub_x_list[0], pub_y_list[0], c="red")
        img2_sub = wind2.scatter(sub_x_list[0], sub_y_list[0], c="blue")
        img2_pub_sub = wind2.scatter(pub_sub_x_list[0], pub_sub_y_list[0], c="purple")
        img2_edge = wind2.scatter(edge_x, edge_y, s=20, c="green", marker="s")
        img3_pub = wind3.scatter(pub_x_list[1], pub_y_list[1], c="red")
        img3_sub = wind3.scatter(sub_x_list[1], sub_y_list[1], c="blue")
        img3_pub_sub = wind3.scatter(pub_sub_x_list[1], pub_sub_y_list[1], c="purple")
        img3_edge = wind3.scatter(edge_x, edge_y, s=20, c="green", marker="s")
        img4_pub = wind4.scatter(pub_x_list[2], pub_y_list[2], c="red")
        img4_sub = wind4.scatter(sub_x_list[2], sub_y_list[2], c="blue")
        img4_pub_sub = wind4.scatter(pub_sub_x_list[2], pub_sub_y_list[2], c="purple")
        img4_edge = wind4.scatter(edge_x, edge_y, s=20, c="green", marker="s")
        img_list = [my_title, img1_client, img1_edge, img2_pub, img2_sub, img2_pub_sub, img2_edge, img3_pub, img3_sub, img3_pub_sub, img3_edge, img4_pub, img4_sub, img4_pub_sub, img4_edge]

        # 描画情報を追加
        imgs.append(img_list)
    
    # アニメーションの作成
    ani = animation.ArtistAnimation(fig, imgs, interval=1)

    # アニメーションの出力
    # fps は1~50までしかとれない
    ani.save(out_file, writer=animation.PillowWriter(fps=FPS))


# 割り当て付きの分布の可視化
# 要改修
def create_animation_single_topic(index_file, out_file, FPS):
    df_index = pd.read_csv(index_file, index_col=0)

    config_file = df_index.at['data', 'config_file']
    data_file = df_index.at['data', 'solve_file']
    edge_file = df_index.at['data', 'edge_file']

    parameter = util.read_config(config_file)

    min_x = parameter['min_x']
    max_x = parameter['max_x']
    min_y = parameter['min_y']
    max_y = parameter['max_y']
    num_edge = parameter['num_edge']
    num_client = parameter['num_client']
    num_topic = parameter['num_topic']
    simulation_time = parameter['simulation_time']
    time_step = parameter['time_step']

    data_set = util.read_data_set_solution(data_file, config_file)

    # 描画領域の設定
    fig = plt.figure()
    wind1 = fig.add_subplot(1, 2, 1)
    wind2 = fig.add_subplot(1, 2, 2)
    wind1.grid()
    wind2.grid()
    wind1.set_xlim(min_x, max_x)
    wind1.set_ylim(min_y, max_y)
    wind2.set_xlim(0, simulation_time)
    wind2.set_ylim(0.8, 1.5)
    wind1.set_xticks(np.arange(0, 13, 4))
    wind1.set_yticks(np.arange(0, 13, 4))

    # エッジサーバの作成
    all_edge = util.read_edge(edge_file)
    edge_x = np.zeros(num_edge)
    edge_y = np.zeros(num_edge)

    for edge in all_edge:
        edge_x[edge.id] = edge.x
        edge_y[edge.id] = edge.y

    imgs = []
    delay_history = []

    for t in range(0, simulation_time, time_step):
        # 各タイムステップにおけるクライアントの座標を格納
        x1_list = []
        y1_list = []
        line_list = []
        pub_list = []
        sub_list = []

        for id in range(num_client):
            data = data_set.pop(0)

            # 実際に使う時には要修正
            for i in range(num_topic):
                edge_id = data.pub_edge[i]
                if edge_id != -1:
                    x1_list.append(data.x)
                    y1_list.append(data.y)
                    
                    client = Client(data.id, data.x, data.y, edge_id, edge_id)
                    pub_list.append(client)
                    sub_list.append(client)

                    line_list.append([(data.x, data.y), (all_edge[edge_id].x, all_edge[edge_id].y)])

        delay = 0
        tmp = 0
        for i in range(num_topic):
            for c1 in pub_list:
                for c2 in sub_list:
                    delay += util.cal_delay(c1, c2, all_edge)
                    tmp += 1
  
        delay_history.append(delay/tmp)

        time = [i for i in range(0, t+1, time_step)]

        my_title = wind1.text(11.5, 13, 'time : {}'.format(t))
        img1_client = wind1.scatter(x1_list, y1_list, c="blue")
        img1_edge = wind1.scatter(edge_x, edge_y, s=20, c="green", marker="s")

        img_list = [my_title, img1_client, img1_edge]

        img2 = wind2.plot(time, delay_history, marker="o", color="k")

        img_list.extend(img2)


        for line in line_list:
            img_list.extend(wind1.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color="k"))

        imgs.append(img_list)

    ani = animation.ArtistAnimation(fig, imgs, interval=1)

    # fps は1~50までしかとれない
    ani.save(out_file, writer=animation.PillowWriter(fps=FPS))


# トラッキング情報のアニメーション化
def create_traking_animation(index_file, out_file, FPS=20):
    # インデックスファイルの読み込み
    df_index = pd.read_csv(index_file, index_col=0)

    config_file = df_index.at['data', 'config_file']
    data_file = df_index.at['data', 'traking_file']
    edge_file = df_index.at['data', 'edge_file']

    # 設定ファイルからパラメーター情報の取り出し
    parameter = util.read_config(config_file)

    min_x = parameter['min_x']
    max_x = parameter['max_x']
    min_y = parameter['min_y']
    max_y = parameter['max_y']
    num_edge = parameter['num_edge']
    num_client = parameter['num_client']
    simulation_time = parameter['simulation_time']
    time_step = parameter['time_step']

    # トラッキングデータの読み込み
    data_set = util.read_data_set_traking(data_file)

    # 描画領域の設定
    fig = plt.figure()
    wind1 = fig.add_subplot(1, 1, 1)
    wind1.grid()
    wind1.set_xlim(min_x, max_x)
    wind1.set_ylim(min_y, max_y)
    wind1.set_xticks(np.arange(min_x, max_x+1, (max_x-min_x)/3))
    wind1.set_yticks(np.arange(min_y, max_y+1, (max_y-min_y)/3))

    # エッジサーバの作成
    all_edge = util.read_edge(edge_file)
    edge_x = np.zeros(num_edge)
    edge_y = np.zeros(num_edge)

    for edge in all_edge:
        edge_x[edge.id] = edge.x
        edge_y[edge.id] = edge.y

    imgs = []

    # アニメーションの準備
    for t in range(0, simulation_time, time_step):
        # 各タイムステップにおけるクライアントの座標を格納
        x1_list = []
        y1_list = []

        for id in range(num_client):
            data = data_set.pop(0)

            x1_list.append(data.x)
            y1_list.append(data.y)

        # 各タイムステップにおける描画情報の作成
        my_title = wind1.text((max_x-min_x)/2 - 0.8, 13, 'time : {}'.format(t))
        img1_client = wind1.scatter(x1_list, y1_list, c="blue")
        img1_edge = wind1.scatter(edge_x, edge_y, s=20, c="green", marker="s")

        img_list = [my_title, img1_client, img1_edge]

        imgs.append(img_list)

    # アニメーションの作成
    ani = animation.ArtistAnimation(fig, imgs, interval=1)

    # アニメーションの出力
    # fps は1~50までしかとれない
    ani.save(out_file, writer=animation.PillowWriter(fps=FPS))
