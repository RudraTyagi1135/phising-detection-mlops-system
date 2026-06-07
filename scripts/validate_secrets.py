from __future__ import annotations

import argparse
import os
import sys


CI_REQUIRED = [
    "APP_ENV",
]

CD_REQUIRED = [
    "DOCKER_USERNAME",
    "DOCKER_PASSWORD"
]


def _present(name: str) -> bool:
    return bool(os.getenv(name))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["ci", "cd"], default="ci")
    args = parser.parse_args()

    required = CI_REQUIRED if args.mode == "ci" else CD_REQUIRED
    missing = [name for name in required if not _present(name)]


    if missing:
        message = "Missing required secrets/env vars: " + ", ".join(sorted(set(missing)))
        print(message, file=sys.stderr)
        return 1 if args.mode == "cd" else 0

    print(f"{args.mode.upper()} secret validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
