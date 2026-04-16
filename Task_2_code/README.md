## Overview
This repository contains the code for **Task 2** of the HKMU 8080 course.

The application is a terminal-based English writing checker

this project introduces and implements a **Trie (Prefix Tree)** data data structure and **Depth First Search (DFS)** algorithm (both declared in `trie.py` file)

## 🌟 Features
1. **Check a Piece of Writing:** Scans a text input for misspelled words. For any word not in the vocabulary list, the app uses DFS to search the Trie and provide a list of suggested corrections based on the word's prefix.
2. **Exact Word Search:** Instantly checks if a specific word exists in vocabulary list using Trie traversal.
3. **Prefix Matching:** Given a short prefix (e.g., "ap"), the application traverses to the end of the prefix in the Trie, then uses DFS to retrieve all valid words that start with those letters.


## 📂 File Structure
* `main-3.py`: The main execution script containing the interactive command-line menu.
* `spell_checker.py`: Contains the `SpellingChecker` class, which handles text cleaning, vocabulary loading, and bridges the prompt interface with the Trie data structure.
* `trie.py`: The core implementation of the `TrieNode` and `Trie` for the Trie data structure and the recursive `dfs_search_word` DFS algorithm.
* `p3_vocab_list.txt`: The text dataset containing the English vocabulary words.

## 🚀 How to Run
To run the script, run the following command:
   ```bash
   python main.py
