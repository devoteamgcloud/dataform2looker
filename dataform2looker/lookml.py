import json
import logging
import os

import lkml

from .database_mappers import GenericTable


class LookML:
    def __init__(
        self,
        source_json_path: str,
        db_type: str,
        views_target_folder: str,
        tags: list[str] = None,
    ) -> None:
        self.path = source_json_path
        self.db_type = db_type
        self.__tables_ids = self.__get_list_of_table_ids()
        self.__tables_list = self.__initialize_tables(self.__tables_ids)
        self.lookml_templates = self.__generate_lookml_templates(self.__tables_list)
        self.views_target_folder = views_target_folder
        # TODO finish setting up tags to be used as filters
        # when getting the list of tables
        self.tags = set(tags or [])

    def save_lookml_views(self) -> None:
        for table_name, table_template in self.lookml_templates.items():
            file_path = f"{self.views_target_folder}/" f"{table_name}.view.lkml"
            with open(file_path, "w") as f:
                f.write(table_template)
        logging.info(
            f"A total of {len(self.lookml_templates)} LookML view files successfully \
                created in folder '{self.views_target_folder}'"
        )

    def __generate_lookml_templates(self, tables_list: list[GenericTable]) -> dict:
        lookml_tables = {}
        for table in tables_list:
            lookml_tables[table.table_name] = lkml.dump(table.table_dictionary)
            # TODO check if we should use lkml dump to create the file
            # If we want to control the saving of the file might be easier
            # to do it outside the lib
            # https://lkml.readthedocs.io/en/latest/lkml.html#module-lkml
        return lookml_tables

    def __initialize_tables(
        self,
        tables_ids: list[str],
    ) -> list[GenericTable]:
        tables_list = [GenericTable(table_id, self.db_type) for table_id in tables_ids]
        return tables_list

    def __get_list_of_table_ids(self) -> list[str]:
        with open(self.path, "r") as file:
            data = json.load(file)
            tables = data["tables"]
        table_id_list = [
            f"{table['target']['database']}.{table['target']['schema']}.{table['target']['name']}"
            for table in tables
        ]
        logging.debug(f"Read file {self.path}, found {len(tables)}")
        # TODO implement tag filter
        # pass the following parameter tags:set[str] = None
        # use this as a filter [
        # x for table in tables if self.tags.intersection(set(table["tags"]))
        return table_id_list


if __name__ == "__main__":
    lookml_directory_name = "views"
    os.makedirs(lookml_directory_name, exist_ok=True)
    lookml_object = LookML(
        "./result.json", "bigquery", f"{os.getcwd()}/{lookml_directory_name}"
    )
    lookml_object.save_lookml_views()
