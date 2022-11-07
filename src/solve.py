from util import *

def cal_distance(x1, y1, x2, y2):
    distance = math.sqrt(pow(x1-x2,2)+pow(y1-y2,2))

    return distance


def solve_near_edge(data_file, out_file):

    config_file, all_edge, all_topic, data_set_topic, min_x, max_x, min_y, max_y, simulation_time, time_step, num_client, num_topic, num_edge, volume, cpu_power, save_period, speed = read_data_set_topic(data_file)

    with open(out_file, mode='w') as f:
        f.write(config_file + "\n")

    writeEdgeCSV(out_file, all_edge, num_topic)

    writeTopicCSV(out_file, all_topic)

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

            
            writeSolutionCSV(out_file, id, time, data.x, data.y, pub_edge, sub_edge, num_topic)