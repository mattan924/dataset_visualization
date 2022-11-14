import util
from client import Client_traking
from client import Client_topic
from data import Data_traking, Data_topic
from edge import Edge
from topic import Topic
import random
import pandas as pd
import os
import math


def generate_traking(index_file, config_file, out_file, seed=0):
    if not os.path.exists(index_file):
        util.create_index_file(index_file, config_file)

    if seed != 0:
        random.seed(seed)
    else:
        seed = random.randint(1, 100000000)
        random.seed(seed)

    df_index = pd.read_csv(index_file, index_col=0)
    df_index.at['data', 'config_file'] = config_file
    df_index.at['data', 'traking_seed'] = seed
    df_index.at['data', 'traking_file'] = out_file

    df_index.to_csv(index_file)
    
    min_x, max_x, min_y, max_y, simulation_time, time_step, num_client, num_topic, num_edge, volume, cpu_power, save_period, speed = util.read_config(config_file)
    
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

            x, y = c.random_walk(time_step, min_x, max_x, min_y, max_y)

            util.writeTrakingCSV(out_file, Data_traking(c.id, time, x, y))


def assignTopic(index_file, out_file, seed=0):
    if not os.path.exists(index_file):
        print("Traking data is not exist. Create traking data in advance.")
    else:
        if seed != 0:
            random.seed(seed)
        else:
            seed = random.randint(1, 100000000)
            random.seed(seed)
        
        df_index = pd.read_csv(index_file, index_col=0)
        df_index.at['data', 'assign_file'] = out_file
        df_index.at['data', 'assign_seed'] = seed

        config_file = df_index.at['data', 'config_file']
        traking_file = df_index.at['data', 'traking_file']
        topic_file = df_index.at['data', 'topic_file']

        df_index.to_csv(index_file)
    
        data_set_traking = util.read_data_set_traking(traking_file)
        all_topic = util.read_topic(topic_file)

        min_x, max_x, min_y, max_y, simulation_time, time_step, num_client, num_topic, num_edge, volume, cpu_power, save_period, speed = util.read_config(config_file)

        all_client = []

        for i in range(num_client):
            data_traking = data_set_traking.pop(0)

            init_topic = []

            for t in all_topic:
                if t.init_topic(data_traking.x, data_traking.y):
                    init_topic.append(t.id)

            c_topic = Client_topic(data_traking.id, data_traking.x, data_traking.y, init_topic)

            all_client.append(c_topic)

            util.writeAssginCSV(out_file, Data_topic(c_topic.id, 0, c_topic.x, c_topic.y, init_topic))


        for time in range(time_step, simulation_time, time_step):
            for t in all_topic:
                if t.role == 2:
                    t.decide_random_point(min_x, max_x, min_y, max_y, time_step)

            for c in all_client:
                data_traking = data_set_traking.pop(0)

                c.x = data_traking.x
                c.y = data_traking.y

                c.select_topic(all_topic)

                util.writeAssginCSV(out_file, Data_topic(c.id, time, c.x, c.y, c.topic))


def generate_edge(index_file, config_file, out_file):
    if not os.path.exists(index_file):
        util.create_index_file(index_file, config_file)

    df_index = pd.read_csv(index_file, index_col=0)
    df_index.at['data', 'config_file'] = config_file
    df_index.at['data', 'edge_file'] = out_file

    df_index.to_csv(index_file)

    min_x, max_x, min_y, max_y, simulation_time, time_step, num_client, num_topic, num_edge, volume, cpu_power, save_period, speed = util.read_config(config_file)

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


def generate_topic(index_file, config_file, out_file):
    if not os.path.exists(index_file):
        util.create_index_file(index_file, config_file)

    df_index = pd.read_csv(index_file, index_col=0)
    df_index.at['data', 'config_file'] = config_file
    df_index.at['data', 'topic_file'] = out_file

    df_index.to_csv(index_file)
    
    min_x, max_x, min_y, max_y, simulation_time, time_step, num_client, num_topic, num_edge, volume, cpu_power, save_period, speed = util.read_config(config_file)

    all_topic = []
    # トピックの生成
    for i in range(num_topic):
        all_topic.append(Topic(id=i, role=i, save_period=save_period, min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y))

    util.writeTopicCSV(out_file, all_topic)
