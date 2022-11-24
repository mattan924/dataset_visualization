from generator import *
from animation import *
from util import *
from solve import solve_near_edge


index_file = "../dataset/data/index/readme.csv"
config_file = "../dataset/config/readme_config.csv"
traking_file = "../dataset/data/traking/readme_traking.csv"
edge_file = "../dataset/data/edge/readme_edge.csv"
animation_file = "../dataset/animation/readme_animation.gif"


generate_traking(index_file, config_file, traking_file)

generate_edge(index_file, config_file, edge_file)

create_traking_animation(index_file, animation_file, 20)


"""
generate_num = 10

index_file = "../dataset/data/index/system_presen"

config_file = "../dataset/config/system_presen.csv"

traking_file = "../dataset/data/traking/system_presen_traking"

edge_file = "../dataset/data/edge/system_presen_edge"

topic_file = "../dataset/data/topic/system_presen_topic"

assign_file = "../dataset/data/assign/system_presen_assign"

solve_file = "../dataset/data/solved/system_presen_solve"

animation_file = "../dataset/animation/system_presen_animation"


for i in range(1, generate_num+1):
    index_file_tmp = index_file + str(i) + ".csv"
    create_index_file(index_file_tmp, config_file)

    generate_traking(index_file_tmp, config_file, traking_file + str(i) + ".csv")

    generate_edge(index_file_tmp, config_file, edge_file + str(i) + ".csv")

    generate_topic(index_file_tmp, config_file, topic_file + str(i) + ".csv")

    assignTopic(index_file_tmp, assign_file + str(i) + ".csv")

    solve_near_edge(index_file_tmp, solve_file + str(i) + ".csv")

    create_animation_single_topic(index_file_tmp, animation_file + str(i) + ".gif", 20)

    print(f"{i}/{generate_num} created.")
"""
