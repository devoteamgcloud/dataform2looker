"""Test configuraitons."""

from pytest import FixtureRequest, Parser, fixture


def pytest_addoption(parser: Parser) -> None:
    """Fixture bq_table_id parser."""
    parser.addoption(
        "--bq_table_id",
        action="store",
        default="bigquery-public-data.chicago_taxi_trips.taxi_trips",
        help="bigqueyr table id to use for testing, \
              use chicago taxi trips schema from public data in BigQuery",
    )


@fixture()
def bq_table_id(request: FixtureRequest) -> str:
    """Fixture bq_table_id."""
    return request.config.getoption("--bq_table_id")
