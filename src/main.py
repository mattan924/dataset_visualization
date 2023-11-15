from generator import *
from animation import *
from util import *
import random
import pandas
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


def create_similar_dataset(traking_data_size, assign_data_size, edge_data_size, topic_data_size, train_dir, test_dir, file_base, test_data_size):
    generate_data_size = traking_data_size*assign_data_size*edge_data_size*topic_data_size
    seed_base = random.randint(1, 1000000)

    config_file = train_dir + "config/" + file_base + ".csv"
    index_file_base = train_dir + "index/" + file_base
    traking_file_base = train_dir + "traking/" + file_base
    edge_file_base = train_dir + "edge/" + file_base
    topic_file_base = train_dir + "topic/" + file_base
    assign_file_base = train_dir + "assign/" + file_base

    count = 0
    index_file_list = []
    for traking_num in range(traking_data_size):
        for assign_num in range(assign_data_size):
            for edge_num in range(edge_data_size):
                for topic_num in range(topic_data_size):
                    index_file = index_file_base + "_traking" + str(traking_num) + "_assign" + str(assign_num) + "_edge" + str(edge_num) + "_topic" + str(topic_num) + ".csv"
                    create_index_file(index_file, config_file)
                    index_file_list.append(index_file)

                    traking_file = traking_file_base + str(traking_num) + "_assign" + str(assign_num) + "_edge" + str(edge_num) + "_topic" + str(topic_num) + ".csv"
                    generate_traking(index_file, config_file, traking_file, seed=seed_base+traking_num)

                    edge_file = edge_file_base + str(edge_num) + "_traking" + str(traking_num) + "_assign" + str(assign_num) + "_topic" + str(topic_num) + ".csv"
                    generate_edge(index_file, config_file, edge_file, seed=seed_base+edge_num)

                    topic_file = topic_file_base + str(topic_num) + "_traking" + str(traking_num) + "_assign" + str(assign_num) + "_edge" + str(edge_num) + ".csv"
                    generate_topic(index_file, config_file, topic_file, seed=seed_base+topic_num)

                    assign_file = assign_file_base + str(assign_num) + "_traking" + str(traking_num) + "_edge" + str(edge_num) + "_topic" + str(topic_num) + ".csv"
                    assign_topic(index_file, assign_file, seed=seed_base+assign_num)

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


train_dir = "../../reinforcement_learning/dataset/similar_dataset/easy/small15_select/train/"
test_dir = "../../reinforcement_learning/dataset/similar_dataset/easy/small15_select/test/"

file_base = "hight_load"

create_similar_dataset(5, 5, 1, 1, train_dir, test_dir, file_base, 10)

#dataset_size = 10
#create_data_set(dataset_size, index_file_base, config_file, traking_file_base, assign_file_base, edge_file_base, topic_file_base)



# index_file = "../dataset/data/index/index_readme.csv"
# config_file = "../dataset/data/config/config_readme.csv"
# traking_file = "../dataset/data/traking/traking_readme.csv"
# assign_file = "../dataset/data/assign/assign_readme.csv"
# edge_file = "../dataset/data/edge/edge_readme.csv"
# topic_file = "../dataset/data/topic/topic_readme.csv"
# animation_file = "../dataset/data/animation/animation_readme.gif"

# traking_animation_file = "../dataset/data/animation/traking_readme.gif"


# generate_traking(index_file, config_file, traking_file)

# generate_edge(index_file, config_file, edge_file)

# generate_topic(index_file, config_file, topic_file)

# assign_topic(index_file, assign_file)

# create_topic_animation(index_file, animation_file, 10)

# create_traking_animation(index_file, traking_animation_file, 10)
