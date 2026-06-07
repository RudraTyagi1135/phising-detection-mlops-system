import tempfile

import pandas as pd

from push_data import NetworkDataExtract


def test_csv_to_json_converter():

    df = pd.DataFrame(
        {
            "feature_1": [1, 2],
            "feature_2": [3, 4],
            "Result": [0, 1],
        }
    )

    with tempfile.NamedTemporaryFile(
        suffix=".csv",
        delete=False,
    ) as temp_file:

        df.to_csv(
            temp_file.name,
            index=False,
        )

        records = (
            NetworkDataExtract()
            .csv_to_json_converter(
                temp_file.name
            )
        )

    assert len(records) == 2
    assert "Result" in records[0]