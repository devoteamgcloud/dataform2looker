class UnsupportedDatabaseTypeError(Exception):
    def __init__(self, db_type: str) -> None:
        self.msg_template = f"'{db_type}' is not a supported database type"
        super().__init__(self.msg_template)
