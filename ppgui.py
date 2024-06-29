import os, logging, time
import xml.etree.ElementTree as ET
import pypdfium2 as pdfium
import argparse
import usrinput
from IT8951 import constants
from PIL import Image, ImageFont, ImageDraw


current_dir = os.path.dirname(os.path.abspath(__file__))
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

emulate = argparse.ArgumentParser(description='enable emulator')
emulate.add_argument('-v', '--virtual', action='store_true')
args = emulate.parse_args()

if not args.virtual:     
    from IT8951.display import AutoEPDDisplay
    display = AutoEPDDisplay(vcom=-1.71, spi_hz=24000000, rotate='CW')
    peripheral = usrinput.get_gpio

else:    
    import epdemulator
    display = epdemulator.EPD(update_interval=1)
    peripheral = usrinput.get_key

width, height = display.width, display.height     
font = ImageFont.truetype(os.path.join(current_dir, 'Arial.ttf'), 48)

pdfs, chrts = [], [] 
airport = ''

try:    
    tree = ET.parse(os.path.join(current_dir, 'd-tpp_Metafile.xml'))
    root = tree.getroot() 

except:
    print('check d-tpp metafile file present') 

class plates():

    def next_alpha(s):
            return chr((ord(s.upper())+1 - 65) % 26 + 65)
    
    def prev_alpha(s):
            return chr((ord(s.upper())-1 - 65) % 26 + 65)

    def select_airport():
        
        s = 'K'        
        x = 100
        
        display.clear() 
        draw = ImageDraw.Draw(display.frame_buf) 
        draw.text((50, 50), 'SELECT DESTINATION AIRPORT:', font = font)
        draw.rectangle((x, 150, 134, 200), fill=0, outline=0)
        draw.text((x, 150), s, font = font, fill=255)
        display.draw_partial(constants.DisplayModes.DU) 

        while True:            

            key = peripheral.get_input(press='')          

            if key == 'UP':   
                display.clear()        
                draw.rectangle((x, 150, x + 34, 200), fill=0, outline=0)
                s = plates.prev_alpha(s)
                draw.text((x, 150), s, font = font, fill=255)
                display.draw_partial(constants.DisplayModes.DU)
                    

            if key == 'DOWN':               
                display.clear()        
                draw.rectangle((x, 150, x + 34, 200), fill=0, outline=0)
                s = plates.next_alpha(s)
                draw.text((x, 150), s, font = font, fill=255)
                display.draw_partial(constants.DisplayModes.DU)

            if key == 'ENTER':
                x += 50   
                #break  

            #display.draw_partial(constants.DisplayModes.DU) 

            #time.sleep(3)

        dest = 'PDX' #input('Destination: ').upper()
        rnwy = '28' #input('Runway: ').upper()
        global pdfs, chrts, airport
        
        for airport_name in root.findall('.//airport_name[@apt_ident="' + dest + '"]'):
            chrt_pdfs = zip(airport_name.findall('.//chart_name'), airport_name.findall('.//pdf_name'))

            for chart_name, pdf_name in chrt_pdfs:

                if rnwy in (chart_name.text):                
                    chrts.append(chart_name.text)
                    pdfs.append(pdf_name.text)

                elif rnwy == 'ALL':
                    chrts.append(chart_name.text)
                    pdfs.append(pdf_name.text)

        airport = airport_name.get('ID') + ':'

    def select_plate():
            
        display.clear() 
        draw = ImageDraw.Draw(display.frame_buf) 
        y = 150
        c, line = 0, 0         

        while True:        
            
            draw.rectangle((0, 0, 1404, y + 1872), fill=255, outline=255)         
            draw.text((50, 50), 'SELECT APPROACH FOR ' + airport, font = font)
            line = 0        
        
            for chrt in chrts:               
                draw.text((100, 150 + (line * 50)), chrt, font=font, fill=0)
                line += 1

            draw.rectangle((98, y, 700, y + 52), fill=0, outline=0)
            draw.text((100, y), chrts[c], font=font, fill=255) 
            display.draw_partial(constants.DisplayModes.DU) 
            
            key = peripheral.get_input(press='')          

            if key == 'UP' and c != 0:            
                y -= 50
                c -= 1

            if key == 'DOWN' and c < (len(chrts) - 1):                
                y += 50 
                c += 1  

            if key == 'ENTER':
                plates.select_plate.trgt = pdfs[c]      
                break      

    def display_plate():    
        
        try:
            pdf = pdfium.PdfDocument('tppData/' + plates.select_plate.trgt)
            page = pdf.get_page(0)
            pil_image = page.render(scale = 300/72).to_pil()
            image_name =f'plate.bmp'    
            pil_image.save(image_name)  

        except:
            print('check tppData folder is populated')

        image1 = Image.open(os.path.join(current_dir, 'plate.bmp'))
        new_width1, new_height1 = int(image1.width * 0.875), int(image1.height * 0.875)
        image1 = image1.resize((new_width1, new_height1))    
        y_bottom1 = height - new_height1     
        
        display.frame_buf.paste(image1, (0, y_bottom1 + 143))
        display.draw_full(constants.DisplayModes.GC16)

        while peripheral.get_input(press='') != 'ENTER':
            continue

try:
        
    while(True):
        plates.select_airport()

        while(True):
            plates.select_plate()
            plates.display_plate()      

except IOError as e:   
    logging.info(e)

except KeyboardInterrupt:
    logging.info('ctrl + c:')
    display.clear()
    exit()

