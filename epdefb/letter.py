from statistics import median
from definitions import ROOT_DIR
import xml.etree.ElementTree as ET
import os

xml_file = os.path.join(ROOT_DIR,'tppData/d-tpp_Metafile.xml')
#xmlurl = urllib.request.urlopen('https://aeronav.faa.gov/d-tpp/2407/xml_data/d-tpp_Metafile.xml')
tree = ET.parse(xml_file)
root = tree.getroot()

first = 'P' #input('first letter: ').upper()
second = 'D'
states = ['OR','WA','CA']
airports = []

first_letter = []
second_letter = []
third_letter = []

for state in states:
    for state_codes in root.findall('.//state_code[@ID="' + state + '"]'):
        for airport_name in state_codes.findall('.//airport_name'):
            airports.append(airport_name.attrib['apt_ident'])
            #print(airports)
        
for airport in airports:
    if airport[0] not in first_letter:
        first_letter.append(airport[0])

print(sorted(first_letter))
#print(median(first_letter))

for airport in airports:
    if airport[0] == first and airport[1] not in second_letter:
        second_letter.append(airport[1])

print(sorted(second_letter))
#print(median(second_letter))

for airport in airports:
    if airport[1] == second and airport[2] not in third_letter:
        third_letter.append(airport[2])

print(sorted(third_letter))



