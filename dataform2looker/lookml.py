import json
import os

from google.cloud import bigquery


class Column:
    def __init__(self, description: str, type: str, name: str) -> None:
        self.description = description
        self.type = type
        self.name = name


class BigqueryTable:
    def __init__(self, table_id: str) -> None:
        self.table_id = table_id
        self.columns = self.__create_columns_array()

    def __create_columns_array(self) -> list[Column]:
        client = bigquery.Client()
        table = client.get_table(self.table_id)
        columns = [
            Column(field.description, field.field_type, field.name)
            for field in table.schema
        ]
        return columns

    def get_number_of_columns(self) -> int:
        return len(self.columns)


class LookML:
    def __init__(self, path: str) -> None:
        self.path = path
        self.__tables_list = self.__read_json_into_list_of_tables()
        self.__table_id_list = self.__create_list_of_table_ids()
        self.__bigquery_table_info = (
            self.__create_bigquery_table_id_to_columns_mapping()
        )
        self.__lookml_views_string = self.__generate_lookml_views()

    def create_lookml_view_files(self) -> None:
        lookml_directory_name = "views"
        cwd = os.getcwd()
        os.makedirs(lookml_directory_name, exist_ok=True)
        view_definitions = self.__lookml_views_string.split("view: ")[1:]
        for view_def in view_definitions:
            view_name = view_def.split(" {")[0]
            file_name = f"{view_name}.view.lkml"
            file_path = os.path.join(lookml_directory_name, file_name)
            with open(file_path, "w") as f:
                f.write("view: " + view_def)
        return print(
            f"LookML view files successfully created in folder "
            f"'{cwd}/{lookml_directory_name}'."
        )

    def __generate_lookml_views(self) -> str:
        lookml_views = ""
        for table_id, columns in self.__bigquery_table_info.items():
            view_name = table_id.split(".")[-1]
            lookml_views += f"view: {view_name} {{\n"
            lookml_views += f"  sql_table_name: {table_id} ;;\n\n"
            for column in columns:
                lookml_views += f"  dimension: {column.name} {{\n"
                lookml_views += f"    type: {column.type}\n"
                lookml_views += f'    description: "{column.description}"\n'
                lookml_views += "  }\n\n"
            lookml_views += "}\n\n"
        return lookml_views

    def __create_bigquery_table_id_to_columns_mapping(self) -> dict[list[Column]]:
        bigquery_table_info = {
            table_id: BigqueryTable(table_id).columns
            for table_id in self.__table_id_list
        }
        return bigquery_table_info

    def __create_list_of_table_ids(self) -> list[str]:
        table_id_list = [
            (
                table["target"]["database"]
                + "."
                + table["target"]["schema"]
                + "."
                + table["target"]["name"]
            )
            for table in self.__tables_list
        ]
        return table_id_list

    def __read_json_into_list_of_tables(self) -> list[dict]:
        with open(self.path, "r") as file:
            data = json.load(file)
            tables = data["tables"]
            return tables


if __name__ == "__main__":
    lookml_object = LookML("./result.json")
    lookml_object.create_lookml_view_files()
