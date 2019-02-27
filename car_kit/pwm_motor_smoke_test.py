import RPi.GPIO as GPIO
from time import sleep

EN_A = 21
IN_1 = 20
IN_2 = 16
IN_3 = 7
IN_4 = 8
EN_B = 25

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(EN_A, GPIO.OUT)
GPIO.setup(IN_1, GPIO.OUT)
GPIO.setup(IN_2, GPIO.OUT)
GPIO.setup(IN_3, GPIO.OUT)
GPIO.setup(IN_4, GPIO.OUT)
GPIO.setup(EN_B, GPIO.OUT)

en_a_pwm = GPIO.PWM(EN_A, 100)
en_b_pwm = GPIO.PWM(EN_B, 100)
en_a_pwm.start(0)
en_b_pwm.start(0)

sleep_time = 2
off = 0
low = 50
med = 75
high = 100
try:
    GPIO.output(IN_1, GPIO.HIGH)
    GPIO.output(IN_2, GPIO.LOW)
    GPIO.output(IN_3, GPIO.HIGH)
    GPIO.output(IN_4, GPIO.LOW)
    while True:
        en_a_pwm.ChangeDutyCycle(low)
        en_b_pwm.ChangeDutyCycle(low)
        sleep(sleep_time)

        en_a_pwm.ChangeDutyCycle(med)
        en_b_pwm.ChangeDutyCycle(med)
        sleep(sleep_time)

        en_a_pwm.ChangeDutyCycle(high)
        en_b_pwm.ChangeDutyCycle(high)
        sleep(sleep_time)

        en_a_pwm.ChangeDutyCycle(off)
        en_b_pwm.ChangeDutyCycle(off)
        sleep(sleep_time)


except KeyboardInterrupt:
    print("\nCleaning up...")
    en_a_pwm.stop()
    en_b_pwm.stop()
    GPIO.cleanup()
