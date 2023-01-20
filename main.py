# Wordle Solver

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

def filter_words(guess_word, guess_result, word_list):

    for result, index in enumerate(guess_result):
        if result == "x" and word_list[]
    return
