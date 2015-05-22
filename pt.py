"""Parse Tree"""

def parse_file(fn):
    """Parse a tree file.

    Args:
        fn: filename
    """
    # fs: file string
    # tss: tree structures
    with open(fn) as f:
        fs = f.read()
        trees = fs.split("\n\n")
        tss = []
        for tree in trees:
            tss.append(parse_tree(tree))
    return tss

def glue_trees(rm, nm):
    """Modify nodes in-place to connect trees.

    Args:
        rm: reference mapping for tree jumps
        nm: name mapping
    """
    for key, val in rm.iteritems():
        node = nm[key]
        for name in val:
            nm[name].next.append(node)

def parse_tree(tstr, ind_sz=4):
    """Parse tree.

    Args:
        tstr: tree string
        ind_sz: indent size
    """
    # ts: tree structure
    # lp: list of pointers to sublists in ts
    # rm: reference mapping for tree jumps
    # cs: current string
    # ic: indentation counter
    # i: loop counter
    # len_s: length of tree_s
    # mode: loop mode
        # 0: build string
        # 1: count whitespace
    ts = []
    lp = [ts]
    rm = {}
    cs = []
    ic = 0
    i = 0
    mode = 0
    len_s = len(tstr)
    while i < len_s:
        # ch: current character
        # is_ch_s: is current character a string character?
        ch = tstr[i]
        is_ch_s = ch.isalnum() or (ch == '_')
        if mode == 0:
            if is_ch_s:
                cs.append(ch)
                if i + 1 == len_s:
                    lp[-1].append(''.join(cs))

            elif ch == '*':
                node = ''.join(cs)
                cs = []
                mode = 1
                i += 1

                # Record a "jump" in the tree.
                if node in rm:
                    rm[node].append(lp[-2][-2])
                else:
                    rm[node] = [lp[-2][-2]]

                # Remove the empty lists.
                del lp[-2][-1]
                del lp[-1]

            elif ch == '\n':
                lp[-1].append(''.join(cs))
                cs = []
                mode = 1
            else:
                assert False

        elif mode == 1:
            if ch == ' ':
                ic += 1
            elif ch == '\n':
                # skip empty line
                pass
            elif is_ch_s:
                cs.append(ch)

                # Calculate indentation level.
                # il: indent level
                assert ic % ind_sz == 0
                il = ic / ind_sz
                ic = 0
                mode = 0

                # Assemble container for new children.
                # nl: new list, represents the current indentation level
                # lp_il: indentation level denoted by length of lp
                nl = []
                lp_il = len(lp) - 1
                if il == lp_il:
                    # same indentation level
                    pass
                elif il > lp_il:
                    # increased indent
                    assert lp_il + 1 == il
                    lp[-1].append(nl)
                    lp.append(nl)
                elif il < lp_il:
                    # decreased indent
                    del lp[il+1:]
                else:
                    assert False
            else:
                assert False
        i += 1
    return ts, rm

def test():
    from pprint import pprint
    with open("tree.txt", 'r') as f:
        st, rm = parse_tree(f.read())
        pprint(st)
        print
        pprint(rm)

if __name__ == "__main__":
    test()