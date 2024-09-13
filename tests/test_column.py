"""This module contains unit tests for the `Column` class from the `dataform2looker.database_mappers` module."""  # noqa: E501

from pytest import fixture

from dataform2looker.database_mappers import Column

my_column_description = "this is a column description"
my_field_type = "string"
my_column_name = "column_name"
my_dimension_type = "dimension"


class TestColumn:
    """Test class for the `Column` class."""

    @fixture()
    def my_column(self) -> Column:
        """Creates a `Column` object for testing."""
        return Column(
            description=my_column_description,
            field_type=my_field_type,
            name=my_column_name,
        )

    def test_init(self, my_column: Column) -> None:
        """Tests the initialization of a `Column` object.

        Verifies that the attributes of the created `Column` object match the expected values.
        """  # noqa: E501
        assert my_column.description == my_column_description
        assert my_column.field_type == my_field_type
        assert my_column.name == my_column_name
        assert my_column.dimension_type == my_dimension_type

    def test_dimension_dictionar(self, my_column: Column) -> None:
        """Tests the `column_dictionary` attribute of a `Column` object.

        Verifies that the `column_dictionary` is constructed correctly based on the column's attributes.
        """  # noqa: E501
        column_dictionary = {
            "name": my_column_name,
            "type": my_field_type,
            "description": my_column_description,
            "sql": f"{{TABLE}}.{my_column_name}",
        }
        assert my_column.column_dictionary == column_dictionary
