from generator import *
from animation import *
from util import *


def create_data_set(data_set_size, index_file_base, config_file, traking_file_base, assign_file_base, edge_file_base, topic_file_base, animation_file_base=None):
    for i in range(data_set_size):
        index_file = index_file_base + "_" + str(i) + ".csv"
        traking_file = traking_file_base + "_" + str(i) + ".csv"
        assign_file = assign_file_base + "_" + str(i) + ".csv"
        edge_file = edge_file_base + "_" + str(i) + ".csv"
        topic_file = topic_file_base + "_" + str(i) + ".csv"

        generate_traking(index_file, config_file, traking_file)

        generate_edge(index_file, config_file, edge_file)

        generate_topic(index_file, config_file, topic_file)

        assign_topic(index_file, assign_file)

        if animation_file_base != None:
            animation_file = animation_file_base + "_" + str(i) + ".gif"
            create_topic_animation(index_file, animation_file, 20)

        print(f"data_set is created {(i / data_set_size)*100}%")


"""
index_file_base = "../../reinforcement_learning/dataset/data_set_hard/index/index"
config_file = "../../reinforcement_learning/dataset/data_set_hard/config/config.csv"
traking_file_base = "../../reinforcement_learning/dataset/data_set_hard/traking/traking"
assign_file_base = "../../reinforcement_learning/dataset/data_set_hard/assign/assign"
edge_file_base = "../../reinforcement_learning/dataset/data_set_hard/edge/edge"
topic_file_base = "../../reinforcement_learning/dataset/test_data_set_hard/topic/topic"
animation_file_base = "../../reinforcement_learning/dataset/data_set_hard/animation/animation"

dataset_size = 1000

create_data_set(dataset_size, index_file_base, config_file, traking_file_base, assign_file_base, edge_file_base, topic_file_base)
"""



index_file = "../../reinforcement_learning/dataset/learning_data/index/index_multi2.csv"
config_file = "../../reinforcement_learning/dataset/test_data_set_hard/config/config.csv"
traking_file = "../../reinforcement_learning/dataset/test_data_set_hard/traking/traking_0.csv"
assign_file = "../../reinforcement_learning/dataset/test_data_set_hard/assign/assign_0.csv"
edge_file = "../../reinforcement_learning/dataset/test_data_set_hard/edge/edge_0.csv"
topic_file = "../../reinforcement_learning/dataset/test_data_set_hard/topic/topic_0.csv"
animation_file = "../../reinforcement_learning/dataset/learning_data/animation/animation_multi2.gif"

#generate_traking(index_file, config_file, traking_file)

#generate_edge(index_file, config_file, edge_file)

#generate_topic(index_file, config_file, topic_file)

#assign_topic(index_file, assign_file)

create_topic_animation(index_file, animation_file, 10)
