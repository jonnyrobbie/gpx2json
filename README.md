The pytohn script is used to convert GPX files exported by C:GEO geocaching application to GeoJSON format.
Since Github does some neat nifty automatic map rendering for GeoJSON files, I'm also hosting my found caches here on this repo.

```
usage: gpx2json.py [-h] [-j] [-v] gpx [gpx ...]

Converts c:geo gpx to geojson.

positional arguments:
  gpx            GPX files exported from c:geo

optional arguments:
  -h, --help     show this help message and exit
  -j, --json     Outputs formatted GeoJSON.
  -v, --verbose  Outputs cache parsing details.
```

Needs non-standard library `gpxpy` to be installed.
