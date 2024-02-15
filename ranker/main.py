from ranker import Ranker


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ranker")
    parser.add_argument("query", type=str, help="The query to rank the documents")
    args = parser.parse_args()

    ranker = Ranker("documents.json", "title_pos_index.json", "content_pos_index.json")
    ranker.run(args.query)
