# Wordle-Solver
#### Wordle-solving algorithm using Mean Guessmap Minimisation.

## Performance

**Stats: 98.7% win rate, Mean 3.88 guesses with Standard Deviation 0.98 guesses needed to win on average.**
![hist_guesser](https://user-images.githubusercontent.com/73920832/171768059-a8d8338b-89dd-4a25-a6a9-40a999fafb3c.png)

This figure (Matplotlib) shows the number of guesses needed by my Wordle Solver to solve all possible unique Wordle games. There are 2315 possible unique games, since there are 2315 words that can be the Wordle solution word. Thus, my Solver played 2315 games, each with a different solution word, and recorded the number of guesses needed to win.

The Solver needs 7 guesses for 30 games, which count as losses since a Wordle game must be "won" in at most 6 guesses. Thus, the win percentage is (2315-30)/2315 = 98.7%. Also, the mean number of guesses is 3.88, with SD = 0.98 guesses. If you want to verify these statistics, please see the *GuesserSimulation_v2.txt* file in SOLVER-ALGO folder - it is the file used to generate the above plot and contains the number of guesses for each Wordle game.

## Algorithm Explanation
My Wordle Solver algorithm is my own original solution to the Wordle game hosted by the New York Times. My algorithm functions by first defining the Wordle rules that produce the 'colourmap' (aka 'guessmap') of colours corresponding to the guessed word's letters relative to the correct word's letters. The guessed word is the 'guessword' and the correct word on a single Wordle game is the 'trueword'. I define a green colour as 0, yellow as 1 and grey as 2. Thus, any guessword compared to the trueword produces a list of 5 colours (one for each letter) represented by numbers {0,1,2}. This is the guessmap, and it can be represented as a five-digit ternary number (base 3). Then, the 5-digit ternary guessmap is converted to a base-10 representation in the range 0-242 (since 3^5 = 243).

In multiple points in my algorithm, the Wordle Solver must know the guessmap associated with a guessword and trueword, or the possible truewords that are associated with a specific guessmap and guessword. Moreover, the algorithm must sometimes calculate and compare these scenarios for ALL possible guesswords (~12000). Thus, to speed up the algorithm, I wrote an initial program called **word_colour_pattern.py** that defines the Wordle rules and then applies them to ALL possible guessword-trueword pairs (12972 x 2315 = 30030180 pairs). Then, it computes the associated guessmap for each of 30M pairs and stores this data into a Hash Table using the Hash Table class **HashTableWordle.py**. The Hash Table is saved as *hashfile_wordkey.json*, which is ~714 MB so I pushed it to GitHub with LFS. Therefore, the algorithm's tasks are now reduced to iterating through the look-up table (Hash Table), which speeds up the algorithm.

The main Wordle Solver is implemented in my **guesser.py** script. The Hash Table is arranged as each guessword matched with all 2315 truewords and the associated guessmap. Iterating through the Hash Table for all guesswords and all truewords, the mean guessmap (base-10) associated with each guessword is calculated and the Solver guesses the guessword with the smallest guessmap, i.e. the guessword which will, on average, yield the largest amount of information by yielding a guessmap that is closest to all-green (zero). Apparently, the best first guess for this algorithm is *early*.

Once the Solver makes this guess, the selected guessword is compared against the trueword using the Hash Table and the guessmap is produced. Then, the guessmap and guessword are used to iterate over the Hash Table and find all possible truewords that could fit the given guessmap and guessword. Note that although the correct trueword is used to find the correct guessmap, this process is completely separate from the Solver algorithm that decides the next guess. Namely, the Solver is not "cheating" and it does not "know" the correct trueword when it decides on its next guess. Once the set of possible truewords is restricted by the guessmap-guessword search, the algorithm finds the next "best" guess by another iteration of Mean Guessmap Minimisation applied to only the guesswords and truewords that are in the restricted set of possible solution words. This process repeats until there is one possible solution word, which is then guessed by the algoritm.

## Game Modes
My Wordle Solver has 3 Game Modes: "autosolve", "manual" and "sim".

Autosolve selects a random solution word and solves it automatically with no user input.

Manual makes recommendations to the user for which word to guess; it accepts user input for which word the user *actually* guessed and the resulting guessmap. It then uses this data to make the next guess recommendation. This process repeats until the user reports to the Solver that the guessmap is 00000, meaning all-green.

Sim mode iterates over the list of all 2315 possible solution words and solves each one, recording the number of guesses needed to solve each word. This mode was used to create the Performance plot above.
