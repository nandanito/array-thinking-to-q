NB. J twin for lesson 03 — grouping and windows, without names.
NB. Run: jconsole < lessons/03-qsql/j/group-and-window.ijs
w =: ;: 'the cat sat on the mat the'   NB. ;: cuts a string into boxed words
#/.~ w                                 NB. /. is "key": group by value, then apply #
~. w                                   NB. the labels are a SEPARATE result
3 (+/ % #)\ 1 2 3 4 5 6                NB. 3-wide windows — COMPLETE ones only
