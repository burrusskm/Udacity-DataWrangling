import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict

OSMFILE = "SLC_map.osm"
street_types = defaultdict(set)

# evaluates and matches the last word in the street name
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Circle", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "North", "East", "South", "West", "Temple", "Way", "Terrace"]

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
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    return street_types

st_types = audit(OSMFILE)
pprint.pprint(dict(st_types))
