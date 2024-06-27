import os
import logging
import xml.etree.ElementTree as ET
import pypdfium2 as pdfium
import argparse
import epdemulator
from IT8951 import constants
from IT8951.display import AutoEPDDisplay
from PIL import Image, ImageFont, ImageDraw
from getkey import getkey, keys

current_dir = os.path.dirname(os.path.abspath(__file__))
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

p = argparse.ArgumentParser(description='Test EPD functionality')
p.add_argument('-v', '--virtual', action='store_true')
args = p.parse_args()

if not args.virtual:    
    display = AutoEPDDisplay(vcom=-1.71, spi_hz=24000000, rotate='CW')
else:    
    display = epdemulator.EPD(update_interval=1)

width, height = display.width, display.height     
font = ImageFont.truetype(os.path.join(current_dir, 'Arial.ttf'), 48)

try:
    
    tree = ET.parse(os.path.join(current_dir, "d-tpp_Metafile.xml"))
    root = tree.getroot()       
    dest = 'PDX' #input('Destination: ').upper()
    rnwy = '28' #input('Runway: ').upper()
    pdfs, chrts = [], [] 
    
    for airport_name in root.findall('.//airport_name[@apt_ident="' + dest + '"]'):
        chrt_pdfs = zip(airport_name.findall(".//chart_name"), airport_name.findall(".//pdf_name"))
        for chart_name, pdf_name in chrt_pdfs:
            if rnwy in (chart_name.text):                
                chrts.append(chart_name.text)
                pdfs.append(pdf_name.text)
            elif rnwy == 'ALL':
                chrts.append(chart_name.text)
                pdfs.append(pdf_name.text)

except:
    print('check d-tpp metafile file present')

def select_plate():
        
    display.clear() 
    y = 150
    c, i = 0, 0         

    while True:
       
        draw = ImageDraw.Draw(display.frame_buf) 
        draw.rectangle((0, 0, 1404, y + 1872), fill=255, outline=255)         
        draw.text((50, 50), "SELECT APPROACH FOR " + airport_name.get('ID') + ":", font = font)
        #i = 0        
    
        for chrt in chrts:               
            draw.text((100, 150 + (i * 50)), chrt, font=font, fill=0)
            i += 1

        draw.rectangle((98, y, 700, y + 52), fill=0, outline=0)
        draw.text((100, y), chrts[c], font=font, fill=255) 
        display.draw_partial(constants.DisplayModes.DU) 

        key = getkey()
        if key == keys.UP:               
            y -= 50
            c -= 1
        if key == keys.DOWN:                
            y += 50 
            c += 1   
        if key == keys.ENTER:
            select_plate.trgt = pdfs[c]      
            break      

def display_plate():    
    
    try:
        pdf = pdfium.PdfDocument('tppData/' + select_plate.trgt)
        page = pdf.get_page(0)
        pil_image = page.render(scale = 300/72).to_pil()
        image_name =f"plate.bmp"    
        pil_image.save(image_name)  
    except:
        print('check tppData folder is populated')

    image1 = Image.open(os.path.join(current_dir, 'plate.bmp'))
    new_width1, new_height1 = int(image1.width * 0.875), int(image1.height * 0.875)
    image1 = image1.resize((new_width1, new_height1))    
    y_bottom1 = height - new_height1     
    
    display.frame_buf.paste(image1, (0, y_bottom1 + 143))
    display.draw_full(constants.DisplayModes.DU)#GC16)

    input('Press enter to go back')

try:
        
    while(True):

        select_plate()
        display_plate()      

except IOError as e:   
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    display.clear()
    exit()

