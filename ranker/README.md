# Index Construction Project

This Python project is designed to construct a minimal ranking from a provided index and a query by applying a simple ranking algorithm.

## Dependencies

This project requires the following libraries:

- json for reading the index and query files.

Python 3.x is required. Ensure it is properly installed on your system.

## Dependency Installation

To install the necessary dependencies, execute the following command in your terminal:

```bash
pip install json
```

## Project Structure

The project is structured as follows:

- `main.py`: The main script that orchestrates the ranking process and requires the query and index files as arguments.
- `ranker.py`: The script that applies the ranking algorithm to the index and query.

## Usage

To run the script, place your JSON file containing the index in the data folder. Then execute the `main.py` script with the following command:

```bash
python main.py query
```

## Generated Files

After execution, the script generates the following file in the results directory:

- `results.json`: The ranking results.

## Contributors

- Riyad Chamekh
