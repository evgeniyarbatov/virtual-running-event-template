# Virtual Running Event Template

This template builds a static site for a virtual running event and deploys it to S3 with Terraform. Event fields and deployment settings live in `config.json` and are rendered into `site/public/event.json`.

## Requirements
- Node.js 18+
- npm
- Python 3.10+
- Terraform 1.5+
- AWS credentials with access to S3

## Setup
1. Create the virtual environment and install Python dependencies:
   `make install`
2. Update `config.json`:
   set `aws_region`, `s3_bucket`, and the `event_*` values.
3. Generate event JSON:
   `make render`
4. Install frontend dependencies:
   `cd site && npm install`

## Run Locally
1. `make run`

## Build
1. `make build`

## Route Tools
- `make route` generates `output/route.gpx` using `START_POINT` and `FINISH_POINT`.
- `make stats` writes `output/summary.json` with total distance.
- `make polyline` writes `output/polyline.json` for the map.
- `make point` prints the coordinate and reverse-geocoded city at `DISTANCE`.

## Update Progress
1. Ensure `output/route.gpx` exists.
2. Update `site/public/log.json` with new runs.
3. `make update`

## Deploy
1. `make deploy`

`make deploy` builds the site and runs `terraform apply` to upload the `site/dist` output to S3.
