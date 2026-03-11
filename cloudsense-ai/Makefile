.PHONY: help venv test docker-build deploy destroy

VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

help:
	@echo "CloudSense AI Makefile"
	@echo "-----------------------"
	@echo "make venv         - Create Python virtual environment and install dependencies"
	@echo "make test         - Run Pytest (TDD)"
	@echo "make docker-build - Build the AI Engine Docker image"
	@echo "make deploy       - Provision Terraform infrastructure and apply GitOps apps"
	@echo "make destroy      - Teardown all AWS Terraform infrastructure"

venv:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "Virtual environment created. Run 'source $(VENV_DIR)/bin/activate' to continue."

test: venv
	PYTHONPATH=$(PWD) $(VENV_DIR)/bin/pytest tests/

docker-build:
	docker build -t cloudsense-ai:latest .

deploy:
	@echo "🚀 Provisioning Infrastructure..."
	cd terraform && terraform init && terraform apply -auto-approve
	@echo "🚀 Applying GitOps Configuration..."
	aws eks update-kubeconfig --region us-east-1 --name cloudsense-ai-cluster
	kubectl apply -f k8s/argocd/applications.yaml
	@echo "✅ Deployment complete. Check ArgoCD for sync status."

destroy:
	@echo "🗑️ Destroying Infrastructure..."
	cd terraform && terraform destroy -auto-approve
	@echo "✅ Teardown complete."
