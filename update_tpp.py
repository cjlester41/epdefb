import logging
import urllib.request
import xml.etree.ElementTree as ET
import os
import requests
import xml # type: ignore

try:

    xmlurl = urllib.request.urlopen('https://aeronav.faa.gov/d-tpp/2406/xml_data/d-tpp_Metafile.xml')
    xmlrootline = str(xmlurl.read(140)).split('cycle="')[1:][0]
    newEdition = int(xmlrootline.split('"')[0])    
            
    tree = ET.parse('d-tpp_Metafile.xml')  # only read first line?
    root = tree.getroot()
    oldEdition = int(root.attrib['cycle'])

    print(oldEdition)
    print(newEdition)

    from_date = root.attrib['from_edate'].split("Z ")[1:][0]       
    to_date = root.attrib['to_edate'].split("Z ")[1:][0]
    print('Current cycle is valid from' + from_date + ' to' + to_date)
    #print("do you want to update? (y/n):") # invoke inquirer later
       
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
    oldEdition = 2404 #int(fileContents)

    if(newEdition == oldEdition):
        exit()        

    elif(newEdition - 1 == oldEdition):  # what if new year?
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

            #with open("cycle.txt", "w") as f:
                #f.write(str(newEdition))

    elif(newEdition - 1 > oldEdition): # if differnt need to dl new xml file
        update_state = input('State to update: ').upper()
        for state_codes in root.findall('.//state_code[@ID="' + update_state + '"]'):
            for chart_codes, pdf_names in zip(state_codes.findall('.//chart_code'), state_codes.findall('.//pdf_name')): 
                pdf_nam = pdf_names.text
                if(chart_codes.text != "MIN"):                    
                    download('https://aeronav.faa.gov/d-tpp/2406/' + pdf_nam, dest_folder="tppData") # variable cycle
            
            #with open("cycle.txt", "w") as f:
            #    f.write(str(newEdition))

    elif(oldEdition is None):
        with open("cycle.txt", "w") as f:
            f.write(str(newEdition))

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    exit()
