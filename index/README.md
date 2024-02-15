# Index Construction Project

This Python project is designed to construct a minimal index from a provided list of URLs by extracting page titles, tokenizing them, and building three types of indexes: a non-positional index, a non-positional index with stemming, and a positional index with stemming. It also features an option to display the progress of each step.

## Dependencies

This project requires the following libraries:

- NLTK for tokenizing and stemming.
- Requests for fetching HTML content from URLs.

Python 3.x is required. Ensure it is properly installed on your system.

## Dependency Installation

To install the necessary dependencies, execute the following command in your terminal:

```bash
pip install beautifulsoup4 nltk pandas requests
```

After installing the packages, you might need to download additional data for NLTK, especially for the tokenizer and stemmer. To do so, run:

```python
import nltk
nltk.download('punkt')
```

## Project Structure

The project is structured as follows:

- `main.py`: The main script that orchestrates the index construction process and accepts a `-v` or `--verbose` argument to display progress.
- `tokenizer.py`: Tokenizes the extracted titles.
- `stemmer.py`: Applies stemming to the tokens.
- `index_builder.py`: Builds the non-positional and positional indexes.
- `statistics_calculator.py`: Calculates and records statistics on the documents and tokens.

## Usage

To run the script, place your JSON file containing the URLs in the project folder named `urls.json`. Then execute the `main.py` script with the following command:

```bash
python main.py
```

To display the progress of each step, use the `-v` or `--verbose` option:

```bash
python main.py --verbose
```

## Generated Files

After execution, the script generates the following files in the results directory:

- `title.non_pos_index.json`: The non-positional index.
- `mon_stemmer.title.non_pos_index.json`: The non-positional index with stemming.
- `title.pos_index.json`: The positional index with stemming.
- `metadata.json`: The statistics calculated on documents and tokens.

## Contributors

- Riyad Chamekh
