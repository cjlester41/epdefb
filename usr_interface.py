import os, logging, time
import xml.etree.ElementTree as ET
import pypdfium2 as pdfium
import argparse
import usr_input
import epd_emulator
from IT8951.display import AutoEPDDisplay
from IT8951 import constants
from PIL import Image, ImageFont, ImageDraw


current_dir = os.path.dirname(os.path.abspath(__file__))
font = ImageFont.truetype(os.path.join(current_dir, 'ui_files/Arial.ttf'), 48)

emulate = argparse.ArgumentParser(description='enable emulator')    # check for argument to run in emulator
emulate.add_argument('-v', '--virtual', action='store_true')
args = emulate.parse_args()

if not args.virtual:    # if no argument initialize display driver and knob/button input
    display = AutoEPDDisplay(vcom=-1.71, spi_hz=24000000, rotate='CW')
    peripheral = usr_input.get_gpio

else:    # if -v argument initialize display emulator and keyboard input
    display = epd_emulator.EPD(update_interval=1)
    peripheral = usr_input.get_key

class plates:

    def __init__(self):

        self.xml_file: 'tppData/d-tpp_Metafile.xml'
        #return xml_file

    def parse_metafile(xml_file):    # open and parse faa database xml file, needs to occur at beginning
        
        try:    
            tree = ET.parse(os.path.join(current_dir, xml_file))
            root = tree.getroot() 

        except:
            print('check d-tpp metafile file present') 

        return root

    def next_alpha(airport_char):    # generate next character in alphabetical sequence
            return chr((ord(airport_char.upper())+1 - 65) % 26 + 65)
    
    def prev_alpha(airport_char):    # generate previous character in alphabetical sequence
            return chr((ord(airport_char.upper())-1 - 65) % 26 + 65)

    def select_airport():    # manually select airpot. PoC and not functioning, default PDX
        
        airport_char = 'K'    # initial character displayed     
        x_offset = 100    # initial x axis offset for display output
        
        display.clear() 
        draw = ImageDraw.Draw(display.frame_buf)    # set display buffer
        draw.text((50, 50), 'SELECT DESTINATION AIRPORT:', font = font)
        draw.rectangle((x_offset, 150, 134, 200), fill=0, outline=0)
        draw.text((x_offset, 150), airport_char, font = font, fill=255)
        display.draw_partial(constants.DisplayModes.DU)    # output display

        while True:            

            key = peripheral.get_input(press='')    # initialize usr_input and return key/knob         

            if key == 'UP':    # display previous character
                display.clear()        
                draw.rectangle((x_offset, 150, x_offset + 34, 200), fill=0, outline=0)
                airport_char = plates.prev_alpha(airport_char)
                draw.text((x_offset, 150), airport_char, font = font, fill=255)
                display.draw_partial(constants.DisplayModes.DU)                    

            if key == 'DOWN':    # display next character        
                display.clear()        
                draw.rectangle((x_offset, 150, x_offset + 34, 200), fill=0, outline=0)
                airport_char = plates.next_alpha(airport_char)
                draw.text((x_offset, 150), airport_char, font = font, fill=255)
                display.draw_partial(constants.DisplayModes.DU)

            if key == 'ENTER':    # move on to select_plate
                x_offset += 50   
                break  

            #display.draw_partial(constants.DisplayModes.DU) 

            #time.sleep(3)

        dest = 'PDX' #input('Destination: ').upper()
        return dest

    def select_runway():

        rnwy = '28' #input('Runway: ').upper()
        return rnwy

    def create_plate_list(root, dest, rnwy):
        
        pdfs, chrts = [], []
        #airport = airport_name.get('ID') + ':'
        
        for airport_name in root.findall('.//airport_name[@apt_ident="' + dest + '"]'):    # find all matches for PDX in xml file
            chrt_pdfs = zip(airport_name.findall('.//chart_name'), airport_name.findall('.//pdf_name'))    # merge lists of pdfs that match chart name

            for chart_name, pdf_name in chrt_pdfs:    # for all chart names for selected airport

                if rnwy in (chart_name.text):    # if user selected runway only return plates for that runway                
                    chrts.append(chart_name.text)
                    pdfs.append(pdf_name.text)

                elif rnwy == 'ALL':    # if user selected all return all plates for airport
                    chrts.append(chart_name.text)
                    pdfs.append(pdf_name.text)

        airport = airport_name.get('ID') + ':'    # define full airport name for ui output
        return airport, chrts, pdfs

    def select_plate(airport, chrts, pdfs):    # ui to choose plate to be displayed
            
        display.clear() 
        draw = ImageDraw.Draw(display.frame_buf) 
        y_offset = 150    # y axis offset for text
        c, line = 0, 0         

        while True:        
            
            draw.rectangle((0, 0, 1404, 1872), fill=255, outline=255)    # clear buffer without clearing dispaly, should be function       
            draw.text((50, 50), 'SELECT APPROACH FOR ' + airport, font = font)
            line = 0        
        
            for chrt in chrts:    # display all the charts for previous airport/runway selection               
                draw.text((100, 150 + (line * 50)), chrt, font=font, fill=0)
                line += 1

            draw.rectangle((98, y_offset, 700, y_offset + 52), fill=0, outline=0)    # make black backround for selection 'cursor'
            draw.text((100, y_offset), chrts[c], font=font, fill=255)    # make selected item text white
            display.draw_partial(constants.DisplayModes.DU) 
            
            key = peripheral.get_input(press='')    # get the users input          

            if key == 'UP' and c != 0:    # move up the list if not at top         
                y_offset -= 50
                c -= 1

            if key == 'DOWN' and c < (len(chrts) - 1):    # move down the list if not at bottom              
                y_offset += 50 
                c += 1  

            if key == 'ENTER':    # create variable trgt; pdf name in tppData that matches the user selection
                trgt = pdfs[c]                 
                return trgt
                
    def display_plate(trgt):    # show the plate

        width, height = display.width, display.height 
        
        try:            
            pdf = pdfium.PdfDocument(os.path.join(current_dir, 'tppData/' + trgt))    # convert from pdf to bmp (required)      
            page = pdf.get_page(0)
            pil_image = page.render(scale = 300/72).to_pil()
            image_name =f'plate.bmp'    
            pil_image.save(os.path.join(current_dir, 'ui_files/', image_name))  

        except:
            print('check tppData folder is populated')

        image1 = Image.open(os.path.join(current_dir, 'ui_files/plate.bmp'))    # open, resize, and position the bmp
        new_width1, new_height1 = int(image1.width * 0.875), int(image1.height * 0.875)
        image1 = image1.resize((new_width1, new_height1))    
        y_bottom1 = height - new_height1     
        
        display.frame_buf.paste(image1, (0, y_bottom1 + 143))    # paste the bmp to buffer
        display.draw_full(constants.DisplayModes.GC16)    # display the bmp

        while peripheral.get_input(press='') != 'ENTER':    # wait for enter, then return to select_plate
            continue


