"""Parent class for all DB to Looker Mappers and Generic table wrapper."""

from google.cloud import bigquery

from .exceptions import UnsupportedDatabaseTypeError


class Column:
    """Base column class for representing column information.

    Attributes:
        _DIMENSION_TYPE_MAP (dict): A mapping of Looker data types to dimension types.
        _DIMENSION_GROUP_MAP (dict): A mapping of time-related Looker types to their available timeframes.
        name (str): The name of the column.
        description (str): The description of the column (or an empty string if not provided).
        field_type (str): The Looker data type of the column.
        dimension_type (str): The type of dimension ("dimension" or "time_dimension_group").
        column_dictionary (dict): A dictionary representation of the column for Looker integration.

    Methods:
        __init__(self, description: str, field_type: str, name: str) -> None:
            Initializes the `Column` object and constructs the `column_dictionary`.

    Raises:
        AssertionError: If an invalid `field_type` is provided.
    """  # noqa: E501

    _DIMENSION_TYPE_MAP = {
        "number": "dimension",
        "string": "dimension",
        "timestamp": "time_dimension_group",
        "datetime": "time_dimension_group",
        "date": "time_dimension_group",
        "yesno": "dimension",
    }

    _DIMENSION_GROUP_MAP = {
        "timestamp": [
            "raw",
            "time",
            "hour",
            "date",
            "week",
            "month",
            "quarter",
            "year",
        ],
        "datetime": [
            "raw",
            "time",
            "hour",
            "date",
            "week",
            "month",
            "quarter",
            "year",
        ],
        "date": ["raw", "date", "week", "month", "quarter", "year"],
    }

    def __init__(self, description: str, field_type: str, name: str) -> None:
        """Initializes the `Column` object.

        Args:
            description: The description of the column.
            field_type: The Looker data type of the column.
            name: The name of the column.

        Raises:
            AssertionError: If an invalid `field_type` is provided.

        Sets the attributes and constructs the `column_dictionary` for Looker integration.
        If the column is a time dimension group, it adds `timeframes` and `datatype` to the dictionary.
        """  # noqa: E501
        self.name = name
        self.description = description or ""
        self.field_type = field_type
        assert (
            self.field_type in self._DIMENSION_TYPE_MAP
        ), f"Invalid field type, use one of {self._DIMENSION_TYPE_MAP.keys()}"
        self.dimension_type = self._DIMENSION_TYPE_MAP[self.field_type]
        self.column_dictionary = {
            "name": self.name,
            "type": self.field_type,
            "description": self.description,
            "sql": f"{{TABLE}}.{self.name}",
        }
        if self.dimension_type == "time_dimension_group":
            self.column_dictionary["timeframes"] = self._DIMENSION_GROUP_MAP[
                self.dimension_type
            ]
            self.column_dictionary["datatype"] = self.dimension_type


class GenericTable:
    """Base Table class for representing tables from different database types.

    Attributes:
        table_id (str): The full ID of the table in the database.
        table_name (str): The name of the table (extracted from `table_id`).
        dimensions (list[dict]): A list of dictionaries representing dimensions in the table.
        dimension_group (list[dict]): A list of dictionaries representing time dimension groups.

    Methods:
        __init__(self, table_id: str, db_type: str) -> None:
            Initializes the `GenericTable` object based on the `db_type`.
            Currently supports only "bigquery" and raises an exception for other types.

    Raises:
        UnsupportedDatabaseTypeError: If an unsupported `db_type` is provided.
    """  # noqa: E501

    def __init__(self, table_id: str, db_type: str) -> None:
        """Initializes the `GenericTable` object based on the database type.

        Args:
            table_id: The full ID of the table in the database.
            db_type: The type of the database ("bigquery" currently supported).

        Raises:
            UnsupportedDatabaseTypeError: If an unsupported `db_type` is provided.
        """  # noqa: E501
        if db_type != "bigquery":
            raise UnsupportedDatabaseTypeError(db_type)
        self.__table = BigqueryTable(table_id)
        self.table_id = table_id
        self.table_name = self.__table.table_name
        self.__db_type = db_type
        # At the moment the dictionary for views and dimensions are built
        # this is because the lkml lib requires the dict
        # in case something different is used then we would need to
        # re-factor the dictionary for GenericTable and Column
        self.dimensions = [
            column.column_dictionary
            for column in self.__table.columns
            if column.dimension_type == "dimension"
        ]
        self.dimension_group = [
            column.column_dictionary
            for column in self.__table.columns
            if column.dimension_type == "time_dimension_group"
        ]
        # self.measures = # TODO set up measures
        # All views should contain count
        # TODO discuss if sum measures should be created automatically
        # for for all type numbers
        self.table_dictionary = {
            "view": {
                "name": f"{self.table_name}",
                "sql_table_name": f"{table_id}",
                "dimensions": self.dimensions,
                "dimension_groups": self.dimension_group,
                # "meausres": self.measures,
            }
        }


