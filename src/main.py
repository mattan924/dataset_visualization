from generator import *
from animation import *
from util import *
from solve import solve_near_edge


index_file = "../dataset/data/index/test.csv"
config_file = "../dataset/config/test.csv"
traking_file = "../dataset/data/traking/test.csv"
assign_file = "../dataset/data/assign/test.csv"
edge_file = "../dataset/data/edge/test.csv"
topic_file = "../dataset/data/topic/test.csv"
animation_file1 = "../dataset/animation/traking.gif"
animation_file2 = "../dataset/animation/assign_traking.gif"

generate_traking(index_file, config_file, traking_file)

generate_edge(index_file, config_file, edge_file)

generate_topic(index_file, config_file, topic_file)

assignTopic(index_file, assign_file)

create_traking_animation(index_file, animation_file1, 20)

create_topic_animation(index_file, animation_file2, 20)


"""
index_file = "../../reinforcement/dataset/learning_data/index/index.csv"
config_file = "../../reinforcement/dataset/learning_data/config/config.csv"
traking_file = "../../reinforcement/dataset/learning_data/traking/traking.csv"
assign_file = "../../reinforcement/dataset/learning_data/assign/assign.csv"
edge_file = "../../reinforcement/dataset/learning_data/edge/edge.csv"
topic_file = "../../reinforcement/dataset/learning_data/topic/topic.csv"
animation_file = "../../reinforcement/dataset/learning_data/animation/animation.gif"


generate_traking(index_file, config_file, traking_file)

generate_edge(index_file, config_file, edge_file)

generate_topic(index_file, config_file, topic_file)

assignTopic(index_file, assign_file)

create_assign_animation(index_file, animation_file, 20)
"""