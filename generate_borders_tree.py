import argparse
import json
import sys

def countries2borders(countries):
    """ Generate json in format:
    {
      "key": "Argentina",
      "label": "Documents",
      "icon": "pi pi-fw pi-inbox",
      "children": [
        {...}
      ]
    }
    """
    borders = []
    for cntr in countries:
        if cntr["id"].startswith("World"):
            continue
        brdr = {
            "key": cntr["id"],
            "label": cntr["id"],
            "icon": "pi pi-fw pi-inbox"
        }
        if "g" in cntr:
            brdr["children"] = countries2borders(cntr["g"])

        borders.append(brdr)

    return borders

def countries_to_tree_json(filename, out_stream):
    print("Loading `countries.txt` file ...", file=sys.stderr)
    with open(filename, "rt") as fin:
        countries = json.load(fin)

    print("Converting to JSON for Vue.js frontend ...", file=sys.stderr)
    borders = countries2borders(countries["g"])

    print("Exporting to JSON ...", file=sys.stderr)
    json.dump(borders, out_stream, indent=2)

    print("Done!", file=sys.stderr)

def main():
    # Create OptionParser object and set options
    parser = argparse.ArgumentParser(
        description="Converts countries.txt from OrganicMaps data to simplified JSON used by Vue.js tree component."
    )

    parser.add_argument(
        "-o",
        "--out",
        dest="file",
        help="output file name; defaults to “-” for stdout",
        default="-",
    )
    parser.add_argument(
        "countries_txt",
        type=str,
        help="path to file countries.txt from OrganicMaps data",
    )

    # Parse and store the command-line arguments in dictionary
    opts = parser.parse_args()
    kwargs = vars(opts)

    out_stream = sys.stdout
    if kwargs["file"] and kwargs["file"] != "-":
        out_stream = open(kwargs["file"], "wt")

    countries_to_tree_json(kwargs["countries_txt"], out_stream)
    if out_stream is not sys.stdout:
        out_stream.close()

if __name__ == '__main__':
    main()
