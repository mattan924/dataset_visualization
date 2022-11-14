from data import Data_topic, Data_traking, Data_solution
import random
import math
import pandas as pd

from edge import Edge
from topic import Topic

 
def create_index_file(index_file, config_file):
    with open(index_file, mode='w') as f:
        f.write(",config_file,edge_file,topic_file,traking_file,traking_seed,assign_file,assign_seed,solve_file\n")
        f.write("data," + config_file + ",,,,,,,")

# 設定ファイルの読み込み
def read_config(path):
    f = open(path)

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
    cpu_power = int(f.readline().split(",")[1])
    save_period = int(f.readline().split(",")[1])
    speed = int(f.readline().split(",")[1])

    return min_x, max_x, min_y, max_y, simulation_time, time_step, num_client, num_topic, num_edge, volume, cpu_power, save_period, speed


def read_edge(path):
    df = pd.read_csv(path)
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


def read_topic(path):
    df = pd.read_csv(path)
    num_topic = len(df.index)

    all_topic = []
    for i in range(num_topic):
        data = df.iloc[i]
        id = data['id']
        role = data['role']
        save_period = data['save_period']
        base_x = data['base_x']
        base_y = data['base_y']
        publish_rate = data['publish_rate']
        data_size = data['data_size']

        topic = Topic(id, role, save_period, base_point=(base_x, base_y), publish_rate=publish_rate, data_size=data_size)
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

        data_traking = Data_traking(id, time, x, y)

        data_set_traking.append(data_traking)

    return data_set_traking


# トピックの情報を持つデータを読み込む
def read_data_set_topic(path):
    data_set_topic = []
    f = open(path)

    for line in f:
        l = line.split(",")

        id = int(l.pop(0))
        time = l.pop(0)
        x = float(l.pop(0))
        y = float(l.pop(0))

        topic_list = []
        for t in l:
            topic_list.append(int(float(t.split('\n')[0])))

        data_topic = Data_topic(id, time, x, y, topic_list)

        data_set_topic.append(data_topic)

    return data_set_topic


def read_data_set_solution(data_path, config_path):
    min_x, max_x, min_y, max_y, simulation_time, time_step, num_client, num_topic, num_edge, volume, cpu_power, save_period, speed = read_config(config_path)
    
    f = open(data_path)
    data_set_solution = []

    for line in f:
        l = line.split(",")

        id = int(l.pop(0))
        time = l.pop(0)
        x = float(l.pop(0))
        y = float(l.pop(0))

        pub_edge = []
        for t in l[:num_topic]:
            pub_edge.append(int(t))

        sub_edge = []
        for t in l[num_topic:]:
            sub_edge.append(int(t))

        data_solution = Data_solution(id, time, x, y, pub_edge, sub_edge)

        data_set_solution.append(data_solution)

    return data_set_solution


# 指定したファイルにデータを一行追加
def writeTrakingCSV(filename, data_traking):
    file = open(filename, "a")

    file.write(f"{data_traking.id},{data_traking.time},{data_traking.x},{data_traking.y}\n")

    file.close()


# 指定したファイルにデータを一行追加
def writeAssginCSV(filename, data_topic):
    file = open(filename, "a")

    file.write(f"{data_topic.id},{data_topic.time},{data_topic.x},{data_topic.y}")

    for topic in data_topic.topic_list:
        file.write(f",{topic}")
    
    file.write("\n")

    file.close()


def writeSolutionCSV(filename, id, time, x, y, pub_edge, sub_edge, num_topic):
    file = open(filename, "a")

    file.write(f"{id},{time},{x},{y}")

    for i in range(num_topic):
        file.write(f",{pub_edge[i]}")

    for i in range(num_topic):
        file.write(f",{sub_edge[i]}")

    file.write("\n")

    file.close()


def writeEdgeCSV(filename, all_edge):
    file = open(filename, "w")

    file.write("id,x,y,volume,cpu_power\n")

    for edge in all_edge:
        file.write(f"{edge.id},{edge.x},{edge.y},{edge.volume},{edge.cpu_power}\n")

    file.close()


def writeTopicCSV(filename, all_topic):
    file = open(filename, "w")

    file.write("id,role,save_period,base_x,base_y,publish_rate,data_size\n")

    for topic in all_topic:
        file.write(f"{topic.id},{topic.role},{topic.save_period},{topic.base_point[0]},{topic.base_point[1]},{topic.publish_rate},{topic.data_size}\n")

    file.close()


# クライアントの初期位置の決定
def init_point(min_x, max_x, min_y, max_y):

    x = random.randint(min_x, max_x)
    y = random.randint(min_y, max_y)

    return x, y


def cal_distance(x1, y1, x2, y2):
    distance = math.sqrt(pow(x1-x2,2)+pow(y1-y2,2))

    return distance


def cal_delay(client1, client2, all_edge):
    delay = 0

    pub_edge = all_edge[client1.pub_edge_id]
    sub_edge = all_edge[client2.sub_edge_id]

    delay += cal_distance(client1.x, client2.y, pub_edge.x, pub_edge.y)*0.1

    delay += cal_distance(pub_edge.x, pub_edge.y, sub_edge.x, sub_edge.y)*0.1

    delay += cal_distance(sub_edge.x, sub_edge.y, client2.x, client2.y)*0.1

    return delay
