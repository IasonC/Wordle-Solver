# Author: Iason Chaimalas
# Date: 2 June 2022



import json

class HashTableWordle():
    """
    Hash Table of 12972 allowed * 2315 solution words = 30030180 key-value pairs

    Stores the 5-element integer list associated with each pair of guessed and 
    correct word. The int list elements can be:
        0 = green
        1 = yellow
        2 = grey

    There will be an int list for all *possible* guessed-correct word pairs
    for Wordle.

    This is computationally intensive but dramatically decreases the actual
    Wordle simulation's runtime as the colour map for each pair of guessed and
    correct word is already computed and stored here.

    This Hash Table has a method to add a word pair and corresponding int list,
    and a method to search the Hash Table for the int list of a specific pair.
    
    """

    def __init__(self): # constructor
        self.hash_table = {} # initialise hash table as an empty dict

        # could be improved to allocate empty dict of preallocated size ~30 million
        # so one continuous memory chunk is allocated (saving the memory space for 
        # linked-list pointers)

    def add_words(self, key, val):
        """
        Adds a word tuple -- guess word and correct word -- into the hash table
        
        Parameters:
            key - tuple of strings: (guess_word, correct_word)
                e.g. ("gains", "games")
            val - the list of ints from 0 to 2 indicating colour of each letter
                0 = green, 1 = yellow, 2 = grey
                e.g. for key = ("gains", "games"), val = [0, 0, 2, 2, 0]

        Return:
            None

        """
        hashed_key = key
        self.hash_table.update({hashed_key: val})

    def search_words(self, key):
        """
        Searches the Hash Map for the provided key and returns the 
        associated value.

        Parameters:
            key - tuple of strings: (guess_word, correct_word)
        
        Return:
            The 5-element int list indicating the colour map for the word guess
                given the correct word.
        """

        hashed_key = key[0] + ',' + key[1]
            # typically the hashkey is hashed as hash(key) but this method does not
            # work well with this Wordle algorithm since the hash func cannot be unhashed
            # Thus, the key here is string combination of guessword and trueword
            # since tuple cannot be a key. Key is UNIQUE
        if hashed_key in self.hash_table: # check that this key input is valid
            return self.hash_table[hashed_key]
            # return int list corresponding to (guess_word, correct_word) pair
        else:
            raise KeyError(f"This key argument {key} is not in the Hash Table.")
            # stop runtime to inspect the issue in the code

    def search_value(self, val):
        """
        Searches the Hash Map for the provided value and returns the 
        associated key.

        Parameters:
            val - guessmap 5-element int list indicating the colour map for the word guess
                given the correct word
        
        Return:
            key - tuple of strings: (guess_word, correct_word)
        """

        return [tuple(k.split(',')) for k,v in self.hash_table.items() if v == val]
            # result is a list of keys which have associated value v = val.
            # then, tuple(k.split(',')) converts the list key elements into a tuple
            # of the guessword and trueword after separating the str key at the comma delimiter
    
    def save_json(self, filename):
        """ Saves the data of the hash table dictionary into a json file 
        for user readability. filename must be a str in single quotes '' """

        with open(f'{filename}.json', 'w', encoding='utf-8') as f:
            json.dump(self.hash_table, f, ensure_ascii=False, indent=4)
            # human readable json file save of hash table dir

    def read_json(self, filename):
        """ Reads from the json file storing the hash table when doing a lookup. 
        filename must be a str in single quotes: '' """

        with open(f'{filename}.json') as f:
            self.hash_table = json.load(f)
            # unloads json lookup as a python dict into the class attribute
