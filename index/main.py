import argparse
import os
from utils.tokenizer import Tokenizer
from utils.stemmer import Stemmer
from utils.index_builder import IndexBuilder
from utils.statistics_calculator import StatisticsCalculator
import json


def main(verbose):
    if verbose:
        print("Loading crawled urls from JSON file...")
        crawled_urls = json.load(open("data/crawled_urls.json", encoding="utf-8"))
    titles = []
    if verbose:
        print("Extracting titles from URLs...")
        titles = [url["title"] for url in crawled_urls]

    if verbose:
        print("Tokenizing and stemming titles...")
    tokenizer = Tokenizer()
    stemmer = Stemmer()
    stemmed_titles = []
    for title in titles:
        tokens = tokenizer.tokenize(title)
        stemmed_tokens = stemmer.stem_tokens(tokens)
        stemmed_titles.append(stemmed_tokens)

    if verbose:
        print("Building non-positional index...")
    non_positional_index_builder = IndexBuilder()
    for doc_id, tokens in enumerate(stemmed_titles):
        non_positional_index_builder.add_to_non_positional_index(tokens, doc_id)
    non_positional_index_builder.save_index(
        non_positional_index_builder.non_positional_index,
        "results/title.non_pos_index.json",
    )

    if verbose:
        print("Building stemmed non-positional index...")
    stemmed_non_positional_index_builder = IndexBuilder()
    for doc_id, tokens in enumerate(stemmed_titles):
        stemmed_non_positional_index_builder.add_to_non_positional_index(
            stemmed_tokens, doc_id
        )
    stemmed_non_positional_index_builder.save_index(
        stemmed_non_positional_index_builder.non_positional_index,
        "results/mon_stemmer.title.non_pos_index.json",
    )

    if verbose:
        print("Building stemmed positional index...")
    positional_index_builder = IndexBuilder()
    for doc_id, tokens in enumerate(stemmed_titles):
        positional_index_builder.add_to_positional_index(stemmed_tokens, doc_id)
    positional_index_builder.save_index(
        positional_index_builder.positional_index, "results/title.pos_index.json"
    )

    if verbose:
        print("Calculating and saving statistics...")
    stats = StatisticsCalculator.calculate_statistics(crawled_urls)
    StatisticsCalculator.save_statistics(stats, "results/metadata.json")

    if verbose:
        print("Process completed successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build indexes from a list of URLs.")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Display progress of each step.",
    )
    args = parser.parse_args()
    main(args.verbose)
