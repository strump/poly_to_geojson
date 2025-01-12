import argparse
import os
import json
from pathlib import Path
import hashlib

import sys


def parse_poly_files(borders_dir: str):
    borders_dir = Path(borders_dir)
    for filepath in borders_dir.iterdir():
        if filepath.is_file() and filepath.suffix == ".poly":
            print(f"Parsing {filepath} ...")
            yield parse_poly_coords(filepath)

def parse_poly_coords(filepath):
    with open(filepath, "rt") as fin:
        name = None
        polygon_index = None
        polygons = []
        current_poly = []
        for line in fin:
            line = line.rstrip()
            if line == "END":
                if polygon_index is not None:
                    # close current polygon
                    polygon_index = None
                    polygons.append(current_poly)
                    current_poly = []
                else:
                    # reached the end of the file
                    pass
                continue
            if name is None:
                name = line
                continue
            if polygon_index is None:
                polygon_index = int(line)
                continue
            if line.startswith("\t") or line.startswith("   "):
                lat, lon = line.strip().split()
                current_poly.append( (float(lat), float(lon)) )
            else:
                raise Exception(f"Unknown line: `{line}`")
    return name, polygons

def name2color(name):
    m = hashlib.sha256()
    m.update(name.encode('UTF8'))
    return "#" + m.hexdigest()[-6:]

# Generates GeoJson object with each border as a separate feature
def polys_to_single_geojson(borders):
    features = []

    for name, polygons in borders:
        feature = {
          "type": "Feature",
          "properties": {
            "title": name,
            "fill": name2color(name), #555555
          }
        }

        # Set geometry
        if len(polygons) == 1:
            feature["geometry"] = {
                "type": "Polygon",
                "coordinates": polygons,
            }
        else:
            feature["geometry"] = {
                "type": "MultiPolygon",
                "coordinates": [[poly] for poly in polygons],
            }

        features.append(feature)

    return { "type": "FeatureCollection",
             "features": features }

# Generates GeoJson object with each border as a separate feature
def poly_to_geojson(name, polygons, output_dir: Path):
    print(f"Saving {name}.geojson ...")
    # Build GeoJson object
    feature = {
      "type": "Feature",
      "properties": {
        "title": name,
        "fill": name2color(name), #555555
      }
    }

    # Set geometry
    if len(polygons) == 1:
        feature["geometry"] = {
            "type": "Polygon",
            "coordinates": polygons,
        }
    else:
        feature["geometry"] = {
            "type": "MultiPolygon",
            "coordinates": [[poly] for poly in polygons],
        }

    geojson = { "type": "FeatureCollection",
                "features": [feature] }

    # Export 'geojson' to {name}.geojson file
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / f"{name}.geojson", "wt") as fout:
        json.dump(geojson, fout)

def save_poly_to_geojsons(borders_dir: str, output_dir: Path):
    print("Loading POLY files")
    borders = parse_poly_files(borders_dir)
    for name, polygons in borders:
        poly_to_geojson(name, polygons, output_dir)

def save_poly_to_single_geojson(borders_dir: str, output_file: str):
    print("Loading POLY files")
    borders = parse_poly_files(borders_dir)
    geojson = polys_to_single_geojson(borders)

    print("Saving GEOJSON")
    directory = os.path.dirname(output_file)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(output_file, "wt") as fout:
        json.dump(geojson, fout, indent=2)

def main():
    parser = argparse.ArgumentParser(
        description="Converts *.poly wiles with borders geometry from OrganicMaps data to Geojson format.\n"
                    "Could generate new Geojson file for each poly file or merge all polygons into a single Geojson file."
    )

    parser.add_argument(
        "-o",
        "--out",
        dest="file",
        help="output Geojson file",
        default=None,
    )
    parser.add_argument(
        "-d",
        "--dir",
        dest="dir",
        help="output directory for multiple Geojson output",
        default=None,
    )
    parser.add_argument(
        "borders_dir",
        metavar="borders_dir",
        type=str,
        help="path to directory with *.poly files from OrganicMaps data",
    )

    opts = parser.parse_args()
    kwargs = vars(opts)

    if kwargs["file"] is None and kwargs["dir"] is None:
        print("Either output `file` or `dir` should be specified", file=sys.stderr)
        exit(1)

    if kwargs["file"] is not None:
        save_poly_to_single_geojson(kwargs["borders_dir"], kwargs["file"])

    if kwargs["dir"] is not None:
        output_dir = Path(kwargs["dir"])
        save_poly_to_geojsons(kwargs["borders_dir"], output_dir)


if __name__ == '__main__':
    main()

