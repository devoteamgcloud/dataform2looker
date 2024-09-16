"""Test configuraitons."""

from pytest import FixtureRequest, Parser, fixture


def pytest_addoption(parser: Parser) -> None:
    """Fixture parsers."""
    parser.addoption(
        "--bq_table_id",
        action="store",
        default="bigquery-public-data.chicago_taxi_trips.taxi_trips",
        help="BigQuery table id to use for testing, \
              use chicago taxi trips schema from public data in BigQuery.",
    )
    parser.addoption(
        "--source_json_path",
        action="store",
        default="tests/dataform_result.json",
        help="Path to the Dataform JSON file used for testing.",
    )
    parser.addoption(
        "--target_folder_path",
        action="store",
        default="tests/",
        help="Target path for the generated views.",
    )


@fixture()
def bq_table_id(request: FixtureRequest) -> str:
    """Fixture bq_table_id."""
    return request.config.getoption("--bq_table_id")


@fixture()
def source_json_path(request: FixtureRequest) -> str:
    """Fixture source_json_path."""
    return request.config.getoption("--source_json_path")


@fixture()
def target_folder_path(request: FixtureRequest) -> str:
    """Fixture target_folder_path."""
    return request.config.getoption("--target_folder_path")
