import logging
import urllib.request
import xml.etree.ElementTree as ET
import os, ast
import requests
# from interface.IT8951 import constants
# from PIL import Image, ImageFont, ImageDraw
# from definitions import ROOT_DIR
from states import us_states


try:

    xmlurl = urllib.request.urlopen('https://aeronav.faa.gov/d-tpp/2407/xml_data/d-tpp_Metafile.xml') # need to find new cycle first for url to work
    xmlrootline = str(xmlurl.read(140)).split('cycle="')[1:][0]
    newEdition = int(xmlrootline.split('"')[0])    
            
    tree = ET.parse('d-tpp_Metafile.xml')  # only read first line?
    root = tree.getroot()
    oldEdition = int(root.attrib['cycle'])
    airport_codes = []

    print(oldEdition)
    print(newEdition)

    from_date = root.attrib['from_edate'].split("Z ")[1:][0]       
    to_date = root.attrib['to_edate'].split("Z ")[1:][0]
    print('Current cycle is valid from' + from_date + ' to' + to_date)    
       
    def download(url: str, dest_folder: str):
        filename = url.split('/')[-1].replace(" ", "_")        
        file_path = os.path.join(dest_folder, filename)

        r = requests.get(url, stream=True)  # use urllib?
        if r.ok:
            print("saving to", os.path.abspath(file_path))
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 8):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        os.fsync(f.fileno())
        else:  
            print("Download failed: status code {}\n{}".format(r.status_code, r.text))
        
    #with open('cycle.txt', 'r') as file:
    #    fileContents = file.read().rstrip()  #int()
    #    if fileContents != "":
    

    def single_update():    

        print('single cycle update')
        xmlu = urllib.request.urlopen('https://external-api.faa.gov/apra/dtpp/chart?edition=changeset')
        tree = ET.parse(xmlu)
        root = tree.getroot()

        for pdfDownloads in root.findall('.//{http://arpa.ait.faa.gov/arpa_response}product'):
            pdf_url = pdfDownloads.get('url')
            print(pdf_url)
            furl = pdf_url.replace('tpp', 'tpp/' + newEdition)     
            print('downloading ' + furl)
            download(furl, dest_folder="tppData") 

            with open("cycle.txt", "w") as f:
                f.write(str(newEdition))

    def full_update(): # if differnt need to dl new xml file

        with open("states.txt", "r") as f:
            update_states = f.read()

        update_states = ast.literal_eval(update_states) # input('State to update: ').upper()

        for update_state in update_states:
        
            for state_codes in root.findall('.//state_code[@ID="' + update_state + '"]'):

                for airport_ident in state_codes.findall('.//airport_name'):                
                    airport_codes.append(airport_ident.attrib['apt_ident'])

                for chart_codes, pdf_names in zip(state_codes.findall('.//chart_code'), state_codes.findall('.//pdf_name')): 
                    pdf_name = pdf_names.text
                    if(chart_codes.text == "IAP" and not os.path.exists('tppData/' + pdf_name)):                    
                        download('https://aeronav.faa.gov/d-tpp/2407/' + pdf_name, dest_folder="tppData") # variable cycle

            first_chr, secnd_chr, third_chr = [], [] ,[]

            for airport_code in airport_codes:
                first_chr.append(airport_code[0])
                secnd_chr.append(airport_code[1])
                third_chr.append(airport_code[2])
        
        airport_chrs = [sorted(set(first_chr)), sorted(set(secnd_chr)), sorted(set(third_chr))]

        with open("airports.txt", "w") as f:
            f.write(str(airport_codes))

        with open("characters.txt", "w") as f:
            f.write(str(airport_chrs))

        # with open("cycle.txt", "w") as f:
        #     f.write(str(newEdition))

    oldEdition = 2404 #int(fileContents)
 
    if(newEdition == oldEdition):
        exit()        

    elif(newEdition - 1 == oldEdition):  # what if new year?
        single_update()

    elif(newEdition - 1 > oldEdition):
        full_update()

    elif(oldEdition is None):
        with open("cycle.txt", "w") as f:
            f.write(str(newEdition))

    
except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    exit()
