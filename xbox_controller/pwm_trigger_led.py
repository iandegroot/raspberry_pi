import RPi.GPIO as GPIO
from time import sleep
import xbox

LED = 14

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(LED, GPIO.OUT)

pwm = GPIO.PWM(LED, 100)
pwm.start(0)

joy = xbox.Joystick()

pwmScaleFactor = 100
try:
    while True:
        scaledTriggerReading = joy.rightTrigger() * pwmScaleFactor
        pwm.ChangeDutyCycle(scaledTriggerReading)

except KeyboardInterrupt:
    print("\nCleaning up...")
    pwm.stop()
    GPIO.cleanup()
