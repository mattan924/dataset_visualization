from assign import *
from generator import *
from animation import *
from solve import solve_near_edge


config_file = "../dataset/config/presen_config.csv"

out_file1 = "../dataset/data/test1.csv"

generate_traking(config_file, out_file1)

out_file2 = "../dataset/data/test1_topic1.csv"

assignTopic(out_file1, out_file2)

out_file3 = "../dataset/animation/test1.gif"

#create_animation(out_file2, out_file3, 20)

out_file4 = "../dataset/data/test1_topic1_solution1.csv"

solve_near_edge(out_file2, out_file4)

out_file5 = "../dataset/animation/test1_topic1_solution.gif"

create_animation_test(out_file4, out_file5, 20)


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