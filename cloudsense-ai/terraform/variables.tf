variable "aws_region" {
  description = "The AWS region to deploy to"
  type        = string
  default     = "us-east-1"
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "cloudsense-ai-cluster"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "demo"
}
