"""A game of chance and encounter."""

import os
import yaml
import pt
from nodefs import nodefs
from objects import *

MAPDIR = "map"

class Game(object):
    """A run of the game.

    Attributes:
        objs: characters
        dm: node definition mapping
        fn: first node
        choice: player's latest choice
    """

    def __init__(self):
        self.objs = {}
        self.maps = []

    def load(self):
        # self.out("n0")
        # c0 = self.choice(self.c0)
        # chrc = Chrc(c0)
        # self.out(self.n1, chrc.ccls)

        # dm: story node definition mappings
        # sts: story trees
        # rm: reference mapping from parse_tree
        # self.fn
        with open("story/carnival/intro.yaml") as f:
            self.dm = yaml.load(f)
        sts = pt.parse_file("story/carnival/intro.txt")

        # Generate nodes and set first node.
        rms = {}
        for i, st in enumerate(sts):
            ts, rm = st
            rms.update(rm)
            if i == 0:
                self.fn = self.r(ts)
            else:
                self.r(ts)
        pt.glue_trees(rms, self.dm)
        # self.debug(self.fn)
        
        # Load game object definitions.
        for _, obj in globals().iteritems():
            if isinstance(obj, objects.Object):
                cn = obj.__class__.__name__
                if cn in self.objs:
                    self.objs[cn].append(obj)
                else:
                    self.objs[cn] = [obj]

        # Load maps/instantiate objects.
        maps = []
        for f in os.listdir(MAPDIR):
            if not f.endswith(".yaml"):
                continue
            with open(os.path.join(MAPDIR, f)) as m:
                mp = yaml.load(m)
            for inst, data in mp.iteritems():
                n_inst, attrs = data

    def run(self):
        self.fn.run()

    def debug(self, node):
        print "node.name, node.next: {0}, {1}".format(
            node.name, 
            [n.name for n in node.next])
        if isinstance(node.next, Node):
            self.debug(node.next)
        elif isinstance(node.next, list):
            for n in node.next:
                self.debug(n)

    def p(self, name):
        """Process the node."""
        # nd: node definition
        nd = self.dm[name]
        args = dict(
            game = self,
            name = name, 
            ndef = nd)
        if isinstance(nd, str):
            node_obj = Line(**args)
        elif isinstance(nd, list):
            node_obj = Choice(**args)
        self.dm[name] = node_obj
        return node_obj

    def r(self, st, prev=None, parent=None):
        """Traverse the tree recursively."""
        # check for end of tree
        if st:
            node = st[0]
        else:
            return

        if isinstance(node, str):
            node_obj = self.p(node)

            if parent:
                parent.next.append(node_obj)
            elif prev:
                prev.next.append(node_obj)

            # base case
            if len(st) > 1:
                self.r(st[1:], node_obj, parent)

            # return first node only
            if (not prev) and (not parent):
                return node_obj

        elif isinstance(node, list):
            # recursive calls
            self.r(st[0], None, prev)
            if len(st) > 1:
                self.r(st[1:], parent)
        else:
            assert False

class Node(object):
    """A node in the story tree.

    Attributes:
        game: game object
        name: node name
        ndef: node definition
        next: next node or, next possible nodes, to run
        cond: condition function
        eff: effect function
    """

    def __init__(self, game, name, ndef):
        self.game = game
        self.name = name
        self.ndef = ndef
        self.next = []

        # Store cond and eff functions.
        cond = "{0}_c".format(name)
        eff = "{0}_e".format(name)
        self.cond = (getattr(nodefs, cond)
            if hasattr(nodefs, cond)
            else lambda g: True)
        self.eff = (getattr(nodefs, eff)
            if hasattr(nodefs, eff)
            else lambda g: None)

    def run(self):
        if not self.next:
            # exit clause for terminal
            raw_input("Press enter to exit.")
            exit()

        self.display(self.eff(self.game))
        for node in self.next:
            if node.cond(self.game):
                node.run()
                break

    def display(self):
        """..."""

class Line(Node):
    """A narration line."""

    def display(self, *a):
        """..."""
        print self.ndef.format(*a)

class Choice(Node):
    """A choice given to the player."""

    def display(self, *a):
        """Ask the player to make a choice."""
        # Build the choice string.
        # cn: choice narration line
        # cs: choices
        # cstr: choice string to output
        cn, cs = self.ndef
        cstr = []
        for i, choice in enumerate(cs):
            cstr.append("{0}: {1}".format(i + 1, choice))
        s = "{0}\n{1}".format(cn, '\n'.join(cstr))

        # Display the choice.
        # cnr: choice number range
        cnr = map(str, range(1, len(cs) + 1))
        inp = raw_input("{0}\n".format(s))
        while True:
            if inp in cnr:
                self.game.choice = inp
                break
            else:
                print "Please choose a valid option."
                inp = raw_input()

def main():
    g = Game()
    g.load()
    g.run()

if __name__ == "__main__":
    main()