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
