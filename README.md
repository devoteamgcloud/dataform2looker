# dataform2looker

This repository provides a tool to generate LookML models from Dataform models.

## Installation

### Using requirements.txt

You can install the library using pip. Doing this you can be sure that all requirements are installed in your environment and pre-commits are installed. 

```bash
pip install -r requirements.txt
```

### From a local folder (during development)

If you have the library code locally, you can install it using:

```bash
pip install <folder_location>
```

### From a repository
You can install the library from a repository using:

```bash
pip install git+ssh://git@github.com:devoteamgcloud/dataform2looker.git
```
OR
```bash
pip install git+https://github.com/devoteamgcloud/dataform2looker.git
```

# TODO: update from here on.
## Usage

```python
from dataform2looker import generate_lookml

# Replace with your Dataform model path
dataform_model_path = "/path/to/your/dataform/model"

# Replace with your LookML output path
lookml_output_path = "/path/to/your/lookml/output"

generate_lookml(dataform_model_path, lookml_output_path)
```
This will generate LookML models based on your Dataform model and save them to the specified output path.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.