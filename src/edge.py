import numpy as np

class Edge:

    def __init__(self, id, x, y, volume, cpu_power):
        self.id = id
        self.x = x
        self.y = y
        self.volume = volume
        self.cpu_power = cpu_power


    def add_broker(self, topic):
        if self.used_volume + topic.volume <= self.volume:
            self.broker_list.append(topic)
            self.used_volume = self.used_volume + topic.volume

    
    def allocation_power(self):
        for topic in self.broker_list:
            self.power_allocation[topic.id] = self.power/len(self.broker_list)
    

    def cal_delay(self, topic):
        return topic.task/self.power_allocation[topic.id]