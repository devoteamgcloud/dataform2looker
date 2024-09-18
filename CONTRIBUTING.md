# Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## Installation

### Poetry

Installing the requirements file makes sure you have all libraries needed to develop the in the codebase.

```bash
poetry install
```

### From a local folder (during development)

If you have the library code locally, you can install it using:

```bash
pip install <path/to/dataform2looker>
```

The `--force-reinstall` flag makes certain that the newest iteration of the code will be installed even if the version number has not been updated.

### BigQuery

This project requires a way to run BigQuery Jobs to run the tests against the table `bigquery-public-data.chicago_taxi_trips.taxi_trips`
