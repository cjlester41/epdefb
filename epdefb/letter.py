from statistics import median
from definitions import ROOT_DIR
import xml.etree.ElementTree as ET
import os

xml_file = os.path.join(ROOT_DIR,'tppData/d-tpp_Metafile.xml')
#xmlurl = urllib.request.urlopen('https://aeronav.faa.gov/d-tpp/2407/xml_data/d-tpp_Metafile.xml')
tree = ET.parse(xml_file)
root = tree.getroot()

first = 'P' #input('first letter: ').upper()
state = 'OR'
airports = []

first_letter = []
second_letter = []
third_letter = []

for state_codes in root.findall('.//state_code[@ID="' + state + '"]'):
    for airport_name in state_codes.findall('.//airport_name'):
        airports.append(airport_name.attrib['apt_ident'])
        #print(airports)
        
for airport in airports:
    if airport[0] not in first_letter:
        first_letter.append(airport[0])

print(sorted(first_letter))
print(median(first_letter))



