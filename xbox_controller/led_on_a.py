import RPi.GPIO as GPIO
from time import sleep
import xbox

LED = 14

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(LED, GPIO.OUT)

joy = xbox.Joystick()

try:
    while not joy.Back():
        if joy.A():
            GPIO.output(LED, GPIO.HIGH)
        else:
            GPIO.output(LED, GPIO.LOW)

except KeyboardInterrupt:
    print("\nCleaning up...")
    GPIO.cleanup()
