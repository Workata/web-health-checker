from utils import YamlReader
import pytest
import typing as t


@pytest.fixture
def loaded_config_file() -> t.Any:
    return YamlReader.read(file_path="./config_example.yaml")

def test_read_config_file(loaded_config_file):
    print(loaded_config_file)
