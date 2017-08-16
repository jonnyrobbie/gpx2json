GPX_DIR = ~/Documents/jonnyrobbie-cgeo-history/*
jonnyrobbie.geojson: $(GPX_DIR) process.py
	./process.py -j $(GPX_DIR) > jonnyrobbie.geojson
clean:
	-rm jonnyrobbie.geojson
