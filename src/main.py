from generator import *
from animation import *
from util import *
from solve import solve_near_edge


index_file = "../dataset/data/index/readme.csv"
config_file = "../dataset/config/readme_config.csv"
traking_file = "../dataset/data/traking/readme_traking.csv"
assign_file = "../dataset/data/assign/readme_assgin.csv"
edge_file = "../dataset/data/edge/readme_edge.csv"
topic_file = "../dataset/data/topic/readme_edge.csv"
animation_file = "../dataset/animation/readme_animation.gif"

generate_traking(index_file, config_file, traking_file, seed=41176121)

#generate_edge(index_file, config_file, edge_file)

generate_topic(index_file, config_file, topic_file)

assignTopic(index_file, assign_file)

create_single_topic_animation(index_file, animation_file, 20)
