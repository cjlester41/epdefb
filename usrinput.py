from getkey import getkey, keys
from time import sleep
import RPi.GPIO as GPIO

class get_gpio():
       
    def get_input(press):

        btn = 22
        clk = 27
        dt = 18

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        clkLastState = GPIO.input(clk)
       
        while press == '':

            btnState = GPIO.input(btn)
            clkState = GPIO.input(clk)
            dtState = GPIO.input(dt)

            if clkState != clkLastState:

                if dtState != clkState:
                        press = 'UP'
                        return press
                else:
                        press = 'DOWN'       
                        return press  
                                       
            if btnState == GPIO.LOW:                    
                press = 'ENTER'    
                return press
            
            clkLastState = clkState
            sleep(0.001)
      
class get_key():
    
    def get_input(press):
        
        key = getkey()

        if key == keys.UP:
            press = 'UP'
            return press
        
        if key == keys.DOWN:
            press = 'DOWN'
            return press  
        
        if key == keys.ENTER:
            press = 'ENTER'
            return press  
        

        