OSMFILE = "SLC_map.osm"

postalcode_re = re.compile(r'^8\d{4}-?(\d{4})?$')

def is_postalcode(elem):
    """Check if elem is postcode"""
    return (elem.attrib['k'] == "addr:postcode" or elem.attrib['k'] == "postal_code")

def audit_postalcode(postalcodes,value):
    """Audit the format of value and return unexpecteed value"""
    m = postalcode_re.search(value)
    if not m: #if the value is not a postcode
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
