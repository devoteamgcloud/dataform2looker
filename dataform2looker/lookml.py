import json
import os
from database_mappers import GenericTable


class LookML:
    
    def __init__(self, path: str, db_type: str, views_target_folder: str)-> None:
        self.path = path
        self.db_type = db_type
        self.tables_list = [
            GenericTable(table_id, db_type)
            for table_id in self.___get_table_ids()
        ] #TODO Move it to a function Khachatur
        self.lookml_template = None # TODO either use Jinja or use the example reference
        self.views_target_folder = None 

    def __khachatur_fun1(self)->None:
        # This function needs to save all of the templates that exist IN the LookML class
        pass

    def __khachatur_fun1(self)->None:
        # This function generates string of all of the templates 
        # that exists in the class either from template or a python lib
        pass

    def __get_list_of_tables(self) -> list[dict]:
        with open(self.path, "r") as file:
            data = json.load(file)
            tables = data["tables"]
            # TODO filter for tags, there should be a paremeter for this
            return tables
        
    def ___get_table_ids(self) -> list[str]:
        table_id_list = [
            f"{table['database']}.{table['schema']}.{table['name']}"
            for table in self.__get_list_of_tables()
        ]
        return table_id_list

    def __get_list_of_tables(self) -> list[dict]:
        with open(self.path, "r") as file:
            data = json.load(file)
            tables = data["tables"]
            # TODO filter for tags, there should be a paremeter for this
            return tables

if main="main"
    
    # Initialize LookML Class
    # Save the data to a path using the intialized class
