from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from network_security.config.settings import get_settings
from network_security.db.mongodb import check_mongodb_health
from network_security.utils.main_utils.utils import read_yaml_file


def _fail(message: str) -> None:
    raise RuntimeError(message)


def main() -> int:
    settings = get_settings()

    # Validate config file
    if not settings.config_path.exists():
        _fail(f"Config file is missing: {settings.config_path}")

    # Validate schema
    schema = read_yaml_file(settings.paths.schema_file_path)

    columns = schema.get("columns", [])
    if not columns:
        _fail("Schema file does not define any columns")

    schema_column_names = []

    for column in columns:
        if isinstance(column, dict):
            schema_column_names.extend(column.keys())
        else:
            schema_column_names.append(str(column))

    if settings.data.target_column not in schema_column_names:
        _fail(
            f"Target column '{settings.data.target_column}' "
            f"is missing from schema"
        )

    # Validate required project paths
    required_paths = [
        settings.paths.schema_file_path,
        settings.paths.templates_dir,
        settings.config_path,
        settings.paths.final_model_dir,
        
    ]

    missing_paths = [
        str(path)
        for path in required_paths
        if not Path(path).exists()
    ]

    if missing_paths:
        _fail(f"Required paths are missing: {missing_paths}")

    # Optional MongoDB health check
    health = check_mongodb_health(required=False)

    print(
        f"Project validation passed. "
        f"MongoDB health: {health['status']}"
    )

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(
            f"Project validation failed: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(1)