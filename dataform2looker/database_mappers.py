from google.cloud import bigquery

LOOKER_BIGQUERY_TYPE_MAP = {
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

class Column:
    def __init__(self, description: str, field_type: str, name: str, looker_type: str) -> None:
        self.description = description
        self.field_type = field_type
        self.name = name
        self.looker_type = looker_type

class BigqueryTable:
    
    def __init__(self, table_id: str) -> None:
        self.table_id = table_id
        self.columns = self.__get_columns()

    def __get_columns(self) -> list[Column]:
        client = bigquery.Client()
        table = client.get_table(self.table_id)
        columns = [
            Column(field.description, field.field_type, field.name, self.__map_bigquery_to_looker_type(field.field_type))
            for field in table.schema
        ]
        return columns
    
    def __map_bigquery_to_looker_type(self, field_type: str) -> str:
        return LOOKER_BIGQUERY_TYPE_MAP.get(field_type, "string")
