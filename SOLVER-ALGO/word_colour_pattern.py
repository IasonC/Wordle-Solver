# Author: Iason Chaimalas
# Date: 2 June 2022



import os
from collections import Counter # to count val occurences in dict
import json # for hash table read/write

import time
from tqdm import tqdm as ProgressBarLookup # to see the progress of the lookup creation

from HashTableWordle import HashTableWordle # import class for hash table

txtpath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "Words"
)

ALLOWED_WORDS_FILE = os.path.join(txtpath, "AllowedWords.txt")
SOLUTION_WORDS_FILE = os.path.join(txtpath, "SolutionWord.txt")

# read txt file with words to make the python lists that contain the words
def read_list(wordpath = 0):
    """
    Reads from the file paths for AllowedWords and SolutionWords and parses the words 
    from these txt files into a str list

    Input: wordpath
        If 0 (default) read from ALLOWED_WORDS_FILE path -> AllowedWords.txt
        Else (typically pass 1) read from SOLUTION_WORDS_FILE path -> SolutionWords.txt
    
    """
    wordlist = []
    file = ALLOWED_WORDS_FILE if wordpath == 0 else SOLUTION_WORDS_FILE
    with open(file) as f:
        words_iter = [word.strip() for word in f.readlines()]
        # iterable list of space-stripped (as failsafe - optional) words from word path
        wordlist.extend(words_iter)
        # iterate over words_iter and add each element to the wordlist
    return wordlist

# finder of string occurences
def find_nth(haystack, needle, n):
    """ haystack = list, needle = val, n = nth occurence to find """
    occ = haystack.find(needle)
    while occ >= 0 and n > 1:
        occ = haystack.find(needle, occ + len(needle))
        n -= 1
    return occ

# convert list to dict
def listtodict(lst):
    """ Converts list to dict with keys = indices and vals = list elements """
    return {i: lst[i] for i in range(len(lst))}

# set up rules
def green_letter(guess_word, true_word):
    green_index = [] # contains the indices/pos for green letters
    for i in range(len(guess_word)):
        if guess_word[i] == true_word[i]:
            green_index.append(i) # position of green letter
    
    return green_index

def yellow_letter(guess_word, true_word, green_index):
    yellow_index = []

    green_letters = list(map(lambda x: guess_word[x], green_index))
        # to get the green-flagged letters from their index list
    guess_dict = listtodict(guess_word)
        # to remove elements that are green while not losing the
        # correct index of the non-green elements in original guess_word
        # since the index is the static key
    true_dict = listtodict(true_word)

    for i in range(len(guess_word)):
        if guess_word[i] in green_letters and i in green_index:
            # this letter has already been marked green
            del guess_dict[i] # remove green elements to only analyse non-green
            del true_dict[i]

    for i in guess_dict: # i assumes vals = all non-green elements' indices
        if guess_dict[i] in [list(true_dict.items())[i][1] for i in range(len(true_dict))]:
            # letter is not green/correct but is in the true word
            # i.e. MISPLACED (Yellow) letter

            # rule - first non-green instance of a MISPLACED letter is flagged yellow. 
            # Then, if the guess contains the same letter many times.

            guess_count = sum(map((guess_dict[i]).__eq__, guess_dict.values()))
            true_count = sum(map((guess_dict[i]).__eq__, true_dict.values()))
                # optimised counter for the number of occurences of the same letter

            #print(f"i = {i} -- letter {guess_dict[i]} -- guesscount = {guess_count} -- truecount = {true_count}")

            index_ignore = []
            occ2 = find_nth(guess_word, guess_word[i], 2) # finds second occurence
            if guess_count != true_count and occ2 in guess_dict:
                # occ2 is not a green letter but is in the dict of other letters
                index_ignore.append(occ2)

            if (i not in index_ignore): yellow_index.append(i)
            # if this is not a letter that must be ignored from being flagged yellow

    return yellow_index

# colour map
def colour_map(guess_word, true_word):
    """
    Creates the colour map of a given pair of guessed and correct words.

    Parameters:
        guess_word: 5-character string
        true_word: 5-character string
    
    Output:
        int_list: 5-element list of ints from 0 to 2. 0 = green, 1 = yellow, 2 = grey.

    """

    int_list = [] # initialise the int list that represents the colour map
    
    green = green_letter(guess_word, true_word)
    yellow = yellow_letter(guess_word, true_word, green)

    for j in range(5): # 0,1,2,3,4
        if j in green: int_list.append(0) # j is green
        elif j in yellow: int_list.append(1) # j is yellow
        else: int_list.append(2) # if j is not green or yellow, it is grey

    return int_list

# convert int_list to base-10 for hash-table storage
def ternary_to_int(int_list):
    """
    Treats the int list of 5 elements representing the colour of the 5 letters
    as a 5-bit base-3 (ternary) number and converts it to an equivalent base-10
    int. This makes the storage in the hash table more memory-efficient
    
    """
    
    int_sum = 0
    for i in range(len(int_list)):
        int_sum += int_list[i] * 3 ** (len(int_list) - 1 - i)

    return int_sum

# convert hash-table base-10 to base-3 int-list to read the colour map
def int_to_ternary(tern):
    """
    The hash table stores one base-10 int as the val for the guess-true word pair.
    When reading from the hash table, this base-10 int is converted back to a 
    5-element list of ints from 0 to 2 (ternary - base 3). This re-creates the 
    colour map.
    
    """

    el = [] # int list elements
    while tern > 0:
        tern, r = divmod(tern, 3)
        # tern is updated to tern//3 floor division
        # r is the remainder of tern/3, i.e. tern % 3
        el.append(r) # the base-3 number is made up of the remainders till tern == 0
    
    el = el[::-1] # flip the element list as the elements were appended in flipped order
    while len(el) < 5: # list has less elements -- division finished early
        el.insert(0, 0) # pad with zeros at index 0

    return el

# main func -- compiles the colour map for all possible word pairs and saves to file
def hash_lookup():
    """ Creates the hash table from all the combinations of allowed and solution words """

    allowed_words = read_list(0)
    solution_words = read_list(1)

    hash_dir = HashTableWordle()

    progress_sol = ProgressBarLookup(allowed_words) # tqdm outside look -> manual control
    for guess in progress_sol: # tqdm progress bar for this task
        for true in solution_words:
            # check all guesses for a given correct/true word

            int_list_n = colour_map(guess, true)
            hash_val_n = ternary_to_int(int_list_n)
            
            key_n = (guess, true)
            hash_key_n = key_n[0] + ',' + key_n[1] # convert to str for valid key
                # comma , is valid identifier separating the guessword and trueword

            hash_dir.add_words(hash_key_n, hash_val_n)
            # go through all word pairs and append their colour map to the hash table

            progstr = f"Pairs for guessword {guess} -- Key: {hash_key_n} -- Prog: {allowed_words.index(guess)} / {len(allowed_words)}"
            progress_sol.set_description(progstr) # manual control
    
    hash_dir.save_json('hashfile_wordkey') # save hash table to json

if __name__ == "__main__":
    start = time.time()
    hash_lookup()
    end = time.time()
    print(f"Runtime = {end - start}")
