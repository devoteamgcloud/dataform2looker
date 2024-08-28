import argparse
import logging
import os
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

from dataform2looker.lookml import LookML


def _generate_view(lookml_directory_name: str, target_dir: str) -> int:
    """Generates LookML view files from a Dataform model.

    Args:
        lookml_directory_name (str): Path to the Dataform model file or directory.
        target_dir (str): Target directory for Looker views.
    """
    logging.info(f" Generating view for: {lookml_directory_name}")
    try:
        # os.makedirs(lookml_directory_name, exist_ok=True)
        lookml_object = LookML(lookml_directory_name, "BigQuery", target_dir)
        lookml_object.save_lookml_views()
        return 0
    except subprocess.CalledProcessError as e:
        logging.error(f"I failed....: {e}")
        return 1


def main(argv: Sequence[str] | None = None) -> int:
    """Main function for the CLI script."""
    script_dir = Path(__file__).resolve().parent

    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(
        description="Generate Looker view files from dataform models",
    )

    parser.add_argument(
        "-dir",
        type=Path,
        default=script_dir / "views",
        help="Path to the views file or directory containing views.",
    )
    parser.add_argument(
        "-target-dir",
        type=Path,
        default=script_dir.parent / "views" / "output",
        help="Target directory for looker views. Default is 'views/output'.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging.",
    )

    args = parser.parse_args(argv)

    input_path = args.dir
    target_dir = args.target_dir
    verbose = args.verbose

    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

    if input_path.is_file():
        logging.info(f" Processing file: {input_path}")
        return _generate_view(str(input_path), str(target_dir))
    elif input_path.is_dir():
        for file in input_path.glob("*.py"):
            logging.info(f" Processing file: {file}")
            return _generate_view(str(file), str(target_dir))
    else:
        logging.error("The provided path is neither a file nor a directory")
        sys.exit(1)


if __name__ == "__main__":
    raise SystemExit(main())
