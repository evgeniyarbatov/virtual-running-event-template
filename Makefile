SITE_DIR = site
TERRAFORM_DIR = terraform

render:
	.venv/bin/python scripts/render_event.py

run:
	cd $(SITE_DIR) && npm run dev

build:
	$(MAKE) render
	cd $(SITE_DIR) && npm run build

deploy:
	$(MAKE) render
	cd $(SITE_DIR) && npm run build
	cd $(TERRAFORM_DIR) && terraform apply -auto-approve

.PHONY: render run build deploy
