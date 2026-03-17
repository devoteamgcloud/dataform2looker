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
        global_labels: dict[str, str] = None,
        global_group_labels: dict[str, str] = None,
        custom_timeframes: list[str] = None,
    ) -> None:
        """Initializes the `LookML` object.

        Args:
            source_json_path: The path to the source JSON file.
            target_folder_path: The target folder for LookML view files.
            db_type: The type of the database ("bigquery" currently supported).
            tags: A list of tags to filter tables (not yet implemented).
            global_labels: A dictionary of global labels for views.
            global_group_labels: A dictionary of global group labels for views.
            custom_timeframes: A list of custom timeframes for time dimension groups.
        """  # noqa: E501
        self.source_json_path = source_json_path
        self.db_type = db_type
        self.tags = set(tags or [])
        self.global_labels = global_labels or {}
        self.global_group_labels = global_group_labels or {}
        self.custom_timeframes = custom_timeframes
        self.__tables_data = self.__get_list_of_tables()
        self.__tables_list = self.__initialize_tables(self.__tables_data)
        self.lookml_templates = self.__generate_lookml_templates(self.__tables_list)
        self.target_folder_path = target_folder_path

    def save_lookml_views(self) -> None:
        """Generates and saves LookML view files for each table."""  # noqa: E501
        import os

        os.makedirs(self.target_folder_path, exist_ok=True)

        for table_name, table_template in self.lookml_templates.items():
            file_path = f"{self.target_folder_path}/" f"{table_name}.view.lkml"
            logging.debug(f"Creating file {file_path}")
            with open(file_path, "w") as f:
                f.write(table_template)

        msg = (
            f"Generated {len(self.lookml_templates)} views in {self.target_folder_path}"
        )
        logging.info(msg)
        print(f"\n✅ {msg}\n")

    def __generate_lookml_templates(self, tables_list: list[GenericTable]) -> dict:
        """Generates LookML view templates for a list of `GenericTable` objects.

        Args:
            tables_list: A list of `GenericTable` objects representing the tables.

        Returns:
            A dictionary mapping table names to their LookML view templates.
        """  # noqa: E501
        lookml_tables = {}
        for table in tables_list:
            view_dict = table.table_dictionary["view"]
            if self.global_labels and view_dict["name"] in self.global_labels:
                view_dict["label"] = self.global_labels[view_dict["name"]]

            if (
                self.global_group_labels
                and view_dict["name"] in self.global_group_labels
            ):
                view_dict["group_label"] = self.global_group_labels[view_dict["name"]]

            # Apply custom timeframes to all dimension groups
            if self.custom_timeframes:
                for group in view_dict.get("dimension_groups", []):
                    group["timeframes"] = self.custom_timeframes

            lookml_tables[table.table_name] = lkml.dump(table.table_dictionary)
        return lookml_tables

    def __initialize_tables(
        self,
        tables_data: list[dict],
    ) -> list[GenericTable]:
        """Initializes `GenericTable` objects for a list of table dictionaries.

        Args:
            tables_data: A list of table dictionaries.

        Returns:
            A list of `GenericTable` objects representing the tables.
        """  # noqa: E501
        tables_list = []
        for table_dict in tables_data:
            target = table_dict["target"]
            table_id = f"{target['database']}.{target['schema']}.{target['name']}"
            tables_list.append(
                GenericTable(table_id, self.db_type, dataform_table=table_dict)
            )
        return tables_list

    def __get_list_of_tables(self) -> list[dict]:
        """Extracts table dictionaries from the source JSON file.

        Returns:
            A list of table dictionaries.
        """  # noqa: E501
        with open(self.source_json_path) as file:
            data = json.load(file)
            tables = data.get("tables", [])
        if self.tags:
            table_list = [
                table
                for table in tables
                if self.tags.intersection(set(table.get("tags", [])))
            ]
        else:
            table_list = [table for table in tables]
        logging.debug(f"Read file {self.source_json_path}, found {len(tables)}")
        return table_list
