import logging
from interface.usr_interface import plates


xml_file = 'tppData/d-tpp_Metafile.xml'

try:
    
    root = plates.parse_metafile(xml_file)
    
    while(True):
        
        dest, airport, chrt_pdfs = plates.select_airport(root)    
        rnwy = plates.select_runway()
        chrts, pdfs = plates.create_plate_list(chrt_pdfs, dest, rnwy)

        while(True):
            
            trgt = plates.select_plate(airport, chrts, pdfs)            
            plates.display_plate(trgt)      

except IOError as e:   
    logging.info(e)

except KeyboardInterrupt:
    logging.info('ctrl + c:')
    #display.clear()    # clear the display some other way for screen longevity?  
    exit()

