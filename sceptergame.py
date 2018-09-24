# THE SCEPTER OF WIZARDRY
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
                # Check if ogre is dead before exiting the cave
                if pc.location == cave and not flag.ogre_dead:
                    print("You try to escape the ogre, but it is too quick for you. He smashes\n"
                          "his club down on your head and you are killed.")
                    sys.exit()

                # Test for victory condition (player has Scepter) before entering town
                elif pc.location == gate and exit == 'south':
                    exit_found = True
                    do_test_for_victory()

                # Default response if approved exit is found
                else:
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


def do_take():
    if parsed.noun == "NA":
        print("What do you want to take?")
        return

    item_there = False

    for item in pc.location.inventory:
        if parsed.noun == item.id:
            item_there = True
            if item.is_takeable:
                pc.location.inventory.drop(item)
                pc.inventory.add(item)
                print("Taken.")
            else:
                print("You can't take that.")

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
        print("You are not carrying a(n)",parsed.noun)

    return


def do_look():
    if parsed.noun == "NA":
        pc.location.isvisited = False
        return

    item_found = False

    for item in pc.location.inventory:
        if parsed.noun == item.id:
            print(item.desc)
            item_found = True
            break

    for item in pc.inventory:
        if parsed.noun == item.id:
            print(item.desc)
            item_found = True
            break

    if item_found == False:
        print("I don't see a(n)",parsed.noun,"here.")

    return


def do_read():
    if parsed.noun == "spellbook":
        do_look()
    else:
        print("You can't read that.")


def do_inventory():
    print("You are carrying:")

    if len(pc.inventory) == 0:
        print("Nothing")
    else:
        pc.inventory.display()


def do_cast():
    # Player must be carrying the spellbook to cast spells
    if pc.inventory.has('spellbook'):
        if parsed.noun == "light":
            do_cast_light()
        elif parsed.noun == "arrow":
            do_cast_arrow()
        elif parsed.noun == "unlock":
            do_cast_unlock()
        elif parsed.noun == "teleport":
            do_cast_teleport()
        elif parsed.noun == "sleep":
            do_cast_sleep()
        elif parsed.noun == "NA" or parsed.noun == "spell":
            print("What spell do you want to cast?")
        else:
            print("You don't know that spell.")
    else:
        print("You're not carrying your spellbook, and therefore cannot\n"
              "cast any spells.")


def do_cast_light():
    # Player only needs to cast light once to have it apply for the whole game
    print("You cast the light spell and a small, bright orb of light\n"
          "appears above your head. It should last all day.")
    if not flag.is_lit:
        # Change light flag and cave data, to prevent player from being killed upon
        # entering the cave
        flag.is_lit = True
        cave.desc = "You are in a small, dank cave. A large ogre stands before you, holding a\n" \
                    "giant club. You get the feeling he wants to smash your skull."
        cave.add_exit(east="denseforest")


def do_cast_arrow():
    if pc.location == cave:
        if not flag.ogre_dead:
            # Kill the ogre, update flags and cave room data
            print("You cast an arrow spell. A thin beam of light shoots from your fingers\n"
                  "and strikes the ogre, killing it.")
            flag.ogre_dead = True
            cave.desc = "You are relieved to see that the ogre lies in a crumpled heap upon\n" \
                        "the ground, dead. Now that you are able to focus more clearly on the\n" \
                        "rest of the room, you notice a door built into the west wall. It seems\n" \
                        "to be locked."
            cave.isvisited = False
        elif flag.ogre_dead:
            print("You cast another arrow spell at the ogre. Yep, still dead.")

    elif pc.location == gate:
        print("You cast the arrow spell at the guard. It strikes him, killing him\n"
              "instantly.\n"
              "     A gigantic, ghostly, bearded face appears in the air before you.\n"
              "It is the face of the head of the Wizard's Guild of Bookburg. He has\n"
              "been watching through magical means.\n"
              "     \"Murderer!\" he shouts. \"You shall pay for this!\"\n"
              "     The air around you begins to feel hot. Suddenly you burst into\n"
              "flame and die.")
        sys.exit()

    else:
        print("A thin beam of light shoots from your fingers. Nothing exceptional\n"
              "happens. You wonder if you should be wasting your magical energy\n"
              "like that.")


def do_cast_unlock():
    # If ogre is already dead in the cave, unlock the door if not already unlocked
    if pc.location == cave and flag.ogre_dead:
        if not flag.door_unlocked:
            print("You cast the unlock spell, and you hear a loud click come from the\n"
                  "door. It swings open, revealing a chamber on the other side.")
            flag.door_unlocked = True
            cave.desc = "The ogre is dead and the door to the west is unlocked. You look\n" \
                        "around the cave and feel quite a sense of accomplishment."
            cave.isvisited = False
            cave.add_exit(west="chamber")
        else:
            print("You've already unlocked the door. No sense wasting your magical\n"
                  "energy.")
    else:
        print("You cast the unlock spell, though you're not sure what you hoped to\n"
              "accomplish by doing so.")


