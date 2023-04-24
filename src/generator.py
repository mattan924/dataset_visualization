import util
from client import ClientTraking, ClientTopic
from data import DataTraking, DataTopic
from edge import Edge
from topic import TopicUniform, TopicLocal, TopicIncident
import random
import pandas as pd
import numpy as np
import os
import sys


# トラッキングデータの生成
def generate_traking(index_file, config_file, out_file, seed=0):
    # インデックスファイルが存在しない場合、生成
    if not os.path.exists(index_file):
        util.create_index_file(index_file, config_file)

    # シード値を指定した場合
    if seed != 0:
        random.seed(seed)
    # シード値を指定しなかった場合、ランダムにシード値を決定
    else:
        seed = random.randint(1, 100000000)
        random.seed(seed)

    # インデックスファイルから情報を取り出しと更新
    df_index = pd.read_csv(index_file, index_col=0)
    df_index.at['data', 'config_file'] = config_file
    df_index.at['data', 'traking_seed'] = seed
    df_index.at['data', 'traking_file'] = out_file

    # 更新後のインデックスファイルの書き出し
    df_index.to_csv(index_file)
    
    # 設定ファイルからパラメーター情報の受け取り
    parameter = util.read_config(config_file)

    # パラメーターの取り出し
    min_x = parameter['min_x']
    max_x = parameter['max_x']
    min_y = parameter['min_y']
    max_y = parameter['max_y']
    num_client = parameter['num_client']
    speed = parameter['speed']
    simulation_time = parameter['simulation_time']
    time_step = parameter['time_step']
    
    # 出力ファイルの上書き
    with open(out_file, mode='w') as f:
        f.write("id,time,x,y\n")
    
    # クライアントの生成
    all_client = []

    for id in range(num_client):
        # 各クライアントの初期位置の決定
        init_x, init_y = util.init_point(min_x, max_x, min_y, max_y)

        c = ClientTraking(id, init_x, init_y, speed)

        all_client.append(c)

    # データの生成および書き込み
    for time in range(0, simulation_time, time_step):
        for c in all_client:
            # クライアントをランダムに移動させる
            c.random_walk(time_step, min_x, max_x, min_y, max_y)

            util.write_traking_csv(out_file, DataTraking(c.id, time, c.x, c.y))


# トラッキングデータに pub/sub 関係を割り当てる
def assign_topic(index_file, out_file, seed=0):
    # インデックスファイルが存在しない場合
    if not os.path.exists(index_file):
        sys.exit("index_file is not exist. Create index_file in advance.")
    else:
        # インデックスファイルを読み込み、更新する
        df_index = pd.read_csv(index_file, index_col=0)

        config_file = df_index.at['data', 'config_file']
        traking_file = df_index.at['data', 'traking_file']
        topic_file = df_index.at['data', 'topic_file']

        if not os.path.exists(traking_file):
            sys.exit("traking_file is not exist. Generate traking_file in advance.")

        # シード値をした場合
        if seed != 0:
            random.seed(seed)
        # シード値を指定しない場合、ランダムにシード値を決定
        else:
            seed = random.randint(1, 100000000)
            random.seed(seed)
        
        
        df_index.at['data', 'assign_file'] = out_file
        df_index.at['data', 'assign_seed'] = seed

        df_index.to_csv(index_file)

        # トラッキングデータの読み込み
        data_set_traking = util.read_data_set_traking(traking_file)
        # エッジサーバのデータの読み込み
        all_topic = util.read_topic(topic_file)
        
        # パラメーター情報を読み取り、取り出す
        parameter = util.read_config(config_file)

        min_x = parameter['min_x']
        max_x = parameter['max_x']
        min_y = parameter['min_y']
        max_y = parameter['max_y']
        num_client = parameter['num_client']
        num_topic = parameter['num_topic']
        simulation_time = parameter['simulation_time']
        time_step = parameter['time_step']

        # 出力ファイルの初期化
        f = open(out_file, mode="w")
        f.close()

        all_client = []

        # トラッキングデータに対して pub/sub 関係を割り当てる
        for i in range(num_client):
            data_traking = data_set_traking.pop(0)

            # 初期トピックの割り当て
            init_pub_topic = np.zeros(num_topic)
            init_sub_topic = np.zeros(num_topic)

            #  必ず pub/sub のどちらかはTrue
            flag = True
            while(flag):
                for t in all_topic:
                    if t.init_topic(data_traking.x, data_traking.y):
                        init_pub_topic[t.id] = True
                        flag = False
                    
                    if t.init_topic(data_traking.x, data_traking.y):
                        init_sub_topic[t.id] = True
                        flag = False

            c_topic = ClientTopic(data_traking.id, data_traking.x, data_traking.y, init_pub_topic, init_sub_topic)

            all_client.append(c_topic)

            util.write_assgin_csv(out_file, DataTopic(c_topic.id, 0, c_topic.x, c_topic.y, c_topic.pub_topic, c_topic.sub_topic))

        # 時間を1ステップずつ進めにがら、pub/sub 関係を決める
        for time in range(time_step, simulation_time, time_step):
            # 突発的なトピックの更新
            for t in all_topic:
                if t.role == 2:
                    t.decide_random_point(min_x, max_x, min_y, max_y, time_step)

            # 各クライアントのトピックの選択
            for c in all_client:
                data_traking = data_set_traking.pop(0)

                c.x = data_traking.x
                c.y = data_traking.y

                c.select_topic(all_topic)

                util.write_assgin_csv(out_file, DataTopic(c.id, time, c.x, c.y, c.pub_topic, c.sub_topic))


# エッジサーバの生成
def generate_edge(index_file, config_file, out_file):
    # インデックスファイルが存在しない場合、生成する
    if not os.path.exists(index_file):
        util.create_index_file(index_file, config_file)

    # インデックスファイルの読み込み、更新
    df_index = pd.read_csv(index_file, index_col=0)
    df_index.at['data', 'edge_file'] = out_file

    df_index.to_csv(index_file)

    # 設定ファイルからパラメーター情報の読み込み
    parameter = util.read_config(config_file)

    volume = parameter['volume']
    cpu_power = parameter['cpu_power']

    # エッジサーバの生成
    all_edge = []

    # 今はエッジの数を3×3で固定している。改修ポイント
    for i in range(3):
        for j in range(3):
            id = i*3+j
            x = 2 + 4*j
            y = 2 + 4*i
            all_edge.append(Edge(id, x, y, volume, cpu_power))
    
    util.write_edge_csv(out_file, all_edge)


# トピックの生成
def generate_topic(index_file, config_file, out_file):
    # インデックスファイルが存在しない場合、生成する
    if not os.path.exists(index_file):
        util.create_index_file(index_file, config_file)

    # インデックスファイルの読み込み、更新
    df_index = pd.read_csv(index_file, index_col=0)
    df_index.at['data', 'topic_file'] = out_file

    df_index.to_csv(index_file)
    
    # 設定ファイルからパラメーター情報を取り出す
    parameter = util.read_config(config_file)

    min_x = parameter['min_x']
    max_x = parameter['max_x']
    min_y = parameter['min_y']
    max_y = parameter['max_y']
    num_topic = parameter['num_topic']
    save_period = parameter['save_period']

    all_topic = []
    # トピックの生成
    #  作成したい topic に応じてここを変える
    for i in range(num_topic):
        t = TopicUniform(i, save_period)
        all_topic.append(t)

    util.write_topic_csv(out_file, all_topic)
