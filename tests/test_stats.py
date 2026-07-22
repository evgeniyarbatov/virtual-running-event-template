import json
import tempfile
import unittest
from pathlib import Path

from geopy.distance import geodesic

from scripts.stats import calculate_total_distance, save_to_json

POINTS = [
    (21.0000, 105.0000),
    (21.0100, 105.0050),
    (21.0050, 105.0200),
]

GPX_TWO_TRACKS = f"""<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="test">
  <trk>
    <trkseg>
      <trkpt lat="{POINTS[0][0]}" lon="{POINTS[0][1]}" />
      <trkpt lat="{POINTS[1][0]}" lon="{POINTS[1][1]}" />
    </trkseg>
  </trk>
  <trk>
    <trkseg>
      <trkpt lat="{POINTS[1][0]}" lon="{POINTS[1][1]}" />
      <trkpt lat="{POINTS[2][0]}" lon="{POINTS[2][1]}" />
    </trkseg>
  </trk>
</gpx>
"""


class CalculateTotalDistanceTests(unittest.TestCase):
    def test_sums_across_multiple_tracks_and_segments(self) -> None:
        expected_km = geodesic(POINTS[0], POINTS[1]).km + geodesic(POINTS[1], POINTS[2]).km

        with tempfile.TemporaryDirectory() as tmpdir:
            gpx_path = Path(tmpdir) / "route.gpx"
            gpx_path.write_text(GPX_TWO_TRACKS, encoding="utf-8")

            result = calculate_total_distance(str(gpx_path))

        self.assertAlmostEqual(result["distance_km"], round(expected_km, 2), places=2)
        self.assertAlmostEqual(
            result["distance_miles"], round(expected_km * 0.621371, 2), places=2
        )

    def test_single_point_has_zero_distance(self) -> None:
        gpx = f"""<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="test">
  <trk>
    <trkseg>
      <trkpt lat="{POINTS[0][0]}" lon="{POINTS[0][1]}" />
    </trkseg>
  </trk>
</gpx>
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            gpx_path = Path(tmpdir) / "route.gpx"
            gpx_path.write_text(gpx, encoding="utf-8")

            result = calculate_total_distance(str(gpx_path))

        self.assertEqual(result["distance_km"], 0.0)
        self.assertEqual(result["distance_miles"], 0.0)


class SaveToJsonTests(unittest.TestCase):
    def test_writes_indented_json(self) -> None:
        data = {"distance_km": 12.34, "distance_miles": 7.67}

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "summary.json"
            save_to_json(data, str(output_path))

            written = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertEqual(written, data)


if __name__ == "__main__":
    unittest.main()
