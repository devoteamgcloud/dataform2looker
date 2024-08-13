
class LookML:
    def __init__(self, columns, name, table_sql):
        self.columns = columns
        self.name = name
        self.table_sql = table_sql

    def Generate(self):
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
        lookml_code += f"  derived_table: {{\n"
        lookml_code += f"    sql: {self.table_sql} ;;\n"
        lookml_code += f"  }}\n\n"

        # Define dimensions from columns
        for col in self.columns:
            lookml_code += f"  dimension: {col} {{\n"
            lookml_code += f"    type: string\n"  # TO BE ADJUSTED
            lookml_code += f"    sql: ${{TABLE}}.{col} ;;\n"
            lookml_code += f"  }}\n\n"

        lookml_code += f"}}\n"

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

    lookml_obj = LookML(columns, name, table_sql)
    lookml_code = lookml_obj.Generate()
    print(lookml_code)
