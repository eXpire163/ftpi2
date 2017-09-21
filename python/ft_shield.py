""" Managing the adafruit shield """

import atexit
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT #, Adafruit_DCMotor
from python.conf import Config

class FTShield(object):
    """ the shield """

    maxSpeed = 204
    dir = {}
    spe = {}
    debug = True
    isLive = True
    left_motor = 1
    right_motor = 2

    def __init__(self):
        """ init method """
        atexit.register(self.turn_off_motors)
        self.motor_hat = Adafruit_MotorHAT(addr=0x60)

    @classmethod
    def log(cls, txt):
        """ logging """
        Config.printme("ftShield", txt)

    def get_direction(self, nummer):
        """ get direction """
        try:
            return self.dir[nummer]
        except KeyError:
            return 'nix'

    def set_direction(self, nummer, direction):
        """ set direction """
        if self.get_direction(nummer) != direction:
            self.set_speed(nummer, 0.0)
            self.dir[nummer] = direction
            self.log('set {} {}'.format(nummer, direction))
            if self.isLive:
                self.motor_hat.getMotor(nummer).setSpeed(0)
            if direction == 'left':
                if bool(self.isLive):
                    self.motor_hat.getMotor(nummer).run(Adafruit_MotorHAT.FORWARD)
            else:
                if bool(self.isLive):
                    self.motor_hat.getMotor(nummer).run(Adafruit_MotorHAT.BACKWARD)
        else:
            self.log('skip set {} {}'.format(nummer, direction))

    def get_speed(self, nummer):
        """ get speed """
        try:
            return self.spe[nummer]
        except KeyError:
            return 0

    def set_speed(self, nummer, tempo):
        """ set speed """
        if self.get_speed(nummer) != tempo:
            self.spe[nummer] = tempo
            self.log('set {} {}'.format(nummer, tempo))
        else:
            self.log('skip set {} {}'.format(nummer, tempo))

    def set_motor(self, nummer, direction, speed):
        """ main function to modefy motors """
        self.log('set {} {} {}'.format(nummer, direction, speed))
        num = int(float(nummer))
        tempo = int(float(speed)*self.maxSpeed)
        self.set_direction(num, direction)
        self.set_speed(num, tempo)

    def turn_off_motors(self):
        """ killing all motors """
        self.log("motor aus ------------")
        self.motor_hat.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        self.motor_hat.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        self.motor_hat.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        self.motor_hat.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

    def move(self, speed=1):
        """ speed from 0 to 1 """
        self.set_motor(self.left_motor, 'left', speed)
        self.set_motor(self.right_motor, 'right', speed)
        time.sleep(0.5)

    def stop(self):
        """ stop movement """
        self.move(0)

    def turn_left(self, duration):
        """ turning left in tank mode """
        self.set_motor(self.left_motor, 'right', 0.5)
        self.set_motor(self.right_motor, 'right', 0.5)
        time.sleep(duration)

    def turn_right(self, duration):
        """ turning right in tank mode """
        self.set_motor(self.left_motor, 'left', 0.5)
        self.set_motor(self.right_motor, 'left', 0.5)
        time.sleep(duration)

    def backward(self, duration):
        """ moving backwards in tank mode """
        self.set_motor(self.left_motor, 'right', 0.5)
        self.set_motor(self.right_motor, 'left', 0.5)
        time.sleep(duration)
