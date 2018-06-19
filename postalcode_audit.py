import xml.etree.cElementTree as ET
import pprint
import os
import re
from collections import defaultdict
import pprint

# list for any issues found in the data
problematics = []

# OpenStreetMaps file
OSMFILE = "SLC_map.osm"

#regex to check the formatting of postal codes
postalcode_re = re.compile(r'^8\d{4}-?(\d{4})?$')


for value in postalcodes:
    value = value.replace('-', '')
    m = postalcode_re.search(value)
    if m:
        return(value)
    else:
        problematics.append(value)
    # am I to be adding to the problematics list here?

def is_postalcode(elem):
    """Check if elem is postcode"""
    return (elem.attrib['k'] == "addr:postcode" or elem.attrib['k'] == "postal_code")

def audit_postalcode(postalcodes,value):
    """Audit the format of value and return unexpecteed value"""
    m = postalcode_re.search(value)
    if not m: #if the value is not a postcode
    # is this where I would add to the problematics list?
        postalcodes.add(value)

def audit(osmfile):
    """Return expected postcode values"""
    osm_file = open(osmfile, "r")
    postalcodes = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way": #only check way and node
            for tag in elem.iter("tag"):
                if is_postalcode(tag):
                    audit_postalcode(postalcodes,tag.attrib['v'])
    osm_file.close()
    return postalcodes

postalcodes = audit(OSMFILE)
print "unexpected postal codes:"
pprint.pprint(postalcodes)
