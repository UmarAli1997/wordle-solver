# Wordle Solver

from collections import Counter
import string

def wordle_solver():

    word_list = get_words("word_files/valid-wordle-words.txt")

    # Guesses taken from MITs paper
    # https://auction-upload-files.s3.amazonaws.com/Wordle_Paper_Final.pdf
    optimal_guesses = ["salet", "reast", "trace", "crate", "slate"]
    return

def get_words(file: str):
    # Define list to store 5 letter words
    word_list = []

    # Open file and read words into a list
    with open(file, "r", encoding="utf-8") as wordFile:
        for word in wordFile:
            word = word.replace("\n", "")
            word_list.append(word)

    return word_list

def letter_frequency(word_list: list):

    # Loops through words and adds each letter to the variable to give a dictionary of letter frequency
    for index, word in enumerate(word_list):
        if index == 0:
            letter_freq = Counter(word)
        else:
            letter_freq.update(word)

    # Finds the occurance of a letter in the whole list as a percentage
    total_letters = sum(letter_freq.values())
    for letter, value in letter_freq.items():
        letter_freq[letter] = value / total_letters

    return letter_freq

def score_words(word_list: list, letter_freq: Counter):

    if len(word_list) <= 2:
        return word_list[0]

    # Initialise dictionary to store word scores
    word_scores = {key: 0 for key in word_list}

    # Loop through word_list and score words based on the frequency of the letters that appear
    for word in word_list:
        for letter in word:
            word_scores[word] += letter_freq[letter]

    # Returns the highest scoring word
    best_guess = max(word_scores, key=word_scores.get)

    return best_guess

def is_possible_word(word: str, allowed_letters: set, yellow_letters: set):

    for index, letter in enumerate(word):
        if letter not in allowed_letters[index]:
            return False

        for yellow_letter in yellow_letters:
            if yellow_letter not in word:
                return False
        return True

def find_possible_words(word_list, allowed_letters, yellow_letters):
    word_list = [word for word in word_list if is_possible_word(word, allowed_letters, yellow_letters)]
    return word_list

def filter_words(guess_word: str, guess_result: str, word_list: list):
    # x = Grey, letter does not exist in the solution
    # y = Yellow, letter does exist in the solution but is not in the correct index
    # g =  Green, letter does exist in the solution and is in the correct index

    if guess_result == "ggggg":
        print("Congrats!")
        exit()

    for index, result in enumerate(guess_result):

        letter = guess_word[index]

        if result == "x":
            for idx, letter_set in enumerate(allowed_letters):
                if letter in letter_set:
                    allowed_letters[idx].remove(letter)

        elif result == "y":                             # Need to fix this here
            yellow_letters.add(letter)
            if letter in allowed_letters[index]:
                allowed_letters[index].remove(letter)

        if result == "g":
            allowed_letters[index] = {letter}

    word_list = find_possible_words(word_list, allowed_letters, yellow_letters)
    print(word_list)
    return word_list


# Main loop
MAX_GUESSES = 5
count = 0

word_list = get_words("word_files/valid-wordle-words.txt")
letter_freq = letter_frequency(word_list)

# 5 Sets of the alphabet to filter down
allowed_letters = [set(string.ascii_lowercase), set(string.ascii_lowercase), set(string.ascii_lowercase), set(string.ascii_lowercase), set(string.ascii_lowercase)]
# Letters that exist in the word but are not in the correct position
yellow_letters = set()

while count <= MAX_GUESSES:
    user_guess = input("Enter your guess: ")
    guess_result = input('''Enter the result of your guess:
g = Green
y = Yellow
x = Grey
: ''')

    word_list = filter_words(user_guess, guess_result, word_list)
    best_guess = score_words(word_list, letter_freq)
    print(f"Your best guess would be: {best_guess}\n")