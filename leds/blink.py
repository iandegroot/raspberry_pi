import RPi.GPIO as GPIO
from time import sleep

LED = 14

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(LED, GPIO.OUT)

while True:
    GPIO.output(LED, GPIO.HIGH)
    sleep(1)
    GPIO.output(LED, GPIO.LOW)
    sleep(1)
