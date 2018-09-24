from ifclasses import *


class Flags():
    def __init__(self):
        self.is_lit = False
        self.ogre_dead = False
        self.door_unlocked = False
        self.guard_asleep = False


# ITEMS

spellbook = Item('spellbook')
spellbook.title = 'A spellbook'
spellbook.desc = "This is your personal spellbook, containing five spells:\n" \
                 "ARROW: Shoots a magical arrow.\n" \
                 "LIGHT: Creates a magical orb of light that floats above you.\n" \
                 "SLEEP: Causes the target to fall asleep.\n" \
                 "TELEPORT: Teleports you back to your hut.\n" \
                 "UNLOCK: Opens a lock.\n" \
                 "To cast a spell, enter CAST <SPELL NAME>"

scepter = Item('scepter')
scepter.title = 'The Scepter of Wizardry'
scepter.desc = "A plain, unadorned rod. You don't see what all the fuss is about."

ogre = Item('ogre')
ogre.title = 'An ogre'
ogre.desc = "This is a big, muscular, ugly and smelly ogre. You're fairly certain\n" \
            "this is the ogre that stole the Scepter of Wizardry from you."
ogre.is_listed = False
ogre.is_takeable = False

guard = Item('guard')
guard.title = 'Town Guard'
guard.desc = "The town guard has been ordered to prevent you from entering town\n" \
             "until you've retrieved the Scepter of Wizardry. This one eyes you\n" \
             "suspiciously."
guard.is_listed = False
guard.is_takeable = False

# ROOMS

room_list = []


# ---- ABANDONED HUT ----

hut = Room('hut')
hut.title = "ABANDONED HUT"
hut.desc = "You are in an old, rickety hut that was probably once used by\n" \
           "hunters from town. Since your recent exile from Bookburg, it\n" \
           "has become your home."
hut.add_exit(west='outsidehut')
hut.inventory.add(spellbook)
room_list.append(hut)


# ---- OUTSIDE HUT ----

outsidehut = Room('outsidehut')
outsidehut.title = "OUTSIDE HUT"
outsidehut.desc = "You stand outside an unimpressive looking hut that looks like\n" \
               "it will soon fall apart. To the west is the forest path that\n" \
               "leads to town."
outsidehut.add_exit(east='hut', west='forestpath')
room_list.append(outsidehut)


# ---- FOREST PATH ----

forestpath = Room('forestpath')
forestpath.title = "FOREST PATH"
forestpath.desc = "You are on a narrow dirt trail through the forest. The path\n" \
                  "heads to the north, where the forest seems to grow more dense,\n" \
                  "and the south, where the foliage seems to be more sparse."
forestpath.add_exit(north='denseforest', east='outsidehut', south='farmersfield')
room_list.append(forestpath)


# ---- FARMER'S FIELD ----

farmersfield = Room('farmersfield')
farmersfield.title = "FARMER'S FIELD"
farmersfield.desc = "You are on a road that leads through a farmer's field. To the north\n" \
                    "is the forest and to the south lies the town of Bookburg."
farmersfield.add_exit(north='forestpath', south='gate')
room_list.append(farmersfield)


# ---- TOWN GATE ----

gate = Room('gate')
gate.title = "TOWN GATE"
gate.desc = "You stand outside the gate leading into the town of Bookburg. A guard blocks\n" \
            "the entrance and will not let you pass."
gate.inventory.add(guard)
gate.add_exit(north='farmersfield')
room_list.append(gate)


# ---- TOWN OF BOOKBURG ----

town = Room('town')
town.title = "TOWN OF BOOKBURG"
town.desc = "You enter the town with trepidation, knowing you have not yet returned the\n" \
            "Scepter of Wizardry. You only get a few steps down the street when a gigantic,\n" \
            "bearded, ghostly face appears before you. It is the face of the head of the\n" \
            "Wizard's Guild of Bookburg.\n" \
            "   \"You dare to enter Bookburg without retrieving the Scepter of Wizardry?\" a\n" \
            "voice booms. \"Get thee hence and return when you have retrieved it!\"\n" \
# NO EXITS -- Text displayed in town is entirely dependent upon victory condition
room_list.append(town)


# ---- DENSE FOREST ----

denseforest = Room('denseforest')
denseforest.title = "DENSE FOREST"
denseforest.desc = "The path heading to the south ends here, and you find yourself in the middle\n" \
                   "of a dense cluster of trees and underbrush. It seems someone has been here\n" \
                   "recently, however, as the brush is trampled to the north and to the west."
denseforest.add_exit(north='cliff', west='caveentrance', south='forestpath')
room_list.append(denseforest)


# ---- CLIFF ----

cliff = Room('cliff')
cliff.title = "MOUNTAIN CLIFF"
cliff.desc = "Whoever had come here before you doesn't seem to have gotten far. There is a\n" \
             "tall cliff here, the side of Merlin Mountain. It looks like you'll have to go\n" \
             "back the way you came."
cliff.add_exit(south='denseforest')
room_list.append(cliff)


# ---- CAVE ENTRANCE ----

caveentrance = Room('caveentrance')
caveentrance.title = "CAVE ENTRANCE"
caveentrance.desc = "You are at the entrance to a large cave. Bones from unknown creatures\n" \
                    "litter the ground, and the cave itself seems dark and dangerous."
caveentrance.add_exit(west='cave', east='denseforest')
room_list.append(caveentrance)


# ---- CAVE ----

cave = Room('cave')
cave.title = "DARK CAVE"
cave.desc = "You bravely enter the dark cave and quickly regret it. Although you never see\n" \
            "what hits you, something hard slams down on your head and thrusts you into\n" \
            "eternal sleep."
cave.inventory.add(ogre)
# NO EXITS INTIALLY - Will be added when player casts Light
room_list.append(cave)


# ---- LOCKED CHAMBER ----

chamber = Room('chamber')
chamber.title = "CHAMBER"
chamber.desc = "You are in a small chamber, barely wide enough for you to lie down."
chamber.inventory.add(scepter)
chamber.add_exit(east='cave')
room_list.append(chamber)


# start the player in hut
pc = Player(hut)
flag = Flags()
