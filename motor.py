import RPi.GPIO as GPIO
import time

class Motor():
    def __init__(self,config):
        self.duty = config['MOTER'].get('duty')
        self.right_pwm = config['MOTER'].get('right_pwm')
        self.left_pwm = config['MOTER'].get('left_pwm')
        self.right_phase = config['MOTER'].get('right_ph')
        self.left_phase = config['MOTER'].get('right_ph')

        GPIO.setmode(GPIO.BCM)#setmodeでBCMを用いて指定することを宣言　#GPIOピン番号のこと！

        self.setup_gpio()

        self.initialize_motors()

    def setup_gpio(self):
        GPIO.setup(right_pwm,GPIO.OUT)#PWM出力
        GPIO.setup(right_phase,GPIO.OUT)#デジタル出力
        GPIO.setup(left_pwm,GPIO.OUT)#PWM出力
        GPIO.setup(left_phase,GPIO.OUT)#デジタル出力

    def initialize_motors(self):
        self.right = GPIO.PWM(right_pwm,200)
        self.left = GPIO.PWM(left_pwm,200)
        GPIO.output(right_phase,GPIO.LOW)
        GPIO.output(left_phase,GPIO.LOW)
        self.right.start(0)
        self.left.start(0)

    def move(self,direction,moter_active_time):
        self.adjust_duty_cycle(direction)

        stop_time = time.time() + moter_active_time
        while time.time() < stop_time:
            self.right.ChangeDutyCycle(self.right_duty)
            self.left.ChangeDutyCycle(self.left_duty)

        self.right.ChangeDutyCycle(0)
        self.left.ChangeDutyCycle(0)

    def adjust_duty_cycle(self,direction):
        if direction == "forward":
            self.right_duty = self.left_duty = self.duty
        elif direction == "right":
            self.right_duty = self.duty * 0.6
            self.left_duty = self.duty
        elif direction == "left":
            self.right_duty = self.duty
            self.left_duty = self.duty * 0.6
        else:
            self.right_duty = self.left_duty = self.duty
            GPIO.output(self.right_phase,GPIO.HIGH)
            GPIO.output(self.left_phase,GPIO.HIGH)
        
    def cleanup(self):
        GPIO.cleanup()