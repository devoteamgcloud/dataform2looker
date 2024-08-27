# dataform2looker
This repository provides a tool to generate LookML models from Dataform models.

## Installation

### From the repository
You can install the library using:

```bash
pip install git+ssh://git@github.com:devoteamgcloud/dataform2looker.git --force-reinstall
```
OR
```bash
pip install git+https://github.com/devoteamgcloud/dataform2looker.git --force-reinstall
```

The `--force-reinstall` flag makes certain that the newest iteration of the code will be installed even if the version number has not been updated.

`@branch_name` can be added to the end of the git URL to install the library from a specific branch.

## Usage
### CLI Commands
You can use the following CLI commands to generate LookML models:

```bash
# Generate LookML views using default values:
#    dir =  ./views
#    target_dir = ./views/output
d2l

# Generate LookML views from a single file
d2l -dir <path/to/your/dataform/model.py>

# Generate LookML views from a directory containing multiple files and specify a target directory
d2l -dir <path/to/your/dataform/models/directory> --target-dir <path/to/your/lookml/output>


```

Replace <path/to/your/dataform/model.py> with the actual path to your Dataform model file or directory. Replace <path/to/your/lookml/output> with the desired output path for your LookML models.

#### Command Line Arguments

- `-dir`: Path to the Dataform model file or directory. This is a required argument.
- `-target-dir`: Target directory for the output LookML files. Defaults to the current directory.
- `--verbose`: Enable verbose logging for debugging purposes.
- `-h, --help `: bring out help message.

## License
This project is licensed under the MIT License.
