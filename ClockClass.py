"""
##################################################
More accurate than using time.sleep() for rep rates
##################################################
# Author:   Liam Droog
# Email:    droog@ualberta.ca
# Year:     2021
# Version:  V.1.0.0
##################################################
"""
import time


class Clock:

    def __init__(self, dly):
        self.exists = True
        self.start = time.perf_counter()
        self.shot_len = 1/dly

    @property
    def tick(self):
        return int((time.perf_counter() - self.start) / self.shot_len)

    def sleep(self):
        r = self.tick + 1
        while self.tick < r:
            time.sleep(1 / 1000)
