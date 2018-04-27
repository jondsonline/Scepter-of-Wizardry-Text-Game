# sceptergame.py
# A text adventure game where you play a wizard

import sys
# from ifclasses import *
from scepterdata import *

# ----------
# SOME DATA
# ----------

# directions used in the game
known_directions = ('east', 'e', 'west', 'w', 'north', 'n', 'south', 's')
formal_directions = ('north', 'east', 'south', 'west')

# initialize parser input class
parsed = ParsedCommand()

# ---------------------
# DISPLAY ROOM ROUTINE
# ---------------------

def show_room():
    print()
    if pc.location in room_list:
        for room in room_list:
            if pc.location == room:
                if pc.location.isvisited == False:
                    pc.location.show_long_desc()
                    pc.location.isvisited = True
                else:
                    pc.location.show_short_desc()
    else:
        print("ERROR: pc.location not in room_list")
        sys.exit()

# ---------------------
# VERB/ACTION ROUTINES
# ---------------------


def do_go():
    if parsed.noun in formal_directions:
        # loop through current room exits

        exit_found = False

        for exit in pc.location.exits:
            if parsed.noun == exit:
                for room in room_list:
                    if pc.location.exits[parsed.noun] == room.id:
                        exit_found = True
                        pc.location = room
                        break

        if exit_found == False:
            print("You can't go that way.")

    else:
        print("That is not a valid direction")
        return
"""
def do_go():
    if parsed.noun in formal_directions:
        # loop through current room exits
        for exit in pc.location.exits:
            # if parsed noun matches existing exit
            try:
                if parsed.noun in pc.location.exits[parsed.noun]:
                    for room in room_list:
                        if pc.location.exits[parsed.noun] == room.id:
                            pc.location = room
                            break
            except KeyError:
                print("You can't go that way.")
                break
"""
def do_take():
    if parsed.noun == "NA":
        print("What do you want to take?")
        return

    item_there = False

    for item in pc.location.inventory:
        if parsed.noun == item.id:
            pc.location.inventory.drop(item)
            pc.inventory.add(item)
            item_there = True
            print("Taken.")

    if item_there == False:
        print("I dont see a(n)",parsed.noun,"here.")

    return


def do_drop():
    if parsed.noun == "NA":
        print("What do you want to drop?")
        return

    item_carried = False

    for item in pc.inventory:
        if parsed.noun == item.id:
            pc.inventory.drop(item)
            pc.location.inventory.add(item)
            item_carried = True
            print("Dropped.")

    if item_carried == False:
        print("You are not carrying a",parsed.noun)

    return


def do_look():
    if parsed.noun == "NA":
        pc.location.show_long_desc()
        return

    item_found = False

    for item in pc.location.inventory:
        if parsed.noun == item.id:
            print(item.desc)
            item_found = True

    for item in pc.inventory:
        if parsed.noun == item.id:
            print(item.desc)
            item_found = True

    if item_found == False:
        print("I don't see a(n)",parsed.noun,"here.")

    return


def do_inventory():
    print("You are carrying:")

    if len(pc.inventory) == 0:
        print("Nothing")
    else:
        pc.inventory.display()


def do_exit():
    print("This will exit the game.")
    sys.exit()


def do_help():
    print("To play the game, enter either a VERB or a VERB NOUN command combination.")
    print("For a list of verbs understood by the parser, enter \"verbs\".")
    print("The game will be won when you have returned the cube to the starting room.")
    return

#
# DON'T FORGET TO EDIT THIS UPON COMPLETION!!!
#
def do_nothing():
    print ("do_nothing routine called.")
    return

# ---------------
# DEFINED VERBS
# ---------------

# set up dictionary of verbs and the fucntions they use
verbs = Verbs()
verbs.add(go=do_go)
verbs.add(get=do_take, take=do_take)
verbs.add(drop=do_drop)
verbs.add(look=do_look, x=do_look, examine=do_look)
verbs.add(i=do_inventory, inventory=do_inventory)
verbs.add(verbs="do_verbs")
verbs.add(help=do_help)
verbs.add(exit=do_exit)
verbs.add(NA=do_nothing)

# --------------
# DEFINED NOUNS
# --------------

# set up dictionary of nouns/item_id's
nouns = Nouns()
nouns.add(book="spellbook", spellbook="spellbook")
nouns.add(bread="bread", loaf="bread")
nouns.add(north="north", n="north", east="east", e="east")
nouns.add(south="south", s="south", west="west", w="west")
nouns.add(NA="NA")

# -----------------
# PARSER ROUTINES
# -----------------


def parser_get_input():
    parsed.reset()
    parsed.raw_input = (input("> ").lower()).split()


def parser_match_words():
    if len(parsed.raw_input) > 2 or len(parsed.raw_input) < 1:
        print("Commands must contain a two word verb/noun combination")
        parsed.verb = 'NA'
        return
    if len(parsed.raw_input) == 1:
        parsed.raw_input.append("NA")

    first_word = parsed.raw_input[0]
    second_word = parsed.raw_input[1]

    if first_word in known_directions:
        second_word = first_word
        first_word = "go"

    parsed.verb = parser_match_verb(first_word)

    parsed.noun = parser_match_noun(second_word)


def parser_match_verb(word):
    temp_verb = verbs.match_verb(word)
    if temp_verb == "ERR":
        print("I do not know how to", word)
        return 'NA'
    else:
        return temp_verb


def parser_match_noun(word):
    temp_noun = nouns.match_noun(word)
    if temp_noun == "ERR":
        print ("I do not know what a(n)", word, "is.")
        parsed.verb = 'NA'   # be sure to select do_nothing as a verb routine
        return
    else:
        return temp_noun


def select_verb_routine(verb_selection):
    return verbs.match_routine(verb_selection)




# ----------
# THE GAME
# ----------

game_continues = True

while game_continues == True:

    show_room()
    parser_get_input()
    parser_match_words()

    parsed.routine = select_verb_routine(parsed.verb)
    parsed.routine()


