import json
import os

import lkml

from dataform2looker.database_mappers import Column, GenericTable


class LookML:
    def __init__(
        self, source_json_path: str, db_type: str, views_target_folder: str
    ) -> None:
        self.path = source_json_path
        self.db_type = db_type
        self.tables_list = self.__create_tables()
        self.lookml_templates = self.__generate_lookml_templates()
        self.views_target_folder = views_target_folder

    def save_lookml_views(self) -> None:
        for index, template in enumerate(self.lookml_templates):
            file_path = (
                f"{self.views_target_folder}/"
                f"{self.tables_list[index].table.table_name}.view.lkml"
            )
            with open(file_path, "w") as f:
                f.write(template)
        return print(
            f"LookML view files successfully created in folder "
            f"'{self.views_target_folder}'"
        )

    def __generate_lookml_templates(self) -> list[str]:
        lookml_views_list = []
        for table in self.tables_list:
            lookml_view = self.__create_lookml_view(table)
            lookml_views_list.append(lkml.dump(lookml_view))
        return lookml_views_list

    def __create_lookml_view(self, table: GenericTable) -> dict:
        dimensions_list, datetime_list, date_list = self.__categorize_columns(table)

        return {
            "view": {
                "name": f"{table.table.table_name}",
                "sql_table_name": f"{table.table.table_id}",
                "dimensions": dimensions_list,
                "dimension_group": datetime_list + date_list,
            }
        }

    def __categorize_columns(self, table: GenericTable) -> tuple[list, list, list]:
        dimensions_list = []
        datetime_list = []
        date_list = []

        for column in table.table.columns:
            match column.looker_type:
                case "timestamp" | "datetime":
                    datetime_list.append(
                        self.__create_time_dimension(
                            column,
                            [
                                "raw",
                                "time",
                                "hour",
                                "date",
                                "week",
                                "month",
                                "quarter",
                                "year",
                            ],
                        )
                    )
                case "date":
                    date_list.append(
                        self.__create_time_dimension(
                            column, ["raw", "date", "week", "month", "quarter", "year"]
                        )
                    )
                case _:
                    dimensions_list.append(self.__create_dimension(column))

        return dimensions_list, datetime_list, date_list

    def __create_time_dimension(self, column: Column, timeframes: list[str]) -> dict:
        return {
            "type": "time",
            "description": f"{column.description}",
            "name": f"{column.name}",
            "datatype": f"{column.looker_type}",
            "timeframes": timeframes,
            "sql": f"{{TABLE}}.{column.name}",
        }

    def __create_dimension(self, column: Column) -> dict:
        return {
            "type": f"{column.looker_type}",
            "description": f"{column.description}",
            "name": f"{column.name}",
            "sql": f"{{TABLE}}.{column.name}",
        }

    def __create_tables(self) -> list[GenericTable]:
        tables_list = [
            GenericTable(table_id, self.db_type) for table_id in self.__get_table_ids()
        ]
        return tables_list

    def __get_table_ids(self) -> list[str]:
        table_id_list = [
            f"{table['target']['database']}.{table['target']['schema']}.{table['target']['name']}"
            for table in self.__get_list_of_tables()
        ]
        return table_id_list

    def __get_list_of_tables(self) -> list[dict]:
        with open(self.path, "r") as file:
            data = json.load(file)
            tables = data["tables"]
            return tables


if __name__ == "__main__":
    lookml_directory_name = "views"
    os.makedirs(lookml_directory_name, exist_ok=True)
    lookml_object = LookML(
        "./result.json", "BigQuery", f"{os.getcwd()}/{lookml_directory_name}"
    )
    lookml_object.save_lookml_views()
