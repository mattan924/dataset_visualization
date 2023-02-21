from generator import *
from animation import *
from util import *
from solve import solve_near_edge


index_file = "../../reinforcement_learning/dataset/learning_data/index/index_test.csv"
config_file = "../../reinforcement_learning/dataset/learning_data/config/config_test.csv"
traking_file = "../../reinforcement_learning/dataset/learning_data/traking/traking_test.csv"
assign_file = "../../reinforcement_learning/dataset/learning_data/assign/assign_test.csv"
edge_file = "../../reinforcement_learning/dataset/learning_data/edge/edge_test.csv"
topic_file = "../../reinforcement_learning/dataset/learning_data/topic/topic_test.csv"
animation_file = "../../reinforcement_learning/dataset/learning_data/animation/animation_test.gif"

generate_traking(index_file, config_file, traking_file)

generate_edge(index_file, config_file, edge_file)

generate_topic(index_file, config_file, topic_file)

assignTopic(index_file, assign_file)

create_single_topic_animation(index_file, animation_file, 20)


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