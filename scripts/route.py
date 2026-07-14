import sys

import gpxpy
import pandas as pd
import polyline
import requests

OSRM_ROUTE_URL = "https://router.project-osrm.org/route/v1/driving/"
OSRM_NEAREST_URL = "https://router.project-osrm.org/nearest/v1/driving/"


def parse_latlon(latlon_str: str) -> tuple[float, float]:
    """Convert 'lat,lon' string to (lon, lat) tuple."""
    lat, lon = map(float, latlon_str.split(","))
    return (lat, lon)


def get_nearest(coords: tuple[float, float]) -> tuple[float, float]:
    coords_str = f"{coords[1]},{coords[0]}"
    url = f"{OSRM_NEAREST_URL}{coords_str}"
    response = requests.get(url, timeout=30)

    if response.status_code == 200:
        data = response.json()
        nearest = data["waypoints"][0]["location"]  # [lon, lat]
        return (nearest[1], nearest[0])
    raise Exception(f"Error from OSRM server: {response.status_code} - {response.text}")


def get_route(start_str: str, stop_str: str) -> pd.DataFrame:
    start = get_nearest(parse_latlon(start_str))
    stop = get_nearest(parse_latlon(stop_str))

    coords = f"{start[1]},{start[0]};{stop[1]},{stop[0]}"
    url = f"{OSRM_ROUTE_URL}{coords}?geometries=polyline6&overview=full&annotations=false&steps=false"
    response = requests.get(url, timeout=30)

    data = response.json()

    if not data.get("routes"):
        raise ValueError("No route found")

    polyline_str = data["routes"][0]["geometry"]
    decoded_coords = polyline.decode(polyline_str, 6)

    return pd.DataFrame(decoded_coords, columns=["lat", "lon"])


def make_gpx(df: pd.DataFrame, trip_gpx: str) -> None:
    gpx = gpxpy.gpx.GPX()
    gpx.author_name = "Evgeny Arbatov"

    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    for _, row in df.iterrows():
        point = gpxpy.gpx.GPXTrackPoint(latitude=row["lat"], longitude=row["lon"])
        gpx_segment.points.append(point)

    with open(trip_gpx, "w") as f:
        f.write(gpx.to_xml())


def main(
    start_point: str,
    finish_point: str,
    route_gpx: str,
) -> None:
    route_df = get_route(start_point, finish_point)

    make_gpx(route_df, route_gpx)


if __name__ == "__main__":
    main(*sys.argv[1:])
