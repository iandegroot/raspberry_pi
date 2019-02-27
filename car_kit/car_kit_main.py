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
try:
    set_right_side_to_forward()
    set_left_side_to_forward()

    while True:
        scaled_trigger_reading = joy.rightTrigger() * pwm_scaling_factor
        if scaled_trigger_reading > 0 and scaled_trigger_reading < motor_low_threshold:
            scaled_trigger_reading = motor_low_threshold
        right_pwm.ChangeDutyCycle(scaled_trigger_reading)

        scaled_trigger_reading = joy.leftTrigger() * pwm_scaling_factor
        if scaled_trigger_reading > 0 and scaled_trigger_reading < motor_low_threshold:
            scaled_trigger_reading = motor_low_threshold
        left_pwm.ChangeDutyCycle(scaled_trigger_reading)

        if joy.Y():
            GPIO.output(YELLOW_LED, GPIO.HIGH)
        else:
            GPIO.output(YELLOW_LED, GPIO.LOW)
        """
        if joy.rightBumper():
            set_right_side_to_backward()
            right_pwm.ChangeDutyCycle(backward_speed)

        if joy.leftBumper():
            set_left_side_to_backward()
            left_pwm.ChangeDutyCycle(backward_speed)
        """    

except KeyboardInterrupt:
    print("\nCleaning up...")
    left_pwm.stop()
    right_pwm.stop()
    GPIO.cleanup()
