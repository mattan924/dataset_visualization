import random
import math
import numpy as np
import sys


class Client_traking:
    
    def __init__(self, id, x, y, speed):
        self.id = id
        self.x = x
        self.y = y
        self.direction = random.uniform(0, 360)
        self.speed = speed


    # time_step : 何秒後の位置を求めるか
    def random_walk(self, time_step, min_x, max_x, min_y, max_y):
        speed = random.gauss(self.speed, 10)

        tmp = random.uniform(0, 100)

        # 進行方向の決定
        if tmp <= 98.5:
            self.direction = random.gauss(self.direction, 1)
        elif tmp <= 99.25:
            self.direction = random.gauss(self.direction - 90, 1)
        elif tmp <= 99.99:
            self.direction = random.gauss(self.direction + 90, 1)
        else:
            self.direction = random.gauss(self.direction + 180, 1)

        if self.direction >= 360:
            self.direction = self.direction%360
        elif self.direction < 0:
            self.direction = 360 - (0 - self.direction)%360

        # 位置の更新
        self.x = self.x + ((speed/3600)*time_step)*math.cos(math.radians(self.direction))
        self.y = self.y + ((speed/3600)*time_step)*math.sin(math.radians(self.direction))

        # 領域外に出ないように調整
        if self.x > max_x:
            self.x = max_x
        elif self.x < min_x:
            self.x = min_x

        if self.y > max_y:
            self.y = max_y
        elif self.y < min_y:
            self.y = min_y

        return self.x, self.y


class Client_topic:
    
    def __init__(self, id, x, y, init_topic):
        self.id = id
        self.x = x
        self.y = y
        self.topic = init_topic


    # topic の選択をするメソッド
    def select_topic(self, all_topic):
        now_topic = self.topic.copy()
        self.topic.clear()

        # トピックごとの選択方法
        for t in all_topic:
            if t.role == 0:
                if now_topic.count(t.id) == 1 and random.uniform(0, 100) < 99.9:
                    self.topic.append(t.id)
                elif now_topic.count(t.id) == 0 and random.uniform(0, 100) < 0.1:
                    self.topic.append(t.id)

            elif t.role == 1:
                distance = math.sqrt(pow(self.x - t.base_point[0], 2) + pow(self.y - t.base_point[1], 2))
                if distance <= t.threshold:
                    self.topic.append(t.id)
        
            elif t.role == 2:       
                for point in t.random_point:
                    rank = point.cal_rank(self.x, self.y)

                    if rank == 0:
                        self.topic.append(t.id)
            else:
                sys.exit("追加されていない role です。class Client_topic の select_topic を修正して下さい。")
            
        return self.topic  
    

class Client:

    def __init__(self, id, x, y, pub_edge_id, sub_edge_id):
        self.id = id
        self.x = x
        self.y = y
        self.pub_edge_id = pub_edge_id
        self.sub_edge_id = sub_edge_id
