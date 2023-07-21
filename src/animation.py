import util
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd


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
        edge_x[int(edge.id)] = edge.x
        edge_y[int(edge.id)] = edge.y

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
        img1_client = wind1.scatter(x1_list, y1_list, c="black")
        img1_edge = wind1.scatter(edge_x, edge_y, s=20, c="green", marker="s")

        img_list = [my_title, img1_client, img1_edge]

        imgs.append(img_list)

    # アニメーションの作成
    ani = animation.ArtistAnimation(fig, imgs, interval=1)

    # アニメーションの出力
    # fps は1~50までしかとれない
    ani.save(out_file, writer=animation.PillowWriter(fps=FPS))


# 2×2のウィンドウで3種類のトピックを持つアニメーションの生成
def create_topic_animation(index_file, out_file, FPS):
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
        edge_x[int(edge.id)] = edge.x
        edge_y[int(edge.id)] = edge.y

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
        img1_client = wind1.scatter(x_list, y_list, c="black")
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


# pub/sub関係を含む情報のアニメーション化(シングルトピック)
def create_single_topic_animation(index_file, out_file, FPS=20):
    # インデックスファイルの読み込み
    df_index = pd.read_csv(index_file, index_col=0)

    config_file = df_index.at['data', 'config_file']
    data_file = df_index.at['data', 'assign_file']
    edge_file = df_index.at['data', 'edge_file']

    # 設定ファイルからパラメーター情報の取り出し
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

    # トラッキングデータの読み込み
    data_set = util.read_data_set_topic(data_file, num_topic)

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
        edge_x[int(edge.id)] = edge.x
        edge_y[int(edge.id)] = edge.y

    imgs = []

    # アニメーションの準備
    for t in range(0, simulation_time, time_step):
        # publisher/subsciber の分布
        pub_x_list = [[] for i in range(1)]
        pub_y_list = [[] for i in range(1)]
        sub_x_list = [[] for i in range(1)]
        sub_y_list = [[] for i in range(1)]
        pub_sub_x_list = [[] for i in range(1)]
        pub_sub_y_list = [[] for i in range(1)]

        for id in range(num_client):
            data = data_set.pop(0)

            if data.pub_topic[0] == True and data.sub_topic[0] == True:
                pub_sub_x_list[0].append(data.x)
                pub_sub_y_list[0].append(data.y)
            elif data.pub_topic[0] == True:
                pub_x_list[0].append(data.x)
                pub_y_list[0].append(data.y)
            elif data.sub_topic[0] == True:
                sub_x_list[0].append(data.x)
                sub_y_list[0].append(data.y)

        # 各タイムステップにおける描画情報の作成
        my_title = wind1.text((max_x-min_x)/2 - 0.8, 13, 'time : {}'.format(t))
        img1_pub = wind1.scatter(pub_x_list[0], pub_y_list[0], c="red")
        img1_sub = wind1.scatter(sub_x_list[0], sub_y_list[0], c="blue")
        img1_pub_sub = wind1.scatter(pub_sub_x_list[0], pub_sub_y_list[0], c="purple")
        img1_edge = wind1.scatter(edge_x, edge_y, s=20, c="green", marker="s")

        img_list = [my_title, img1_pub, img1_sub, img1_pub_sub, img1_edge]

        imgs.append(img_list)

    # アニメーションの作成
    ani = animation.ArtistAnimation(fig, imgs, interval=1)

    # アニメーションの出力
    # fps は1~50までしかとれない
    ani.save(out_file, writer=animation.PillowWriter(fps=FPS))


