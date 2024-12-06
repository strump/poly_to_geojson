 # Scripts to convert *.POLY files

## poly_to_geojson

Use `poly_to_geojson.py` script to convert batch of POLY files into single
Geojson file or multiple Geojson files.

```shell
python poly_to_geojson.py /path/to/organicmaps/data/borders \
       -o data/borders_all.geojson \ 
       -d data/borders_geojson
```

If you need only single Geojson with all borders included:
(Warning: generated file could be too large to work with)

```shell
python poly_to_geojson.py /path/to/organicmaps/data/borders \
       -o data/borders_all.geojson
```

If you need multiple Geojson`s:

```shell
python poly_to_geojson.py /path/to/organicmaps/data/borders \
       -d data/borders_geojson
```

## generate_borders_tree

Use `generate_borders_tree.py` script to convert `countries.txt` file into
JSON suitable for Vue.js frontend. (TODO: add link to frontend repo)

```shell
generate_borders_tree.py /path/to/organicmaps/data/countries.txt \
    -o data/borders_tree.json
```

## Generate TopoJson

Single Geojson file with all borders could be converted to
[TopoJson](https://github.com/topojson/topojson-specification) format.
First install [`pytopojson`](https://pypi.org/project/pytopojson/). Then run

```shell
geo2topo -o data/borders_all.topojson \
    data/borders_all.geojson
```

## Vector tiles

Visualize all borders is hard problem for modern PC. It required a lot of
memory to render 1148 border polygons on a map. To make it possible one can
convert `data/borders_geojson/*.geojson` files into static vector tiles.
After that MapBox.js would be able to show polygons with ease.

First install [tippecanoe](https://github.com/mapbox/tippecanoe) tool.

Then run it to generate static *.PBF files for vector layer:

```shell
tippecanoe -e data/borders_tiles \
    --drop-densest-as-needed --extend-zooms-if-still-dropping \
    -Z0 -z10 \
    --no-tile-compression \
    -l borders \
    --allow-existing \
    data/borders_geojson/*.geojson
```

Generating deep zooms could take significant amount of time. Here are my benchmarks with
MacBook M2 Pro, 16 GB RAM:

* Zooms 0-9 => runs for 20 sec, generates 236 779 PBF files, 52 MB
* Zooms 0-10 => runs for 3 minutes, generates 932 115 PBF files, 144 MB
* Zooms 0-11 => runs for 8-14 minutes, generates 3 696 828 PBF files, 478 MB (time to delete - 15 min)
* Zooms 0-12 => runs for 43 minutes, generates 14 722 520 PBF files, 1762 MB (time to delete - 1 hour)

To preview vector tiles use `preview.html` file. You can run static server with:

```shell
python3 -m http.server
```
