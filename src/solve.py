import util
import math
import pandas as pd

def cal_distance(x1, y1, x2, y2):
    distance = math.sqrt(pow(x1-x2,2)+pow(y1-y2,2))

    return distance


def solve_near_edge(index_file, out_file):
    df_index = pd.read_csv(index_file, index_col=0)

    data_file = df_index.at['data', 'assign_file']
    config_file = df_index.at['data', 'config_file']
    edge_file = df_index.at['data', 'edge_file']

    df_index.at['data', 'solve_file'] = out_file

    df_index.to_csv(index_file)

    data_set_topic = util.read_data_set_topic(data_file)
    parameter = util.read_config(config_file)

    simulation_time = parameter['simulation_time']
    time_step = parameter['time_step']
    num_client = parameter['num_client']
    num_topic = parameter['num_topic']

    f = open(out_file, mode="w")
    f.close()

    all_edge = util.read_edge(edge_file)

    # 最も近いエッジを解とするとき
    for time in range(0, simulation_time, time_step):
        for id in range(num_client):
            data = data_set_topic.pop(0)

            min_distance = 10000000
            min_id = -1
            for edge in all_edge:
                distance = cal_distance(data.x, data.y, edge.x, edge.y)

                if distance < min_distance:
                    min_distance = distance
                    min_id = edge.id

            pub_edge = []
            sub_edge = []
            for t in range(num_topic):
                if data.topic_list.count(t) == 0:
                    pub_edge.append(-1)
                    sub_edge.append(-1)
                else:
                    pub_edge.append(min_id)
                    sub_edge.append(min_id)

            util.writeSolutionCSV(out_file, id, time, data.x, data.y, pub_edge, sub_edge, num_topic)