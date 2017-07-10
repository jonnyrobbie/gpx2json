jonnyrobbie.geojson: process.py gpx-exports/*
	./process.py -j > jonnyrobbie.geojson
clean:
	rm jonnyrobbie.geojson
