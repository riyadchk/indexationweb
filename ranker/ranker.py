import json


class Ranker:
    def __init__(self, documents_file, title_index_file, content_index_file):
        with open(documents_file, "r", encoding="utf-8") as f:
            self.documents = json.load(f)

        with open(title_index_file, "r", encoding="utf-8") as f:
            self.title_index = json.load(f)

        with open(content_index_file, "r", encoding="utf-8") as f:
            self.content_index = json.load(f)

    def preprocess_text(self, text):
        tokens = text.lower().split()
        return tokens

    def filter_documents(self, query_tokens):
        matching_docs = set(self.title_index.keys()).union(self.content_index.keys())

        for token in query_tokens:
            matching_docs.intersection_update(
                set(self.title_index.get(token, {}).keys())
                | set(self.content_index.get(token, {}).keys())
            )

        return matching_docs

    def linear_ranking(self, documents, query_tokens):
        rankings = {}

        for doc_id in documents:
            score_title = 0
            score_content = 0

            for token in query_tokens:
                if doc_id in self.title_index.get(token, {}):
                    score_title += (
                        self.title_index[token].get(doc_id, {}).get("count", 0)
                    )

                if doc_id in self.content_index.get(token, {}):
                    score_content += (
                        self.content_index[token].get(doc_id, {}).get("count", 0)
                    )

            score = 0.8 * score_title + 0.2 * score_content
            rankings[doc_id] = score

        sorted_documents = sorted(rankings.items(), key=lambda x: x[1], reverse=True)
        return sorted_documents

    def generate_results_json(
        self, sorted_documents, output_file="results/results.json"
    ):
        results = []

        for doc_id, score in sorted_documents:
            doc_info = {
                "Title": self.documents[int(doc_id)]["title"],
                "Url": self.documents[int(doc_id)]["url"],
            }
            results.append(doc_info)

        result_data = {
            "Number of documents in the index": len(self.documents),
            "Number of documents that survived the filter": len(sorted_documents),
            "Documents": results,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)

    def run(self, query):
        query_tokens = self.preprocess_text(query)
        matching_docs = self.filter_documents(query_tokens)
        sorted_documents = self.linear_ranking(matching_docs, query_tokens)
        self.generate_results_json(sorted_documents)
