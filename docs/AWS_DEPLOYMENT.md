# AWS Deployment Guide

Official references:

- AWS credential action: https://github.com/aws-actions/configure-aws-credentials
- ECS deploy action: https://github.com/aws-actions/amazon-ecs-deploy-task-definition

## AWS Resources

Create:

- ECR repository: `phishing-detection-api`
- ECS cluster
- ECS Fargate service behind an Application Load Balancer or public service endpoint
- CloudWatch log group: `/ecs/phishing-detection-api`
- IAM task execution role
- IAM task role
- IAM role for GitHub Actions OIDC
- AWS Secrets Manager secrets for MongoDB and DagsHub token

## Secrets Manager

Create these secrets:

```text
phishing/MONGODB_URI
phishing/DAGSHUB_TOKEN
```

Store their ARNs as GitHub secrets:

```text
MONGODB_URI_SECRET_ARN
DAGSHUB_TOKEN_SECRET_ARN
```

## GitHub Actions IAM Role

Prefer OIDC. The role needs permissions for:

- `ecr:GetAuthorizationToken`
- `ecr:BatchCheckLayerAvailability`
- `ecr:CompleteLayerUpload`
- `ecr:CreateRepository`
- `ecr:DescribeRepositories`
- `ecr:InitiateLayerUpload`
- `ecr:PutImage`
- `ecr:UploadLayerPart`
- `ecs:DescribeServices`
- `ecs:DescribeTaskDefinition`
- `ecs:RegisterTaskDefinition`
- `ecs:UpdateService`
- `iam:PassRole` for the ECS task roles

Set the trust policy to allow the GitHub repository to assume the role through OIDC.

## ECS Task Definition

Template:

```text
deploy/aws/ecs-task-definition.json
```

The CD workflow injects:

- ECS family
- execution role
- task role
- container name
- image URI
- runtime environment
- Secrets Manager ARNs

## Deployment

Once GitHub secrets are set:

```text
push to main
```

or manually run:

```text
Actions -> cd -> Run workflow
```

The CD workflow:

1. validates deployment secrets
2. pulls DVC artifacts from DagsHub
3. authenticates to AWS
4. creates ECR repository if missing
5. builds and pushes Docker image
6. deploys ECS service
