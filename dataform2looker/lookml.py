class Lookml:
    def __init__(self, columns: list[str], name: str, table_sql: str) -> None:
        self.columns = columns
        self.name = name
        self.table_sql = table_sql

    def generate(self) -> str:
        """
        Generates LookML code based on the provided table_sql.

        Args:
            None (uses self.table_sql)

        Returns:
            str: The LookML code representation.
        """

        # LookML View structure
        lookml_code = f"view: {self.name} {{\n"

        # Add derived table logic (assuming Dataform-style SQL)
        lookml_code += "  derived_table: {\n"
        lookml_code += f"    sql: {self.table_sql} ;;\n"
        lookml_code += "  }\n\n"

        # Define dimensions from columns
        for col in self.columns:
            lookml_code += f"  dimension: {col} {{\n"
            lookml_code += "    type: string\n"  # TO BE ADJUSTED
            lookml_code += f"    sql: ${{TABLE}}.{col} ;;\n"
            lookml_code += "  }\n\n"

        lookml_code += "}\n"

        return lookml_code


if __name__ == "__main__":
    columns = ["customer_id", "order_date", "total_amount"]
    name = "orders_view"
    table_sql = """
    SELECT
      customer_id,
      order_date,
      SUM(amount) AS total_amount
    FROM orders
    GROUP BY 1, 2
    """

    lookml_obj = Lookml(columns, name, table_sql)
    lookml_code = lookml_obj.generate()
    print(lookml_code)
