import re

class TrieNode:
    def __init__(self):
        self.children = {}
        self.endOfWord = False


class Trie:
    def __init__(self):
        self.root = TrieNode()


    def insert(self, word: str) -> None:
        cur = self.root

        for c in word.lower():
            if c not in cur.children:
                cur.children[c] = TrieNode()
            cur = cur.children[c]
        cur.endOfWord = True


    def search(self, word: str) -> bool:
        cur = self.root
        for c in word.lower():
            if c not in cur.children:
                return False
            cur = cur.children[c]
        return cur.endOfWord  # implicitly know if the search word is a word stored in Trie
    
    
    def start_with(self, prefix: str) -> bool:
        cur = self.root

        for c in prefix.lower():
            if c not in cur.children:
                return False
            cur = cur.children[c]
        return True
    

    def get_word_with_prefix(self, prefix: str, limit: int = 10):
        cur = self.root
        prefix = prefix.lower()
        for c in prefix:
            if c not in cur.children:
                return []
            cur = cur.children[c]   # jump to the last node of the Trie tree

        return self.dfs_search_word(cur, prefix, limit)  # pass the last Trie node tp DFS, tgt with the entire prefix



# Perform DFS, to collect full words from a given prefix
    def dfs_search_word(self, cur: TrieNode, curWord, limit):
        result = []

        if cur.endOfWord:
            result.append(curWord)

        for c in sorted(cur.children.keys()):
            if len(result) >= limit:
                break

            childResult = self.dfs_search_word(cur.children[c], curWord + c, limit - len(result))
            result.extend(childResult)
        
        return result