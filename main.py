# Wordle Solver

from collections import Counter

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

    # Initialise dictionary to store word scores
    word_scores = {key: 0 for key in word_list}

    # Loop through word_list and score words based on the frequency of the letters that appear
    for word in word_list:
        for letter in word:
            word_scores[word] += letter_freq[letter]

    # Returns the highest scoring word
    best_guess = max(word_scores, key=word_scores.get)

    return best_guess

def filter_words(guess_word: str, guess_result: str, word_list: list):  # Need to fix this function, it doesn't filter words correctly

    # Loops through each element of the guess_result string and compares the equivalent index of guess_word with each word in the word_list
    # Removes words from the word_list if it does not satify the if else block
    # Likely a better way to search through this

    # x = Grey, letter does not exist in the solution
    # y = Yellow, letter does exist in the solution but is not in the correct index
    # g =  Green, letter does exist in the solution and is in the correct index

    if guess_result == "ggggg":
        print("Congrats!")

    for index, result in enumerate(guess_result):
        if result == "x":
            for word in word_list[:]:
                if guess_word[index] in word[index]:
                    word_list.remove(word)

        elif result == "y":
            for word in word_list[:]:
                if guess_word[index] not in word[index]:
                    word_list.remove(word)

        elif result == "g":
            for word in word_list[:]:
                if guess_word[index] != word[index]:
                    #print(word[index])
                    word_list.remove(word)

    return word_list


# Main loop
MAX_GUESSES = 6
count = 0

word_list = get_words("word_files/valid-wordle-words.txt")
letter_freq = letter_frequency(word_list)

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