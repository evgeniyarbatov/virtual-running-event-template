import tempfile
import unittest
from pathlib import Path
from unittest import mock

import gpxpy.gpx
from geopy.distance import geodesic

from scripts.get_point import compute_distance, get_point, inverse_geocode

POINTS = [
    (21.0000, 105.0000),
    (21.0100, 105.0000),
    (21.0200, 105.0000),
    (21.0300, 105.0000),
]

GPX_SINGLE_TRACK = f"""<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="test">
  <trk>
    <trkseg>
      <trkpt lat="{POINTS[0][0]}" lon="{POINTS[0][1]}" />
      <trkpt lat="{POINTS[1][0]}" lon="{POINTS[1][1]}" />
      <trkpt lat="{POINTS[2][0]}" lon="{POINTS[2][1]}" />
      <trkpt lat="{POINTS[3][0]}" lon="{POINTS[3][1]}" />
    </trkseg>
  </trk>
</gpx>
"""


class ComputeDistanceTests(unittest.TestCase):
    def test_matches_geodesic_distance_between_two_points(self) -> None:
        p1 = gpxpy.gpx.GPXTrackPoint(latitude=POINTS[0][0], longitude=POINTS[0][1])
        p2 = gpxpy.gpx.GPXTrackPoint(latitude=POINTS[1][0], longitude=POINTS[1][1])

        result = compute_distance(p1, p2)

        self.assertAlmostEqual(result, geodesic(POINTS[0], POINTS[1]).km, places=6)


class GetPointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cum_km = [0.0]
        for i in range(1, len(POINTS)):
            self.cum_km.append(self.cum_km[-1] + geodesic(POINTS[i - 1], POINTS[i]).km)

        self.tmpdir = tempfile.TemporaryDirectory()
        self.gpx_path = Path(self.tmpdir.name) / "route.gpx"
        self.gpx_path.write_text(GPX_SINGLE_TRACK, encoding="utf-8")

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def test_returns_point_reached_within_first_segment(self) -> None:
        target = self.cum_km[1] / 2

        point = get_point(str(self.gpx_path), target)

        self.assertEqual(point, POINTS[1])

    def test_returns_point_reached_in_a_later_segment(self) -> None:
        target = (self.cum_km[1] + self.cum_km[2]) / 2

        point = get_point(str(self.gpx_path), target)

        self.assertEqual(point, POINTS[2])

    def test_returns_none_when_distance_exceeds_total_route(self) -> None:
        point = get_point(str(self.gpx_path), self.cum_km[-1] + 100)

        self.assertIsNone(point)


class InverseGeocodeTests(unittest.TestCase):
    def test_prefers_city_then_town_then_village(self) -> None:
        location = mock.Mock()
        location.raw = {"address": {"town": "Some Town"}}

        with mock.patch("scripts.get_point.Nominatim") as mock_nominatim:
            mock_nominatim.return_value.reverse.return_value = location

            city = inverse_geocode((21.0, 105.0))

        self.assertEqual(city, "Some Town")
        mock_nominatim.return_value.reverse.assert_called_once_with(
            (21.0, 105.0), exactly_one=True
        )

    def test_falls_back_to_unknown_when_no_address_fields_present(self) -> None:
        location = mock.Mock()
        location.raw = {"address": {}}

        with mock.patch("scripts.get_point.Nominatim") as mock_nominatim:
            mock_nominatim.return_value.reverse.return_value = location

            city = inverse_geocode((21.0, 105.0))

        self.assertEqual(city, "Unknown")


if __name__ == "__main__":
    unittest.main()
