# Virtual Running Event Template

This template builds a static site for a virtual running event and deploys it to S3 with Terraform. Event fields (country, custom texts, start and stop points) are defined in Terraform variables and rendered into `site/public/event.json`.

## Requirements
- Node.js 18+
- npm
- Python 3.10+
- Terraform 1.5+
- AWS credentials with access to S3

## Setup
1. Create and activate a virtual environment:
   `python3 -m venv .venv`
   `./.venv/bin/pip install -r requirements.txt`
2. Update `terraform/terraform.tfvars.json`:
   set `s3_bucket`, `aws_region`, and the `event_*` values.
3. Generate event JSON:
   `make render`
4. Install frontend dependencies:
   `cd site && npm install`

## Run Locally
1. `make run`

## Build
1. `make build`

## Deploy
1. `make deploy`

`make deploy` builds the site and runs `terraform apply` to upload the `site/dist` output to S3.
