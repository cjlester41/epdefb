import logging, os
import interface.usr_input as usr_input
import emulator.epd_emulator as epd_emulator
from interface.usr_interface import Plates
from interface.IT8951.display import AutoEPDDisplay
from definitions import ROOT_DIR

if os.environ['HOME'] == '/home/cjlester':   
    display = AutoEPDDisplay(vcom=-1.71, spi_hz=24000000, rotate='CW')
    peripheral = usr_input.get_gpio

else:    
    display = epd_emulator.EPD(update_interval=.333)
    peripheral = usr_input.get_key

xml_file = os.path.join(ROOT_DIR,'tppData/d-tpp_Metafile.xml')    # bring this in from updates.py?

try:
    
    plates = Plates(display, peripheral)
    root = plates.parse_metafile(xml_file)
    
    while(True):
        
        dest, airport, chrt_pdfs = plates.select_airport(root)    
        rnwy = plates.select_runway(airport, chrt_pdfs)
        chrts, pdfs = plates.create_plate_list(chrt_pdfs, rnwy)

        while(True):
            
            trgt = plates.select_plate(airport, chrts, pdfs)            
            plates.display_plate(trgt)      

except IOError as e:   
    logging.info(e)

except KeyboardInterrupt:
    logging.info('ctrl + c:')
    #display.clear()    # clear the display some other way for screen longevity?  
    exit()

