import RPi.GPIO as GPIO
import keyboard
from time import sleep

class get_gpio():    # get inputs from rotary encoder on pi
                     
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
            
        while True:
        
            event = keyboard.read_event()

            if event.event_type == keyboard.KEY_DOWN and event.name == 'up':
                press = 'UP'
                return press
            
            if event.event_type == keyboard.KEY_DOWN and event.name == 'down':
                press = 'DOWN'
                return press  
            
            if event.event_type == keyboard.KEY_DOWN and event.name == 'enter':
                press = 'ENTER'
                return press  
        

        