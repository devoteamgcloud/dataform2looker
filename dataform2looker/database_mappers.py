"""Parent class for all DB to Looker Mappers and Generic table wrapper."""  # noqa: E501

import logging

from google.cloud import bigquery

from dataform2looker.exceptions import UnsupportedDatabaseTypeError


class Column:
    """Represents a column in a database table and its mapping to Looker.

    Attributes:
        name (str): The name of the column.
        description (str): The description of the column (or an empty string if not provided).
        field_type (str): The Looker data type of the column.
        data_type (str): The original database data type of the column.
        time_frames (list[str]): A list of timeframes for time dimension groups (optional).
        dimension_type (str): The type of dimension ("dimension" or "time_dimension_group").
        column_dictionary (dict): A dictionary representation of the column for Looker integration.

    """  # noqa: E501

    _DIMENSION_TYPE_MAP = {
        "number": "dimension",
        "string": "dimension",
        "timestamp": "time_dimension_group",
        "datetime": "time_dimension_group",
        "time": "time_dimension_group",
        "date": "time_dimension_group",
        "yesno": "dimension",
    }

    def __init__(
        self,
        name: str,
        description: str,
        field_type: str,
        data_type: str = None,
        time_frames: list[str] = None,
    ) -> None:
        """Initializes the `Column` object.

        Args:
            name: The name of the column.
            description: The description of the column.
            field_type: The Looker data type of the column.
            data_type: The original database data type of the column.
            time_frames: A list of timeframes for time dimension groups (optional).

        Sets the attributes and constructs the `column_dictionary` for Looker integration.
        If the column is a time dimension group, it adds `timeframes` and `datatype` to the dictionary.
        """  # noqa: E501
        self.name = name
        self.description = description or ""
        self.field_type = field_type
        self.data_type = data_type
        self.time_frames = time_frames
        assert (
            self.field_type in self._DIMENSION_TYPE_MAP
        ), f"Invalid field type, use one of {self._DIMENSION_TYPE_MAP.keys()},\
            got {self.field_type}"
        self.dimension_type = self._DIMENSION_TYPE_MAP[self.field_type]
        self.column_dictionary = {
            "name": self.name,
            "type": self.field_type,
            "description": self.description,
            "sql": f"${{TABLE}}.{self.name}",
        }
        if self.dimension_type == "time_dimension_group":
            self.column_dictionary["datatype"] = self.data_type
            self.column_dictionary["timeframes"] = self.time_frames


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

    def __init__(self, table_id: str, db_type: str = "bigquery") -> None:
        """Initializes the `GenericTable` object based on the database type.

        Args:
            table_id: The full ID of the table in the database.
            db_type: The type of the database ("bigquery" currently supported).

        Raises:
            UnsupportedDatabaseTypeError: If an unsupported `db_type` is provided.
        """  # noqa: E501
        if db_type != "bigquery":
            raise UnsupportedDatabaseTypeError(db_type)
        self.__table = BigQueryTable(table_id)
        self.table_id = table_id
        self.table_name = self.__table.table_name
        self.__db_type = db_type
        # TODO implement self.description = self.__table.description
        # This is not implemented at the moment lkml views don't support descriptions
        # At the moment the dictionary for views and dimensions are built
        # this is because the lkml lib requires the dict
        # in case something different is used then we would need to
        # re-factor the dictionary for GenericTable and Column
        self.dimensions = [
            column.column_dictionary
            for column in self.__table.columns
            if column.dimension_type == "dimension"
        ]
        logging.debug(f"Dimensions for table {self.table_name}: {self.dimensions}")
        self.dimension_group = [
            column.column_dictionary
            for column in self.__table.columns
            if column.dimension_type == "time_dimension_group"
        ]
        logging.debug(
            f"Dimensions Group for table {self.table_name}: {self.dimension_group}"
        )
        self.measures = [{"type": "count", "name": "count"}]
        # TODO it should be possible to include other measures by passing an argument
        # Include measures if needed such as sums of all number dimensions
        # include count_distinct

        self.table_dictionary = {
            "view": {
                "name": f"{self.table_name}",
                "sql_table_name": f"{table_id}",
                "dimensions": self.dimensions,
                "dimension_groups": self.dimension_group,
                "measures": self.measures,
            }
        }


class BigQueryTable:
    """Base Table class for representing BigQuery tables and their column information.

    Attributes:
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
        "TIMESTAMP": "time",
        "DATETIME": "time",
        "DATE": "time",
        "TIME": "string",
        "BOOL": "yesno",
        "ARRAY": "string",
        "GEOGRAPHY": "string",
        "BYTES": "string",
    }

    _TIME_FRAMES_MAP = {
        "TIMESTAMP": [
            "raw",
            "time",
            "hour",
            "date",
            "week",
            "month",
            "quarter",
            "year",
        ],
        "DATETIME": [
            "raw",
            "time",
            "hour",
            "date",
            "week",
            "month",
            "quarter",
            "year",
        ],
        "DATE": ["raw", "date", "week", "month", "quarter", "year"],
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
            list[Column]: A list of `Column` objects, each representing a column in the BigQuery table.
        """  # noqa: E501
        client = bigquery.Client()
        table = client.get_table(self.table_id)
        logging.debug(f"Got table schema from table {self.table_id}")
        columns = [
            Column(
                name=field.name,
                description=field.description,
                field_type=self._LOOKER_TYPE_MAP[field.field_type],
                data_type=field.field_type.lower(),
                time_frames=self._TIME_FRAMES_MAP.get(field.field_type, None),
            )
            for field in table.schema
        ]
        return columns
