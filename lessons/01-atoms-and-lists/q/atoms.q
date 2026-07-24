/ Lesson 01 — atoms, lists, and the death of the loop.
/ Runnable end to end: q lessons/01-atoms-and-lists/q/atoms.q -q < /dev/null

/ --- 1. an atom is not a one-element list ------------------------------
show type 42;            / an atom: type is NEGATIVE
show type til 5;         / a list:  same type, POSITIVE
show count 42;           / an atom still answers count -> 1
show count til 5;        / a list of five

/ --- 2. the loop you do not write -------------------------------------
/ "double every element" is not a loop; it is one multiplication.
show 2 * til 5;
show (til 5) + 10 20 30 40 50;
show (til 5) > 2;        / a comparison yields a boolean vector

/ --- 3. reductions, and the machine under the built-in ----------------
show sum til 5;          / the idiom
show (+/) til 5;         / what sum IS: + inserted between elements (over)
show avg til 5;          / mean is a built-in; note the float result
show max til 5;

/ --- 4. each / over / scan: the three shapes of iteration -------------
show sums til 5;         / running total = + SCANNED across the list
show (+\) til 5;         / the scan mechanism sums names
show count each ("aa"; "bbb"; "c");   / each dives one level down
