from getkey import getkey, keys
from time import sleep
import RPi.GPIO as GPIO

#GPIO.cleanup()

press = ''

clk = 27
dt = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0
clkLastState = GPIO.input(clk)

try:

    while True: #press == '':
            
            btnState = GPIO.input(22)
            clkState = GPIO.input(clk)
            dtState = GPIO.input(dt)
            if clkState != clkLastState:
                    if dtState != clkState:
                            press = 'UP'
                            print(press)
                    else:
                            press = 'DOWN'
                            print(press)                                
            if btnState == GPIO.LOW:                    
                press = 'ENTER'    
                print(press)
            clkLastState = clkState
            sleep(0.01)
finally:
        GPIO.cleanup()