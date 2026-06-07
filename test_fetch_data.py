from push_data import NetworkDataExtract


def test_csv_to_json_converter_reads_seed_dataset():
    records = NetworkDataExtract().csv_to_json_converter("network_data/phisingData.csv")
    assert records
    assert "Result" in records[0]
