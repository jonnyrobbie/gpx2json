#!/usr/bin/python
from xml.etree import ElementTree as ET
import json, os, argparse, logging

vcount = {2: logging.DEBUG,
		  1: logging.INFO,
		  None: logging.WARNING}

#argument parser
parser = argparse.ArgumentParser(description='Converts c:geo gpx to geojson.')
parser.add_argument("-j", "--json", help="Outputs formatted GeoJSON.", action="store_true")
parser.add_argument("-v", "--verbose", help="Verbose output.", action="count")
parser.add_argument('gpx', nargs='+', help="GPX files exported from c:geo")
args = parser.parse_args()
if args.json == True:
	json_print = 1
else:
	json_print = 0

logging.basicConfig(level=vcount[args.verbose])

#geocache variables
ns = {"tg": "http://www.topografix.com/GPX/1/0"}
features = []
unknowns_detected = []
names = []
colors = {"Geocache|Traditional Cache": "#02874d",
		  "Geocache|Unknown Cache": "#12508c",
		  "Geocache|Multi-cache": "#e98300",
		  "Geocache|Virtual Cache": "#ffffff",
		  "Geocache|Earthcache": "#009bbb",
		  "fallback": "#ff0000"}

for filename in args.gpx:
	logging.info("====================")
	logging.info("Parsing %s", filename)
	logging.info("--------------------")
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
			logging.info("%s %s %s %f %f", gc_name, gc_type, gc_desc, gc_lat, gc_lon)
			properties = {"title": gc_name, "description": gc_desc, "type": gc_type, "marker-color": gc_color, "stroke-width": "1", "marker-symbol": "circle"}
			geometry = {"type": "Point", "coordinates": [gc_lon, gc_lat]}
			feature = {"type": "Feature", "properties": properties, "geometry": geometry}
			features.append(feature)
			names.append(gc_name)

def find_dups(l):
	return list(set([x for x in l if l.count(x) > 1]))
duplicates = find_dups(names)

logging.info("====================")
logging.info("Detected unidentified cache types: %i", len(unknowns_detected))
logging.info("Duplicate caches: %i", len(duplicates))
if len(duplicates) != 0: logging.info("List of diplicates: %s", duplicates)
logging.info("Total caches added: %i", len(features))
logging.info("====================")
geojson = {"type": "FeatureCollection", "features": features}
if json_print:
	print(json.JSONEncoder(indent=2, ensure_ascii=False).encode(geojson))
