from spell_checker import SpellingChecker


def display_menu():
    print("\n======= English Writing Checker (Primary School Level)=======")
    print("1. Check a piece of writing")
    print("2. Search whether a word exists")
    print("3. Show words with a prefix")
    print("4. Exit")



def main():
    checker = SpellingChecker()

    while True:
        display_menu()
        input_choice = input("Enter Your Choice (1 to 4): ").strip()

        if input_choice == "1":
            text = input("\nEnter the Student's Writing: \n")
            wrong_word = checker.check_text(text)

            if not wrong_word:
                print("\nNo Spelling Mistakes Found")
            else:
                print("\nPossible Spelling Mistakes:")
                for word in wrong_word:
                    suggest_word = checker.suggest_words(word)
                    print("for the word: " + word)
                    if suggest_word:
                        print(f"Suggestions: {', '.join(suggest_word)}\n")
                input("Enter Any Word to Continue...")


        elif input_choice == "2":
            word = input('Enter a word to search: ').strip().lower()
            if checker.trie.search(word):
                print(f"The word - {word} - is in the vocabulary list.")
            else:
                print(f"The word - {word} - is not the vocabulary list.")
            input("Enter Any Word to Continue...")



        elif input_choice == "3":
            prefix = input('Enter a prefix: ').strip().lower()
            match_word = checker.trie.get_word_with_prefix(prefix)

            if match_word:
                print("Word found: ", ": ".join(match_word))
            input("Enter Any Word to Continue...")

        elif input_choice == '4':
            print('Bye! ')
            break

        else:
            print('Invalid choice. Please enter 1, 2, 3, or 4.')


if __name__ == "__main__":
    main()