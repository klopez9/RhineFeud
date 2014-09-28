"""
RhineFeud, a.k.a. Rhinequivalent
Python 2.x
RhineFeud (C) Kevin Lopez, Shane Thompson, Lily Li 2014
Rhine (C) Speare 2014

This is a simple game using the Rhine API. Rhine checks the "semantic distance"
between two "entities." That is, it quantifies the relationship between two
abstract ideas by aggregating crowd-sourced data and analyzing how inter-
connected they are (or appear to be). This game gets a phrase from a supplied
dictionary file and queries Rhine for the closest entities (that is, phrases
and ideas with the smallest semantic distances) to the given phrase. Then the
program gives the user a certain amount of these closest entities to choose
from. If the user can figure out which is the semantically closest entity to
the given word, she moves on to the next difficulty. The user wins after
correctly guessing at difficulty = 10.
"""

import RhineClient
import random
import sys
#import ast
import urllib

API_KEY = "sdf0b913e4b07b5243b7f527"
DEBUG = False
CHEATS = True
MAX_DIFFICULTY = 10

class RhineGame:
        """
        init function
        dict_f is the name of the dict file formatted 1 word per line
        Rhine_Prox is the Rhine client interface
        """
        def __init__(self, dict_file_name):
                self.dict_f = dict_file_name
                self.Rhine_Prox = RhineClient.Rhine(API_KEY)

        """
        picks random word from the dictionary file for use in the game
        """
        def pick_rand_word(self):
                dict_file = open(self.dict_f, 'r')
                line_list = dict_file.read().splitlines()
                rand_word = random.choice(line_list)
                dict_file.close()
                debug("word: " + rand_word)
                return rand_word

        """
        creates the closest entity list using the given word
        """
        def get_choices(self, word):
                return self.Rhine_Prox.closest_entities(word)

        """
        parses and formats the awkward return value from RhineAPI closest_entities
        """
        def create_word_list(self, char_list):
                for w in char_list:
                        w = w.replace('_', ' ')

        """
        returns entity sublist with size less than or equal to difficulty level
        """
        def sub_divide_list(self, entity_list, difficulty):
                return entity_list if len(entity_list) <= difficulty else entity_list[:difficulty]

        """
        formats and prints choices from entity sublist
        """
        def present_guesses(self, choice_list, special_word):
                stringChoices = "\n"
                i = 1
                for choice in choice_list:
                        choice = choice.replace("_", " ")
                        stringChoices += str(i) + '.' + ' ' + choice
                        if CHEATS:
                                stringChoices += '\t' + str(self.Rhine_Prox.distance(choice, special_word)) + '\n'
                        i += 1
                print stringChoices

        """
        checks distance value of input phrase against correct minimum distance value
        """
        def is_correct(self, problem_word, chosen_word, closest_dist):
                resulting_distance = self.Rhine_Prox.distance(problem_word, chosen_word)
                return abs(closest_dist - resulting_distance) <= .001
                
        """
        gets the smallest semantic distance from the list of related entities
        """
        def get_min_distance(self, word, choice_list):
                dist_list = []
                for choice in choice_list:
                        dist_list.append(self.Rhine_Prox.distance(word, choice))
                retval = min(dist_list)
                debug("Min dist = " + str(retval))
                return retval

        """
        gets semantic Rhine data and saves to .txt, then returns the choice list
        """
        def generate_choices(self, special_word, difficulty):
                """
                Try to open <special_word>_RhineFeud.txt and read values from it;
                if it does not exist, retrieve data from Rhine and write to file
                """
                file_name = special_word.replace(" ", "_") + "_RhineFeud.txt"
                file_was_read = False
                choices = []
                distances = []
                while not file_was_read:
                        connection_error = False
                        try:
                                if connection_error:
                                        raise IOError("reconnecting")
                                rhine_word_file = open(file_name, 'r')
                                while True:
                                        c = rhine_word_file.readline()
                                        if not c:
                                                break
                                        d = rhine_word_file.readline()
                                        if not d:
                                                break
                                        choices.append(str(c))
                                        if (str(d) != "nan"):
                                                distances.append(float(d))
                                        else:
                                                rhine_word_file.close()
                                                print "nan dist value encountered; retrieving new Rhine data"
                                                raise IOError("nan")
                                rhine_word_file.close()
                                file_was_read = True
                        except IOError:
                                choices = self.get_choices(special_word)
                                debug("retrieved closest entities")
                                debug("writing to file...")
                                self.create_word_list(choices)
                                rhine_word_file_new = open(file_name, 'w')
                                for l in choices:
                                        l = l.replace("_", " ")
                                        rhine_word_file_new.write(l + '\n')
                                        try:
                                                dist = str(self.Rhine_Prox.distance(special_word, l))
                                                rhine_word_file_new.write(dist + '\n')
                                        except Exception as e:
                                                rhine_word_file_new.close()
                                                print "connection failure"
                                                connection_error = True
                                                pass
                                if not connection_error:
                                        debug("written to file " + file_name)
                                else:
                                        debug("re-retrieving Rhine data")
                                rhine_word_file_new.close()

                for c in choices:
                        debug(urllib.unquote(c))
                for d in distances:
                        debug(d)
                
                random.shuffle(choices)
                final_choices = self.sub_divide_list(choices, difficulty)
                debug("created final choice list")
                return final_choices

        """
        Fun victory messages
        """
        def win_message(self, d):
                if d == 2:
                        print "We're just getting warmed up here.\nIncreasing Difficulty Levels..."
                elif d == 3:
                        print "Not bad.\nBut can you handle..."
                elif d == 4:
                        print "Alright, you're pretty good.\nHow about..."
                elif d == 5:
                        print "That was a tough one!\nThis should be a piece of cake then..."
                elif d == 6:
                        print "What?! I thought I had you for sure!\nVery well..."
                elif d == 7:
                        print "Hmm... perhaps desperate times\ncall for desperate measures..."
                elif d == 8:
                        print "How did you make it this far?\nWhy won't you give up?!"
                elif d == 9:
                        print "No!\nI won't let you win!"
                elif d == MAX_DIFFICULTY:
                        raw_input("You win! (Press Enter to continue.)")
                        raw_input("I am bested.")
                        raw_input("Congratulations.")
                else:
                        print "..."

                if d < 10:
                        raw_input("Difficulty Level " + str(d-1) + "!\n(Press Enter to continue.)")

        """
        Game Logic
        """
        def game(self):
                difficulty = 2
                print "Hello! Welcome to Rhinequivalent."
                print "The goal here is to pick the word that you think is closest semantically to the given special phrase."
                print "Let's begin!"

                #loop continuously as phrases are generated and guesses are made
                while(difficulty <= MAX_DIFFICULTY and difficulty > 1):
                        
                        print "\nLoading..."

                        #randomly pick word from dictionary
                        special_word = self.pick_rand_word()
                        #cull entity list
                        final_choices = self.generate_choices(special_word, difficulty)
                        #find minimum semantic distance
                        min_dist = self.get_min_distance(special_word, final_choices)
                        #print formatted entity list to user
                        self.present_guesses(final_choices, special_word)

                        print "Your special phrase is: " + special_word

                        #get guess number from user
                        #reject input and loop if out of bounds or non-integer
                        index = -1
                        while index < 0 or index >= len(final_choices):
                                if index != -1:
                                        print "Out of bounds."
                                choice = raw_input("Choose a number.\n")
                                try:
                                        index = int(choice) - 1
                                except ValueError:
                                        print "Invalid input."
                                        index = 0

                        #if user is correct, up difficulty
                        if self.is_correct(special_word, final_choices[index], min_dist):
                                print "You are correct! The semantic distance is: " + str(min_dist) + "."
                                self.win_message(difficulty)
                                difficulty += 1
                        else:
                                print "Sorry, you picked wrong."
                                print "Let's try again!"

"""
print debugging is the best kind of debugging
"""
def debug(message):
        if DEBUG:
                print message

"""
main function
"""
def main():

        game = RhineGame("dictionary.txt")
        game.game()

main()
