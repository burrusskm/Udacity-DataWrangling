import xml.etree.cElementTree as ET
import pprint
import os
import re
from collections import defaultdict
import pprint

OSMFILE = "SLC_map.osm"

# evaluates and matches the last word in the street name
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Circle", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "North", "East", "South", "West", "Temple", "Way", "Terrace"]

mapping = { "St": "Street",
            "St.": "Street",
            "Rd.": "Road",
            "Rd": "Road",
            "Ave.": "Avenue",
            "Ave": "Avenue",
            "Dr": "Drive",
            "Dr.": "Drive",
            "W": "West",
            "S": "South",
            "W.": "West"
          }

# evaluate if the tag is the street address
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

# this function is to update the street names to what's specified in the mapping dict, e.g. Ave.-->Avenue
def update_name(name, mapping):
    for search_error in mapping:
        if search_error in name:
            name = re.sub(r'\b' + search_error + r'\b\.?', mapping[search_error], name)

    return name


st_types = audit(OSMFILE)
pprint.pprint(dict(st_types))
