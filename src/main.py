from generator import *
from animation import *
from util import *
import random
import pandas as pd
import os


def create_data_set(data_set_size, index_file_base, config_file, traking_file_base, assign_file_base, edge_file_base, topic_file_base, animation_file_base=None):
    for i in range(data_set_size):
        index_file = index_file_base + "_" + str(i) + ".csv"
        traking_file = traking_file_base + "_" + str(i) + ".csv"
        assign_file = assign_file_base + "_" + str(i) + ".csv"
        edge_file = edge_file_base + "_" + str(i) + ".csv"
        topic_file = topic_file_base + "_" + str(i) + ".csv"

        generate_traking(index_file, config_file, traking_file, seed=0)

        generate_edge(index_file, config_file, edge_file, seed=0)

        generate_topic(index_file, config_file, topic_file, seed=0)

        assign_topic(index_file, assign_file, seed=0)

        if animation_file_base != None:
            animation_file = animation_file_base + "_" + str(i) + ".gif"
            create_topic_animation(index_file, animation_file, 20)

        print(f"data_set is created {(i / data_set_size)*100}%")


def create_similar_dataset(traking_data_size, assign_data_size, edge_data_size, topic_data_size, train_dir, test_dir, file_base, test_data_size, num_publisher=None):
    generate_data_size = traking_data_size*assign_data_size*edge_data_size*topic_data_size
    seed_base = random.randint(1, 1000000)

    config_file = train_dir + "config/" + file_base + ".csv"
    index_file_base = train_dir + "index/" + file_base
    traking_file_base = train_dir + "traking/" + file_base
    edge_file_base = train_dir + "edge/" + file_base
    topic_file_base = train_dir + "topic/" + file_base
    assign_file_base = train_dir + "assign/" + file_base

    parameter = util.read_config(config_file)
    num_topic = parameter['num_topic']
    num_edge = parameter['num_edge']
    edge_max_cycle = float(parameter['cpu_cycle'])
    max_volume = float(parameter['volume'])

    count = 0
    index_file_list = []
    topic_seed_list = []

    for topic_num in range(topic_data_size):
        index_file = index_file_base + "_tmp.csv"
        create_index_file(index_file, config_file)
        topic_file = topic_file_base + "_tmp.csv"

        while(True):
            topic_seed = random.randint(1, 1000000)
            generate_topic(index_file, config_file, topic_file, seed=topic_seed)

            all_topic = util.read_topic(topic_file)

            sum_edge_cycle = 0
            sum_total_cycle = 0
            sum_volume = 0

            flag = True
            print(f"start")

            for topic in all_topic:
                edge_cycle = topic.publish_rate * (num_publisher / (num_topic * num_edge)) * topic.require_cycle * math.log(topic.publish_rate * topic.save_period * (num_publisher / num_topic))
                total_cycle = topic.publish_rate * (num_publisher / num_topic) * topic.require_cycle * math.log(topic.publish_rate * topic.save_period * (num_publisher / num_topic))

                volume = topic.publish_rate * topic.save_period * (num_publisher / num_topic) * topic.data_size

                if volume >= max_volume:
                    flag = False
                    print(f"break")
                    break

                print(f"edge_cycle = {edge_cycle}, total_cycle = {total_cycle}, volume = {volume}")
                sum_edge_cycle += edge_cycle
                sum_total_cycle += total_cycle
                sum_volume += volume

            if flag:
                if sum_total_cycle < edge_max_cycle:
                    print(f"sum: {sum_edge_cycle}, {sum_total_cycle}, {sum_volume}")

                    print(f"{topic_num}/{topic_data_size}: generate data\n generate next data?\n input y:yes or n:not")
                    input_str = input()

                    if input_str == 'y':
                        topic_seed_list.append(topic_seed)
                        break
                    elif input_str == 'n':
                        print(f"you input n: regenerate data")
                    else:
                        sys.exit(f"error")

    os.remove(index_file_base + "_tmp.csv")
    os.remove(topic_file_base + "_tmp.csv")
    
    for traking_num in range(traking_data_size):
        for assign_num in range(assign_data_size):
            for edge_num in range(edge_data_size):
                for topic_num in range(topic_data_size):
                    index_file = index_file_base + "_traking" + str(traking_num) + "_assign" + str(assign_num) + "_edge" + str(edge_num) + "_topic" + str(topic_num) + ".csv"
                    create_index_file(index_file, config_file)
                    index_file_list.append(index_file)

                    topic_file = topic_file_base + str(topic_num) + "_traking" + str(traking_num) + "_assign" + str(assign_num) + "_edge" + str(edge_num) + ".csv"
                    generate_topic(index_file, config_file, topic_file, seed=topic_seed_list[topic_num])

                    edge_file = edge_file_base + str(edge_num) + "_traking" + str(traking_num) + "_assign" + str(assign_num) + "_topic" + str(topic_num) + ".csv"
                    generate_edge(index_file, config_file, edge_file, seed=seed_base+edge_num)

                    traking_file = traking_file_base + str(traking_num) + "_assign" + str(assign_num) + "_edge" + str(edge_num) + "_topic" + str(topic_num) + ".csv"
                    generate_traking(index_file, config_file, traking_file, seed=seed_base+traking_num)

                    assign_file = assign_file_base + str(assign_num) + "_traking" + str(traking_num) + "_edge" + str(edge_num) + "_topic" + str(topic_num) + ".csv"
                    assign_topic(index_file, assign_file, num_publisher=num_publisher, seed=seed_base+assign_num)

                    count += 1
                    print(f"data_set is created {(count / generate_data_size)*100}%")

    count = 0
    test_index_list = random.sample(index_file_list, test_data_size)
    for idx in range(len(test_index_list)):
        index_file_path = test_index_list[idx]
        df_index = pd.read_csv(index_file_path, index_col=0, dtype=str)
        old_index_file = index_file_path.split("/")[-1]

        old_traking_file_path = df_index.at['data', 'traking_file']
        old_edge_file_path = df_index.at['data', 'edge_file']
        old_topic_file_path = df_index.at['data', 'topic_file']
        old_assign_file_path = df_index.at['data', 'assign_file']
        old_config_file_path = df_index.at['data', 'config_file']

        old_traking_file = old_traking_file_path.split("/")[-1]
        old_edge_file = old_edge_file_path.split("/")[-1]
        old_topic_file = old_topic_file_path.split("/")[-1]
        old_assign_file = old_assign_file_path.split("/")[-1]
        old_config_file = old_config_file_path.split("/")[-1]

        new_index_file_path = test_dir + "index/" + old_index_file
        new_traking_file_path = test_dir + "traking/" + old_traking_file
        new_edge_file_path = test_dir + "edge/" + old_edge_file
        new_topic_file_path = test_dir + "topic/" + old_topic_file
        new_assign_file_path = test_dir + "assign/" + old_assign_file
        new_config_file_path = test_dir + "config/" + old_config_file

        df_index.at['data', 'traking_file'] = new_traking_file_path
        df_index.at['data', 'edge_file'] = new_edge_file_path
        df_index.at['data', 'topic_file'] = new_topic_file_path
        df_index.at['data', 'assign_file'] = new_assign_file_path
        df_index.at['data', 'config_file'] = new_config_file_path

        df_index.to_csv(index_file_path)

        os.rename(index_file_path, new_index_file_path)
        os.rename(old_traking_file_path, new_traking_file_path)
        os.rename(old_edge_file_path, new_edge_file_path)
        os.rename(old_topic_file_path, new_topic_file_path)
        os.rename(old_assign_file_path, new_assign_file_path)

        count += 1
        print(f"{(count / test_data_size)*100} data is move to test dir")




