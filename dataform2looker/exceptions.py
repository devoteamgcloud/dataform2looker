"""Custom Exception class."""  # noqa: E501


class UnsupportedDatabaseTypeError(Exception):
    """Exception raised when an unsupported database type is encountered.

    Attributes:
        msg_template (str): The error message template, containing the unsupported database type.
    """  # noqa: E501

    def __init__(self, db_type: str) -> None:
        """Initializes the `UnsupportedDatabaseTypeError` exception.

        Args:
            db_type (str): The unsupported database type.
        """  # noqa: E501
        self.msg_template = f"'{db_type}' is not a supported database type"
        super().__init__(self.msg_template)


class InvalidFieldTypeError(Exception):
    """Exception raised when an invalid field type is encountered."""

    def __init__(self, field_type: str, allowed_types: list) -> None:
        """Initializes the `InvalidFieldTypeError` exception.

        Args:
            field_type (str): The unsupported field type.
            allowed_types (list): The list of allowed types.
        """
        self.msg_template = (
            f"Invalid field type, use one of {allowed_types}, got {field_type}"
        )
        super().__init__(self.msg_template)


class TableNotFoundError(Exception):
    """Exception raised when a table is not found in the database."""

    def __init__(self, table_id: str) -> None:
        """Initializes the `TableNotFoundError` exception.

        Args:
            table_id (str): The ID of the table that was not found.
        """
        self.msg_template = (
            f"Table '{table_id}' was not found, check permissions "
            f"or if the table exists"
        )
        super().__init__(self.msg_template)
