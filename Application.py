import logging
from usr_interface import plates


xml_file = 'tppData/d-tpp_Metafile.xml'

try:
        
    while(True):
        
        root = plates.parse_metafile(xml_file)
        dest = plates.select_airport()    
        rnwy = plates.select_runway()
        airport, chrts, pdfs = plates.create_plate_list(root, dest, rnwy)

        while(True):
            
            trgt = plates.select_plate(airport, chrts, pdfs)            
            plates.display_plate(trgt)      

except IOError as e:   
    logging.info(e)

except KeyboardInterrupt:
    logging.info('ctrl + c:')
    #display.clear()    # clear the display some other way for screen longevity?  
    exit()

