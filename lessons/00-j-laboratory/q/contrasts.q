/ Part I, the J laboratory: the q side of every contrast the lesson draws.
/ Written and run BEFORE the J file (CLAUDE.md rule 1, Q-first).
/ Runnable end to end: q lessons/00-j-laboratory/q/contrasts.q -q < /dev/null

/ --- 1. q lets you write the loop, and it works -------------------------
/ (the transliterated loop the lesson opens with; it is the anti-idiom)
x:1 2 3 4 5;
r:0; i:0;
do[count x; r+:x i; i+:1];
show r;

/ --- 2. iteration is a modifier: q hides it behind names ---------------
show sum til 5;               / the idiom
show (+/) til 5;              / what sum IS: + folded with the over adverb
show sums 1 2 3 4 5 6;        / running total
show 3 msum 1 2 3 4 5 6;      / 3-wide moving sum: a different NAME, not a parameter

/ --- 3. depth: q has one fixed move, each -------------------------------
show sum (1 2 3; 4 5 6);      / sum over the items: the two rows added
show sum each (1 2 3; 4 5 6); / one level down: each row summed
show (-':) 1 3 6 10 15;       / each-prior: adjacent pairs, which is not depth at all
