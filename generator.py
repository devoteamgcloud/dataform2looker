import argparse
import glob
import logging
import os
import subprocess
import sys
from pathlib import Path

from dataform2looker import LookML


def generate_view(lookml_directory_name: str, target_dir: str) -> None:
    logging.info(f" Generating view for: {lookml_directory_name}")
    try:
        os.makedirs(lookml_directory_name, exist_ok=True)
        lookml_object = LookML(
            "./result.json", "BigQuery", f"{os.getcwd()}/{lookml_directory_name}"
        )
        lookml_object.save_lookml_views(target_dir)
    except subprocess.CalledProcessError as e:
        logging.error(f"I failed....: {e}")



def run_pre_commit_hooks(dir: str) -> None:
    logging.info(f" Running pre-commit hooks for: {dir}")
    python_files = glob.glob(str(dir / "*.py")) #TODO: can extend for other file types 
    try:
        subprocess.run(["pre-commit", "run", "--files"] + python_files, check=True)
        logging.info("Pre-commit hooks executed successfully")
    except subprocess.CalledProcessError as e:
        logging.error(f" Error running pre-commit hooks: {e}")


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent

    parser = argparse.ArgumentParser(
        description="Generate Looker view files from dataform models"
    )
    parser.add_argument(
        "-dir",
        type=Path,
        default=script_dir / "views",
        help="Path to the views file or directory containing views.",
    )
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=script_dir.parent / "views" / "output",
        help="Target directory for looker views. Default is 'views/output'.",
    )
    parser.add_argument(
        "--pre-commit",
        action="store_true",
        help="Run pre-commits on the output files.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging.",
    )

    args = parser.parse_args()

    input_path = args.dir
    target_dir = args.target_dir
    pre_commit = args.pre_commit
    verbose = args.verbose

    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)


    if input_path.is_file():
        logging.info(f" Processing file: {input_path}")
        generate_view(input_path, target_dir)
    elif input_path.is_dir():
        for file in input_path.glob("*.py"):
            logging.info(f" Processing file: {file}")
            generate_view(file, target_dir)
    else:
        logging.error("The provided path is neither a file nor a directory")
        sys.exit(1)

    if pre_commit:
        run_pre_commit_hooks(target_dir)
