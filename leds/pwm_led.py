import RPi.GPIO as GPIO
from time import sleep

LED = 14

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(LED, GPIO.OUT)

pwm = GPIO.PWM(LED, 100)
pwm.start(0)

sleepTime = 0.01
numLoops = 100
try:
    while True:
        for x in xrange(numLoops):
            pwm.ChangeDutyCycle(x)
            sleep(sleepTime)

        for x in xrange(numLoops, 0, -1):
            pwm.ChangeDutyCycle(x)
            sleep(sleepTime)

except KeyboardInterrupt:
    print("\nCleaning up...")
    pwm.stop()
    GPIO.cleanup()
