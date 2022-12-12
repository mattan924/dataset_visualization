
class Data_traking:

    def __init__(self, id, time, x, y):
        self.id = id
        self.time = time
        self.x = x
        self.y = y


class Data_topic:

    def __init__(self, id, time, x, y, pub_topic, sub_topic):
        self.id = id
        self.time = time
        self.x = x
        self.y = y
        self.pub_topic = pub_topic
        self.sub_topic = sub_topic


class Data_solution:

    def __init__(self, id, time, x, y, pub_edge, sub_edge):
        self.id = id
        self.time = time
        self.x = x
        self.y = y
        self.pub_edge = pub_edge
        self.sub_edge = sub_edge