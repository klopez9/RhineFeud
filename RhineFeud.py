"""
Rhinefeud, a.k.a. Rhinequivalent

(C) Kevin Lopez, Shane Thompson, Lily Li 2014
"""

import RhineClient
import random
import sys
#Permits better parsing of Rhine return vals
import ast

debug = True

class RhineGame:
        #Dict_file_name is the name of the dict file formatted 1 word per line
        def __init__(self, dict_file_name):
                self.dict_f = dict_file_name
                self.Rhine_Prox = RhineClient.Rhine("sdf0b913e4b07b5243b7f527")

        def pick_rand_word(self):
                dict_file = open(self.dict_f, 'r')
                line_list = dict_file.read().splitlines()
                rand_word = random.choice(line_list)
                dict_file.close()
                debug("Your special phrase is: " + rand_word)
                return rand_word

        #Parse the awkward return value from RhineAPI closest_entities
        def create_word_list(self, char_list):
                cur_words = ast.literal_eval(char_list)
                cur_words = [n.strip() for n in cur_words]
                random.shuffle(cur_words)
                return cur_words
                #We randomize the list here^, so as to have a more efficent random choice selection
                
        def is_correct(self, problem_word, chosen_word, closest_dist):
                resulting_distance = self.Rhine_Prox.distance(problem_word, chosen_word)
                return abs(self.Rhine_Prox.distance(problem_word, chosen_word) - resulting_distance) <= .001

        def sub_divide_list(self, centity_list, difficulty):
                difficulty_accounting_list = centity_list[:difficulty]
                return difficulty_accounting_list

        def present_guesses(self, choice_list, special_word):
                stringChoices = ""
                i = 1
                for choice in choice_list:
                        choice = choice.replace("_", " ")
                        stringChoices += str(i) + '.' + ' ' + choice + "\t" + str(self.Rhine_Prox.distance(choice, special_word)) + '\n'
                        i += 1
                print stringChoices

        def get_choices(self, word):
                return self.Rhine_Prox.closest_entities(word)

        def get_min_distance(self, word, choice_list):
                dist_list = []
                for choice in choice_list:
                        dist_list.append(self.Rhine_Prox.distance(word, choice))
                retval = min(dist_list)
                debug("Min dist = " + str(retval))
                return retval

        def generate_choices(self, special_word):
                raw_choices = self.get_choices(special_word)
                debug("retrieved raw closest entities")
                all_choices = self.create_word_list(raw_choices)
                debug("formatted/randomized entity list")
                final_choices = self.sub_divide_list(all_choices, difficulty)
                debug("created final choice list")
                return final_choices

        def game(self):
                difficulty = 2
                print "Hello and welcome to Rhinequivalent."
                print "The goal here is to pick the word that you think is closest semantically to the given special word."
                print "Let's begin"
                while(difficulty <= 10 and difficulty > 1):
                        special_word = self.pick_rand_word()

                        final_choices = self.generate_choices(special_word)
                        
                        min_dist = self.get_min_distance(special_word, final_choices)

                        self.present_guesses(final_choices, special_word)
                        
                        guess = raw_input("Make a choice!\n")
                        
                        if self.is_correct(special_word, guess, min_dist):
                                print "You are correct and the distance is: " + str(min_dist)
                                print "Let's kick the difficulty up a notch!"
                                difficulty += 1
                        else:
                                print "Sorry, you picked wrong"
                                print "Let's try again!"
                                
                print("You win!")

def debug(message):
        if debug:
                print message

def main():
        game = RhineGame("dictionary.txt")
        game.game()
        """
        try:
                game.game()
        except:
                input("whoops")
        """

main()
