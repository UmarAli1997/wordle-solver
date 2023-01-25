# Wordle Solver

from collections import Counter
import string
from sys import argv

# 5 Sets of the alphabet to filter down
allowed_letters = [set(string.ascii_lowercase), set(string.ascii_lowercase), set(string.ascii_lowercase), set(string.ascii_lowercase), set(string.ascii_lowercase)]
# Letters that exist in the word but are not in the correct position
yellow_letters = set()
MAX_GUESSES = 6
count = 1

def play_wordle():

    word_list = get_words("word_files/valid-wordle-words.txt")
    answer_list = get_words("word_files/wordle-answers.txt")
    score_list = []
    letter_freq = letter_frequency(word_list)

    # Guesses taken from MITs paper
    # https://auction-upload-files.s3.amazonaws.com/Wordle_Paper_Final.pdf
    optimal_guesses = ["salet", "reast", "trace", "crate", "slate"]

    for guess in optimal_guesses:
        for answer in answer_list:
            count = 1
            while count <= MAX_GUESSES:
                guess_result = guess_response(guess, answer)
                if guess_result == "ggggg":
                    print(f"Answer found in {count} tries")
                    score_list.append(count) # How will I gather starting word statistics

                word_list = filter_letters(guess, guess_result, word_list)
                guess = score_words(word_list, letter_freq)

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

    # If there are only 2 words left in the list take the first as it is a 50/50
    if len(word_list) <= 2:
        return word_list[0]

    # Initialise dictionary to store word scores
    word_scores = {key: 0 for key in word_list}

    # Loop through word_list and score words based on the frequency of the letters that appear
    for word in word_list:
        for letter in word:
            word_scores[word] += letter_freq[letter]

    # Simple weighting algorithm to encourage more unique letters in words over the same repeating letters
    for word, score in word_scores.items():
        word_scores[word] = score / (5 - len(set(word)) + 1)

    # Returns the highest scoring word
    best_guess = max(word_scores, key=word_scores.get)

    return best_guess

def guess_response(guess_word: str, answer_word: str):
    # Function returns the comparison between the guess word and the answer word
    # like the wordle website would
    answer_word_letter_freq = {key: 0 for key in answer_word}
    response = ""

    for letter in answer_word:
        answer_word_letter_freq[letter] += 1


    for index, letter in enumerate(guess_word):
        if letter == answer_word[index]:
            response += "g"
        elif letter in answer_word:
            response += "y"
        else:
            response += "x"

    return response

def is_possible_word(word: str, allowed_letters: set, yellow_letters: set):
    # Function loops through each letter in a word and checks if it exists
    # or not in each set. If the letter does not exist in a possible solution
    # the word is not added to the new word list.

    # Loop to check if all the letters in the word are contained within the allowed_letters sets
    for index, letter in enumerate(word):
        if letter not in allowed_letters[index]:
            return False

    # If all the letters are allowed, check if they contain a yellow letter
    # If they do, then it is added to the new list
    for yellow_letter in yellow_letters:
        if yellow_letter not in word:
            return False
    return True

def find_possible_words(word_list: list, allowed_letters: set, yellow_letters: set):
    # Function builds a new list containing only possible words
    word_list = [word for word in word_list if is_possible_word(word, allowed_letters, yellow_letters)]
    return word_list

def filter_letters(guess_word: str, guess_result: str, word_list: list):
    # Function filters letters from the set of letters allowed in each position
    # x = Grey, letter does not exist in the solution
    # y = Yellow, letter does exist in the solution but is not in the correct index
    # g =  Green, letter does exist in the solution and is in the correct index

    if guess_result == "ggggg":
        print("Congrats!")
        exit()

    for index, result in enumerate(guess_result):
        letter = guess_word[index]

        # If result is grey, remove the letter from all sets
        if result == "x":
            for idx, letter_set in enumerate(allowed_letters):
                if letter in letter_set and len(letter_set) > 1:
                    allowed_letters[idx].remove(letter)

        # If the result is yellow, remove the letter from the set
        # of the corresponding index and add the letter to a seperate
        # set of letters that must exist in the answer
        elif result == "y":
            yellow_letters.add(letter)
            if letter in allowed_letters[index]:
                allowed_letters[index].remove(letter)

        # If the result is green, make the set at the corresponding index
        # contain only the green letter as it is correct
        elif result == "g":
            allowed_letters[index] = {letter}

    # Call function to filter the word list down
    word_list = find_possible_words(word_list, allowed_letters, yellow_letters)

    return word_list


# # Main loop
# MAX_GUESSES = 6
# count = 1

# word_list = get_words("word_files/valid-wordle-words.txt")
# letter_freq = letter_frequency(word_list)

# # 5 Sets of the alphabet to filter down
# allowed_letters = [set(string.ascii_lowercase), set(string.ascii_lowercase), set(string.ascii_lowercase), set(string.ascii_lowercase), set(string.ascii_lowercase)]
# # Letters that exist in the word but are not in the correct position
# yellow_letters = set()

# while count <= MAX_GUESSES:
#     user_guess = input("Enter your guess: ").lower()
#     guess_result = input('''Enter the result of your guess:
# g = Green
# y = Yellow
# x = Grey
# : ''').lower()

#     word_list = filter_letters(user_guess, guess_result, word_list)
#     best_guess = score_words(word_list, letter_freq)
#     print(f"Your best guess would be: {best_guess}\n")
#     count += 1