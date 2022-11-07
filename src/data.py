
class Data_traking:

    def __init__(self, id, time, x, y):
        self.id = id
        self.time = time
        self.x = x
        self.y = y


class Data_topic:

    def __init__(self, id, time, x, y, topic_list):
        self.id = id
        self.time = time
        self.x = x
        self.y = y
        self.topic_list = topic_list