# 割り当て付きの分布の可視化
def create_single_assign_animation(index_file, out_file, FPS):
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
    wind1 = fig.add_subplot(1, 1, 1)
    wind1.grid()
    wind1.set_xlim(min_x, max_x)
    wind1.set_ylim(min_y, max_y)
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

    for t in range(0, simulation_time, time_step):
        # 各タイムステップにおけるクライアントの座標を格納
        pub_x_list = [[] for i in range(1)]
        pub_y_list = [[] for i in range(1)]
        sub_x_list = [[] for i in range(1)]
        sub_y_list = [[] for i in range(1)]
        pub_sub_x_list = [[] for i in range(1)]
        pub_sub_y_list = [[] for i in range(1)]
        line_list = []

        for id in range(num_client):
            data = data_set.pop(0)

            # 実際に使う時には要修正
            for n in range(num_topic):
                if data.pub_edge[n] != -1 and data.sub_edge != -1:
                    pub_sub_x_list[n].append(data.x)
                    pub_sub_y_list[n].append(data.y)
                    
                    if data.pub_edge[n] == data.sub_edge:
                        line_list.append([(data.x, data.y), (all_edge[data.pub_edge[n]].x, all_edge[data.pub_edge[n]].y), "purple"])
                    else:
                        line_list.append([(data.x, data.y), (all_edge[data.pub_edge[n]].x, all_edge[data.pub_edge[n]].y), "red"])
                        line_list.append([(data.x, data.y), (all_edge[data.sub_edge].x, all_edge[data.sub_edge].y), "blue"])
                elif data.pub_edge[n] != -1:
                    pub_x_list[n].append(data.x)
                    pub_y_list[n].append(data.y)

                    line_list.append([(data.x, data.y), (all_edge[data.pub_edge[n]].x, all_edge[data.pub_edge[n]].y), "red"])
                else:
                    sub_x_list[n].append(data.x)
                    sub_y_list[n].append(data.y)

                    line_list.append([(data.x, data.y), (all_edge[data.sub_edge].x, all_edge[data.sub_edge].y), "blue"])

        my_title = wind1.text(5.5, 13, 'time : {}'.format(t))
        img_publisher = wind1.scatter(pub_x_list[n], pub_y_list[n], c="red")
        img_subscriber = wind1.scatter(sub_x_list[n], sub_y_list[n], c="blue")
        img_pub_sub = wind1.scatter(pub_sub_x_list[n], pub_sub_y_list[n], c="purple")
        img_edge = wind1.scatter(edge_x, edge_y, s=20, c="green", marker="s")

        img_list = [my_title, img_publisher, img_subscriber, img_pub_sub, img_edge]

        for line in line_list:
            img_list.extend(wind1.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color=line[2]))

        imgs.append(img_list)

    ani = animation.ArtistAnimation(fig, imgs, interval=1)

    # fps は1~50までしかとれない
    ani.save(out_file, writer=animation.PillowWriter(fps=FPS))


