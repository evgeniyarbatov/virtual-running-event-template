import json
import os
import subprocess
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest import mock

from scripts.update import (
    calculate_total_distance,
    run_point,
    update_makefile,
    update_map_json,
    update_metadata_json,
)


class CalculateTotalDistanceTests(unittest.TestCase):
    def test_sums_and_rounds_to_two_decimals(self) -> None:
        entries = [{"distance": "1.005"}, {"distance": "2.111"}, {"distance": "0.334"}]

        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "log.json"
            log_path.write_text(json.dumps(entries), encoding="utf-8")

            result = calculate_total_distance(log_path)

        self.assertEqual(result, Decimal("3.45"))

    def test_empty_log_is_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "log.json"
            log_path.write_text("[]", encoding="utf-8")

            result = calculate_total_distance(log_path)

        self.assertEqual(result, Decimal("0.00"))


class UpdateMakefileTests(unittest.TestCase):
    def test_replaces_distance_line_only(self) -> None:
        content = "SITE_DIR = site\n\nDISTANCE = 12.30\n\nrun:\n\tdo-thing\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            makefile_path = Path(tmpdir) / "Makefile"
            makefile_path.write_text(content, encoding="utf-8")

            update_makefile(makefile_path, Decimal("45.67"))

            updated = makefile_path.read_text(encoding="utf-8")

        self.assertIn("DISTANCE = 45.67", updated)
        self.assertIn("SITE_DIR = site", updated)
        self.assertIn("run:\n\tdo-thing", updated)
        self.assertNotIn("DISTANCE = 12.30", updated)


class RunPointTests(unittest.TestCase):
    def test_parses_coordinates_and_city_from_stdout(self) -> None:
        completed = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="(21.5, 105.5)\nHanoi\n", stderr=""
        )

        with mock.patch("scripts.update.subprocess.run", return_value=completed):
            lat, lon, city = run_point(
                Path("scripts/get_point.py"), Path("route.gpx"), Decimal("10.00"), Path(".")
            )

        self.assertEqual((lat, lon, city), (21.5, 105.5, "Hanoi"))

    def test_defaults_city_to_empty_string_when_missing(self) -> None:
        completed = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="(21.5, 105.5)\n", stderr=""
        )

        with mock.patch("scripts.update.subprocess.run", return_value=completed):
            lat, lon, city = run_point(
                Path("scripts/get_point.py"), Path("route.gpx"), Decimal("10.00"), Path(".")
            )

        self.assertEqual((lat, lon, city), (21.5, 105.5, ""))

    def test_exits_on_called_process_error(self) -> None:
        error = subprocess.CalledProcessError(1, ["cmd"], output="", stderr="boom")

        with (
            mock.patch("scripts.update.subprocess.run", side_effect=error),
            self.assertRaises(SystemExit),
        ):
            run_point(Path("scripts/get_point.py"), Path("route.gpx"), Decimal("10.00"), Path("."))


class UpdateMapJsonTests(unittest.TestCase):
    def test_updates_current_location_in_place(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                public_dir = Path("site/public")
                public_dir.mkdir(parents=True)
                (public_dir / "map.json").write_text(
                    json.dumps({"current_location": [0.0, 0.0], "other": "kept"}),
                    encoding="utf-8",
                )

                update_map_json(21.5, 105.5)

                written = json.loads((public_dir / "map.json").read_text(encoding="utf-8"))
            finally:
                os.chdir(old_cwd)

        self.assertEqual(written["current_location"], [21.5, 105.5])
        self.assertEqual(written["other"], "kept")


class UpdateMetadataJsonTests(unittest.TestCase):
    def _write_metadata(self, public_dir: Path) -> None:
        (public_dir / "metadata.json").write_text(
            json.dumps({"current_point": "", "current_distance": 0.0, "other": "kept"}),
            encoding="utf-8",
        )

    def test_updates_point_and_distance(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                public_dir = Path("site/public")
                public_dir.mkdir(parents=True)
                self._write_metadata(public_dir)

                update_metadata_json("Hanoi", Decimal("42.50"))

                written = json.loads((public_dir / "metadata.json").read_text(encoding="utf-8"))
            finally:
                os.chdir(old_cwd)

        self.assertEqual(written["current_point"], "Hanoi")
        self.assertEqual(written["current_distance"], 42.50)
        self.assertEqual(written["other"], "kept")

    def test_unknown_city_is_stored_as_empty_string(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                public_dir = Path("site/public")
                public_dir.mkdir(parents=True)
                self._write_metadata(public_dir)

                update_metadata_json("Unknown", Decimal("42.50"))

                written = json.loads((public_dir / "metadata.json").read_text(encoding="utf-8"))
            finally:
                os.chdir(old_cwd)

        self.assertEqual(written["current_point"], "")


if __name__ == "__main__":
    unittest.main()
