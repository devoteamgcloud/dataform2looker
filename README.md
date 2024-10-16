# dataform2looker

This repository provides a tool to generate LookML models from Dataform models.

This command-line interface (CLI) tool helps you generate LookML view files from your Dataform models. It simplifies the process of integrating your Dataform data definitions with Looker for analysis and visualization. The tool requires the Dataform compilation JSON output

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

You can use the following CLI commands to generate LookML models. This requires the JSON outpt of the Dataform project compilation

```bash
# Generate LookML views from a single file
df2looker --source-path my_dataform_project/dataform-compile.json --target-dir my_looker_project/views
```

This command will read the dataform.json file, extract the schema information, and generate LookML view files in the my_looker_project/views directory.

#### Command Line Arguments

- `--source-path`: Path to the [Dataform compile model JSON file](https://cloud.google.com/dataform/docs/use-dataform-cli#view_compilation_output). This is a required argument.
- `--target-dir`: Target directory for the output LookML files. Defaults to a folder called `views` in the current directory if not provided.
- `--tags`: List of tags to filter the models.
- `--verbose`: Enable verbose logging for debugging purposes.
- `-h`, `--help`: bring out help message.

### Requirements

- A JSON file containing the [compilation output](https://cloud.google.com/dataform/docs/use-dataform-cli#view_compilation_output).
- A working connection to the BigQuery project to fetch the schemas of the tables

## How it Works

Schema Extraction: The CLI reads the JSON file generated by Dataform, which contains the schema definitions of your models.
LookML Generation: It then uses this schema information to create LookML view files. Each view file represents a Dataform model and includes dimensions, measures, and other relevant LookML configurations.
File Saving: The generated LookML view files are saved to the specified target directory.

### Examples

Generating the LookML Views using multiple tags. This will generate only the views for the models that match the tags.

# Generate LookML views from a single file
```bash
df2looker --source-file-path my_dataform_project/dataform-compile.json --target-dir my_looker_project/views --tags tag_1 tag_2
```

Run Dataform2Looker in verbose mode

# Generate LookML views from a single file
```bash
df2looker --source-file-path my_dataform_project/dataform-compile.json --verbose
```

## Notes

- The tool currently supports BigQuery as the underlying database for Dataform.
- You might need to adjust the generated LookML code further to match your specific Looker project requirements.
- This tool requires the BigQuery tables to exist, the reason is because Dataform doesn't provide schemas out of a compilation so it is not possible to know the schema of a table from the compilation alone.
