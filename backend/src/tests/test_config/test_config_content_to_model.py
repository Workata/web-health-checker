from models import Config, ServiceConfig
from assertpy import assert_that


def test_config_content_to_model(example_config_file):
    config = Config(**example_config_file)

    assert_that(config).is_type_of(Config)
    assert_that(config.refresh_period_seconds).is_equal_to(15)

    assert_that(config.services).is_type_of(list).is_length(6)

    assert_that(config.services[0]).is_type_of(ServiceConfig)
    assert_that(config.services[0].url).is_type_of(str).is_equal_to(
        "https://www.w3schools.com/"
    )
    assert_that(config.services[0].expected_status_code).is_type_of(int).is_equal_to(
        200
    )
    assert_that(config.services[0].xpath).is_type_of(str).is_equal_to(
        "//*[contains(text(), 'Log in')]"
    )

    assert_that(config.services[2].xpath).is_none()
