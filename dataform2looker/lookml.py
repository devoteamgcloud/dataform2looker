"""This module provides functionality for generating LookML view files based on a JSON source containing table information."""  # noqa: E501

import json
import logging

import lkml

from dataform2looker.database_mappers import GenericTable


class LookML:
    """Manages the generation and saving of LookML views.

    Attributes:
        source_json_path (str): The path to the source JSON file containing table information.
        target_folder_path (str): The target folder where LookML view files will be saved.
        lookml_templates (dict): A dictionary mapping table names to their LookML view templates.
        db_type (str): The type of the database ("bigquery" currently supported).
        tags (set[str]): A set of tags to filter tables (not yet implemented).
    """  # noqa: E501

    def __init__(
        self,
        source_json_path: str,
        target_folder_path: str,
        db_type: str = "bigquery",
        tags: list[str] = None,
    ) -> None:
        """Initializes the `LookML` object.

        Args:
            source_json_path: The path to the source JSON file.
            target_folder_path: The target folder for LookML view files.
            db_type: The type of the database ("bigquery" currently supported).
            tags: A list of tags to filter tables (not yet implemented).
        """  # noqa: E501
        self.source_json_path = source_json_path
        self.db_type = db_type
        self.__tables_ids = self.__get_list_of_table_ids()
        self.__tables_list = self.__initialize_tables(self.__tables_ids)
        self.lookml_templates = self.__generate_lookml_templates(self.__tables_list)
        self.target_folder_path = target_folder_path
        # TODO finish setting up tags to be used as filters
        # when getting the list of tables
        self.tags = set(tags or [])

    def save_lookml_views(self) -> None:
        """Generates and saves LookML view files for each table."""  # noqa: E501
        for table_name, table_template in self.lookml_templates.items():
            file_path = f"{self.target_folder_path}/" f"{table_name}.view.lkml"
            logging.debug(f"Creating file {file_path}")
            with open(file_path, "w") as f:
                f.write(table_template)
        logging.info(
            f"A total of {len(self.lookml_templates)} LookML view files successfully \
                created in folder '{self.target_folder_path}'"
        )

    def __generate_lookml_templates(self, tables_list: list[GenericTable]) -> dict:
        """Generates LookML view templates for a list of `GenericTable` objects.

        Args:
            tables_list: A list of `GenericTable` objects representing the tables.

        Returns:
            A dictionary mapping table names to their LookML view templates.
        """  # noqa: E501
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
        """Initializes `GenericTable` objects for a list of table IDs.

        Args:
            tables_ids: A list of table IDs.

        Returns:
            A list of `GenericTable` objects representing the tables.
        """  # noqa: E501
        tables_list = [GenericTable(table_id, self.db_type) for table_id in tables_ids]
        return tables_list

    def __get_list_of_table_ids(self) -> list[str]:
        """Extracts table IDs from the source JSON file.

        Returns:
            A list of table IDs in the format "project.dataset.table".
        """  # noqa: E501
        with open(self.source_json_path) as file:
            data = json.load(file)
            tables = data["tables"]
        table_id_list = [
            f"{table['target']['database']}.{table['target']['schema']}.{table['target']['name']}"
            for table in tables
        ]
        logging.debug(f"Table id list: {table_id_list}")
        logging.debug(f"Read file {self.source_json_path}, found {len(tables)}")
        # TODO implement tag filter
        # pass the following parameter tags:set[str] = None
        # use this as a filter [
        # x for table in tables if self.tags.intersection(set(table["tags"]))
        return table_id_list
