import RPi.GPIO as GPIO
from time import sleep
import xbox

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

    __init__(self, pwm_pin, dir_pin_1, dir_pin_2):
        self.direction = FORWARD
        self.speed_value = motor_off
        self.speed_pin = GPIO.PWM(pwm_pin, 100)
        self.dir_pin_1 = dir_pin_1
        self.dir_pin_2 = dir_pin_2

        self.motor_speed_pin.start(self.speed_value)

    def set_motor_to_forward(self):
        GPIO.output(self.dir_pin_1, GPIO.HIGH)
        GPIO.output(self.dir_pin_2, GPIO.LOW)

    def set_motor_to_backward(self):
        GPIO.output(self.dir_pin_1, GPIO.LOW)
        GPIO.output(self.dir_pin_2, GPIO.HIGH)

    def forward(self):
        self.set_motor_to_forward()
        scaled_trigger_reading = joy.rightTrigger() * pwm_scaling_factor
        if scaled_trigger_reading > 0 and scaled_trigger_reading < motor_low_threshold:
            scaled_trigger_reading = motor_low_threshold
        right_pwm.ChangeDutyCycle(scaled_trigger_reading)

    def backward(self):
        pass

left_pwm = GPIO.PWM(EN_A, 100)
right_pwm = GPIO.PWM(EN_B, 100)
left_pwm.start(0)
right_pwm.start(0)

right_motor_dir = FORWARD
left_motor_dir = FORWARD


def set_right_side_to_forward():
    GPIO.output(IN_3, GPIO.HIGH)
    GPIO.output(IN_4, GPIO.LOW)

def set_right_side_to_backward():
    GPIO.output(IN_3, GPIO.LOW)
    GPIO.output(IN_4, GPIO.HIGH)

def set_left_side_to_forward():
    GPIO.output(IN_1, GPIO.HIGH)
    GPIO.output(IN_2, GPIO.LOW)

def set_left_side_to_backward():
    GPIO.output(IN_1, GPIO.LOW)
    GPIO.output(IN_2, GPIO.HIGH)

joy = xbox.Joystick()

pwm_scaling_factor = 100
motor_low_threshold = 25

backward_speed = 50
motor_off = 0

direction = FORWARD
try:
    set_right_side_to_forward()
    set_left_side_to_forward()

    while True:
        if direction == FORWARD:
            set_right_side_to_forward()
            set_left_side_to_forward()

            scaled_trigger_reading = joy.rightTrigger() * pwm_scaling_factor
            if scaled_trigger_reading > 0 and scaled_trigger_reading < motor_low_threshold:
                scaled_trigger_reading = motor_low_threshold
            right_pwm.ChangeDutyCycle(scaled_trigger_reading)

            scaled_trigger_reading = joy.leftTrigger() * pwm_scaling_factor
            if scaled_trigger_reading > 0 and scaled_trigger_reading < motor_low_threshold:
                scaled_trigger_reading = motor_low_threshold
            left_pwm.ChangeDutyCycle(scaled_trigger_reading)

            if joy.rightBumper() or joy.leftBumper():
                direction = BACKWARD

        elif direction == BACKWARD:
            if joy.rightBumper():
                set_right_side_to_backward()
                right_pwm.ChangeDutyCycle(backward_speed)
            else:
                right_pwm.ChangeDutyCycle(motor_off)

            if joy.leftBumper():
                set_left_side_to_backward()
                left_pwm.ChangeDutyCycle(backward_speed)
            else:
                left_pwm.ChangeDutyCycle(motor_off)

            if joy.rightTrigger() or joy.leftTrigger():
                direction = FORWARD

        if joy.Y():
            GPIO.output(YELLOW_LED, GPIO.HIGH)
        else:
            GPIO.output(YELLOW_LED, GPIO.LOW)



except KeyboardInterrupt:
    print("\nCleaning up...")
    left_pwm.stop()
    right_pwm.stop()
    GPIO.cleanup()
