import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

import gpxpy
import pandas as pd
import polyline

from scripts.route import get_nearest, get_route, make_gpx, parse_latlon


class FakeResponse:
    def __init__(self, status_code: int, payload: dict[str, Any], text: str = "") -> None:
        self.status_code = status_code
        self._payload = payload
        self.text = text

    def json(self) -> dict[str, Any]:
        return self._payload


class ParseLatlonTests(unittest.TestCase):
    def test_splits_lat_and_lon(self) -> None:
        self.assertEqual(parse_latlon("21.5,105.75"), (21.5, 105.75))

    def test_accepts_negative_coordinates(self) -> None:
        self.assertEqual(parse_latlon("-33.87,-70.65"), (-33.87, -70.65))


class GetNearestTests(unittest.TestCase):
    def test_returns_lat_lon_from_osrm_response(self) -> None:
        response = FakeResponse(200, {"waypoints": [{"location": [105.75, 21.5]}]})

        with mock.patch("scripts.route.requests.get", return_value=response) as mock_get:
            result = get_nearest((21.5, 105.75))

        self.assertEqual(result, (21.5, 105.75))
        self.assertIn("105.75,21.5", mock_get.call_args.args[0])

    def test_raises_on_non_200_response(self) -> None:
        response = FakeResponse(500, {}, text="server error")

        with (
            mock.patch("scripts.route.requests.get", return_value=response),
            self.assertRaises(Exception) as err,
        ):
            get_nearest((21.5, 105.75))

        self.assertIn("500", str(err.exception))


class GetRouteTests(unittest.TestCase):
    def test_decodes_polyline6_geometry_into_dataframe(self) -> None:
        route_coords = [(21.0, 105.0), (21.01, 105.01), (21.02, 105.02)]
        encoded = polyline.encode(route_coords, precision=6)
        nearest_response = FakeResponse(200, {"waypoints": [{"location": [105.0, 21.0]}]})
        route_response = FakeResponse(200, {"routes": [{"geometry": encoded}]})

        with mock.patch(
            "scripts.route.requests.get",
            side_effect=[nearest_response, nearest_response, route_response],
        ):
            result = get_route("21.0,105.0", "21.02,105.02")

        self.assertEqual(list(result.columns), ["lat", "lon"])
        self.assertEqual(
            list(zip(result["lat"], result["lon"], strict=True)),
            route_coords,
        )

    def test_raises_value_error_when_no_routes(self) -> None:
        nearest_response = FakeResponse(200, {"waypoints": [{"location": [105.0, 21.0]}]})
        empty_route_response = FakeResponse(200, {"routes": []})

        with (
            mock.patch(
                "scripts.route.requests.get",
                side_effect=[nearest_response, nearest_response, empty_route_response],
            ),
            self.assertRaises(ValueError),
        ):
            get_route("21.0,105.0", "21.02,105.02")


class MakeGpxTests(unittest.TestCase):
    def test_writes_track_points_matching_dataframe(self) -> None:
        df = pd.DataFrame([{"lat": 21.0, "lon": 105.0}, {"lat": 21.1, "lon": 105.1}])

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "route.gpx"
            make_gpx(df, str(output_path))

            with output_path.open() as f:
                gpx = gpxpy.parse(f)

        points = gpx.tracks[0].segments[0].points
        self.assertEqual(len(points), 2)
        self.assertEqual((points[0].latitude, points[0].longitude), (21.0, 105.0))
        self.assertEqual((points[1].latitude, points[1].longitude), (21.1, 105.1))


if __name__ == "__main__":
    unittest.main()
