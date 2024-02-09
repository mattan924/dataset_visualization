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
    df_index = pd.read_csv(index_file, index_col=0, dtype=str)
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
def assign_topic(index_file, out_file, num_publisher=None, seed=0):
    # インデックスファイルが存在しない場合
    if not os.path.exists(index_file):
        sys.exit("index_file is not exist. Create index_file in advance.")
    else:
        # インデックスファイルを読み込み、更新する
        df_index = pd.read_csv(index_file, index_col=0, dtype=str)

        config_file = df_index.at['data', 'config_file']
        traking_file = df_index.at['data', 'traking_file']
        topic_file = df_index.at['data', 'topic_file']

        if not os.path.exists(traking_file):
            sys.exit("traking_file is not exist. Generate traking_file in advance.")

        # シード値を指定した場合
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

        if num_publisher is not None:
            if num_client*num_topic < num_publisher:
                sys.exit("クライアントの数に対して、指定の num_publisher は大きすぎます。")

            select_num = [int(num_publisher/num_topic) for _ in range(num_topic)]

            remain_num_publisher = num_publisher - int(num_publisher/num_topic)*num_topic
                
            while(remain_num_publisher > 0):
                idx = random.randint(0, num_topic-1)
                select_num[idx] += 1
                remain_num_publisher = remain_num_publisher -1

            publisher_list = []
            for n in range(num_topic):
                publisher_list.append(random.sample(list(range(num_client)), select_num[n]))

        # トラッキングデータに対して pub/sub 関係を割り当てる
        for i in range(num_client):
            data_traking = data_set_traking.pop(0)

            # 初期トピックの割り当て
            init_pub_topic = np.zeros(num_topic)
            init_sub_topic = np.zeros(num_topic)

            for t in all_topic:
                if num_publisher is not None:
                    if data_traking.id in publisher_list[t.id]:
                        init_pub_topic[t.id] = True
                    
                    if t.init_topic(data_traking.x, data_traking.y):
                        init_sub_topic[t.id] = True
                else:
                    if t.init_topic(data_traking.x, data_traking.y):
                        init_pub_topic[t.id] = True
                        
                    if t.init_topic(data_traking.x, data_traking.y):
                        init_sub_topic[t.id] = True

            c_topic = ClientTopic(data_traking.id, data_traking.x, data_traking.y, init_pub_topic, init_sub_topic)

            all_client.append(c_topic)

            util.write_assgin_csv(out_file, DataTopic(c_topic.id, 0, c_topic.x, c_topic.y, c_topic.pub_topic, c_topic.sub_topic))

        # 時間を1ステップずつ進めにがら、pub/sub 関係を決める
        for time in range(time_step, simulation_time, time_step):
            # 突発的なトピックの更新
            for t in all_topic:
                t.update(min_x, max_x, min_y, max_y, time_step)

            # 各クライアントのトピックの選択
            for c in all_client:
                data_traking = data_set_traking.pop(0)

                c.x = data_traking.x
                c.y = data_traking.y

                c.select_topic(all_topic)

                util.write_assgin_csv(out_file, DataTopic(c.id, time, c.x, c.y, c.pub_topic, c.sub_topic))


# エッジサーバの生成
def generate_edge(index_file, config_file, out_file, seed=0):
    # インデックスファイルが存在しない場合、生成する
    if not os.path.exists(index_file):
        util.create_index_file(index_file, config_file)

    # シード値を指定した場合
    if seed != 0:
        random.seed(seed)
    # シード値を指定しない場合、ランダムにシード値を決定
    else:
        seed = random.randint(1, 100000000)
        random.seed(seed)

    # インデックスファイルの読み込み、更新
    df_index = pd.read_csv(index_file, index_col=0, dtype=str)
    df_index.at['data', 'edge_file'] = out_file
    df_index.at['data', 'edge_seed'] = seed

    df_index.to_csv(index_file)

    # 設定ファイルからパラメーター情報の読み込み
    parameter = util.read_config(config_file)

    volume = parameter['volume']
    cpu_cycle = parameter['cpu_cycle']

    # エッジサーバの生成
    all_edge = []

    # 今はエッジの数を3×3で固定している。改修ポイント
    for i in range(3):
        for j in range(3):
            id = i*3+j
            x = 2 + 4*j
            y = 2 + 4*i

            """
            tmp = random.randint(0, 2)
            if tmp == 0:
                volume_tmp = volume * 1
            elif tmp == 1:
                volume_tmp = volume * 1.25
            else:
                volume_tmp = volume * 0.75

            tmp = random.randint(0, 2)
            if tmp == 0:
                cpu_cycle_tmp = cpu_cycle * 1
            elif tmp == 1:
                cpu_cycle_tmp = cpu_cycle * 1.25
            else:
                cpu_cycle_tmp = cpu_cycle * 0.75
            
            all_edge.append(Edge(id, x, y, volume_tmp, cpu_cycle_tmp))
            """

            all_edge.append(Edge(id, x, y, volume, cpu_cycle))
    
    util.write_edge_csv(out_file, all_edge)


# トピックの生成
def generate_topic(index_file, config_file, out_file, seed=0):
    # インデックスファイルが存在しない場合、生成する
    if not os.path.exists(index_file):
        util.create_index_file(index_file, config_file)

    # シード値を指定した場合
    if seed != 0:
        random.seed(seed)
    # シード値を指定しない場合、ランダムにシード値を決定
    else:
        seed = random.randint(1, 100000000)
        random.seed(seed)

    # インデックスファイルの読み込み、更新
    df_index = pd.read_csv(index_file, index_col=0, dtype=str)
    df_index.at['data', 'topic_file'] = out_file
    df_index.at['data', 'topic_seed'] = seed

    df_index.to_csv(index_file)
    
    # 設定ファイルからパラメーター情報を取り出す
    parameter = util.read_config(config_file)

    min_x = parameter['min_x']
    max_x = parameter['max_x']
    min_y = parameter['min_y']
    max_y = parameter['max_y']
    num_topic = parameter['num_topic']
    save_period = parameter['save_period']
    topic_cycle = parameter['topic_cycle']
    publish_rate = parameter['publish_rate']

    all_topic = []
    # トピックの生成
    #  作成したい topic に応じてここを変える
    for i in range(num_topic):
        # tmp = random.randint(0, 2)
        # if tmp == 0:
        #     publish_rate_tmp = publish_rate
        # elif tmp == 1:
        #     publish_rate_tmp = publish_rate * 1.5
        # else:
        #     publish_rate_tmp = publish_rate * 0.5
        
        # tmp = random.randint(0, 2)
        # if tmp == 0:
        #     topic_cycle_tmp = topic_cycle
        # elif tmp == 1:
        #     topic_cycle_tmp = topic_cycle * 1.5
        # else:
        #     topic_cycle_tmp = topic_cycle * 0.5

        publish_rate_tmp = publish_rate * random.uniform(0.5, 1.5)
        topic_cycle_tmp = topic_cycle * random.uniform(0.5, 1.5)

        t = TopicUniform(i, save_period, publish_rate=publish_rate_tmp, require_cycle=topic_cycle_tmp)
        all_topic.append(t)

    util.write_topic_csv(out_file, all_topic)
