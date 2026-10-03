variable "project_name" {
  description = "Project name used for AWS resource naming"
  type        = string
  default     = "cloudpulse"
}

variable "vpc_cidr" {
  description = "CIDR block for the CloudPulse VPC"
  type        = string
  default     = "10.0.0.0/16"
}