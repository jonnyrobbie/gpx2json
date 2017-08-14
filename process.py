#!/usr/bin/python
from xml.etree import ElementTree as ET
import json, os, argparse

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
colors = {"Geocache|Traditional Cache": "#02874d",
		  "Geocache|Unknown Cache": "#12508c",
		  "Geocache|Multi-cache": "#e98300",
		  "Geocache|Virtual Cache": "#ffffff",
		  "Geocache|Earthcache": "#009bbb",
		  "fallback": "#ff0000"}

for filename in args.gpx:
	if verbose_print:
		print(20*"=")
		print("Parsing " + filename)
		print(20*"-")
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

#def find_dups(l):
	#return list(set([x for x in l if l.count(x) > 1]))
#duplicates = find_dups(features)

if verbose_print:
	print(20*"=")
	print("Detected unidentified cache types: ", unknowns_detected)
	#print("Duplicate caches:", duplicates)
	print("Total caches added: ", len(features))
	print(20*"=")
geojson = {"type": "FeatureCollection", "features": features}
if json_print:
	print(json.JSONEncoder(indent=2, ensure_ascii=False).encode(geojson))
