# dataform2looker

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