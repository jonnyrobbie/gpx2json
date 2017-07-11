#!/usr/bin/python
from xml.etree import ElementTree as ET
import json, os, argparse

#custom print wrapper
def vprint(message):
	if verbose_print == 1:
		print(message)
def jprint(message):
	if json_print == 1:
		print(message)
		

#argument parser
parser = argparse.ArgumentParser(description='Converts c:geo gpx to geojson.')
parser.add_argument("-j", "--json", help="Outputs formatted GeoJSON.", action="store_true")
parser.add_argument("-v", "--verbose", help="Outputs cache parsing details.", action="store_true")
parser.add_argument('gpx', nargs='+', help="GPX files exported from c:geo")
args = parser.parse_args()
if args.json == True:
	json_print = 1
else:
	json_print = 0
if args.verbose == True:
	verbose_print = 1
else:
	verbose_print = 0

#geocache variables
ns = {"tg": "http://www.topografix.com/GPX/1/0"}
features = []
unknowns_detected = []
colors = {"Geocache|Traditional Cache": "#316013",
		  "Geocache|Unknown Cache": "#0025c1",
		  "Geocache|Multi-cache": "#e56200",
		  "Geocache|Virtual Cache": "#ffffff",
		  "fallback": "#00ff00"}

for filename in args.gpx:
	if verbose_print:
		vprint(20*"=")
		vprint("Parsing " + filename)
		vprint(20*"-")
	#XML parsing
	tree = ET.parse(filename)
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
			if verbose_print: print(gc_name, gc_type, gc_desc, gc_lat, gc_lon)
			properties = {"name": gc_name, "desc": gc_desc, "type": gc_type, "marker-color": gc_color}
			geometry = {"type": "Point", "coordinates": [gc_lon, gc_lat]}
			feature = {"type": "Feature", "properties": properties, "geometry": geometry}
			features.append(feature)
if verbose_print:
	vprint(20*"=")
	vprint("Detected unidentified cache types: " + str(set(unknowns_detected)))
	vprint(20*"=")
geojson = {"type": "FeatureCollection", "features": features}
if json_print:
	print(json.JSONEncoder(indent=2, ensure_ascii=False).encode(geojson))
