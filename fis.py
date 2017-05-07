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
