from getkey import getkey, keys
from time import sleep


class get_gpio():    # get inputs from rotary encoder on pi
                     
    def get_input(press):

        import RPi.GPIO as GPIO

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

                if dtState != clkState:    # if turning knob left
                        press = 'UP'
                        return press
                else:                      # if turning knob right
                        press = 'DOWN'       
                        return press  
                                       
            if btnState == GPIO.LOW:       # if knob button pressed             
                press = 'ENTER'    
                return press
            
            clkLastState = clkState
            sleep(0.001)
      
class get_key():    # get keyboard inputs if in emulator mode
                    ##### must have cursor in termial to capture keyboard inputs #####
    
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
        

        