import sys

import gpxpy
from geopy.distance import geodesic
from geopy.geocoders import Nominatim


def compute_distance(p1: gpxpy.gpx.GPXTrackPoint, p2: gpxpy.gpx.GPXTrackPoint) -> float:
    return float(geodesic((p1.latitude, p1.longitude), (p2.latitude, p2.longitude)).km)


def get_point(gpx_file_path: str, distance: float) -> tuple[float, float] | None:
    with open(gpx_file_path) as gpx_file:
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


def inverse_geocode(point: tuple[float, float]) -> str:
    geolocator = Nominatim(user_agent="gpx_distance_tracker")
    location = geolocator.reverse(point, exactly_one=True)
    city: str = (
        location.raw.get("address", {}).get("city")
        or location.raw.get("address", {}).get("town")
        or location.raw.get("address", {}).get("village")
        or "Unknown"
    )
    return city


def main(
    gpx_file_path: str,
    distance: str,
) -> None:
    point = get_point(gpx_file_path, float(distance))
    if point is None:
        print("No point found at the given distance", file=sys.stderr)
        sys.exit(1)
    print(point)

    city = inverse_geocode(point)
    print(city)


if __name__ == "__main__":
    main(*sys.argv[1:])
