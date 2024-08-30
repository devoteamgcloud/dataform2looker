from exceptions import UnsupportedDatabaseTypeError
from google.cloud import bigquery


class Column:
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

    def __init__(
        self, description: str, field_type: str, name: str, looker_type: str
    ) -> None:
        self.description = description or ""
        self.field_type = field_type
        self.name = name
        self.looker_type = looker_type
        self.column_dictionary = {
            "name": self.name,
            "type": self.field_type,
            "description": self.description,
            "sql": f"{{TABLE}}.{self.name}",
        }
        if self._DIMENSION_TYPE_MAP[self.looker_type] == "time_dimension_group":
            self.column_dictionary["timeframes"] = self._DIMENSION_GROUP_MAP[
                self.looker_type
            ]
            self.column_dictionary["datatype"] = (self.looker_type,)
        self.field_looker_type = self._DIMENSION_TYPE_MAP[self.looker_type]


class GenericTable:
    def __init__(self, table_id: str, db_type: str) -> None:
        if db_type == "bigquery":
            self.__table = BigqueryTable(table_id)
        else:
            raise UnsupportedDatabaseTypeError(db_type)
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
            if column.field_looker_type == "dimension"
        ]
        self.dimension_group = [
            column.column_dictionary
            for column in self.__table.columns
            if column.field_looker_type == "time_dimension_group"
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
        self.table_id = table_id
        self.table_name = table_id.split(".")[-1]
        self.columns = self.__get_columns()

    def __get_columns(self) -> list[Column]:
        client = bigquery.Client()
        table = client.get_table(self.table_id)
        columns = [
            Column(
                field.description,
                field.field_type,
                field.name,
                self.__map_to_looker_type(field.field_type),
            )
            for field in table.schema
        ]
        return columns

    def __map_to_looker_type(self, field_type: str) -> str:
        # Avoid using get since default to "string" might not be the best option
        return self._LOOKER_TYPE_MAP[field_type]
