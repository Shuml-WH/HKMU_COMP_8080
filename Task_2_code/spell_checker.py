import re
from trie import Trie


class SpellingChecker:
    def __init__(self):
        self.trie = Trie()
        self.vocab = []
        self.load_vocab("p3_vocab_list.txt")


    def load_vocab(self, vocab_file: str):
        with open(vocab_file, "r", encoding = "utf-8") as file:
            for line in file:
                word = line.strip().lower()
                if word and word.isalpha():
                    self.vocab.append(word)
                    self.trie.insert(word)  # insert the word as Trie


    def clean_text(self, text: str):
        return re.findall(r"[a-zA-Z]+", text.lower())
    

    def check_text(self, text: str):
        words = self.clean_text(text)
        wrong = []
        for word in words:
            if not self.trie.search(word) and word not in wrong:
                wrong.append(word)
            
        return wrong
    



    def suggest_words(self, word: str, prefix_length: int = 2, limit: int = 10):
        word = word.lower()
        if len(word) < prefix_length:
            prefix_length = len(word)
        prefix = word[:prefix_length]
        
        return self.trie.get_word_with_prefix(prefix, limit)