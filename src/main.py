from generator import *
from animation import *
from util import *
from solve import solve_near_edge


index_file = "../dataset/data/index/system_presen2.csv"
config_file = "../dataset/config/system_presen2.csv"
traking_file = "../dataset/data/traking/system_presen_traking.csv"
assign_file = "../dataset/data/assign/system_presen_assign.csv"
edge_file = "../dataset/data/edge/system_presen_edge.csv"
topic_file = "../dataset/data/topic/system_presen_topic.csv"
animation_file = "../dataset/animation/system_presen_multitopic.gif"


generate_traking(index_file, config_file, traking_file)

generate_edge(index_file, config_file, edge_file)

generate_topic(index_file, config_file, topic_file)

assignTopic(index_file, assign_file)

create_animation(index_file, animation_file, 20)
