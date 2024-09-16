"""This module contains unit tests for the `BigQueryTable` class from the `dataform2looker.database_mappers` module."""  # noqa: E501

import pytest

from dataform2looker.database_mappers import BigQueryTable


class TestBigQueryTable:
    """Test class for the `BigqueryTable` class."""

    @pytest.fixture()
    def my_bq_table(self, bq_table_id: str) -> BigQueryTable:
        """Creates a `BigqueryTable` object for testing.

        Returns:
            BigQueryTable: A `BigQueryTable` object initialized with the provided `bq_table_id`.
        """  # noqa: E501
        return BigQueryTable(bq_table_id)

    def test_init(self, my_bq_table: BigQueryTable, bq_table_id: str) -> None:
        """Tests the initialization of a `BigQueryTable` object.

        Verifies that the attributes of the created `BigQueryTable` object match the expected values.
        """  # noqa: E501
        assert my_bq_table.table_id == bq_table_id
        assert my_bq_table.table_name == bq_table_id.split(".")[-1]
        assert isinstance(my_bq_table.columns, list)


# TODO add other tests for BigQueryTable class.
