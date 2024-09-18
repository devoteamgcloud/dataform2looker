"""This module contains unit tests for the `Column` class from the `dataform2looker.database_mappers` module."""  # noqa: E501

from pytest import fixture, raises

from dataform2looker.database_mappers import Column

my_column_description = "this is a column description"
my_field_type = "string"
my_column_name = "column_name"
my_dimension_type = "dimension"


class TestColumn:
    """Test class for the `Column` class."""

    @fixture()
    def my_column(self) -> Column:
        """Creates a `Column` object for testing.

        Returns:
            Column: A `Column` object.
        """  # noqa: E501
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

    def test_time_dimension_group(self) -> None:
        """Tests the initialization of a time dimension group `Column` object.

        Verifies that the `column_dictionary` is constructed correctly with `timeframes` and `datatype`.
        """  # noqa: E501
        column = Column(
            name="created_at",
            description="Date the record was created",
            data_type="timestamp",
            field_type="datetime",
            time_frames=["raw", "time", "date", "week", "month", "quarter", "year"],
        )
        assert column.dimension_type == "time_dimension_group"
        assert "timeframes" in column.column_dictionary

    def test_invalid_field_type(self) -> None:
        """Tests the initialization of a `Column` object with an invalid field type.

        Verifies that an `AssertionError` is raised when an invalid `field_type` is provided.
        """  # noqa: E501
        with raises(AssertionError):
            Column(
                name="invalid_column",
                description="Invalid column with unsupported type",
                field_type="invalid_type",
            )
