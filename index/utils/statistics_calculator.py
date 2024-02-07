import json


class StatisticsCalculator:
    @staticmethod
    def calculate_statistics(crawled_urls):

        titles = [url["title"] for url in crawled_urls]
        contents = [url["content"] for url in crawled_urls]
        h1s = [url["h1"] for url in crawled_urls]

        total_documents = len(titles)
        total_tokens = 0
        tokens_per_field = {}

        for field, field_content in zip(
            ["titles", "contents", "h1s"], [titles, contents, h1s]
        ):
            tokens = 0
            for content in field_content:
                tokens += len(content.split())
            tokens_per_field[field] = tokens
            total_tokens += tokens

        # Calculate the average number of tokens per document
        average_tokens_per_document = total_tokens / total_documents
        average_token_per_title = tokens_per_field["titles"] / total_documents
        # the number of time "erreur" appears in the titles
        erreur_count = 0
        for title in titles:
            if "erreur" in title.lower():
                erreur_count += 1
        return {
            "total_documents": total_documents,
            "total_tokens": total_tokens,
            "tokens_per_field": tokens_per_field,
            "average_tokens_per_document": average_tokens_per_document,
            "average_tokens_per_titel": average_token_per_title,
            "erreur_count": erreur_count,
        }

    def save_statistics(stats, filename):
        with open(filename, "w") as f:
            json.dump(stats, f, indent=4)
