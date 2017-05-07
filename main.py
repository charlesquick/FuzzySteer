from fis import Fis
from comms import Comms
import time
import sys

class FisHandler:
    def __init__(self):
        self.DELTA_EMPHASIS = 1         # Initial tuning parameter for delta
        self.DISTANCE_EMPHASIS = 1      # Initial tuning parameter for distance
        self.STEER_RATE = 3             # Multiplier for converting steering recommendation into PWM%
        self.STEER_BASE = 0             # Minimum PWM value (other than 0)
        self.distance = None
        self.delta = None
        self.speed = None
        self.fis = Fis()

    def runfis(self, distance, delta, speed):

        if delta > 15000:           # Cutoff to ensure that inputs do not exceed the universe of discourse for the FIS.
            self.delta = 15000      # 15000 microradians (1.5 rad) corresponds to ~85deg
        elif delta < -15000:
            self.delta = -15000
        else:
            self.delta = delta

        if distance > 15000:        # Similar cutoff for distance. Universe of Discourse -15000 : 15000 mm
            self.distance = 15000
        elif distance < -15000:
            self.distance = -15000
        else:
            self.distance = distance

        if speed > 30:        # Similar cutoff for distance. Universe of Discourse -15000 : 15000 mm
            self.speed = 30
        else:
            self.speed = speed

        self.distance = self.distance * self.DISTANCE_EMPHASIS
        self.delta = self.delta * self.DELTA_EMPHASIS

        return self.fis.compute(self.distance, self.delta, self.speed)  # FIS takes inputs and gives a target steer %

    def integrate(self, target, sangle):
        change = target - sangle  # Compare target with current steering percentage.

        if change < 0:
            # activate coil 1 (steer left)
            val = change * self.STEER_RATE
            val = 0 - val
            if val > 0 and val <= self.STEER_BASE:
                val = self.STEER_BASE

            return {"direction": 'left', 'value': val}

        elif change >= 0:
            val = change * self.STEER_RATE  # activate coil 2 (steer right)
            if val > 0 and val <= self.STEER_BASE:
                val = self.STEER_BASE
            return {"direction": 'right', 'value': val}


class Main:
    def __init__(self):
        self.enable = True
        self.guienable = True
        self.fisout = None
        self.fail = 10
        self.fis = FisHandler()
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
        main.comm.writepwm({"direction": 'left', 'value': 0}, False)
        sys.exit()


if __name__ == '__main__':
    main = Main()
    try:
        main.run()
    except KeyboardInterrupt:
        main.kill()
