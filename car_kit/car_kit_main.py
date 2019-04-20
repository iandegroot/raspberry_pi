import RPi.GPIO as GPIO
from time import sleep
import xbox

## To run on bootup:
# $ sudo crontab -e
# add
# @reboot /usr/bin/python /home/pi/FileCab/raspberry_pi/car_kit/car_kit_main.py &


EN_A = 21
IN_1 = 20
IN_2 = 16
IN_3 = 7
IN_4 = 8
EN_B = 25
YELLOW_LED = 14

FORWARD = 1
BACKWARD = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(EN_A, GPIO.OUT)
GPIO.setup(IN_1, GPIO.OUT)
GPIO.setup(IN_2, GPIO.OUT)
GPIO.setup(IN_3, GPIO.OUT)
GPIO.setup(IN_4, GPIO.OUT)
GPIO.setup(EN_B, GPIO.OUT)
GPIO.setup(YELLOW_LED, GPIO.OUT)

class Motor:

    pwm_scaling_factor = 100
    motor_low_threshold = 25
    motor_off = 0
    backward_speed = 40

    def __init__(self, pwm_pin, dir_pin_1, dir_pin_2, get_trigger_func, get_bumper_func):
        self.direction = FORWARD
        self.speed_value = self.motor_off
        self.speed_pin = GPIO.PWM(pwm_pin, 100)
        self.dir_pin_1 = dir_pin_1
        self.dir_pin_2 = dir_pin_2
        self.trigger_func = get_trigger_func
        self.bumper_func = get_bumper_func

        self.speed_pin.start(self.speed_value)

    def set_to_forward(self):
        GPIO.output(self.dir_pin_1, GPIO.HIGH)
        GPIO.output(self.dir_pin_2, GPIO.LOW)

    def set_to_backward(self):
        GPIO.output(self.dir_pin_1, GPIO.LOW)
        GPIO.output(self.dir_pin_2, GPIO.HIGH)

    def move_forward(self):
        self.set_to_forward()
        scaled_trigger_reading = self.trigger_func() * self.pwm_scaling_factor
        if scaled_trigger_reading > 0 and scaled_trigger_reading < self.motor_low_threshold:
            scaled_trigger_reading = self.motor_low_threshold
        self.speed_pin.ChangeDutyCycle(scaled_trigger_reading)

    def move_backward(self):
        if self.bumper_func():
            self.set_to_backward()
            self.speed_pin.ChangeDutyCycle(self.backward_speed)
        else:
            self.speed_pin.ChangeDutyCycle(self.motor_off)

joy = xbox.Joystick()

try:
    left_motor = Motor(EN_A, IN_1, IN_2, joy.leftTrigger, joy.leftBumper)
    right_motor = Motor(EN_B, IN_3, IN_4, joy.rightTrigger, joy.rightBumper)

    while True:
        if left_motor.direction == FORWARD:
            left_motor.set_to_forward()
            left_motor.move_forward()

            if joy.leftBumper():
                left_motor.direction = BACKWARD

        elif left_motor.direction == BACKWARD:
            left_motor.move_backward()

            if joy.leftTrigger():
                left_motor.direction = FORWARD

        if right_motor.direction == FORWARD:
            right_motor.set_to_forward()
            right_motor.move_forward()

            if joy.rightBumper():
                right_motor.direction = BACKWARD

        elif right_motor.direction == BACKWARD:
            right_motor.move_backward()

            if joy.rightTrigger():
                right_motor.direction = FORWARD

        if joy.Y():
            GPIO.output(YELLOW_LED, GPIO.HIGH)
        else:
            GPIO.output(YELLOW_LED, GPIO.LOW)

except KeyboardInterrupt:
    print("\nCleaning up...")
    left_motor.speed_pin.stop()
    right_motor.speed_pin.stop()
    GPIO.cleanup()
