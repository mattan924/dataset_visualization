import util
from client import Client_traking
from client import Client_topic
from data import Data_traking, Data_topic
from edge import Edge
from topic import Topic_uniform, Topic_local, Topic_incident
import random
import pandas as pd
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

        c = Client_traking(id, init_x, init_y, speed)

        all_client.append(c)

    # データの生成および書き込み
    for time in range(0, simulation_time, time_step):
        for c in all_client:
            # クライアントをランダムに移動させる
            x, y = c.random_walk(time_step, min_x, max_x, min_y, max_y)

            util.writeTrakingCSV(out_file, Data_traking(c.id, time, x, y))


# トラッキングデータにトピックを割り当てる
def assignTopic(index_file, out_file, seed=0):
    # インデックスファイルが存在しない場合
    if not os.path.exists(index_file):
        sys.exit("index_file is not exist. Create index_file in advance.")
    else:
        # シード値をした場合
        if seed != 0:
            random.seed(seed)
        # シード値を指定しない場合、ランダムにシード値を決定
        else:
            seed = random.randint(1, 100000000)
            random.seed(seed)
        
        # インデックスファイルを読み込み、更新する
        df_index = pd.read_csv(index_file, index_col=0)
        df_index.at['data', 'assign_file'] = out_file
        df_index.at['data', 'assign_seed'] = seed

        config_file = df_index.at['data', 'config_file']
        traking_file = df_index.at['data', 'traking_file']
        topic_file = df_index.at['data', 'topic_file']

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
        simulation_time = parameter['simulation_time']
        time_step = parameter['time_step']

        # 出力ファイルの初期化
        f = open(out_file, mode="w")
        f.close()

        all_client = []

        # トラッキングデータに対してトピックを割り当てる
        for i in range(num_client):
            data_traking = data_set_traking.pop(0)

            # 初期トピックの割り当て
            init_topic = []

            for t in all_topic:
                if t.init_topic(data_traking.x, data_traking.y):
                    init_topic.append(t.id)

            c_topic = Client_topic(data_traking.id, data_traking.x, data_traking.y, init_topic)

            all_client.append(c_topic)

            util.writeAssginCSV(out_file, Data_topic(c_topic.id, 0, c_topic.x, c_topic.y, init_topic))

        # 時間を1ステップずつ進めにがら、トピックを割り当てる
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

                util.writeAssginCSV(out_file, Data_topic(c.id, time, c.x, c.y, c.topic))


# エッジサーバの生成
def generate_edge(index_file, config_file, out_file):
    # インデックスファイルが存在しない場合、生成する
    if not os.path.exists(index_file):
        util.create_index_file(index_file, config_file)

    # インデックスファイルの読み込み、更新
    df_index = pd.read_csv(index_file, index_col=0)
    df_index.at['data', 'config_file'] = config_file
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
    
    util.writeEdgeCSV(out_file, all_edge)


# トピックの生成
def generate_topic(index_file, config_file, out_file):
    # インデックスファイルが存在しない場合、生成する
    if not os.path.exists(index_file):
        util.create_index_file(index_file, config_file)

    # インデックスファイルの読み込み、更新
    df_index = pd.read_csv(index_file, index_col=0)
    df_index.at['data', 'config_file'] = config_file
    df_index.at['data', 'topic_file'] = out_file

    df_index.to_csv(index_file)
    
    # 設定ファイルからパラメーター情報を取り出す
    parameter = util.read_config(config_file)

    min_x = parameter['min_x']
    max_x = parameter['max_x']
    min_y = parameter['min_y']
    max_y = parameter['max_y']
    save_period = parameter['save_period']

    all_topic = []
    # トピックの生成
    t = Topic_uniform(0, save_period)
    all_topic.append(t)
    t = Topic_local(1, save_period, min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y)
    all_topic.append(t)
    t = Topic_incident(2, save_period)
    all_topic.append(t)

    util.writeTopicCSV(out_file, all_topic)
