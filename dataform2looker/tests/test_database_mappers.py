import pytest

from dataform2looker.database_mappers import BigqueryTable, Column, GenericTable
from dataform2looker.errors import UnsupportedDatabaseTypeError


# Test for BigqueryTable.__get_columns()
def test_result_should_be_correct_looker_type() -> None:
    table = BigqueryTable("sbx-edgar-dataform.austin_bikeshare.post_pre_operations")

    expected_columns = [
        Column(None, "STRING", "geo_id", "string"),
        Column(None, "INTEGER", "sum_deaths", "number"),
    ]

    assert all(
        [
            actual.looker_type == expected.looker_type
            for actual, expected in zip(table.columns, expected_columns)
        ]
    )


# Test for UnsupportedDatabaseTypeError
def test_should_not_fail_when_unsupported_database_type() -> None:
    with pytest.raises(UnsupportedDatabaseTypeError):
        GenericTable("table_id", "unsupported_db_type")
