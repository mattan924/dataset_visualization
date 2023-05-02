from generator import *
from animation import *
from util import *
from solve import solve_near_edge


index_file = "../../reinforcement_learning/dataset/learning_data/index/index_multi2.csv"
config_file = "../../reinforcement_learning/dataset/learning_data/config/config_multi.csv"
traking_file = "../../reinforcement_learning/dataset/learning_data/traking/traking_multi2.csv"
assign_file = "../../reinforcement_learning/dataset/learning_data/assign/assign_multi2.csv"
edge_file = "../../reinforcement_learning/dataset/learning_data/edge/edge_multi2.csv"
topic_file = "../../reinforcement_learning/dataset/learning_data/topic/topic_multi2.csv"
animation_file = "../../reinforcement_learning/dataset/learning_data/animation/animation_multi2.gif"

generate_traking(index_file, config_file, traking_file)

generate_edge(index_file, config_file, edge_file)

generate_topic(index_file, config_file, topic_file)

assign_topic(index_file, assign_file)

create_topic_animation(index_file, animation_file, 20)
