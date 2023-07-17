
#  Edge サーバの情報を扱うためのクラス
class Edge:

    def __init__(self, id, x, y, volume, cpu_cycle):
        self.id = id
        self.x = x
        self.y = y
        self.volume = volume
        self.cpu_cycle = cpu_cycle