train_dir = "../../reinforcement_learning/dataset/master_thesis/multi_data/general_evaluation/low_capacity_high_cycle_client40_fix40_data10000/train/"
test_dir = "../../reinforcement_learning/dataset/master_thesis/multi_data/general_evaluation/low_capacity_high_cycle_client40_fix40_data10000/test/"

file_base = "data_fix"

create_similar_dataset(50, 40, 1, 5, train_dir, test_dir, file_base, test_data_size=10, num_publisher=40)



"""
num_publisher = 100
num_data = 100

base_path = "../../reinforcement_learning/dataset/master_thesis/single_data/"

file_name_base = "mat_time_client" + str(num_publisher) + "_fix" + str(num_publisher)

config_file = base_path + "config/" + file_name_base + ".csv"

parameter = util.read_config(config_file)
num_topic = parameter['num_topic']
num_edge = parameter['num_edge']

for data_idx in range(num_data):

    file_name = file_name_base + "_" + str(data_idx) + ".csv"

    index_file = base_path + "index/" + file_name_base + "_" + str(data_idx) + ".csv"
    traking_file = base_path + "traking/" + file_name_base + "_" + str(data_idx) + ".csv"
    assign_file = base_path + "assign/" + file_name_base + "_" + str(data_idx) + ".csv"
    edge_file = base_path + "edge/" + file_name_base + "_" + str(data_idx) + ".csv"
    topic_file = base_path + "topic/" + file_name_base + "_" + str(data_idx) + ".csv"

    create_index_file(index_file, config_file)

    if data_idx == 0:
        while(True):
            topic_seed = random.randint(1, 1000000)
            generate_topic(index_file, config_file, topic_file, seed=topic_seed)

            all_topic = util.read_topic(topic_file)

            sum_edge_cycle = 0
            sum_total_cycle = 0
            sum_volume = 0
            for topic in all_topic:
                edge_cycle = topic.publish_rate * (num_publisher / (num_topic * num_edge)) * topic.require_cycle * math.log(topic.publish_rate * topic.save_period * (num_publisher / num_topic))
                total_cycle = topic.publish_rate * (num_publisher / num_topic) * topic.require_cycle * math.log(topic.publish_rate * topic.save_period * (num_publisher / num_topic))

                volume = topic.publish_rate * topic.save_period * (num_publisher / num_topic) * topic.data_size

                print(f"edge_cycle = {edge_cycle}, total_cycle = {total_cycle}, volume = {volume}")
                sum_edge_cycle += edge_cycle
                sum_total_cycle += total_cycle
                sum_volume += volume
                                
            print(f"sum: {sum_edge_cycle}, {sum_total_cycle}, {sum_volume}")

            print(f"generate continue?\n input y:yes, continue. or n:not, regenerate data")
            input_str = input()

            if input_str == 'y':
                break
            elif input_str == 'n':
                print(f"you input n: regenerate data")
            else:
                sys.exit(f"error")

    generate_topic(index_file, config_file, topic_file, seed=topic_seed)

    generate_edge(index_file, config_file, edge_file)

    generate_traking(index_file, config_file, traking_file)

    assign_topic(index_file, assign_file, num_publisher=num_publisher)

    print(f"{(data_idx/num_data)*100} % complete")
"""