def do_cast_teleport():
    # Return the player to the hut
    if pc.location != hut:
        print("There is a sudden flash of light and you find yourself back in\n"
              "your hut.")
        pc.location = hut
    else:
        print("No point casting that. You're already in your hut.")


def do_cast_sleep():
    # Sleep has no effect on the ogre
    if pc.location == cave:
        if flag.ogre_dead == False:
            print("You cast your sleep spell. The ogre seems dazed for a moment.\n"
                  "Then it shrugs and growls menacingly.")
        else:
            print("The ogre is already sleeping eternally.")

    # Put the guard to sleep if have not already done so and update room data
    elif pc.location == gate:
        if flag.guard_asleep == False:
            print("You cast a sleep spell on the guard. He staggers for a moment,\n"
                  "then falls to the ground in a deep slumber.")
            gate.desc = "You are at the gate of the town of Bookburg. The guard that\n" \
                        "was blocking you from entering town is now asleep on the ground,\n" \
                        "thanks to your handiwork."
            flag.guard_asleep = True
            gate.isvisited = False
            gate.add_exit(south='town')
        else:
            print("The guard is already asleep.")
    else:
        print("There's no one around to cast the spell on.")


def do_test_for_victory():
    # Test whether player has scepter upon entering town. If so, victory is attained!
    if not pc.inventory.has('scepter'):
        town.show_long_desc()
        do_cast_teleport()
    else:
        print("You triumphantly march into town and head straight for the Wizard's\n"
              "Guild. You present the Scepter of Wizardry to the Guild and are given\n"
              "back your old quarters--and your status as an official Guild wizard!.\n"
              "\nCongratulations! You have succeeded in your quest and won the game!")
        sys.exit()


def do_exit():
    print("Exiting the game...")
    sys.exit()


def do_help():
    print("To play the game, enter either a VERB or a VERB NOUN command combination.")
    print("For a list of verbs understood by the parser, enter \"verbs\".")
    print("The game will be won when you have returned the Scepter of Wizardry to the")
    print("Guild in town.")
    return


def do_verbs():
    print("The following verbs are recognized:\n"
          "GO, GET, TAKE, DROP, LOOK, EXAMINE, READ, INVENTORY, CAST, HELP, EXIT, QUIT\n"
          "\nYou may enter the first letter of a direction by itself to go in that\n"
          "direction. Also, you may enter X for look/examine, or I for inventory.")


def do_nothing():
    pass

# ---------------
# DEFINED VERBS
# ---------------

# set up dictionary of parser verbs and the functions they use
verbs = Verbs()
verbs.add(go=do_go)
verbs.add(get=do_take, take=do_take)
verbs.add(drop=do_drop)
verbs.add(look=do_look, x=do_look, examine=do_look)
verbs.add(read=do_read)
verbs.add(i=do_inventory, inventory=do_inventory)
verbs.add(cast=do_cast)
verbs.add(verbs=do_verbs)
verbs.add(help=do_help)
verbs.add(exit=do_exit, quit=do_exit)
verbs.add(NA=do_nothing)  # default verb for inaction


# --------------
# DEFINED NOUNS
# --------------

# set up dictionary of nouns/item_id's
nouns = Nouns()
nouns.add(book="spellbook", spellbook="spellbook")
nouns.add(bread="bread", loaf="bread")
nouns.add(scepter="scepter", sceptre="scepter")
nouns.add(ogre="ogre", monster="ogre")
nouns.add(guard="guard", soldier="guard")
nouns.add(spell="spell")
nouns.add(arrow="arrow", light="light", sleep="sleep", teleport="teleport", unlock="unlock")
nouns.add(north="north", n="north", east="east", e="east")
nouns.add(south="south", s="south", west="west", w="west")
nouns.add(NA="NA")   # default noun when single word command entered

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

    # Check if first word is a direction
    if first_word in known_directions:
        second_word = first_word
        first_word = "go"

    parsed.verb = parser_match_verb(first_word)

    parsed.noun = parser_match_noun(second_word)


def parser_match_verb(word):
    # check if parser recognized verb
    temp_verb = verbs.match_verb(word)
    if temp_verb == "ERR":
        print("I do not know how to", word)
        return 'NA'
    else:
        return temp_verb


def parser_match_noun(word):
    # check if parser recognized noun
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

print("Welcome to THE SCEPTER OF WIZARDRY, an old school parser-based text adventure\n"
      "game. You play a sorceror that has been exiled from the town of Bookburg by the\n"
      "Wizard's Guild after having the Scepter of Wizardry stolen from you by an ogre\n"
      "who ambushed you on the road. Your quest is to return the Scepter to the Guild\n"
      "in town. Don't forget to take your spellbook with you!\n"
      "\nType HELP for information on how to play.")

game_continues = True

while game_continues == True:

    show_room()

    if pc.location == cave and not flag.is_lit:
        sys.exit()

    parser_get_input()
    parser_match_words()

    parsed.routine = select_verb_routine(parsed.verb)
    parsed.routine()
