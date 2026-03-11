# Virtual Running Event Template

This template builds a static site for a virtual running event and deploys it to S3 with Terraform.

Event fields live in `config.json`. Terraform deployment defaults live in `terraform/variables.tf`.

## Requirements
- Node.js 18+
- npm
- Python 3.10+
- Terraform 1.5+
- AWS credentials with access to S3

## Setup
1. Create the virtual environment and install Python dependencies:
   `make install`
2. Update `terraform/variables.tf`:
   set `aws_region`, `s3_bucket`, and `s3_bucket_dir`.
3. Update `config.json`:
   set the `event_*` values.
4. Generate event JSON:
   `make render`
5. Install frontend dependencies:
   `cd site && npm install`

## Run Locally
1. `make run`

## First-Time Route Setup
1. Set `START_POINT` and `FINISH_POINT` in `Makefile`.
2. `make route`
3. `make polyline`
4. `make stats`
5. Update `config.json` using the outputs:
   add `event_polyline` from `output/polyline.json` and update the `event_*` values based on `output/summary.json`.

## Route Tools
- `make route` generates `output/route.gpx` using `START_POINT` and `FINISH_POINT`.
- `make stats` writes `output/summary.json` with total distance.
- `make polyline` writes `output/polyline.json` for the map.
- `make point` prints the coordinate and reverse-geocoded city at `DISTANCE`.

## Update Progress
1. Update `site/public/log.json` with new runs.
2. `make update`

## Deploy
1. `make deploy`

`make deploy` builds the site and runs `terraform apply` to upload the `site/dist` output to S3.
