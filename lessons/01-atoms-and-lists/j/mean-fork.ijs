NB. J twin for lesson 01 — the tacit fork q cannot express.
NB. Run: jconsole < lessons/01-atoms-and-lists/j/mean-fork.ijs
sum  =: +/         NB. insert + between items
mean =: +/ % #     NB. a FORK: (sum) divided-by (count), read as one phrase
sum  0 1 2 3 4
mean 0 1 2 3 4
