#import random
#game objects

class Object(object):
    """Base class for game objects."""

class Chrc(Object):
    """A character.

    Attributes:
        cc: character class
        rank: rank
    """

    def __init__(self):
        self.cc = None
        self.rank = 0

def NonLivingObj(Object):
    def __init__(self, **a):
        self.g = a["g"]
        self.name = a["name"]
        self.durabilty = a["durabilty"]
        self.size = a["size"]
        self.weight = a["weight"]

def Stone(NonLivingObj):
    def __init__(self, g, name, durabilty):
        NonLivingObj.__init__(self, g, name, durabilty)

def LivingObj(Object):
    def __init__(self, **a):
        self.g = a["g"]
        self.name = a["name"]
        self.lv = a["lv"]
        self.hp = a["hp"]
        self.att = a["att"]

        #assign value self.exp based on the other stats
    def doAction(s):
        if (s == "attack"):
            print self.name, " is attacking"

def Monster(LivingThing):   
    pass
    def __init__(self, **a):
        LivingObj.__init__(self, **a)
        self.actionList = ["fight"]
    #random choosing from a list of possible actions
def Bat(Monster):
    def __init__(self, **a):
        Monster.__init__(self, **a)




