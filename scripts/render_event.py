#!/usr/bin/env python3

import json
from pathlib import Path


def main():
    repo_root = Path(__file__).resolve().parents[1]
    config_path = repo_root / "config.json"
    output_path = repo_root / "site" / "public" / "event.json"

    with config_path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)

    event = {
        "country": config["event_country"],
        "title": config["event_title"],
        "subtitle": config["event_subtitle"],
        "custom_texts": config["event_custom_texts"],
        "start_point": config["event_start_point"],
        "stop_point": config["event_stop_point"],
    }

    output_path.write_text(
        json.dumps(event, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
