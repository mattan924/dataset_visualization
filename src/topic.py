import math
import random
import sys
import queue


def cal_distance(x1, y1, x2, y2):
    distance = math.sqrt(pow(x1-x2,2)+pow(y1-y2,2))

    return distance

class Topic:
    
    def __init__(self, id, role, min_x, max_x, min_y, max_y, save_period):
        self.id = id
        self.role = role
        self.base_point = self.decide_base_point(min_x, max_x, min_y, max_y)
        self.random_point = []
        self.threshold = [4]
        self.publish_rate = random.randint(20, 200) / 100
        self.data_size = random.randint(1, 256) # 1~256MB (MQTTの最大データサイズ)
        self.num_client_queue = queue.Queue()
        self.total_num_client = 0
        self.save_period = save_period
        self.volume = 0


    def decide_base_point(self, min_x, max_x, min_y, max_y):
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)

        return (x, y)


    def cal_rank(self, x, y):
        distance = cal_distance(x, y, self.base_point[0], self.base_point[1])
        if distance < self.threshold[0]:
            return 0
        else:
            return 1


    # 初期の topic を決定する
    # role : 初期化の方法
    # role = 0 : ランダム
    def init_topic(self, x, y):

        if self.role == 0:
            if random.uniform(0, 100) < 33:
                return True
        elif self.role == 1:
            rank = self.cal_rank(x, y)
            if rank == 0:
                return True
        else:
            return False


    def decide_random_point(self, min_x, max_x, min_y, max_y, time_step):
        for point in self.random_point:
            point.time_advance(time_step)

        if random.uniform(0, 100) < 1:
            time_limit = 60
            x = random.uniform(min_x, max_x)
            y = random.uniform(min_y, max_y)

            point = Point(x, y, 4, time_limit)

            self.random_point.append(point)
        
        for i in reversed(range(len(self.random_point))):
            if self.random_point[i].time <= 0:
                del self.random_point[i]

    
    def cal_volume(self, time_step):
        self.volume = self.data_size*self.publish_rate*time_step*self.total_num_client

    
    def update_client(self, new_num_client, time_step):
        if self.num_client_queue.qsize() < self.save_period/time_step:
            self.num_client_queue.put(new_num_client)
            self.total_num_client = self.total_num_client + new_num_client
        elif self.num_client_queue.qsize() == self.save_period/time_step:
            old_num_client = self.num_client_queue.get()
            self.num_client_queue.put(new_num_client)
            self.total_num_client = self.total_num_client + new_num_client - old_num_client
        else:
            sys.exit("save_periodがtime_stepの正数倍になっていません")

class Point:

    def __init__(self, x, y, threshold, time):
        self.x = x
        self.y = y
        self.threshold = threshold
        self.time = time

    def time_advance(self, advance_time):
        self.time = self.time - advance_time

    def cal_rank(self, x, y):
        distance = cal_distance(x, y, self.x, self.y)
        
        if distance < self.threshold:
            return 0
        else:
            return 1