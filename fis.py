from rpy2.robjects.packages import importr
import rpy2.robjects as ro

class Fis:
    def __init__(self):
        self.fuzzy = importr('FuzzyR')
        ro.r('fis = readfis("/home/pi/autosteer/code/R/fis-20-4.fis")')
        self.fis = ro.r['fis']

    def compute(self, distance, delta, speed):
        inputs = ro.FloatVector([distance, delta, speed])
        result = self.fuzzy.evalfis(inputs, self.fis)[0]
        return result


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