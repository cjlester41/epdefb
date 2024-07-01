import os, logging, time
import argparse
import usr_input
import epd_emulator
import usr_interface
from PIL import ImageFont

current_dir = os.path.dirname(os.path.abspath(__file__))
log = logging.getLogger('werkzeug')    # turn off excess logging from flask
log.setLevel(logging.ERROR)

emulate = argparse.ArgumentParser(description='enable emulator')    # check for argument to run in emulator
emulate.add_argument('-v', '--virtual', action='store_true')
args = emulate.parse_args()

if not args.virtual:    # if no argument initialize display driver and knob/button input
    from IT8951.display import AutoEPDDisplay # type: ignore
    display = AutoEPDDisplay(vcom=-1.71, spi_hz=24000000, rotate='CW')
    peripheral = usr_input.get_gpio

else:    # if -v argument initialize display emulator and keyboard input
    
    display = epd_emulator.EPD(update_interval=1)
    peripheral = usr_input.get_key

width, height = display.width, display.height    # set display dimensions     
font = ImageFont.truetype(os.path.join(current_dir, 'ui_files/Arial.ttf'), 48)

pdfs, chrts = [], []    # some globl variables, need to remove
airport = ''

try:
        
    while(True):

        xml_file = usr_interface.plates.__init__()
        root = usr_interface.plates.parse_metafile(xml_file)
        usr_interface.plates.select_airport(root)    # this runs only once, need option to return to airport selection

        while(True):
            #usr_interface.select_plate()    # cycle back and forth between these
            trgt = usr_interface.plates.select_plate()            
            usr_interface.plates.display_plate(trgt)      

except IOError as e:   
    logging.info(e)

except KeyboardInterrupt:
    logging.info('ctrl + c:')
    display.clear()    # clear the display for screen longevity  
    exit()

