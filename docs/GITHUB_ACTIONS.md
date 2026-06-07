# GitHub Actions Guide

## Workflows

```text
.github/workflows/ci.yml
.github/workflows/cd.yml
```

## CI

Runs on pushes, pull requests, and manual dispatch.

Checks:

- dependency installation
- Ruff critical lint checks
- project configuration validation
- DVC metadata validation
- DVC status
- pytest
- Docker build
- Docker health endpoint
- CI secrets contract validation

Use the CI workflow for branch protection.

## CD

Runs on `main` pushes and manual dispatch.

Steps:

- validate deployment secrets
- configure DVC remote
- pull DVC artifacts from DagsHub
- authenticate to AWS
- build and push ECR image
- render ECS task definition
- deploy ECS service

The production task definition sets `TRAINING_ENDPOINT_ENABLED=false`. Training should run through
controlled jobs or manual pipeline execution, not through the public API container.

## Required Repository Secrets

```text
AWS_REGION
AWS_ROLE_TO_ASSUME
ECR_REPOSITORY_NAME
ECS_CLUSTER
ECS_SERVICE
ECS_TASK_DEFINITION_FAMILY
ECS_CONTAINER_NAME
ECS_EXECUTION_ROLE_ARN
ECS_TASK_ROLE_ARN
MONGODB_URI_SECRET_ARN
DAGSHUB_TOKEN_SECRET_ARN
DAGSHUB_REPO_OWNER
DAGSHUB_REPO_NAME
DAGSHUB_TOKEN
DVC_REMOTE_URL
MLFLOW_TRACKING_URI
```

Fallback AWS access-key deployment is supported if OIDC is not ready:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

OIDC is preferred.

## Branch Protection

Require this status check before merging into `main`:

```text
Validate, test, and build
```

Keep CD restricted to `main` and manual dispatch.
