# Wordle Solver

from collections import Counter
import string
from sys import argv
import statistics as st


MAX_GUESSES = 6
count = 1


def play_wordle():

    word_list = get_words("word_files/valid-wordle-words.txt")
    answer_list = get_words("word_files/answers.txt")
    letter_freq = letter_frequency(word_list)
    score_dict = {}
    

    # Guesses taken from MITs paper
    # https://auction-upload-files.s3.amazonaws.com/Wordle_Paper_Final.pdf
    optimal_guesses = ["salet", "reast", "trace", "crate", "slate"]

    # Loop through the optimal guesses to gather statistics on best guess word with this algorithm
    for guess in optimal_guesses:
        initial_guess = guess
        score_list = []

        # Loop through ever possible answer in the answer list and use it as the hidden word
        for answer in answer_list:

            count = 1
            guess = initial_guess
            word_list_copy = word_list
            # 5 Sets of the alphabet to filter down
            allowed_letters = [set(string.ascii_lowercase), set(string.ascii_lowercase), set(string.ascii_lowercase), set(string.ascii_lowercase), set(string.ascii_lowercase)]
            # Letters that exist in the word but are not in the correct position
            yellow_letters = set()

            # Loop through solver until a solution is found
            while count <= MAX_GUESSES:
                guess_result = guess_response(guess, answer)

                # When a solution is found append it to the score list
                if guess_result == "ggggg":
                    print(f"{initial_guess}/{answer}: Answer found in {count} tries")
                    score_list.append(count)
                    break

                word_list_copy = filter_letters(guess, guess_result, word_list_copy, allowed_letters, yellow_letters)
                guess = score_words(word_list_copy, letter_freq)
                count += 1

        score_dict[initial_guess] = score_list

    game_statistics(score_dict, answer_list)

    return


def get_words(file: str):
    # Gets words from a txt file into a list

    # Define list to store words
    word_list = []

    # Open file and read words into a list
    with open(file, "r", encoding="utf-8") as wordFile:
        for word in wordFile:
            word = word.replace("\n", "")
            word_list.append(word)

    return word_list


def game_statistics(score_dict: dict, answer_list: list):
    # Returns game statistics for each optimal answer

    for starting_word, score_list in score_dict.items():
        max_score = max(score_list)
        min_score = min(score_list)
        mean_score = st.mean(score_list)
        solved = (len(score_list) / len(answer_list)) * 100

        write_string = f'''{starting_word} stats:
Minimum score: {min_score}
Maximum score: {max_score}
Average score: {mean_score}
Solved wordles: {solved}
'''

        with open(f"stats/{starting_word}_stats.txt", "w") as statsFile:
            statsFile.write(write_string)

    return


def guess_response(guess_word: str, answer_word: str):
    # Function returns the comparison between the guess word and the answer word
    # like the wordle website would
    answer_word_letter_freq = {key: 0 for key in answer_word}
    response = ""

    for letter in answer_word:
        answer_word_letter_freq[letter] += 1

    for index, letter in enumerate(guess_word):
        if letter == answer_word[index] and answer_word_letter_freq[letter] > 0:
            response += "g"
        elif letter in answer_word and answer_word_letter_freq[letter] > 0:
            response += "y"
        else:
            response += "x"

    return response


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


def filter_letters(guess_word: str, guess_result: str, word_list: list, allowed_letters: list[set], yellow_letters: set):
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

play_wordle()


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