from client import Client_topic
from util import *
from topic import Topic
import random


def assignTopic(data_traking_file, out_file, seed=0):
    if seed != 0:
        random.seed(seed)
    else:
        seed = random.randint(1, 100000000)
        random.seed(seed)
    
    config_file, all_edge, data_set_traking = read_data_set_traking(data_traking_file)

    min_x, max_x, min_y, max_y, simulation_time, time_step, num_client, num_topic, num_edge, volume, cpu_power, save_period, speed = read_config(config_file)

    with open(out_file, mode='w') as f:
        f.write(config_file + "," + str(seed) + "\n")

    writeEdgeCSV(out_file, all_edge, num_topic)

    all_topic = []
    all_client = []

    # トピックの生成
    for i in range(num_topic):
        all_topic.append(Topic(id=i, role=i, save_period=save_period, min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y))

    writeTopicCSV(out_file, all_topic)

    for i in range(num_client):
        data_traking = data_set_traking.pop(0)

        init_topic = []

        for t in all_topic:
            if t.init_topic(data_traking.x, data_traking.y):
                init_topic.append(t.id)

        c_topic = Client_topic(data_traking.id, data_traking.x, data_traking.y, init_topic)

        all_client.append(c_topic)

        writeAssginCSV(out_file, Data_topic(c_topic.id, 0, c_topic.x, c_topic.y, init_topic))


    for time in range(time_step, simulation_time, time_step):
        for t in all_topic:
            if t.role == 2:
                t.decide_random_point(min_x, max_x, min_y, max_y, time_step)

        for c in all_client:
            data_traking = data_set_traking.pop(0)

            c.x = data_traking.x
            c.y = data_traking.y

            c.select_topic(all_topic)

            writeAssginCSV(out_file, Data_topic(c.id, time, c.x, c.y, c.topic))
