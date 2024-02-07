import json


class IndexBuilder:
    def __init__(self):
        self.non_positional_index = {}
        self.positional_index = {}

    def add_to_non_positional_index(self, tokens, doc_id):
        for token in tokens:
            if token not in self.non_positional_index:
                self.non_positional_index[token] = [doc_id]
            elif doc_id not in self.non_positional_index[token]:
                self.non_positional_index[token].append(doc_id)

    def add_to_positional_index(self, tokens, doc_id):
        for position, token in enumerate(tokens):
            if token not in self.positional_index:
                self.positional_index[token] = {doc_id: [position]}
            elif doc_id not in self.positional_index[token]:
                self.positional_index[token][doc_id] = [position]
            else:
                self.positional_index[token][doc_id].append(position)

    def save_index(self, index, file_name):
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=4, ensure_ascii=False)