# 割り当て付きの分布の可視化
def create_assign_animation(index_file, out_file, FPS):
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

    data_set = util.read_data_set_solution(data_file, num_topic)

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

    # エッジサーバの作成
    all_edge = util.read_edge(edge_file)
    edge_x = np.zeros(num_edge)
    edge_y = np.zeros(num_edge)

    for edge in all_edge:
        edge_x[edge.id] = edge.x
        edge_y[edge.id] = edge.y

    imgs = []

    for t in range(0, simulation_time, time_step):
        #  各タイムステップにおけるクライアントの座標を格納
        #  クライアント全体の分布
        x_list = []
        y_list = []
        #  各 topic の分布
        pub_x_list = [[] for _ in range(num_topic)]
        pub_y_list = [[] for _ in range(num_topic)]
        sub_x_list = [[] for _ in range(num_topic)]
        sub_y_list = [[] for _ in range(num_topic)]
        pub_sub_x_list = [[] for _ in range(num_topic)]
        pub_sub_y_list = [[] for _ in range(num_topic)]
        line_list = [[] for _ in range(num_topic)]

        for id in range(num_client):
            data = data_set.pop(0)

            x_list.append(data.x)
            y_list.append(data.y)

            for n in range(num_topic):
                if data.pub_edge[n] != -1 and data.sub_edge[n] != -1:
                    pub_sub_x_list[n].append(data.x)
                    pub_sub_y_list[n].append(data.y)
                    
                    if data.pub_edge[n] == data.sub_edge[n]:
                        line_list[n].append([(data.x, data.y), (all_edge[data.pub_edge[n]].x, all_edge[data.pub_edge[n]].y), "red"])
                        line_list[n].append([(data.x, data.y), (all_edge[data.pub_edge[n]].x, all_edge[data.pub_edge[n]].y), "purple"])
                    else:
                        line_list[n].append([(data.x, data.y), (all_edge[data.pub_edge[n]].x, all_edge[data.pub_edge[n]].y), "red"])
                        line_list[n].append([(data.x, data.y), (all_edge[data.sub_edge].x, all_edge[data.sub_edge].y), "blue"])
                elif data.pub_edge[n] != -1 and data.sub_edge[n] == -1:
                    pub_x_list[n].append(data.x)
                    pub_y_list[n].append(data.y)

                    line_list[n].append([(data.x, data.y), (all_edge[data.pub_edge[n]].x, all_edge[data.pub_edge[n]].y), "red"])
                elif data.pub_edge[n] == -1 and data.sub_edge[n] != -1:
                    sub_x_list[n].append(data.x)
                    sub_y_list[n].append(data.y)

                    line_list[n].append([(data.x, data.y), (all_edge[data.sub_edge].x, all_edge[data.sub_edge].y), "blue"])

        my_title = wind1.text(13, 13, 'time : {}'.format(t))
        client_dist = wind1.scatter(x_list, y_list, c="black")
        img_edge = wind1.scatter(edge_x, edge_y, s=20, c="green", marker="s")

        img_publisher1 = wind2.scatter(pub_x_list[0], pub_y_list[0], c="red")
        img_subscriber1 = wind2.scatter(sub_x_list[0], sub_y_list[0], c="blue")
        img_pub_sub1 = wind2.scatter(pub_sub_x_list[0], pub_sub_y_list[0], c="purple")
        img_edge1 = wind2.scatter(edge_x, edge_y, s=20, c="green", marker="s")

        img_publisher2 = wind3.scatter(pub_x_list[1], pub_y_list[1], c="red")
        img_subscriber2 = wind3.scatter(sub_x_list[1], sub_y_list[1], c="blue")
        img_pub_sub2 = wind3.scatter(pub_sub_x_list[1], pub_sub_y_list[1], c="purple")
        img_edge2 = wind3.scatter(edge_x, edge_y, s=20, c="green", marker="s")

        img_publisher3 = wind4.scatter(pub_x_list[2], pub_y_list[2], c="red")
        img_subscriber3 = wind4.scatter(sub_x_list[2], sub_y_list[2], c="blue")
        img_pub_sub3 = wind4.scatter(pub_sub_x_list[2], pub_sub_y_list[2], c="purple")
        img_edge3 = wind4.scatter(edge_x, edge_y, s=20, c="green", marker="s")

        img_list = [my_title, client_dist, img_edge, img_publisher1, img_subscriber1, img_pub_sub1, img_edge1, img_publisher2, img_subscriber2, img_pub_sub2, img_edge2, img_publisher3, img_subscriber3, img_pub_sub3, img_edge3]

        for line in line_list[0]:
            img_list.extend(wind2.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color=line[2]))
        
        for line in line_list[1]:
            img_list.extend(wind3.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color=line[2]))
        
        for line in line_list[2]:
            img_list.extend(wind4.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color=line[2]))

        imgs.append(img_list)

    ani = animation.ArtistAnimation(fig, imgs, interval=1)

    # fps は1~50までしかとれない
    ani.save(out_file, writer=animation.PillowWriter(fps=FPS))


