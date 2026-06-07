from pathlib import Path

import yaml


def test_dvc_metadata_files_exist():
    root = Path(__file__).resolve().parents[1]
    dvc_files = [
        root / "network_data" / "phisingData.csv.dvc",
        root / "final_model" / "model.pkl.dvc",
        root / "final_model" / "preprocessor.pkl.dvc",
    ]

    for dvc_file in dvc_files:
        assert dvc_file.exists()
        metadata = yaml.safe_load(dvc_file.read_text(encoding="utf-8"))
        assert metadata["outs"][0]["md5"]
        assert metadata["outs"][0]["path"]
