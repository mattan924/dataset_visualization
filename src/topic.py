from abc import ABCMeta
from abc import abstractclassmethod
import math
import random
import sys
import queue


class Topic(metaclass = ABCMeta):

    def __init__(self, id, save_period, publish_rate, data_size, require_cycle):
        self.id = id
        self.save_period = save_period

        if publish_rate == None:
            self.publish_rate = random.randint(10, 1000) / 100
        else:
            self.publish_rate = publish_rate

        if data_size == None:
            self.data_size = random.randint(1, 256) # 1~256 MB (MQTTの最大データサイズ)
        else:
            self.data_size = data_size

        if require_cycle == None:
            self.require_cycle = random.randint(1e4, 1e5)
        else:
            self.require_cycle = require_cycle


    @abstractclassmethod
    def init_topic(self, x, y):
        pass


class Topic_uniform(Topic):

    def __init__(self, id, save_period, publish_rate=None, data_size=None, require_cycle=None):
        super().__init__(id, save_period, publish_rate, data_size, require_cycle)
        self.role = 0


    def init_topic(self, x, y):
        if random.uniform(0, 100) < 33:
            return True
        else:
            return False


class Topic_local(Topic):

    def __init__(self, id, save_period, publish_rate=None, data_size=None, require_cycle=None, base_point=None, min_x=0, max_x=12, min_y=0, max_y=12):
        super().__init__(id, save_period, publish_rate, data_size, require_cycle)
        self.role = 1
        self.threshold = 4

        if base_point == None:
            self.base_point = (random.uniform(min_x, max_x), random.uniform(min_y, max_y))
        else:
            self.base_point = base_point

    
    def init_topic(self, x, y):
        distance = math.sqrt(pow(x - self.base_point[0], 2) + pow(y - self.base_point[1], 2))

        if distance < self.threshold:
            return True
        else:
            return False


class Topic_incident(Topic):

    def __init__(self, id, save_period, publish_rate=None, data_size=None, require_cycle=None):
        super().__init__(id, save_period, publish_rate, data_size, require_cycle)
        self.role = 2
        self.random_point = []

    
    def init_topic(self, x, y):
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


class Point:

    def __init__(self, x, y, threshold, time):
        self.x = x
        self.y = y
        self.threshold = threshold
        self.time = time


    def time_advance(self, advance_time):
        self.time = self.time - advance_time


    def cal_rank(self, x, y):
        distance = math.sqrt(pow(x - self.x, 2) + pow(y - self.y, 2))
        
        if distance < self.threshold:
            return 0
        else:
            return 1
