from assign import *
from generator import *
from animation import *
from solve import solve_near_edge


index_file = "../dataset/data/index/index1.csv"

create_index_file(index_file)

config_file = "../dataset/config/presen_config.csv"

traking_file = "../dataset/data/traking/test.csv"

generate_traking(index_file, config_file, traking_file)

edge_file = "../dataset/data/edge/edge.csv"

generate_edge(index_file, config_file, edge_file)

topic_file = "../dataset/data/topic/topic.csv"

generate_topic(index_file, config_file, topic_file)


"""
config_file = "../dataset/config/test.csv"
out_file_base = "../dataset/data/"

generate_number = 3

for n in range(1, generate_number+1):
    out_file = out_file_base + "data" + str(n) + ".csv"

    generate_traking(config_file, out_file)

    print(f"Date Generated : {n}/{generate_number}")


data_traking_file = "../dataset/data/data1.csv"
out_file_base = "../dataset/data/data1"

generate_number = 3

for n in range(1, generate_number+1):
    out_file = out_file_base + "_topic" + str(n) + ".csv"

    assignTopic(data_traking_file, out_file)

    print(f"Topic assigned : {n}/{generate_number}")


data_file_base = "../dataset/data/data1_topic"
out_file_base = "../dataset/animation/animation1_"

generate_number = 3

for n in range(1, generate_number+1):
    data_file = data_file_base + str(n) + ".csv"
    out_file = out_file_base + str(n) + ".gif"

    create_animation(data_file, out_file, 20)

    print(f"created animation : {n}/{generate_number}")
"""