from abc import ABCMeta
from abc import abstractclassmethod
import math
import random

#  Topic クラスの抽象クラス
class Topic(metaclass = ABCMeta):

    def __init__(self, id, save_period, publish_rate, data_size, require_cycle):
        self.id = id
        self.save_period = save_period

        if publish_rate == None:
            self.publish_rate = random.randint(500, 1000) / 100
        else:
            self.publish_rate = publish_rate

        if data_size == None:
            self.data_size = (256*random.randint(1, 5)) / 1e6 # 1~256 MB (MQTTの最大データサイズ) TB への変換
        else:
            self.data_size = data_size

        if require_cycle == None:
            self.require_cycle = random.randint(5e6, 1e7) / 1e9
        else:
            self.require_cycle = require_cycle


    @abstractclassmethod
    def init_topic(self, x, y):
        pass


    @abstractclassmethod
    def update(self, min_x, max_x, min_y, max_y, time_step):
        pass


#  一様分布の topic クラス
class TopicUniform(Topic):

    def __init__(self, id, save_period, publish_rate=None, data_size=None, require_cycle=None):
        super().__init__(id, save_period, publish_rate, data_size, require_cycle)
        self.role = 0


    def init_topic(self, x, y):
        if random.uniform(0, 100) < 40:
            return True
        else:
            return False
        
    
    def update(self, min_x, max_x, min_y, max_y, time_step):
        pass


#  局所的に分布する topic クラス
class TopicLocal(Topic):

    def __init__(self, id, save_period, radius, publish_rate=None, data_size=None, require_cycle=None, base_point=None, min_x=0, max_x=12, min_y=0, max_y=12):
        super().__init__(id, save_period, publish_rate, data_size, require_cycle)
        self.role = 1
        #  局所的な領域の半径(km)
        self.radius = radius

        #  base_point: 局所的な領域の中心座標
        if base_point == None:
            self.base_point = (random.uniform(min_x, max_x), random.uniform(min_y, max_y))
        else:
            self.base_point = base_point

    
    def init_topic(self, x, y):
        distance = math.sqrt(pow(x - self.base_point[0], 2) + pow(y - self.base_point[1], 2))

        #  (x, y) が領域の内部にいるかの判定+
        if distance < self.radius:
            return True
        else:
            return False
        
    
    def update(self, min_x, max_x, min_y, max_y, time_step):
        pass
        

#  突発的に発生する topic クラス
class TopicIncident(Topic):

    def __init__(self, id, save_period, radius, time_limit, publish_rate=None, data_size=None, require_cycle=None):
        super().__init__(id, save_period, publish_rate, data_size, require_cycle)
        self.role = 2
        self.radius = radius
        self.time_limit = time_limit
        #  突発的な領域の中心座標のリスト
        self.random_point = []

    
    def init_topic(self, x, y):
        return False
    

    #  領域を更新するメソッド
    def decide_random_point(self, min_x, max_x, min_y, max_y, time_step):
        #  既存の領域のカウントを進める
        for point in self.random_point:
            point.time_advance(time_step)

        #  新規に領域を生成するかどうか
        if random.uniform(0, 100) < 1:
            x = random.uniform(min_x, max_x)
            y = random.uniform(min_y, max_y)

            point = Point(x, y, self.radius, self.time_limit)

            self.random_point.append(point)

        #  領域のカウントが0以下になったら該当領域を削除
        for i in reversed(range(len(self.random_point))):
            if self.random_point[i].time <= 0:
                del self.random_point[i]


    def update(self, min_x, max_x, min_y, max_y, time_step):
        self.decide_random_point(min_x, max_x, min_y, max_y, time_step)


#  制限時間付き領域用のクラス
class Point:

    def __init__(self, x, y, radius, time):
        #  領域に中心座標
        self.x = x
        self.y = y
        #  領域の半径
        self.radius = radius
        #  領域の残り時間
        self.time = time


    #  カウントダウンを進める
    def time_advance(self, advance_time):
        self.time = self.time - advance_time


    #  領域の範囲内にいるかどうかのチェック
    def check_area(self, x, y):
        distance = math.sqrt(pow(x - self.x, 2) + pow(y - self.y, 2))
        
        if distance < self.radius:
            return True
        else:
            return False
