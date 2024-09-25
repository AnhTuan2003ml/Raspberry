import RPi.GPIO as GPIO
import time

BUTTON_UP_PIN = 22
BUTTON_DOWN_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        up_state = GPIO.input(BUTTON_UP_PIN)
        down_state = GPIO.input(BUTTON_DOWN_PIN)
        print(f"Button Up: {up_state}, Button Down: {down_state}")
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
