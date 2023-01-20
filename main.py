# Wordle Solver

from collections import Counter

def wordle_solver():

    word_list = get_words("word_files/valid-wordle-words.txt")

    # Guesses taken from MITs paper
    # https://auction-upload-files.s3.amazonaws.com/Wordle_Paper_Final.pdf
    optimal_guesses = ["salet", "reast", "trace", "crate", "slate"]
    return

def get_words(file):
    # Define list to store 5 letter words
    word_list = []

    # Open file and read words into a list
    with open(file, "r") as wordFile:
        for word in wordFile:
            word = word.replace("\n", "")
            word_list.append(word)

    return word_list

def score_words(word_list):

    # Initialise variable
    letter_freq = Counter()
    for word in word_list:
        letter_freq += Counter(word)

    #letter_freq = (letter_freq.values()/len(word_list) for key, value in letter_freq.items())
    print(letter_freq)
    return

def filter_words(guess_word, guess_result, word_list):

    for result, index in enumerate(guess_result):
        if result == "x":
            word_list = [word_list for word in word_list]
    return

score_words(get_words("word_files/valid-wordle-words.txt"))