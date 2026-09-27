/ Transition chapter: what crosses from the J laboratory into q, and what does not.
/ Written and run BEFORE the J file (CLAUDE.md rule 1, Q-first).
/ Runnable end to end: q lessons/00-transition/q/transition.q -q < /dev/null

/ --- 1. the fork does not parse ----------------------------------------
/ A parse error cannot sit in a runnable file (lesson 01 quotes the REPL
/ transcript, CLAUDE.md rule 3). So hand the text to the parser at runtime,
/ where the failure becomes a value we can show.
parses:{@[{parse x; 1b}; x; 0b]};           / 1b if q's parser accepts the text
show parses "(+/ % #) til 5";                   / the fork
show parses ".[{(+/ % #) til 5};();{(`caught;x)}]";  / the fork inside a guard
show parses "{(sum x) % count x} til 5";        / the same composition, said out loud

/ what q accepts: the composition said out loud
show avg til 5;
show {(sum x) % count x} til 5;

/ --- 2. the windows have a different shape -----------------------------
show 3 mavg 1 2 3 4 5 6f;     / six results: partial windows ramp up at the start
