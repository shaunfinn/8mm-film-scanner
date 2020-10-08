import config
import time 



class testClass():
    def main_loop(self):
        config.run_motor = True
        while config.run_motor:
            time.sleep(0.5)
            print("motor running")
        print("while loop broken")



   
