import util
from client import Client
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd


def create_animation(index_file, out_file, FPS):
    df_index = pd.read_csv(index_file, index_col=0)

    config_file = df_index.at['data', 'config_file']
    data_file = df_index.at['data', 'assgin_file']
    edge_file = df_index.at['data', 'edge_file']

    parameter = util.read_config(config_file)

    min_x = parameter['min_x']
    max_x = parameter['max_x']
    min_y = parameter['min_y']
    max_y = parameter['max_y']
    num_edge = parameter['num_edge']
    num_client = parameter['num_client']
    simulation_time = parameter['simulation_time']
    time_step = parameter['time_step']

    data_set = util.read_data_set_topic(data_file)

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
        # 各タイムステップにおけるクライアントの座標を格納
        x1_list = []
        y1_list = []
        x2_list = []
        y2_list = []
        x3_list = []
        y3_list = []
        x4_list = []
        y4_list = []

        for id in range(num_client):
            data = data_set.pop(0)
            x1_list.append(data.x)
            y1_list.append(data.y)

            for topic in data.topic_list:
                if topic == 0:
                    x2_list.append(data.x)
                    y2_list.append(data.y)
                elif topic == 1:
                    x3_list.append(data.x)
                    y3_list.append(data.y)
                elif topic == 2:
                    x4_list.append(data.x)
                    y4_list.append(data.y)

        my_title = wind1.text(11.5, 14, 'time : {}'.format(t))
        img1_client = wind1.scatter(x1_list, y1_list, c="blue")
        img1_edge = wind1.scatter(edge_x, edge_y, s=20, c="green", marker="s")
        img2_client = wind2.scatter(x2_list, y2_list, c="blue")
        img2_edge = wind2.scatter(edge_x, edge_y, s=20, c="green", marker="s")
        img3_client = wind3.scatter(x3_list, y3_list, c="blue")
        img3_edge = wind3.scatter(edge_x, edge_y, s=20, c="green", marker="s")
        img4_client = wind4.scatter(x4_list, y4_list, c="blue")
        img4_edge = wind4.scatter(edge_x, edge_y, s=20, c="green", marker="s")
        img_list = [my_title, img1_client, img1_edge, img2_client, img2_edge, img3_client, img3_edge, img4_client, img4_edge]

        imgs.append(img_list)

    ani = animation.ArtistAnimation(fig, imgs, interval=1)

    # fps は1~50までしかとれない
    ani.save(out_file, writer=animation.PillowWriter(fps=FPS))


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



def create_traking_animation(index_file, out_file, FPS=20):
    df_index = pd.read_csv(index_file, index_col=0)

    config_file = df_index.at['data', 'config_file']
    data_file = df_index.at['data', 'traking_file']
    edge_file = df_index.at['data', 'edge_file']

    parameter = util.read_config(config_file)

    min_x = parameter['min_x']
    max_x = parameter['max_x']
    min_y = parameter['min_y']
    max_y = parameter['max_y']
    num_edge = parameter['num_edge']
    num_client = parameter['num_client']
    simulation_time = parameter['simulation_time']
    time_step = parameter['time_step']

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

    for t in range(0, simulation_time, time_step):
        # 各タイムステップにおけるクライアントの座標を格納
        x1_list = []
        y1_list = []

        for id in range(num_client):
            data = data_set.pop(0)

            x1_list.append(data.x)
            y1_list.append(data.y)

        my_title = wind1.text((max_x-min_x)/2 - 0.8, 13, 'time : {}'.format(t))
        img1_client = wind1.scatter(x1_list, y1_list, c="blue")
        img1_edge = wind1.scatter(edge_x, edge_y, s=20, c="green", marker="s")

        img_list = [my_title, img1_client, img1_edge]

        imgs.append(img_list)

    ani = animation.ArtistAnimation(fig, imgs, interval=1)

    # fps は1~50までしかとれない
    ani.save(out_file, writer=animation.PillowWriter(fps=FPS))
