# ifclasses.py
# For use with IF games

# A collection of classes that can be used with text adventure games.

class Item:
    """An actual object used in the game.
    The item_id for an item should have a matching
    value in the Nouns dictionary.
    """
    def __init__(self, id):
        self.id = id
        self.title = "item"
        self.desc = "This is an item"
        self.is_listed = True     # is listed in room inventory
        self.is_takeable = True   # can be taken from a room

    def __iter__(self):
        return self


class Inventory(list):
    """The Inventory class should contain a list
    of item_id values from the Item class.
    """

    def add(self, *args):
        for item in args:
            self.append(item)


    def drop(self, item_dropped):
        if item_dropped in self:
            self.remove(item_dropped)


    def display(self):
        for item in self:
            if item.is_listed == True:
                print(item.title)

    def has(self, item_sought):
        self.has_item = False

        for item in self:
            if item_sought == item.id:
                self.has_item = True

        return self.has_item


class Room:
    """A Room class to contain basic
    information about the locations in
    the game.
    """
    def __init__(self, id):
        self.id = id
        self.title = "A Room"
        self.desc = "Enter description"
        self.isvisited = False
        self.exits = {}
        self.inventory = Inventory()

    def add_exit(self, **kwargs):
        self.exits.update(kwargs)

    def remove_exit(self, *args):
        del self.exits[args]

    def show_short_desc(self):
        print(self.title)
        self.show_inventory()
        self.show_exits()

    def show_long_desc(self):

        print(self.title)
        print(self.desc)
        self.show_inventory()
        self.show_exits()

    def show_inventory(self):
        # print objects in room
        if len(self.inventory) > 0:
            list_items = False
            for item in self.inventory:
                if item.is_listed:
                    list_items = True

            if list_items:
                print("OBJECTS HERE:")
                self.inventory.display()

    def show_exits(self):
        # print exits
        print("EXITS: ", end='')
        if len(self.exits) == 0:
            print("none")
        else:
            for key in self.exits:
                print(key, " ", end='')

        print()


class Player:
    """A Player class, containing some very
    basic information such a location, score,
    and inventory.
    """
    def __init__(self, location):
        self.location = location
        self.score = 0
        self.inventory = Inventory([])
        self.is_lit = False


class Verbs:
    """When using the verbs dictionary, the keys will
    be the verbs used by the player/parser, while the
    values will be the names of the routines called
    to process the verb.
    """

    def __init__(self):
        self.verb_dict = {}

    def add(self, **kwargs):
        self.verb_dict.update(kwargs)

    def remove(self, *args):
        for verb in args:
            del self.verb_dict[verb]

    def match_verb(self, choice):
        if choice not in self.verb_dict:
            return 'ERR'
        else:
            return choice

    def match_routine(self, choice):
        if not self.verb_dict[choice]:
            return 'NA'
        else:
            return self.verb_dict[choice]

class Nouns:
    """
    When using the noun dictionary, the keys will
    be the nouns used by the player, while the
    values will be the actual nouns used by the
    program itself.

    Note that an Item is not the same as a noun
    in terms of using it in the program. A noun
    is what is used by the program and parser.
    Every Item in the game should have at least
    one matching value in the Nouns dictionary.
    """
    noun_dict = {}

    def __init__(self, **kwargs):
        self.noun_dict.update(kwargs)

    def add(self, **kwargs):
        self.noun_dict.update(kwargs)

    def remove(self, *args):
        del self.noun_dict[args]

    def match_noun(self, choice):
        if choice not in self.noun_dict:
            return 'ERR'
        else:
            return self.noun_dict[choice]

class ParsedCommand():
    """The verb/noun combination used
    by the parser"""

    def __init__(self):
        self.raw_input = []
        self.verb = "NA"
        self.noun = "NA"
        self.routine = ''

    def reset(self):
        self.verb = "NA"
        self.noun = "NA"
        self.routine = ''