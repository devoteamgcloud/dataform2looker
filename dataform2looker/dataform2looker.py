"""CLI script for generating LookML view files from Dataform models."""

import argparse
import logging
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

from dataform2looker.lookml import LookML


def _generate_view(path_to_json_file: str, target_dir: str, tags: set[str]) -> int:
    """Generates LookML view files from a Dataform model.

    Args:
        path_to_json_file (str): Path to the JSON file from compiled Dataform project.
        target_dir (str): Target directory for Looker views.
        tags (set[str]): Filter to dataform models using this tag.

    Returns:
        int: 0 if the view generation was successful, 1 otherwise.
    """
    logging.info(f" Generating views from: {path_to_json_file}")
    try:
        lookml_object = LookML(path_to_json_file, target_dir, tags=tags)
        lookml_object.save_lookml_views()
        return 0
    except subprocess.CalledProcessError as e:
        logging.error(f"I failed...: {e}")
        return 1


def main(argv: Sequence[str] | None = None) -> int:
    """Main function for the CLI script.

    Returns:
        int: 0 if the script runs successfully, 1 otherwise.
    """
    script_dir = Path(__file__).resolve().parent

    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(
        description="Generate Looker view files from dataform models",
    )

    parser.add_argument(
        "--source-file-path",
        type=Path,
        help="Path to the views file or directory containing views.",
    )
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=script_dir.parent / "views",
        help="Target directory for looker views. Default is 'views'.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging.",
    )

    parser.add_argument(
        "--tags",
        help="Filter to dataform models using this tag",
        default=[],
        type=str,
        nargs="+",
        required=False,
    )

    args = parser.parse_args(argv)

    source_file = args.source_file
    target_dir = args.target_dir
    verbose = args.verbose
    tags = args.tags

    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

    if source_file.is_file():
        logging.info(f" Processing file: {source_file}")
        return _generate_view(str(source_file), str(target_dir), set(tags))
    logging.error("The provided path is not taking to a JSON file")
    sys.exit(1)
