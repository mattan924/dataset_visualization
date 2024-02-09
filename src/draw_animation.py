from generator import *
from animation import *
from util import *


data_index_path = "../../reinforcement_learning/dataset/debug/debug/index/index_hard.csv"

solution_file = "../../reinforcement_learning/dataset/debug/debug/solution/solution_hard_opt.csv"

animation_path = "../../reinforcement_learning/result/save/master_thesis/animation_hard.gif"

create_opt_animation(data_index_path, animation_path, solution_file, FPS=20)
