from getkey import getkey, keys
import RPi.GPIO as GPIO

class usr_input():
    
    def get_key(press):
        
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
        

    #def get_gpio(press):

     #   kkey = getkey()

        