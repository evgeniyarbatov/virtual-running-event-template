import sys
import gpxpy

from geopy.geocoders import Nominatim
from geopy.distance import geodesic


def compute_distance(p1, p2):
    return geodesic((p1.latitude, p1.longitude), (p2.latitude, p2.longitude)).km


def get_point(gpx_file_path, distance):
    with open(gpx_file_path, "r") as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    point = None
    total_distance = 0.0

    for track in gpx.tracks:
        for segment in track.segments:
            for i in range(1, len(segment.points)):
                pt1 = segment.points[i - 1]
                pt2 = segment.points[i]

                segment_distance = compute_distance(pt1, pt2)
                total_distance += segment_distance

                if total_distance >= distance:
                    point = (pt2.latitude, pt2.longitude)
                    break

    return point


def inverse_geocode(point):
    geolocator = Nominatim(user_agent="gpx_distance_tracker")
    location = geolocator.reverse(point, exactly_one=True)
    return (
        location.raw.get("address", {}).get("city")
        or location.raw.get("address", {}).get("town")
        or location.raw.get("address", {}).get("village")
        or "Unknown"
    )


def main(
    gpx_file_path,
    distance,
):
    point = get_point(gpx_file_path, float(distance))
    print(point)

    city = inverse_geocode(point)
    print(city)


if __name__ == "__main__":
    main(*sys.argv[1:])