# 割り当て付きの分布の可視化
def create_opt_animation(index_file, out_file, opt_solution, FPS):
    df_index = pd.read_csv(index_file, index_col=0)

    config_file = df_index.at['data', 'config_file']
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

    data_set = util.read_data_set_solution(opt_solution, num_topic)

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

    # エッジサーバの作成
    all_edge = util.read_edge(edge_file)
    edge_x = np.zeros(num_edge)
    edge_y = np.zeros(num_edge)

    for edge in all_edge:
        edge_x[edge.id] = edge.x
        edge_y[edge.id] = edge.y

    imgs = []

    for t in range(0, simulation_time, time_step):
        #  各タイムステップにおけるクライアントの座標を格納
        #  クライアント全体の分布
        x_list = []
        y_list = []
        #  各 topic の分布
        pub_x_list = [[] for _ in range(num_topic)]
        pub_y_list = [[] for _ in range(num_topic)]
        sub_x_list = [[] for _ in range(num_topic)]
        sub_y_list = [[] for _ in range(num_topic)]
        pub_sub_x_list = [[] for _ in range(num_topic)]
        pub_sub_y_list = [[] for _ in range(num_topic)]
        line_list = [[] for _ in range(num_topic)]

        for id in range(num_client):
            data = data_set.pop(0)

            x_list.append(data.x)
            y_list.append(data.y)

            for n in range(num_topic):
                if data.pub_edge[n] != -1 and data.sub_edge[n] != -1:
                    pub_sub_x_list[n].append(data.x)
                    pub_sub_y_list[n].append(data.y)
                    
                    if data.pub_edge[n] == data.sub_edge[n]:
                        line_list[n].append([(data.x, data.y), (all_edge[data.pub_edge[n]].x, all_edge[data.pub_edge[n]].y), "red"])
                        line_list[n].append([(data.x, data.y), (all_edge[data.pub_edge[n]].x, all_edge[data.pub_edge[n]].y), "purple"])
                    else:
                        line_list[n].append([(data.x, data.y), (all_edge[data.pub_edge[n]].x, all_edge[data.pub_edge[n]].y), "red"])
                        line_list[n].append([(data.x, data.y), (all_edge[data.sub_edge[n]].x, all_edge[data.sub_edge[n]].y), "blue"])
                elif data.pub_edge[n] != -1 and data.sub_edge[n] == -1:
                    pub_x_list[n].append(data.x)
                    pub_y_list[n].append(data.y)

                    line_list[n].append([(data.x, data.y), (all_edge[data.pub_edge[n]].x, all_edge[data.pub_edge[n]].y), "red"])
                elif data.pub_edge[n] == -1 and data.sub_edge[n] != -1:
                    sub_x_list[n].append(data.x)
                    sub_y_list[n].append(data.y)

                    line_list[n].append([(data.x, data.y), (all_edge[data.sub_edge[n]].x, all_edge[data.sub_edge[n]].y), "blue"])
                
        my_title = wind1.text(11, 13, 'time : {}'.format(t))
        client_dist = wind1.scatter(x_list, y_list, c="black")
        img_edge = wind1.scatter(edge_x, edge_y, s=20, c="green", marker="s")

        img_publisher1 = wind2.scatter(pub_x_list[0], pub_y_list[0], c="red")
        img_subscriber1 = wind2.scatter(sub_x_list[0], sub_y_list[0], c="blue")
        img_pub_sub1 = wind2.scatter(pub_sub_x_list[0], pub_sub_y_list[0], c="purple")
        img_edge1 = wind2.scatter(edge_x, edge_y, s=20, c="green", marker="s")

        img_publisher2 = wind3.scatter(pub_x_list[1], pub_y_list[1], c="red")
        img_subscriber2 = wind3.scatter(sub_x_list[1], sub_y_list[1], c="blue")
        img_pub_sub2 = wind3.scatter(pub_sub_x_list[1], pub_sub_y_list[1], c="purple")
        img_edge2 = wind3.scatter(edge_x, edge_y, s=20, c="green", marker="s")

        img_publisher3 = wind4.scatter(pub_x_list[2], pub_y_list[2], c="red")
        img_subscriber3 = wind4.scatter(sub_x_list[2], sub_y_list[2], c="blue")
        img_pub_sub3 = wind4.scatter(pub_sub_x_list[2], pub_sub_y_list[2], c="purple")
        img_edge3 = wind4.scatter(edge_x, edge_y, s=20, c="green", marker="s")

        img_list = [my_title, client_dist, img_edge, img_publisher1, img_subscriber1, img_pub_sub1, img_edge1, img_publisher2, img_subscriber2, img_pub_sub2, img_edge2, img_publisher3, img_subscriber3, img_pub_sub3, img_edge3]

        for line in line_list[0]:
            img_list.extend(wind2.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color=line[2]))
        
        for line in line_list[1]:
            img_list.extend(wind3.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color=line[2]))
        
        for line in line_list[2]:
            img_list.extend(wind4.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color=line[2]))

        imgs.append(img_list)

    ani = animation.ArtistAnimation(fig, imgs, interval=1)

    # fps は1~50までしかとれない
    ani.save(out_file, writer=animation.PillowWriter(fps=FPS))
