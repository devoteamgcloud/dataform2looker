"""This module contains unit tests for the `LookML` class from the `dataform2looker.lookml` module."""  # noqa: E501

import pytest

from dataform2looker.lookml import LookML


class TestLookML:
    """Test class for the `LookML` class."""

    @pytest.fixture()
    def my_lookml(self, source_json_path: str, target_folder_path: str) -> LookML:
        """Creates a `LookML` object for testing.

        Returns:
            LookML: A `LookML` object initialized with the provided `source_json_path` and `target_folder_path`.
        """  # noqa: E501
        return LookML(source_json_path, target_folder_path)

    def test_init(
        self, my_lookml: LookML, source_json_path: str, target_folder_path: str
    ) -> None:
        """Tests the initialization of a `LookML` object.

        Verifies that the attributes of the created `LookML` object match the expected values.
        """  # noqa: E501
        assert my_lookml.source_json_path == source_json_path
        assert my_lookml.target_folder_path == target_folder_path
        # Only 1 because there's only 1 table declared in the dataform result json
        assert len(my_lookml.lookml_templates) == 1
        assert my_lookml.db_type == "bigquery"


# TODO include a test for the generated template
