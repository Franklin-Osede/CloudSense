terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11"
    }
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = "CloudSense AI"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

# Providers for Kubernetes & Helm (used by ArgoCD) are configured in eks.tf and argocd.tf
