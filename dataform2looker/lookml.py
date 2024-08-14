import re


class Column:
    def __init__(self, description: str, type: str, name: str) -> None:
        self.description = description
        self.type = type
        self.name = name

    def get_description(self) -> str:
        return self.description

    def get_type(self) -> str:
        return self.type

    def set_type(self, value: str) -> None:
        self.type = value

    def get_name(self) -> str:
        return self.name


class LookML:
    def __init__(
        self, path: str, table_name: str, description: str, columns: list[Column]
    ) -> None:
        self.path = path
        self.table_name = table_name
        self.description = description
        self.columns = columns

    def get_path(self) -> str:
        return self.path

    def get_config(self) -> str | None:
        with open(self.path, "r") as file:
            content = file.read()

        # Match the config block using a regular expression
        match = re.search(r"config \{\n(.*?)\}\n", content, re.DOTALL)

        if match:
            return match.group(1).strip()
        else:
            return None

    def get_type(self) -> str | None:
        config_block = self.get_config()

        # Match the specific comment pattern within the config block
        type_match = re.search(r"//df2lkml:type:(\w+)", config_block)

        if type_match:
            return type_match.group(1)
        else:
            return None

    def get_column_name(self) -> str:
        column_name = ""
        return column_name

    def get_column_description(self) -> str | None:
        column_description = ""
        return column_description

    def create_column(self) -> Column:
        return Column(
            self.get_column_description(), self.get_type(), self.get_column_name()
        )

    def create_columns(self) -> list[Column]:
        columns = []
        print("IMPLEMENT ME!!! CREATE COLUMNS[]")
        return columns

    # def generate(self) -> str:
    #     """
    #     Generates LookML code based on the provided table_sql.
    #
    #     Args:
    #         None (uses self.table_sql)
    #
    #     Returns:
    #         str: The LookML code representation.
    #     """
    #
    #     # LookML View structure
    #     lookml_code = f"view: {self.name} {{\n"
    #
    #     # Add derived table logic (assuming Dataform-style SQL)
    #     lookml_code += "  derived_table: {\n"
    #     lookml_code += f"    sql: {self.table_sql} ;;\n"
    #     lookml_code += "  }\n\n"
    #
    #     # Define dimensions from columns
    #     for col in self.columns:
    #         lookml_code += f"  dimension: {col} {{\n"
    #         lookml_code += "    type: string\n"  # TO BE ADJUSTED
    #         lookml_code += f"    sql: ${{TABLE}}.{col} ;;\n"
    #         lookml_code += "  }\n\n"
    #
    #     lookml_code += "}\n"
    #
    #     return lookml_code


if __name__ == "__main__":
    column_vardavar = Column("My column description", "VARCHAR", "Vardavar")
    column_amanor = Column("My column description", "VARCHAR", "Amanor")
    print(
        column_vardavar.get_name(),
        column_vardavar.get_type(),
        column_vardavar.get_description(),
    )

    path_to_sqlx = "/Users/khachatur/dataform2looker/example/synthetic_definition.sqlx"
    table_name = "Festivities"
    description = "My Festivities' description"
    columns = [column_vardavar, column_amanor]

    lookml_obj = LookML(path_to_sqlx, table_name, description, columns)

    print(lookml_obj.get_config())
    print(lookml_obj.get_type())
    empty_column_type = lookml_obj.create_column()
    print(empty_column_type.get_type())
