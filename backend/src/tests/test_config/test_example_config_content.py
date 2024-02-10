from assertpy import assert_that


def test_example_config_file_content(example_config_file):
    assert_that(example_config_file['refresh_period_seconds']).is_equal_to(15)
