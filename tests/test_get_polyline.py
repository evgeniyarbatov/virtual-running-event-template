import json
import tempfile
import unittest
from pathlib import Path

import polyline

from scripts.get_polyline import gpx_to_polyline, save_to_json

COORDS = [(21.0000, 105.0000), (21.0100, 105.0050), (21.0050, 105.0200)]

GPX_MULTI_TRACK = f"""<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="test">
  <trk>
    <trkseg>
      <trkpt lat="{COORDS[0][0]}" lon="{COORDS[0][1]}" />
      <trkpt lat="{COORDS[1][0]}" lon="{COORDS[1][1]}" />
    </trkseg>
  </trk>
  <trk>
    <trkseg>
      <trkpt lat="{COORDS[2][0]}" lon="{COORDS[2][1]}" />
    </trkseg>
  </trk>
</gpx>
"""


class GpxToPolylineTests(unittest.TestCase):
    def test_encodes_points_from_all_tracks_in_order(self) -> None:
        expected = polyline.encode(COORDS)

        with tempfile.TemporaryDirectory() as tmpdir:
            gpx_path = Path(tmpdir) / "route.gpx"
            gpx_path.write_text(GPX_MULTI_TRACK, encoding="utf-8")

            result = gpx_to_polyline(str(gpx_path))

        self.assertEqual(result, {"polyline": expected})
        self.assertEqual(polyline.decode(result["polyline"]), COORDS)


class SaveToJsonTests(unittest.TestCase):
    def test_writes_indented_json(self) -> None:
        data = {"polyline": "abc123"}

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "polyline.json"
            save_to_json(data, str(output_path))

            written = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertEqual(written, data)


if __name__ == "__main__":
    unittest.main()
