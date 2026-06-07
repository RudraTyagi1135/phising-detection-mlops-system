from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    dvc_config = ROOT / ".dvc" / "config"
    if not dvc_config.exists():
        raise RuntimeError(".dvc/config is missing")

    dvc_files = [
        ROOT / "network_data" / "phisingData.csv.dvc",
        ROOT / "final_model" / "model.pkl.dvc",
        ROOT / "final_model" / "preprocessor.pkl.dvc",
    ]

    for dvc_file in dvc_files:
        if not dvc_file.exists():
            raise RuntimeError(f"DVC metadata is missing: {dvc_file}")
        metadata = dvc_file.read_text(encoding="utf-8")
        if "outs:" not in metadata or "md5:" not in metadata or "path:" not in metadata:
            raise RuntimeError(f"DVC metadata is incomplete: {dvc_file}")

    config_text = dvc_config.read_text(encoding="utf-8").lower()
    forbidden_tokens = ["password", "token", "secret", "access_key"]
    leaked = [token for token in forbidden_tokens if token in config_text]
    if leaked:
        raise RuntimeError(f"DVC config appears to contain secret fields: {leaked}")

    print("DVC metadata validation passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"DVC validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
