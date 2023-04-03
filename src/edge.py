import numpy as np


#  Edge サーバの情報を扱うためのクラス
class Edge:

    def __init__(self, id, x, y, volume, cpu_power):
        self.id = id
        self.x = x
        self.y = y
        self.volume = volume
        self.cpu_power = cpu_power