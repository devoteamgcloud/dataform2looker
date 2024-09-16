"""This module contains unit tests for the `GenericTable` class from the `dataform2looker.database_mappers` module."""  # noqa: E501

import pytest

from dataform2looker.database_mappers import GenericTable
from dataform2looker.exceptions import UnsupportedDatabaseTypeError


class TestGenericTable:
    """Test class for the `BigqueryTable` class."""

    @pytest.fixture()
    def my_generic_table(self, bq_table_id: str) -> GenericTable:
        """Creates a `GenericTable` object for testing.

        Returns:
            GenericTable: A `GenericTable` object initialized with the provided `bq_table_id`.
        """  # noqa: E501
        return GenericTable(bq_table_id)

    def test_init(self, my_generic_table: GenericTable, bq_table_id: str) -> None:
        """Tests the initialization of a `GenericTable` object.

        Verifies that the attributes of the created `GenericTable` object match the expected values.
        """  # noqa: E501
        assert my_generic_table.table_id == bq_table_id
        assert my_generic_table.table_name == bq_table_id.split(".")[-1]
        assert isinstance(my_generic_table.dimensions, list)
        assert isinstance(my_generic_table.dimension_group, list)
        assert isinstance(my_generic_table.table_dictionary, dict)

    def test_init_unsupported_db_type(self, bq_table_id: str) -> None:
        """Tests the initialization of a `GenericTable` object with an unsupported database type.

        Verifies that the `UnsupportedDatabaseTypeError` is raised when an unsupported `db_type` is provided.
        """  # noqa: E501
        with pytest.raises(UnsupportedDatabaseTypeError):
            GenericTable(bq_table_id, "unsupported_db_type")

    def test_table_dictionary_structure(self, my_generic_table: GenericTable) -> None:
        """Tests the structure of the `table_dictionary` attribute.

        Verifies that the `table_dictionary` has the expected keys and structure.
        """  # noqa: E501
        table_dictionary = my_generic_table.table_dictionary
        assert "view" in table_dictionary
        view_keys = ["name", "sql_table_name", "dimensions", "dimension_groups"]
        for key in view_keys:
            assert key in table_dictionary["view"]


# TODO add tests to check the table_dictionary
