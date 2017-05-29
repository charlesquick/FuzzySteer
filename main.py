from fis import FisHandler
from comms import Comms
import time
import sys


class Main:
    def __init__(self):
        self.enable = True
        self.guienable = True
        self.fisout = None
        self.fail = 10
        print("initialising Fuzzy System...")
        self.fis = FisHandler()
        print("Fuzzy System initialised")
        self.comm = Comms()
        self.distance = 0
        self.delta = 0
        self.speed = 0
        self.sAngle = 50

    def run(self):
        while True:
            while True:
                data = self.comm.getserial()
                print(data)
                if not data:
                    self.fail += 1
                    print("fail")
                    continue
                else:
                    self.distance, self.delta, self.speed, self.sAngle = data['distance'], data['delta'], \
                                                                         data['speed'], data['sAngle']
                    print(self.distance, self.delta, self.speed, self.sAngle)
                    self.fisout = self.fis.runfis(self.distance, self.delta, self.speed)
                    print(self.fisout)
                    self.fail = 0
                    break

            self.enable = self.guienable

            if self.fail > 10:
                print('No serial data received')
                self.enable = False

            elif self.distance == 32020:  # Flags for steering disabled/undefined
                print("Steering disabled by tablet")
                self.enable = False

            elif self.distance == 32000:
                print("Unable to find line")
                self.enable = False

            if self.fisout is None:
                continue

            output = self.fis.integrate(self.fisout, self.sAngle)
            self.comm.writepwm(output, self.enable)

            time.sleep(0.01)

    def kill(self):
        self.comm.writepwm({"direction": 'left', 'value': 0}, False)
        sys.exit()


if __name__ == '__main__':
    main = Main()
    try:
        main.run()
    except KeyboardInterrupt:
        main.kill()
