from data import DataTopic, DataTraking, DataSolution
import random
import math
import sys
import pandas as pd
import numpy as np

from edge import Edge
from topic import TopicUniform, TopicLocal, TopicIncident


#  index ファイルの生成
def create_index_file(index_file, config_file):
    with open(index_file, mode='w') as f:
        f.write(",config_file,edge_file,topic_file,traking_file,traking_seed,assign_file,assign_seed,solve_file,opt\n")
        f.write("data," + config_file + ",,,,,,,,")


# 設定ファイルの読み込み
def read_config(config_path):
    f = open(config_path)

    min_x = int(f.readline().split(",")[1])
    max_x = int(f.readline().split(",")[1])
    min_y = int(f.readline().split(",")[1])
    max_y = int(f.readline().split(",")[1])
    simulation_time = int(f.readline().split(",")[1])
    time_step = int(f.readline().split(",")[1])
    num_client = int(f.readline().split(",")[1])
    num_topic = int(f.readline().split(",")[1])
    num_edge = int(f.readline().split(",")[1])
    volume = int(f.readline().split(",")[1])
    cpu_cycle = int(f.readline().split(",")[1])
    cloud_time = int(f.readline().split(",")[1])
    cloud_cycle = int(f.readline().split(",")[1])
    save_period = int(f.readline().split(",")[1])
    speed = int(f.readline().split(",")[1])

    parameter = { 'min_x' : min_x, 'max_x' : max_x, 'min_y' : min_y, 'max_y' : max_y, 'simulation_time' : simulation_time, 'time_step' : time_step}
    parameter1 = { 'num_client' : num_client, 'num_topic' : num_topic, 'num_edge' : num_edge}
    parameter2 = { 'volume' : volume, 'cpu_power' : cpu_cycle, 'cloud_time' : cloud_time, 'cloud_cycle' : cloud_cycle, 'save_period' : save_period, 'speed' : speed}

    parameter.update(parameter1)
    parameter.update(parameter2)

    return parameter


#  edge ファイルの読み込み
def read_edge(edge_path):
    df = pd.read_csv(edge_path)
    num_edge = len(df.index)

    all_edge = []
    for i in range(num_edge):
        data = df.iloc[i]
        id = data['id']
        x = data['x']
        y = data['y']
        volume = data['volume']
        cpu_power = data['cpu_power']

        edge = Edge(id, x, y, volume, cpu_power)
        all_edge.append(edge)

    return all_edge


#  topic ファイルの読み取り
def read_topic(topic_path):
    df = pd.read_csv(topic_path)
    num_topic = len(df.index)

    all_topic = []
    for i in range(num_topic):
        data = df.iloc[i]
        id = int(data['id'])
        role = int(data['role'])
        save_period = data['save_period']        
        publish_rate = data['publish_rate']
        data_size = data['data_size']
        require_cycle = data['require_cycle']
        base_x = data['base_x']
        base_y = data['base_y']

        if role == 0:
            topic = TopicUniform(id, save_period, publish_rate=publish_rate, data_size=data_size, require_cycle=require_cycle)
        elif role == 1:
            topic = TopicLocal(id, save_period, publish_rate=publish_rate, data_size=data_size, require_cycle=require_cycle, base_point=(base_x, base_y))
        elif role == 2:
            topic = TopicIncident(id, save_period, publish_rate=publish_rate, data_size=data_size, require_cycle=require_cycle)
        else:
            sys.exit("追加されていない role です。関数 read_topic を修正して下さい")

        all_topic.append(topic)

    return all_topic


# トラッキングデータを読み込む
def read_data_set_traking(path):
    df = pd.read_csv(path)

    data_set_traking = []

    for i in range(len(df.index)):
        data = df.iloc[i]

        id = int(data['id'])
        time = int(data['time'])
        x = float(data['x'])
        y = float(data['y'])

        data_traking = DataTraking(id, time, x, y)

        data_set_traking.append(data_traking)

    return data_set_traking


