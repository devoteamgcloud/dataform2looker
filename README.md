# dataform2looker
This repository provides a tool to generate LookML models from Dataform models.

## Installation

### From the repository
You can install the library using:

```bash
pip install git+ssh://git@github.com:devoteamgcloud/dataform2looker.git@branch_name --force-reinstall
```
OR
```bash
pip install git+https://github.com/devoteamgcloud/dataform2looker.git@branch_name --force-reinstall
```

The `--force-reinstall` flag makes certain that the newest iteration of the code will be installed even if the version number has not been updated.

## Usage
### CLI Commands
You can use the following CLI commands to generate LookML models:

```bash
# Generate LookML views using default values:
#    dir =  ./views
#    target_dir = ./views/output
python generator.py

# Generate LookML views from a single file
python generator.py -dir <path/to/your/dataform/model.py>

# Generate LookML views from a directory containing multiple files and specify a target directory
python generator.py -dir <path/to/your/dataform/models/directory> --target-dir <path/to/your/lookml/output>


```

Replace <path/to/your/dataform/model.py> with the actual path to your Dataform model file or directory. Replace <path/to/your/lookml/output> with the desired output path for your LookML models.

### Command Line Arguments

- `-dir`: Path to the Dataform model file or directory. This is a required argument.
- `--target-dir`: Target directory for the output LookML files. Defaults to the current directory.
- `--pre-commit`: Run pre-commit formatting checks on the output files.
- `--verbose`: Enable verbose logging for debugging purposes.

## License
This project is licensed under the MIT License.
