from generator import *
from animation import *
from util import *
from solve import solve_near_edge


index_file = "../dataset/data/index/readme.csv"
config_file = "../dataset/config/readme_config.csv"
traking_file = "../dataset/data/traking/test.csv"
assign_file = "../dataset/data/assign/test.csv"
edge_file = "../dataset/data/edge/test.csv"
topic_file = "../dataset/data/topic/test.csv"
animation_file = "../dataset/animation/test.gif"

generate_traking(index_file, config_file, traking_file, seed=41176121)

generate_edge(index_file, config_file, edge_file)

generate_topic(index_file, config_file, topic_file)

assign_topic(index_file, assign_file)

create_single_topic_animation(index_file, animation_file, 20)
