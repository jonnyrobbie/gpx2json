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

Needs non-standard python module `gpxpy` to be installed. Do `pip install gpxpy` or make sure it's installed otherwise.

You can use the script as a standalone, or you can customize the makefile and do `make` after every addition to your gpx folder. You might also want to modify the line 2 of docs/script.js.

---

Github does some neat automatic rendering, so I'm also hosting my personal geocache history here.
[Mobile friendly map rendering.](https://jonnyrobbie.github.io/gpx2json/)
