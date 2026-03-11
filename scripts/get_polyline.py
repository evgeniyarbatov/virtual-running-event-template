import sys
import json
import gpxpy
import polyline


def gpx_to_polyline(gpx_file_path):
    with open(gpx_file_path, "r") as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    coordinates = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                coordinates.append((point.latitude, point.longitude))

    encoded = polyline.encode(coordinates)

    return {"polyline": encoded}


def save_to_json(data, output_path):
    with open(output_path, "w") as json_file:
        json.dump(data, json_file, indent=2)


def main(
    route_gpx,
    polyline_json,
):
    result = gpx_to_polyline(route_gpx)
    save_to_json(result, polyline_json)


if __name__ == "__main__":
    main(*sys.argv[1:])
