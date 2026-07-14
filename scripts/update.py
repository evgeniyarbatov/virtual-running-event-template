#!/usr/bin/env python3

import json
import re
import subprocess
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path


def calculate_total_distance(log_file: Path) -> Decimal:
    """Calculate total distance from log.json entries"""
    with open(log_file) as f:
        entries = json.load(f)

    total = Decimal("0")
    for entry in entries:
        distance = Decimal(str(entry["distance"]))
        total += distance

    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def update_makefile(makefile_path: Path, distance: Decimal) -> None:
    """Update DISTANCE in Makefile"""
    with open(makefile_path) as f:
        content = f.read()

    updated_content = re.sub(
        r"^DISTANCE = .*$", f"DISTANCE = {distance}", content, flags=re.MULTILINE
    )

    with open(makefile_path, "w") as f:
        f.write(updated_content)

    print(f"Updated Makefile: DISTANCE = {distance}")


def run_point(
    script_path: Path, route_gpx: Path, distance: Decimal, cwd: Path
) -> tuple[float, float, str]:
    """Run scripts/get_point.py and capture output"""
    try:
        result = subprocess.run(  # noqa: S603 - args are repo-controlled, not external input
            [sys.executable, str(script_path), str(route_gpx), str(distance)],
            capture_output=True,
            text=True,
            check=True,
            shell=False,
            cwd=cwd,
        )

        lines = result.stdout.strip().split("\n")

        coords_line = lines[0].strip()
        coords = coords_line.strip("()").split(", ")
        lat, lon = float(coords[0]), float(coords[1])

        city = lines[1].strip() if len(lines) > 1 else ""

        return lat, lon, city

    except subprocess.CalledProcessError as e:
        print(f"Error running scripts/get_point.py: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        sys.exit(1)


def update_map_json(lat: float, lon: float) -> None:
    """Update current_location in map.json only"""
    map_file = "site/public/map.json"

    with open(map_file) as f:
        map_data = json.load(f)

    map_data["current_location"] = [lat, lon]

    with open(map_file, "w") as f:
        json.dump(map_data, f, indent=2)

    print(f"Updated site/public/map.json: current_location = [{lat}, {lon}]")


def update_metadata_json(city: str, distance: Decimal) -> None:
    """Update metadata.json with current point and distance"""
    metadata_file = "site/public/metadata.json"

    with open(metadata_file) as f:
        metadata = json.load(f)

    if city == "Unknown":
        city = ""
    metadata["current_point"] = city
    metadata["current_distance"] = float(distance)

    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=4)

    print(
        f"Updated site/public/metadata.json: current_point = '{city}', current_distance = {distance}"
    )


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    log_file = repo_root / "site/public/log.json"
    route_gpx = repo_root / "output/route.gpx"
    makefile_path = repo_root / "Makefile"
    point_script = repo_root / "scripts/get_point.py"

    if not log_file.exists():
        print(f"Error: {log_file} not found")
        sys.exit(1)

    print("Calculating total distance from log.json...")
    total_distance = calculate_total_distance(log_file)
    print(f"Total distance: {total_distance} km")

    print("\nUpdating Makefile...")
    update_makefile(makefile_path, total_distance)

    print("\nRunning scripts/get_point.py to get current coordinates...")
    lat, lon, city = run_point(point_script, route_gpx, total_distance, repo_root)
    print(f"Current position: ({lat}, {lon}) - {city}")

    print("\nUpdating site/public/map.json...")
    update_map_json(lat, lon)

    print("\nUpdating site/public/metadata.json...")
    update_metadata_json(city, total_distance)

    print("\n✅ All files updated successfully!")


if __name__ == "__main__":
    main()
