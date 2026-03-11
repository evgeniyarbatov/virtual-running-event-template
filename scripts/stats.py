import sys
import json
import gpxpy

from geopy.distance import geodesic


def calculate_total_distance(gpx_file_path):
    with open(gpx_file_path, "r") as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    coords = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                coords.append((point.latitude, point.longitude))

    total_distance_km = 0.0
    for i in range(1, len(coords)):
        total_distance_km += geodesic(coords[i - 1], coords[i]).km

    distance_miles = total_distance_km * 0.621371

    return {
        "distance_km": round(total_distance_km, 2),
        "distance_miles": round(distance_miles, 2),
    }


def save_to_json(data, output_path):
    with open(output_path, "w") as json_file:
        json.dump(data, json_file, indent=2)


def main(
    route_gpx,
    sumary_json,
):
    distance_data = calculate_total_distance(route_gpx)
    save_to_json(distance_data, sumary_json)


if __name__ == "__main__":
    main(*sys.argv[1:])
