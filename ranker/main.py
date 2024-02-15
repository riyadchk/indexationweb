from ranker import Ranker


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ranker")
    parser.add_argument("query", type=str, help="The query to rank the documents")
    args = parser.parse_args()

    ranker = Ranker(
        "data/documents.json",
        "data/title_pos_index.json",
        "data/content_pos_index.json",
    )
    ranker.run(args.query)
