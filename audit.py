import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "SLC_map.osm"

# regular expressions from case study that evaluate tag patterns
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# evaluates and matches the last word in a street name
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
# Checks for 5 or 9 digit postal codes, and that first digit is 8
postalcode_re = re.compile(r'^8\d{4}-?(\d{4})?$')

street_types = defaultdict(set)
tags = {}

expected_street = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Circle", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "North", "East", "South", "West", "Temple", "Way"]

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

# find all tags with the street address
def is_street_name(elem):
    return (elem.attrib['k'] == 'addr:street')

# find all postal code tags
def is_postalcode(elem):
    return (elem.attrib['k'] == "addr:postcode" or elem.attrib['k'] == "postal_code")

# audit street types
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type in mapping.keys():
            street_type = mapping[street_type]
        if street_type not in expected_street:
            street_types[street_type].add(street_name)

# audit postal code format and values
def audit_postalcode(postalcode, value):
    m = postalcode_re.search(value)
    if not m:
        postalcodes.add(value)


# postcode = ''.join(ele for ele in postcode if ele.isdigit())

# evaluate and return unexpected street names
def audit():
    osm_file = open(OSMFILE, "r")
    postalcodes = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                if is_postalcode(tag):
                    audit_postalcode(postalcode, tag.attrib['v'])

            osm_file.close()

            return postalcodes, street_types


pprint.pprint(dict(street_types))
pprint.pprint(postalcodes)


if __name__ == "__main__":
    audit()
