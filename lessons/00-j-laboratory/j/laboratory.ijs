NB. Part I, the J laboratory. Read-along: the README shows every output below.
NB. Run: jconsole < lessons/00-j-laboratory/j/laboratory.ijs

NB. --- reading J ---------------------------------------------------------
2 * 3 + 4      NB. right to left: 3 + 4 first, then 2 * 7
- 5            NB. one argument (monad): negate
10 - 3         NB. two arguments (dyad): subtract
i. 5           NB. monad i.: the first five integers, like q's til

NB. --- J has loops too ---------------------------------------------------
sumloop =: 3 : 0
r =. 0
for_i. y do. r =. r + i end.
r
)
sumloop 1 2 3 4 5
+/ 1 2 3 4 5   NB. the idiom: + inserted between the items

NB. --- iteration is a modifier --------------------------------------------
+/\ 1 2 3 4 5 6
3 +/\ 1 2 3 4 5 6

NB. --- composition you can write down -------------------------------------
mean =: +/ % #     NB. a FORK: (sum) divided-by (count), read as one phrase
mean 0 1 2 3 4

NB. --- depth is a parameter -----------------------------------------------
m =: 2 3 $ 1 2 3 4 5 6
+/ m        NB. + inserted between the ITEMS — and a matrix's items are its ROWS
+/"1 m      NB. rank 1: apply to each row instead
<"0 m
<"1 m
2 -~/\ 1 3 6 10 15
