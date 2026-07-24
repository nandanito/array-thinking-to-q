NB. J twin for lesson 02 — flip IS transpose. The difference is names.
NB. Run: jconsole < lessons/02-dict-to-table/j/transpose.ijs
m =: 2 3 $ 1 2 3 4 5 6    NB. a 2x3 matrix, built by reshape ($)
m                         NB. two rows of three
|: m                      NB. |: transposes it: three rows of two
