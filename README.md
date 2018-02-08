This python script is used to convert GPX files exported by C:GEO geocaching application to GeoJSON format.


```
usage: gpx2json.py [-h] [-j] [-o] [-v] [-p] gpx [gpx ...]

Converts c:geo gpx to geojson.

positional arguments:
  gpx             GPX files exported from c:geo

optional arguments:
  -h, --help      show this help message and exit
  -j, --json      Outputs formatted GeoJSON.
  -o, --original  Exports location of 'Original Coordinates' waypoint instead
                  of changed cache location.
  -v, --verbose   Verbose output.
  -p, --premium   Protect premium caches by adding random noise to degrees.
```

Needs non-standard library `gpxpy` to be installed.

---

Github does some neat automatic rendering, so I'm also hosting my personal geocache history here.
[Mobile friendly map rendering.](https://jonnyrobbie.github.io/gpx2json/)
