#  トラッキングデータを生成する際に使用する Data クラス
class DataTraking:

    def __init__(self, id, time, x, y):
        self.id = id
        self.time = time
        self.x = x
        self.y = y


#  pub/sub 関係を決定する際に使用する Data クラス
class DataTopic:

    def __init__(self, id, time, x, y, pub_topic, sub_topic):
        self.id = id
        self.time = time
        self.x = x
        self.y = y
        self.pub_topic = pub_topic
        self.sub_topic = sub_topic


#  トピック割り当てを決定する際に使用する Data クラス
class DataSolution:

    def __init__(self, id, time, x, y, pub_edge, sub_edge):
        self.id = id
        self.time = time
        self.x = x
        self.y = y
        self.pub_edge = pub_edge
        self.sub_edge = sub_edge