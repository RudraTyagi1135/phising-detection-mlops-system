from network_security.config.settings import get_settings


def test_settings_load_config_and_schema_paths():
    settings = get_settings()
    assert settings.config_path.exists()
    assert settings.paths.schema_file_path.exists()
    assert settings.data.target_column == "Result"
