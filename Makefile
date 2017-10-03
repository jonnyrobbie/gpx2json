GPX_DIR = ~/Documents/jonnyrobbie-cgeo-history/*.gpx
jonnyrobbie.geojson: $(GPX_DIR) gpx2json.py
	./gpx2json.py -o -j $(GPX_DIR) > jonnyrobbie.geojson
clean:
	-rm jonnyrobbie.geojson
