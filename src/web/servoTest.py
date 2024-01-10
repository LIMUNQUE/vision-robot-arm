from time import sleep
import RPi.GPIO as GPIO
servo_pin = 19  # GPIO Pin where sero is connected
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
p = GPIO.PWM(servo_pin, 50)  # PWM channel at 50 Hz frequency
p.start(0)  # Zero duty cycle initially
p.ChangeDutyCycle(float(slider))  # 1 to 12.5
sleep(1)
# Pause the servo
p.ChangeDutyCycle(0)
