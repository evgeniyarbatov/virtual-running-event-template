VENV_PATH := .venv

PYTHON := $(VENV_PATH)/bin/python
PIP := $(VENV_PATH)/bin/pip
REQUIREMENTS := requirements.txt

SITE_DIR = site
TERRAFORM_DIR = terraform

START_POINT = 45.52291380947891,141.93657821505906
FINISH_POINT = 30.995217247057777,130.66282806776934

ROUTE_GPX = output/route.gpx
SUMMARY_JSON = output/summary.json
POLYLINE_JSON = output/polyline.json

DISTANCE = 0.00

venv:
	@uv venv $(VENV_PATH)

install: venv
	@uv pip install -q -r $(REQUIREMENTS)

render: install
	@$(PYTHON) scripts/render_event.py
update: install
	@$(PYTHON) scripts/update.py
route: install
	@mkdir -p output
	@$(PYTHON) scripts/route.py \
	$(START_POINT) \
	$(FINISH_POINT) \
	$(ROUTE_GPX)
stats: install
	@$(PYTHON) scripts/stats.py \
	$(ROUTE_GPX) \
	$(SUMMARY_JSON)
polyline: install
	@$(PYTHON) scripts/get_polyline.py \
	$(ROUTE_GPX) \
	$(POLYLINE_JSON)
point: install
	@$(PYTHON) scripts/get_point.py \
	$(ROUTE_GPX) \
	$(DISTANCE)
run:
	cd $(SITE_DIR) && npm run dev

build:
	$(MAKE) render
	cd $(SITE_DIR) && npm run build

deploy:
	$(MAKE) render
	cd $(SITE_DIR) && npm run build
	cd $(TERRAFORM_DIR) && terraform apply -auto-approve

.PHONY: render update run build deploy route stats polyline point