class BigqueryTable:
    """Base Table class for representing BigQuery tables and their column information.

    Attributes:
        _LOOKER_TYPE_MAP (dict): A mapping of BigQuery data types to their corresponding Looker types.
        table_id (str): The full ID of the BigQuery table (e.g., "project.dataset.table").
        table_name (str): The name of the BigQuery table (extracted from `table_id`).
        columns (list[Column]): A list of `Column` objects representing the table's columns.

    Methods:
        __init__(self, table_id: str) -> None:
            Initializes the `BigqueryTable` object by setting the `table_id` and `table_name`,
            and retrieving the column information using `__get_columns()`.

        __get_columns(self) -> list[Column]:
            Retrieves and structures column information from the BigQuery table.

        __map_to_looker_type(self, field_type: str) -> str:
            Maps a BigQuery field type to its corresponding Looker type using the `_LOOKER_TYPE_MAP`.
    """  # noqa: E501

    _LOOKER_TYPE_MAP = {
        "INT64": "number",
        "INTEGER": "number",
        "FLOAT": "number",
        "FLOAT64": "number",
        "NUMERIC": "number",
        "BIGNUMERIC": "number",
        "BOOLEAN": "yesno",
        "STRING": "string",
        "TIMESTAMP": "timestamp",
        "DATETIME": "datetime",
        "DATE": "date",
        "TIME": "string",
        "BOOL": "yesno",
        "ARRAY": "string",
        "GEOGRAPHY": "string",
        "BYTES": "string",
    }

    def __init__(self, table_id: str) -> None:
        """Initializes the `BigqueryTable` object.

        Args:
            table_id: The full ID of the BigQuery table (e.g., "project.dataset.table").

        Sets the `table_id` and `table_name` attributes, and retrieves column information
        using the `__get_columns()` method.
        """  # noqa: E501
        self.table_id = table_id
        self.table_name = table_id.split(".")[-1]
        self.columns = self.__get_columns()

    def __get_columns(self) -> list[Column]:
        """Retrieves and structures column information from a BigQuery table.

        This method connects to BigQuery, fetches the schema of the table identified by `self.table_id`,
        and constructs a list of `Column` objects representing each field in the table.

        Returns:
            list[Column]: A list of `Column` objects, each containing:
                - The field's description (from BigQuery).
                - The field's name.
                - The field's data type, mapped to a corresponding Looker type.
        """  # noqa: E501
        client = bigquery.Client()
        table = client.get_table(self.table_id)
        columns = [
            Column(
                field.description,
                field.name,
                self.__map_to_looker_type(field.field_type),
            )
            for field in table.schema
        ]
        return columns

    def __map_to_looker_type(self, field_type: str) -> str:
        """Maps a BigQuery field type to its corresponding Looker type.

        Args:
            field_type: The BigQuery field type string.

        Returns:
            str: The corresponding Looker type string.

        Note:
            - This method directly accesses the `_LOOKER_TYPE_MAP` dictionary.
            - It does not handle cases where the `field_type` is not found in the map.
        """  # noqa: E501
        # Avoid using get since default to "string" might not be the best option
        return self._LOOKER_TYPE_MAP[field_type]
