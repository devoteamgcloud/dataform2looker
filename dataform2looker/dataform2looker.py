"""CLI script for generating LookML view files from Dataform models."""

import argparse
import logging
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

from dataform2looker.lookml import LookML


def _generate_view(
    path_to_json_file: str,
    target_dir: str,
    tags: set[str],
    global_labels: dict[str, str] = None,
    global_group_labels: dict[str, str] = None,
    custom_timeframes: list[str] = None,
) -> int:
    """Generates LookML view files from a Dataform model.

    Args:
        path_to_json_file (str): Path to the JSON file from compiled Dataform project.
        target_dir (str): Target directory for Looker views.
        tags (set[str]): Filter to dataform models using this tag.
        global_labels (dict[str, str]): Global labels to apply.
        global_group_labels (dict[str, str]): Global group labels to apply.
        custom_timeframes (list[str]): Custom timeframes for dimension groups.

    Returns:
        int: 0 if the view generation was successful, 1 otherwise.
    """
    logging.info(f" Generating views from: {path_to_json_file}")
    try:
        lookml_object = LookML(
            path_to_json_file,
            target_dir,
            tags=tags,
            global_labels=global_labels,
            global_group_labels=global_group_labels,
            custom_timeframes=custom_timeframes,
        )
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

    parser.add_argument(
        "--global-labels",
        help="Global labels to apply (key=value format, can be used multiple times)",
        action="append",
        default=[],
    )

    parser.add_argument(
        "--global-group-labels",
        help="Global group labels to apply (key=value, multiple allowed)",
        action="append",
        default=[],
    )

    parser.add_argument(
        "--custom-timeframes",
        help="Custom timeframes to use for dimension groups",
        default=[],
        type=str,
        nargs="+",
    )

    args = parser.parse_args(argv)

    source_file = args.source_file_path
    target_dir = args.target_dir
    verbose = args.verbose
    tags = args.tags

    global_labels = dict(item.split("=") for item in args.global_labels if "=" in item)
    global_group_labels = dict(
        item.split("=") for item in args.global_group_labels if "=" in item
    )
    custom_timeframes = args.custom_timeframes

    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

    if source_file.is_file():
        logging.info(f" Processing file: {source_file}")
        return _generate_view(
            str(source_file),
            str(target_dir),
            set(tags),
            global_labels=global_labels,
            global_group_labels=global_group_labels,
            custom_timeframes=custom_timeframes,
        )
    logging.error("The provided path is not taking to a JSON file")
    sys.exit(1)
