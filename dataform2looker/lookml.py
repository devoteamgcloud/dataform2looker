import json
import os
from database_mappers import BigqueryTable

class LookML:
    _database_types = ["bq"]

    def __init__(self, path: str, database_type = "bq") -> None:
        self.path = path
        self.database_type = database_type
        self.tables_list = self.__get_list_of_tables()
        self.__table_id_list = self.__create_list_of_table_ids()
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
        # for table_id, columns in self.__bigquery_table_info.items():
        #     view_name = table_id.split(".")[-1]
        #     lookml_views += f"view: {view_name} {{\n"
        #     lookml_views += f"  sql_table_name: {table_id} ;;\n\n"
        #     for column in columns:
        #         lookml_views += f"  dimension: {column.name} {{\n"
        #         lookml_views += f"    type: {column.looker_type}\n"
        #         lookml_views += f'    description: "{column.description}"\n'
        #         lookml_views += "  }\n\n"
        #     lookml_views += "}\n\n"
        return lookml_views

    def __create_bigquery_table_id_to_columns_mapping(self) -> dict[list[Column]]:
        bigquery_table_info = {
            table_id: BigqueryTable(table_id).columns
            for table_id in self.__table_id_list
        }
        return bigquery_table_info

    def __create_list_of_table_ids(self) -> list:
        if self.database_type == "bq":
            table_list = [
                BigqueryTable(f"{table["target"]["database"]}.{table["target"]["schema"]}.{table["target"]["name"]}")
                for table in self.__tables_list
            ]
            
        return table_list

    def __get_list_of_tables(self) -> list[dict]:
        with open(self.path, "r") as file:
            data = json.load(file)
            tables = data["tables"]
            # TODO filter for tags, there should be a paremeter for this
            return tables


if __name__ == "__main__":
    lookml_object = LookML("./result.json")
    lookml_object.create_lookml_view_files()
