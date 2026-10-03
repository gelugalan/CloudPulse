# CloudPulse

> This README was generated with AI assistance.

CloudPulse is a DevOps-focused portfolio project built to practice containerization, CI/CD, Infrastructure as Code, cloud networking, automated testing, and security scanning.

The application itself is intentionally simple: a FastAPI REST API backed by PostgreSQL. The main focus of the project is the engineering workflow around the application.

## Architecture

### Current Architecture

```mermaid
flowchart TD
    DEV[Developer] --> GIT[GitHub Repository]

    GIT --> CI[GitHub Actions CI]

    CI --> TEST[Python Tests]
    CI --> BUILD[Docker Build]
    CI --> TF[Terraform Validation]
    CI --> AUDIT[Dependency Scan]
    CI --> TRIVY[Container Scan]

    APP[FastAPI] --> DB[(PostgreSQL)]

    COMPOSE[Docker Compose] --> APP
    COMPOSE --> DB

    TF --> AWS[AWS Infrastructure as Code]
    AWS --> VPC[VPC]
    VPC --> PUB[Public Subnets]
    VPC --> PRIV[Private Subnets]
    VPC --> IGW[Internet Gateway]
    VPC --> RT[Route Tables]
```

The AWS infrastructure was provisioned with Terraform as a learning exercise and can be destroyed when not in use to avoid unnecessary cloud costs.

## Tech Stack

**Application**
- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pytest

**Containers**
- Docker
- Docker Compose

**Infrastructure as Code**
- Terraform
- AWS Provider

**AWS**
- VPC
- Public and private subnets
- Internet Gateway
- Route tables
- Multi-AZ subnet layout

**CI/CD & Security**
- GitHub Actions
- pip-audit
- Trivy

## API

CloudPulse exposes a small task management API.

Available endpoints include:

```text
GET     /
GET     /health
GET     /health/db

POST    /tasks
GET     /tasks
GET     /tasks/{task_id}
DELETE  /tasks/{task_id}
```

Example:

```bash
curl http://localhost:8000/health
```

Response:

```json
{
  "status": "healthy"
}
```

## Running Locally

### Requirements

Install:

- Git
- Docker
- Docker Compose

Clone the repository:

```bash
git clone https://github.com/gelugalan/CloudPulse.git
cd CloudPulse
```

Start the application:

```bash
docker compose up -d
```

Check the running containers:

```bash
docker compose ps
```

Test the API:

```bash
curl http://localhost:8000/health
```

The API is available at:

```text
http://localhost:8000
```

FastAPI interactive documentation is available at:

```text
http://localhost:8000/docs
```

Stop the environment:

```bash
docker compose down
```

## Docker

The API is packaged into a Docker image using `python:3.12-slim`.

The container includes:

- a non-root application user
- an application health check
- dependency installation through `requirements.txt`
- a minimal Python base image
- updated OS packages for security fixes

Docker Compose provides the local development environment:

```text
Docker Compose
│
├── API
│   └── FastAPI :8000
│
└── Database
    └── PostgreSQL :5432
```

The application receives its database connection through the `DATABASE_URL` environment variable rather than hardcoding environment-specific connection information.

## Testing

Tests are implemented with Pytest and FastAPI's test client.

When PostgreSQL is running locally through Docker Compose, tests can be executed with:

```bash
python -m pytest
```

The database connection is supplied through the environment.

Example for PowerShell:

```powershell
$env:DATABASE_URL="postgresql://cloudpulse:cloudpulse@localhost:5432/cloudpulse"
python -m pytest
```

## CI Pipeline

GitHub Actions automatically runs the CI pipeline on pushes and pull requests targeting `master`.

```text
                 Push / Pull Request
                         │
                         ▼
                   GitHub Actions
                         │
       ┌─────────────────┼──────────────────┐
       │                 │                  │
       ▼                 ▼                  ▼
 Python Tests       Docker Build      Terraform Check
       │
       ├───────────────┐
       ▼               ▼
Dependency Scan   Container Scan
   pip-audit          Trivy
```

