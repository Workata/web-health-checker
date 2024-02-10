from utils import YamlReader
import pytest
import typing as t


@pytest.fixture
def example_config_file() -> t.Any:
    return YamlReader.read(file_path="./config_example.yaml")
