from __future__ import annotations

import argparse
import os
import sys


CI_REQUIRED = [
    "APP_ENV",
]

CD_REQUIRED = [
    "AWS_REGION",
    "ECR_REPOSITORY_NAME",
    "ECS_CLUSTER",
    "ECS_SERVICE",
    "ECS_TASK_DEFINITION_FAMILY",
    "ECS_CONTAINER_NAME",
    "ECS_EXECUTION_ROLE_ARN",
    "ECS_TASK_ROLE_ARN",
    "MONGODB_URI_SECRET_ARN",
    "DAGSHUB_TOKEN_SECRET_ARN",
    "DAGSHUB_REPO_OWNER",
    "DAGSHUB_REPO_NAME",
    "DVC_REMOTE_URL",
]


def _present(name: str) -> bool:
    return bool(os.getenv(name))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["ci", "cd"], default="ci")
    args = parser.parse_args()

    required = CI_REQUIRED if args.mode == "ci" else CD_REQUIRED
    missing = [name for name in required if not _present(name)]

    if args.mode == "cd":
        has_aws_auth = _present("AWS_ROLE_TO_ASSUME") or (
            _present("AWS_ACCESS_KEY_ID") and _present("AWS_SECRET_ACCESS_KEY")
        )
        has_dagshub_auth = _present("DAGSHUB_TOKEN") or (
            _present("MLFLOW_TRACKING_USERNAME") and _present("MLFLOW_TRACKING_PASSWORD")
        )

        if not has_aws_auth:
            missing.append("AWS_ROLE_TO_ASSUME or AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY")
        if not has_dagshub_auth:
            missing.append("DAGSHUB_TOKEN or MLFLOW_TRACKING_USERNAME/MLFLOW_TRACKING_PASSWORD")

    if missing:
        message = "Missing required secrets/env vars: " + ", ".join(sorted(set(missing)))
        print(message, file=sys.stderr)
        return 1 if args.mode == "cd" else 0

    print(f"{args.mode.upper()} secret validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
