# Uses uv (https://docs.astral.sh/uv) for dependency management — uv sync creates/updates .venv; run commands via uv run, no manual activation.

SITE_DIR = site
TERRAFORM_DIR = terraform

START_POINT = 45.52291380947891,141.93657821505906
FINISH_POINT = 30.995217247057777,130.66282806776934

ROUTE_GPX = output/route.gpx
SUMMARY_JSON = output/summary.json
POLYLINE_JSON = output/polyline.json

DISTANCE = 0.00

.DEFAULT_GOAL := help

setup:
	@uv sync

test: setup
	@uv run python -m unittest discover -s tests -p 'test_*.py' -v

render: setup
	@uv run python scripts/render_event.py

update: setup
	@uv run python scripts/update.py

route: setup
	@mkdir -p output
	@uv run python scripts/route.py \
	$(START_POINT) \
	$(FINISH_POINT) \
	$(ROUTE_GPX)

stats: setup
	@uv run python scripts/stats.py \
	$(ROUTE_GPX) \
	$(SUMMARY_JSON)

polyline: setup
	@uv run python scripts/get_polyline.py \
	$(ROUTE_GPX) \
	$(POLYLINE_JSON)

point: setup
	@uv run python scripts/get_point.py \
	$(ROUTE_GPX) \
	$(DISTANCE)

# Entry point: run the site locally.
run:
	cd $(SITE_DIR) && npm run dev

build:
	$(MAKE) render
	cd $(SITE_DIR) && npm run build

deploy:
	$(MAKE) render
	cd $(SITE_DIR) && npm run build
	cd $(TERRAFORM_DIR) && terraform apply -auto-approve

lock:
	@uv lock

help:
	@echo "setup    - uv sync"
	@echo "test     - run unit tests"
	@echo "render   - render event site data"
	@echo "update   - update event data"
	@echo "route    - generate route GPX"
	@echo "stats    - compute route stats"
	@echo "polyline - extract route polyline"
	@echo "point    - get point at distance along route"
	@echo "run      - run site dev server"
	@echo "build    - render and build site"
	@echo "deploy   - render, build, and apply terraform"
	@echo "lock     - uv lock"

.PHONY: setup test render update run build deploy route stats polyline point lock help
