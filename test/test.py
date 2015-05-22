for n in xrange(1, 101):
    out = []
    if n % 3 == 0:
        out.append("Crackle")
    if n % 5 == 0:
        out.append("Pop")
    print ''.join(out) if out else n