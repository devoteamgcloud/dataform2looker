"""Test configurations."""

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
        "--bq_table_id_2",
        action="store",
        default="bigquery-public-data.chicago_crime.crime",
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
    """Fixture bq_table_id.

    Returns:
        str: The BigQuery table ID specified by the `--bq_table_id` command-line option,
             defaulting to "bigquery-public-data.chicago_taxi_trips.taxi_trips".
    """  # noqa: E501
    return request.config.getoption("--bq_table_id")


@fixture()
def bq_table_id_2(request: FixtureRequest) -> str:
    """Fixture bq_table_id.

    Returns:
        str: The BigQuery table ID specified by the `--bq_table_id_2` command-line option,
             defaulting to "bigquery-public-data.chicago_crime.crime".
    """  # noqa: E501
    return request.config.getoption("--bq_table_id_2")


@fixture()
def source_json_path(request: FixtureRequest) -> str:
    """Fixture source_json_path.

    Returns:
        str: The path to the Dataform JSON file specified by the `--source_json_path` command-line option,
             defaulting to "tests/dataform_result.json".
    """  # noqa: E501
    return request.config.getoption("--source_json_path")


@fixture()
def target_folder_path(request: FixtureRequest) -> str:
    """Fixture target_folder_path.

    Returns:
        str: The target folder path specified by the `--target_folder_path` command-line option,
             defaulting to "tests/".
    """  # noqa: E501
    return request.config.getoption("--target_folder_path")


@fixture(autouse=True)
def mock_bigquery_client(mocker: FixtureRequest) -> None:
    """Mock bigquery Client to prevent actual API calls during testing."""
    from unittest.mock import MagicMock

    mock_client = mocker.patch("dataform2looker.database_mappers.bigquery.Client")
    mock_instance = mock_client.return_value

    def get_table_side_effect(table_id: str) -> MagicMock:
        mock_table = MagicMock()

        mock_field1 = MagicMock()
        mock_field1.name = "id"
        mock_field1.description = "Primary Key"
        mock_field1.field_type = "STRING"

        mock_field2 = MagicMock()
        mock_field2.name = "created_at"
        mock_field2.description = "Creation date"
        mock_field2.field_type = "TIMESTAMP"

        mock_table.schema = [mock_field1, mock_field2]
        return mock_table

    mock_instance.get_table.side_effect = get_table_side_effect
    return mock_instance
