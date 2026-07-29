NB. Lesson 04 twin — J has no attribute mechanism at all. I. is a binary
NB. search that ASSUMES its left argument is sorted; nothing in the language
NB. records that assumption, checks it, or notices when it stops holding.
NB. Run: jconsole < lessons/04-attributes/j/sorted-assumption.ijs

times =: 0 2 5                NB. one symbol's quote times, ascending
bids  =: 98.5 99.1 99.4

NB. "prevailing bid at t=3": find the insertion point, step back one.
echo times I. 3               NB. 2
echo bids {~ <: times I. 3    NB. 99.1 — correct

NB. Same verb, same question, rows permuted. No error, no warning.
utimes =: 2 0 5
ubids  =: 99.1 98.5 99.4
echo utimes I. 3
echo ubids {~ <: utimes I. 3

NB. Sorting is available — but /: returns a PERMUTATION you must apply to
NB. every parallel list yourself, and the result carries no memory of it.
echo /: utimes                NB. the grade: how to reorder
echo (/: utimes) { utimes
echo (/: utimes) { ubids

exit 0
