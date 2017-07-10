#!/usr/bin/python
from xml.etree import ElementTree as ET
import json, os, sys, getopt

#help text
def print_help():
	print("Usage: " + sys.argv[0] + " [options]")
	print("Options:")
	print("  -h, --help                  Print this message and exit.")
	print("  -j, --json                  Outputs geojson to stdout.")
	print("  -v, --verbose               Verbose paesing details.")

#custom print wrapper
def vprint(message):
	if verbose_print == 1:
		print(message)
def jprint(message):
	if json_print == 1:
		print(message)
		
#argument parsing
verbose_print = 0
json_print = 0
try:
	opts, args = getopt.getopt(sys.argv[1:],"hvj",["help", "verbose", "json"])
except getopt.GetoptError:
	print_help()
	sys.exit(2)
for opt, arg in opts:
	if opt in ("-h", "--help"):
		print_help()
		sys.exit()
	elif opt in ("-j", "--json"):
		json_print = 1
	elif opt in ("-v", "--verbose"):
		verbose_print = 1

#geocache variables
ns = {"tg": "http://www.topografix.com/GPX/1/0"}
features = []
unknowns_detected = []
colors = {"Geocache|Traditional Cache": "#316013",
		  "Geocache|Unknown Cache": "#0025c1",
		  "Geocache|Multi-cache": "#e56200",
		  "Geocache|Virtual Cache": "#ffffff",
		  "fallback": "#0000ff"}

gpx_dir = "gpx-exports/"
for filename in os.listdir(gpx_dir):
	vprint(20*"=")
	vprint("Parsing " + gpx_dir + filename)
	vprint(20*"-")
	#XML parsing
	tree = ET.parse(gpx_dir + filename)
	gpx = tree.getroot()
	for wpt in gpx:
		if wpt.find('tg:sym', ns).text == "Geocache Found":
			gc_name = wpt.find('tg:name', ns).text
			gc_desc = wpt.find('tg:desc', ns).text
			gc_type = wpt.find('tg:type', ns).text
			gc_lat = float(wpt.attrib['lat'])
			gc_lon = float(wpt.attrib['lon'])
			try:
				gc_color = colors[gc_type]
			except KeyError:
				gc_color = colors["fallback"]
				unknowns_detected.append(gc_type)
			vprint((gc_name, gc_type, gc_desc, gc_lat, gc_lon))
			properties = {"name": gc_name, "desc": gc_desc, "type": gc_type, "marker-color": gc_color}
			geometry = {"type": "Point", "coordinates": [gc_lon, gc_lat]}
			feature = {"type": "Feature", "properties": properties, "geometry": geometry}
			features.append(feature)
vprint(20*"=")
vprint("Detected unidentified cache types: " + str(set(unknowns_detected)))
vprint(20*"=")
geojson = {"type": "FeatureCollection", "features": features}
jprint(json.JSONEncoder(indent=2, ensure_ascii=False).encode(geojson))
