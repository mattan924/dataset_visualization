from generator import *
from animation import *
from util import *
from solve import solve_near_edge


def create_data_set(data_set_size, index_file_base, config_file, traking_file_base, assign_file_base, edge_file_base, topic_file_base):
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

        print(f"data_set is created {(i / data_set_size)*100}%")


index_file_base = "../../reinforcement_learning/dataset/pretrain_data_set/index/index"
config_file = "../../reinforcement_learning/dataset/pretrain_data_set/config/config.csv"
traking_file_base = "../../reinforcement_learning/dataset/pretrain_data_set/traking/traking"
assign_file_base = "../../reinforcement_learning/dataset/pretrain_data_set/assign/assign"
edge_file_base = "../../reinforcement_learning/dataset/pretrain_data_set/edge/edge"
topic_file_base = "../../reinforcement_learning/dataset/pretrain_data_set/topic/topic"

dataset_size = 100

create_data_set(dataset_size, index_file_base, config_file, traking_file_base, assign_file_base, edge_file_base, topic_file_base)