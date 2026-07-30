# CLAUDE.md

## What this is

Template for a virtual running event static site: a runner "travels" a
route (e.g. Exampleland Virtual Ultra) as logged runs accumulate distance.
Builds a static React site and deploys it to S3 via Terraform.

## Key files

- `config.json` — event metadata (title, story, polyline, distance).
- `terraform/variables.tf` — deployment target (region, S3 bucket).
- `site/public/log.json` — logged runs (date + distance) driving progress.
- `scripts/route.py`, `get_polyline.py`, `stats.py`, `get_point.py` — route
  setup tools (GPX, polyline, distance stats).
- `scripts/update.py` — recomputes total distance from `log.json`.
- `scripts/render_event.py` — renders `config.json` into site data.

## How to run

```bash
make run
```

Runs the site's Vite dev server. Full setup (first time): `make install`,
edit `terraform/variables.tf` and `config.json`, `make render`,
`cd site && npm install`, then `make run`. See README for the full
route-setup and deploy workflow (`make route`, `make update`, `make deploy`).

## Conventions / gotchas

- Python deps managed with `uv`; Makefile targets run via `uv run`.
- `START_POINT`/`FINISH_POINT`/`DISTANCE` are Makefile variables, edited
  directly (`DISTANCE` is auto-updated by `make update`).
- `make deploy` applies Terraform and uploads `site/dist` to S3.
