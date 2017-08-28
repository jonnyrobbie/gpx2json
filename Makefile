GPX_DIR = ~/Documents/jonnyrobbie-cgeo-history/*
jonnyrobbie.geojson: $(GPX_DIR) process.py
	./gpx2json.py -j $(GPX_DIR) > jonnyrobbie.geojson
clean:
	-rm jonnyrobbie.geojson