# トピックの情報を持つデータを読み込む
def read_data_set_topic(path, num_topic):
    data_set_topic = []
    f = open(path)

    for line in f:
        l = line.split(",")

        id = int(l.pop(0))
        time = l.pop(0)
        x = float(l.pop(0))
        y = float(l.pop(0))

        pub_topic = np.zeros(num_topic)
        for i in range(num_topic):
            tmp = float(l.pop(0).split('\n')[0])
            if tmp == True:
                pub_topic[i] = True

        sub_topic = np.zeros(num_topic)
        for i in range(num_topic):
            tmp = float(l.pop(0).split('\n')[0])
            if tmp == True:
                sub_topic[i] = True
                
        data_topic = DataTopic(id, time, x, y, pub_topic, sub_topic)

        data_set_topic.append(data_topic)

    return data_set_topic


#  クライアントの割り当て情報の読み込み
def read_data_set_solution(data_path, num_topic):
    
    f = open(data_path)
    data_set_solution = []

    for line in f:
        l = line.split(",")
        
        id = int(l.pop(0))
        time = l.pop(0)
        x = float(l.pop(0))
        y = float(l.pop(0))

        pub_edge = []
        for n in range(num_topic):
            pub_edge.append(int(float(l.pop(0))))

        sub_edge = []
        for n in range(num_topic):
            sub_edge.append(int(float(l.pop(0))))

        data_solution = DataSolution(id, time, x, y, pub_edge, sub_edge)

        data_set_solution.append(data_solution)

    return data_set_solution


# 指定したファイルにデータを一行追加
def write_traking_csv(filename, data_traking):
    file = open(filename, "a")

    file.write(f"{data_traking.id},{data_traking.time},{data_traking.x},{data_traking.y}\n")

    file.close()


# 指定したファイルにデータを一行追加
def write_assgin_csv(filename, data_topic):
    file = open(filename, "a")

    file.write(f"{data_topic.id},{data_topic.time},{data_topic.x},{data_topic.y}")

    for topic in data_topic.pub_topic:
        file.write(f",{topic}")

    for topic in data_topic.sub_topic:
        file.write(f",{topic}")
    
    file.write("\n")

    file.close()


#  クライアントの割り当て情報を一行追記
def write_solution_csv(filename, id, time, x, y, pub_edge, sub_edge, num_topic):
    file = open(filename, "a")

    file.write(f"{id},{time},{x},{y}")

    for n in range(num_topic):
        file.write(f",{pub_edge[n]}")

    for n in range(num_topic):
        file.write(f",{sub_edge[n]}")

    file.write("\n")

    file.close()


#  edge の情報を書き出し
def write_edge_csv(filename, all_edge):
    file = open(filename, "w")

    file.write("id,x,y,volume,cpu_power\n")

    for edge in all_edge:
        file.write(f"{edge.id},{edge.x},{edge.y},{edge.volume},{edge.cpu_power}\n")

    file.close()


#  topic の情報を書き出し
def write_topic_csv(filename, all_topic):
    file = open(filename, "w")

    file.write("id,role,save_period,publish_rate,data_size,require_cycle,base_x,base_y\n")

    for topic in all_topic:
        if topic.role == 0:
            file.write(f"{topic.id},{topic.role},{topic.save_period},{topic.publish_rate},{topic.data_size},{topic.require_cycle},,\n")
        elif topic.role == 1:
            file.write(f"{topic.id},{topic.role},{topic.save_period},{topic.publish_rate},{topic.data_size},{topic.require_cycle},{topic.base_point[0]},{topic.base_point[1]}\n")
        elif topic.role == 2:
            file.write(f"{topic.id},{topic.role},{topic.save_period},{topic.publish_rate},{topic.data_size},{topic.require_cycle},,\n")
        else:
            sys.exit("追加されていない role です。関数writeTopicCSVを修正して下さい")

    file.close()


# クライアントの初期位置の決定
def init_point(min_x, max_x, min_y, max_y):

    x = random.randint(min_x, max_x)
    y = random.randint(min_y, max_y)

    return x, y


#  2点間の距離を測る
def cal_distance(x1, y1, x2, y2):
    distance = math.sqrt(pow(x1-x2,2)+pow(y1-y2,2))

    return distance