The pipeline performs five main checks:

1. **Python Tests** — starts PostgreSQL and executes the automated test suite.
2. **Docker Build** — verifies that the application image can be built successfully.
3. **Terraform Validation** — runs formatting checks, initialization, and configuration validation.
4. **Dependency Scan** — uses `pip-audit` to detect known vulnerabilities in Python dependencies.
5. **Container Scan** — uses Trivy to scan the built container image for HIGH and CRITICAL vulnerabilities.

A failed security gate causes the CI pipeline to fail.

## Infrastructure as Code

AWS networking is defined declaratively using Terraform.

The infrastructure configuration includes:

```text
VPC
├── Public Subnet A
├── Public Subnet B
├── Private Subnet A
├── Private Subnet B
├── Internet Gateway
├── Public Route Table
└── Private Route Table
```

The subnets are distributed across multiple Availability Zones.

Typical Terraform workflow:

```bash
cd infra

terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
```

Inspect Terraform-managed resources:

```bash
terraform state list
```

Destroy the infrastructure when it is no longer needed:

```bash
terraform plan -destroy
terraform destroy
```

The Terraform configuration remains version-controlled even when the corresponding AWS infrastructure is destroyed.

## Terraform Concepts Practiced

This project was used to practice:

- providers
- resources
- variables
- outputs
- resource references
- implicit dependencies
- Terraform state
- execution plans
- infrastructure lifecycle
- AWS networking

For example, resources reference other Terraform resources instead of hardcoding generated AWS IDs. This allows Terraform to construct a dependency graph and determine resource creation order.

## Security

Security checks are integrated directly into CI rather than being treated as a separate manual step.

### Container Security

The application container runs as a non-root user.

Trivy scans the resulting image for HIGH and CRITICAL vulnerabilities.

During development, the security pipeline detected a HIGH-severity vulnerability in an operating-system package inherited by the container image.

The issue was investigated and traced to the Debian package rather than the Python application dependencies. The container build was updated so that patched operating-system packages are installed, after which the image was rebuilt and rescanned.

This provides a practical example of the workflow:

```text
Build
  ↓
Security Scan
  ↓
Vulnerability Detected
  ↓
Investigate
  ↓
Remediate
  ↓
Rebuild
  ↓
Scan Again
```

### Dependency Security

`pip-audit` checks Python dependencies against known vulnerability databases during CI.

### Secrets

Secrets and local environment files are excluded from version control through `.gitignore`.

Application configuration such as the database connection is injected through environment variables.

## Project Structure

```text
CloudPulse/
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── requirements.txt
│
├── infra/
│   ├── main.tf
│   ├── outputs.tf
│   ├── provider.tf
│   ├── variables.tf
│   ├── versions.tf
│   └── vpc.tf
│
├── tests/
│   └── test_health.py
│
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## What I Learned

CloudPulse was built primarily as a hands-on DevOps learning project.

Key areas practiced include:

- building and troubleshooting Docker images
- running multi-container environments with Docker Compose
- injecting configuration through environment variables
- implementing automated tests in CI
- designing GitHub Actions workflows
- provisioning AWS networking using Terraform
- understanding Terraform state and resource dependencies
- separating public and private AWS networking
- integrating vulnerability scanning into CI
- investigating and remediating container vulnerabilities
- maintaining infrastructure code independently from deployed infrastructure

## Future Improvements

A future version of CloudPulse can extend the current foundation with:

- Amazon ECR for container storage
- Amazon ECS with Fargate
- Application Load Balancer
- Amazon RDS for PostgreSQL
- AWS Secrets Manager
- CloudWatch logging and monitoring
- GitHub Actions deployment pipeline
- GitHub OIDC authentication to AWS
- remote Terraform state
- reusable Terraform modules
- HTTPS and custom DNS
- automated deployment and rollback strategies

These services are intentionally outside the current version so the project can remain inexpensive while establishing the core DevOps workflow first.

## Repository

CloudPulse is available on GitHub:

https://github.com/gelugalan/CloudPulse