import serial
import Adafruit_PCA9685


class Comms:
    def __init__(self):
        self.arduinoPort = serial.Serial(port='/dev/ttyUSB0',
                                         baudrate=9600,
                                         parity=serial.PARITY_NONE,
                                         stopbits=serial.STOPBITS_ONE,
                                         bytesize=serial.EIGHTBITS,
                                         timeout=1
                                         )
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(500)

    def getserial(self):
        line = str(self.arduinoPort.readline())
        line.strip("b'")
        split = line.split()
        try:
            return {'distance': float(split[1]), 'delta': float(split[2]),
                    'speed': float(split[3]), 'sAngle': float(split[4])}
        except ValueError or IndexError:
            return False

    def writepwm(self, data, enable):
        direction, val = data['direction'], data['value']

        if direction == 'left' and enable:
            # send pwm to right output
            if val > 100:
                val = 100
            out = self.map(val, 0, 100, 0, 4096)
            print('left', val)
            self.pwm.set_pwm(0, 0, out)
            self.pwm.set_pwm(1, 0, 0)
        elif direction == 'right' and enable:
            # send pwm to right output
            if val > 100:
                val = 100
            out = self.map(val, 0, 100, 0, 4096)
            print('right', val)
            self.pwm.set_pwm(0, 0, 0)
            self.pwm.set_pwm(1, 0, out)
        else:
            self.pwm.set_pwm(0, 0, 0)
            self.pwm.set_pwm(1, 0, 0)

    def map(self, x, in_min, in_max, out_min, out_max):
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


if __name__ == "__main__":
    c = Comms()
    while True:
        f = c.getserial()
