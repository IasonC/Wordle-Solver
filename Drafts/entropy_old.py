# Author: Iason Chaimalas
# Date: 2 June 2022



from HashTableWordle import HashTableWordle
from tqdm import tqdm as ProgressBarLookup # to see the progress of the lookup creation
import os
from word_colour_pattern import read_list

class Entropy(HashTableWordle):
    def __init__(self):
        
        
        pass # add more etc



# entropy of a possible guess
def entropy(guessword, classinst):
    """
    At any point in Wordle, there are poss possible solution words given a new guess
    with its associated guessmap (base-10 int), where E is a subset of poss.

    For any guessword, there are 3^5 possible guessmaps (0-242) as the solution word
    is unknown. Each guessmap has a probability p of occuring given the guessword.
    This p is found as the number of possibilities poss that fit the guessword over
    all possibilities 12792.

    Then, entropy I is the sum of -p*log(p) for all 243 possible guessmaps

    """
    
    I = 0 # entropy - initial sum
    for gm in range(3**5): # all guessmaps gm
        for s in self.poss: # for solution words in list of possible solutions
            poss_poss = 0 # possible solutions in list poss
            #print(f"s = {s}")
            key = (guessword, s)
            #print(f"key = {key}, hashkey = {hash(key)}")
            if self.search_words(key) == gm:
                poss_poss += 1
                # increment occurence of this gm for this given guessword
            
        p = poss_poss / len(self.poss)

        if p != 0: I -= p * log2(p) # entropy formula
        
    return I # entropy of a given guessword over the list of possible solutions at
                # that point in Wordle

def main():
    # initialise paths for allowed and solution words
    txtpath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "Words"
    )

    ALLOWED_WORDS_FILE = os.path.join(txtpath, "AllowedWords.txt")
    allowed_words = read_list(0)
    
    I = Entropy() # instance of class

    entr_prog = ProgressBarLookup(allowed_words) # tqdm entropy hashtable prog bar
    for gw in entr_prog: # for all guesswords gw
        Igw = entropy(gw) # entropy I of a guessword gw
        I.add_words(gw, Igw)

        progstr = f"Entropy for {gw}: {allowed_words.index(gw)} / {len(allowed_words)}"
        entr_prog.set_description(progstr) # manual control
    
    I.save_json('entropy')
    
if __name__ == "__main__":
    main()
