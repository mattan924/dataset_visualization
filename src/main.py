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
index_file_base = "../../reinforcement_learning/dataset/data_set/index/index"
config_file = "../../reinforcement_learning/dataset/data_set/config/config.csv"
traking_file_base = "../../reinforcement_learning/dataset/data_set/traking/traking"
assign_file_base = "../../reinforcement_learning/dataset/data_set/assign/assign"
edge_file_base = "../../reinforcement_learning/dataset/data_set/edge/edge"
topic_file_base = "../../reinforcement_learning/dataset/test_data_set/topic/topic"
animation_file_base = "../../reinforcement_learning/dataset/data_set/animation/animation"

dataset_size = 100


create_data_set(dataset_size, index_file_base, config_file, traking_file_base, assign_file_base, edge_file_base, topic_file_base)
"""


index_file = "../dataset/data/index/index_readme.csv"
config_file = "../dataset/data/config/config_readme.csv"
traking_file = "../dataset/data/traking/traking_readme.csv"
assign_file = "../dataset/data/assign/assign_readme.csv"
edge_file = "../dataset/data/edge/edge_readme.csv"
topic_file = "../dataset/data/topic/topic_readme.csv"
animation_file = "../dataset/data/animation/animation_readme.gif"

traking_animation_file = "../dataset/data/animation/traking_readme.gif"


# generate_traking(index_file, config_file, traking_file)

# generate_edge(index_file, config_file, edge_file)

# generate_topic(index_file, config_file, topic_file)

# assign_topic(index_file, assign_file)

# create_topic_animation(index_file, animation_file, 10)

create_traking_animation(index_file, traking_animation_file, 10)
