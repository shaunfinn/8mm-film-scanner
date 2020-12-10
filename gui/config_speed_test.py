import config
import time

class read:
    def __init__(self):
        # store the start time, end time and total number of frames
        # that were examined between the start and end intervals
        self.variable = True
        config.capture =True

        self.t_end = time.time() + 10.0
    def config_loop(self):
        # start the timer
        cnt=0
        while time.time() <= self.t_end:
            if config.capture:
                cnt+=1
        print("config variable calls in 10s : ", cnt)

    def self_loop(self):
        # start the timer
        cnt=0
        while time.time() <= self.t_end:
            if self.variable:
                cnt+=1
        print("self variable calls in 10s : ", cnt)

r= read().config_loop()
r2= read().self_loop()