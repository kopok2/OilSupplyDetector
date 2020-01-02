# coding=utf-8
"""Oil location exploiter module."""

import json

OUT_FILE_PATH = "locations.json"
GEO_FILE_PATH = "doc.kml"


if __name__ == '__main__':
    # Parse file
    started = False
    name = None
    address = None
    result = []
    for line in open(GEO_FILE_PATH):
        if "<Placemark>" in line:
            started = True
        elif started:
            if "<address>" in line:
                address = line.split("<address>")[1].split("</address>")[0]
            elif "<name>" in line:
                name = line.split("<name>")[1].split("</name>")[0]
            elif "</Placemark>" in line:
                started = False
                result.append({'name': name, 'address': address})

    # Save results
    open(OUT_FILE_PATH, 'w').write(json.dumps({'locations': result}, indent=2))
