import RPi.GPIO as GPIO

duty = 80

#GPIO初期設定
GPIO.setmode(GPIO.BCM)#setmodeでBCMを用いて指定することを宣言　#GPIOピン番号のこと！
GPIO.setup(13,GPIO.OUT)#PWM出力
GPIO.setup(11,GPIO.OUT)#デジタル出力
# GPIO.setup(23,GPIO.OUT)#PWM出力
# GPIO.setup(24,GPIO.OUT)#デジタル出力

right=GPIO.PWM(13,50)
# left=GPIO.PWM(23,50)

right.start(0)
# left.start(0)

print("モータが回転します。ご注意ください")
while True:
    try:
        right.ChangeDutyCycle(duty)
        right_ph=GPIO.output(11,GPIO.LOW)
        # left.ChangeDutyCycle(duty)
        # left_ph=GPIO.output(24,GPIO.LOW)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        GPIO.cleanup()
GPIO.cleanup()