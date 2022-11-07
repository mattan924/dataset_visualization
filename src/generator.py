from util import *
from client import Client_traking
from edge import Edge
import random


def generate_traking(config_file, out_file, seed=0):
    if seed != 0:
        random.seed(seed)
    else:
        seed = random.randint(1, 100000000)
        random.seed(seed)
    
    min_x, max_x, min_y, max_y, simulation_time, time_step, num_client, num_topic, num_edge, volume, cpu_power, save_period, speed = read_config(config_file)

    with open(out_file, mode='w') as f:
        f.write(config_file + "," + str(seed) + "\n")

    # クライアントの生成
    all_client = []

    for id in range(num_client):
        # 各クライアントの初期位置の決定
        init_x, init_y = init_point(min_x, max_x, min_y, max_y)

        c = Client_traking(id, init_x, init_y, speed)

        all_client.append(c)

    # エッジサーバの生成
    all_edge = []

    # 今はエッジの数を3×3で固定している。改修ポイント
    for i in range(3):
        for j in range(3):
            id = i*3+j
            x = 2 + 4*j
            y = 2 + 4*i
            all_edge.append(Edge(id, x, y, volume, cpu_power, num_topic))
    
    writeEdgeCSV(out_file, all_edge, num_topic)

    # データの生成および書き込み
    for time in range(0, simulation_time, time_step):
        for c in all_client:

            x, y = c.random_walk(time_step, min_x, max_x, min_y, max_y)

            writeTrakingCSV(out_file, Data_traking(c.id, time, x, y))
