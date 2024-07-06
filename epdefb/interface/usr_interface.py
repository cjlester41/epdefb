import os, time
import xml.etree.ElementTree as ET
import pypdfium2 as pdfium
from interface.IT8951 import constants
from PIL import Image, ImageFont, ImageDraw
from definitions import ROOT_DIR


class Plates:

    def __init__(self, display, peripheral):

        self.display = display
        self.peripheral = peripheral
        self.font = ImageFont.truetype(os.path.join(ROOT_DIR, 'ui_files/Arial.ttf'), 48)

    def parse_metafile(self, xml_file):  
        
        try:    
            tree = ET.parse(os.path.join(ROOT_DIR, xml_file))
            root = tree.getroot() 

        except:
            print('check d-tpp metafile file present') 

        return root

    def next_alpha(airport_char):    # generate next character in alphabetical sequence
            return chr((ord(airport_char.upper())+1 - 65) % 26 + 65)
    
    def prev_alpha(airport_char):    # generate previous character in alphabetical sequence
            return chr((ord(airport_char.upper())-1 - 65) % 26 + 65)

    def select_airport(self, root):    # manually select airpot. PoC and not functioning, default PDX
        
        airport_char = 'K'    # initial character self.displayed     
        x_offset = 100    # initial x axis offset for self.display output
        
        self.display.clear() 
        draw = ImageDraw.Draw(self.display.frame_buf)    # set self.display buffer
        draw.text((50, 50), 'SELECT DESTINATION AIRPORT:', font = self.font)
        draw.rectangle((x_offset, 150, 134, 200), fill=0, outline=0)
        draw.text((x_offset, 150), airport_char, font = self.font, fill=255)
        self.display.draw_partial(constants.DisplayModes.DU)    # output self.display

        while True:            

            key = self.peripheral.get_input(press='')    # initialize usr_input and return key/knob         

            if key == 'UP':    # self.display previous character
                self.display.clear()        
                draw.rectangle((x_offset, 150, x_offset + 34, 200), fill=0, outline=0)
                airport_char = self.prev_alpha(airport_char)
                draw.text((x_offset, 150), airport_char, font = self.font, fill=255)
                self.display.draw_partial(constants.DisplayModes.DU)                    

            if key == 'DOWN':    # self.display next character        
                self.display.clear()        
                draw.rectangle((x_offset, 150, x_offset + 34, 200), fill=0, outline=0)
                airport_char = self.next_alpha(airport_char)
                draw.text((x_offset, 150), airport_char, font = self.font, fill=255)
                self.display.draw_partial(constants.DisplayModes.DU)

            if key == 'ENTER':    # move on to select_plate
                x_offset += 50   
                dest = 'PDX' #input('Destination: ').upper()
                break  
            
        for airport_name in root.findall('.//airport_name[@apt_ident="' + dest + '"]'):    # find all matches for PDX in xml file
            chrt_pdfs = zip(airport_name.findall('.//chart_name'), airport_name.findall('.//pdf_name'))    # merge lists of pdfs that match chart name

        airport = airport_name.get('ID') + ':'    # define full airport name for ui output

        return dest, airport, chrt_pdfs

    def select_runway(self):

        rnwy = '28' #input('Runway: ').upper()
        return rnwy

    def create_plate_list(self, chrt_pdfs, root, rnwy):
        
        pdfs, chrts = [], []    # make dict or smth?
        
        for chart_name, pdf_name in chrt_pdfs:  

            if rnwy in (chart_name.text):                  
                chrts.append(chart_name.text)
                pdfs.append(pdf_name.text)

            elif rnwy == 'ALL':
                chrts.append(chart_name.text)
                pdfs.append(pdf_name.text)

        return chrts, pdfs

    def select_plate(self, airport, chrts, pdfs):    # ui to choose plate to be self.displayed
            
        self.display.clear() 
        draw = ImageDraw.Draw(self.display.frame_buf)   
                 
        selection = 0         

        while True:       

            y_offset = selection * 50 
            
            draw.rectangle((0, 0, 1404, 1872), fill=255, outline=255)    # clear buffer without clearing dispaly, should be function       
            draw.text((50, 50), 'SELECT APPROACH FOR ' + airport, font = self.font)                 
        
            for count, chrt in enumerate(chrts):    # self.display all the charts for previous airport/runway selection               
                draw.text((100, 150 + (count * 50)), chrt, font=self.font, fill=0)
                
            draw.rectangle((98, y_offset + 150, 700, y_offset + 202), fill=0, outline=0)    # make black backround for selection 'cursor'
            draw.text((100, y_offset + 150), chrts[selection], font=self.font, fill=255)    # make selected item text white
            self.display.draw_partial(constants.DisplayModes.DU) 
            
            key = self.peripheral.get_input(press='')    # get the users input          

            if key == 'UP' and selection >= 1:    # move up the list if not at top         
                selection -= 1

            elif key == 'UP' and selection < 1:
                selection = len(chrts) - 1

            if key == 'DOWN' and selection >= len(chrts) - 1:    # move down the list if not at bottom               
                selection = 0  

            elif key == 'DOWN' and selection < len(chrts) - 1:
                selection += 1

            if key == 'ENTER':    # create variable trgt; pdf name in tppData that matches the user selection
                trgt = pdfs[selection]                 
                return trgt
                
    def display_plate(self, trgt):    # show the plate

        width, height = self.display.width, self.display.height 
        
        try:            
            pdf = pdfium.PdfDocument(os.path.join(ROOT_DIR, 'tppData/' + trgt))    # convert from pdf to bmp (required)      
            page = pdf.get_page(0)
            pil_image = page.render(scale = 300/72).to_pil()
            image_name =f'plate.bmp'    
            pil_image.save(os.path.join(ROOT_DIR, 'ui_files/', image_name))  

        except:
            print('check tppData folder is populated')

        image1 = Image.open(os.path.join(ROOT_DIR, 'ui_files/plate.bmp'))    # open, resize, and position the bmp
        new_width1, new_height1 = int(image1.width * 0.875), int(image1.height * 0.875)
        image1 = image1.resize((new_width1, new_height1))    
        y_bottom1 = height - new_height1     
        
        self.display.frame_buf.paste(image1, (0, y_bottom1 + 143))    # paste the bmp to buffer
        self.display.draw_full(constants.DisplayModes.GC16)    # self.display the bmp

        while self.peripheral.get_input(press='') != 'ENTER':    # wait for enter, then return to select_plate
            continue


