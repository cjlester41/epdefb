import os
import logging
import xml.etree.ElementTree as ET
import pypdfium2 as pdfium
import epdemulator 
from PIL import Image, ImageFont
from getkey import getkey, keys
import sys
sys.path.insert(1, '/usr/local/bin')
import paperpi

current_dir = os.path.dirname(os.path.abspath(__file__))
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

epd = epdemulator.EPD(config_file="epd10in3", use_tkinter=False, use_color=False, update_interval=1, reverse_orientation=False)
epd.init()    
width, height = epd.width, epd.height     
font = ImageFont.truetype(os.path.join(current_dir, 'Arial.ttf'), 48)

try:
    
    tree = ET.parse(os.path.join(current_dir, "d-tpp_Metafile.xml"))
    root = tree.getroot()       
    dest = 'PDX' #input('Destination: ').upper()
    rnwy = '28' #input('Runway: ').upper()
    pdfs = []
    chrts = []

    for airport_name in root.findall('.//airport_name[@apt_ident="' + dest + '"]'):
        for chart_name, pdf_name in zip(airport_name.findall(".//chart_name"), airport_name.findall(".//pdf_name")):
            if rnwy in (chart_name.text):                
                chrts.append(chart_name.text)
                pdfs.append(pdf_name.text)
            elif rnwy == 'ALL':
                chrts.append(chart_name.text)
                pdfs.append(pdf_name.text)

except:
    print('xml error')


class chart():
   
    def select_plate():
            
        y = 150
        c = 0
        epd.Clear(255)
        draw = epd.draw
        i = 0        

        while True:

            epd.Clear(255)    ##############
            draw = epd.draw   ##############
            draw.text((50, 50),"SELECT APPROACH FOR " + airport_name.get('ID') + ":", font=font, fill=0)
            i = 0
        
            for chrt in chrts:               
                draw.text((50, 150 + (i * 50)), chrt, font=font, fill=0)
                i += 1

            draw.rectangle((50, y, 600, y + 52), fill=0, outline=0)
            draw.text((50, y), chrts[c], font=font, fill=255)        

            image_buffer = epd.get_frame_buffer(draw)
            epd.display(image_buffer) 

            key = getkey()
            if key == keys.UP:               
                y -= 50
                c -= 1
            if key == keys.DOWN:                
                y += 50 
                c += 1   
            if key == keys.ENTER:
                chart.select_plate.trgt = pdfs[c]      
                break      

    def display_plate():

        pdf = pdfium.PdfDocument('tppData/' + chart.select_plate.trgt)
        page = pdf.get_page(0)
        pil_image = page.render(scale = 300/72).to_pil()
        image_name =f"plate.bmp"
        pil_image.save(image_name)  

        image1 = Image.open(os.path.join(current_dir, 'plate.bmp'))
        new_width1, new_height1 = int(image1.width * 0.75), int(image1.height * 0.75)
        image1 = image1.resize((new_width1, new_height1))
        x_center1 = (width - new_width1) // 2
        y_bottom1 = height - new_height1
        
        draw = epd.draw
        epd.Clear(255)
        epd.paste_image(image1, (x_center1, y_bottom1 - 1))
        image_buffer = epd.get_frame_buffer(draw)
        epd.display(image_buffer)

        input('Press enter to go back')

try:
        
    while(True):

        chart.select_plate()
        chart.display_plate()      

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    exit()

