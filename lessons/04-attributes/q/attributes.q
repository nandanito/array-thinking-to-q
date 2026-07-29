/ Lesson 04 — attributes & sort discipline. An attribute is a CLAIM about a
/ vector: checked once when you make it, dropped the moment q cannot be sure
/ it still holds, and never able to change an answer. What DOES change answers
/ is the row order the attribute advertises — that is what `aj` depends on.
/ Runnable end to end: q lessons/04-attributes/q/attributes.q -q < /dev/null

/ --- 1. an attribute is metadata: attr reads it, ~ ignores it -----------
show attr 1 2 3;                / ` — no claim has been made
show attr til 5;                / ` — sorted in FACT, but nothing is asserted
show attr asc 1 3 2;            / `s — asc did the sorting, so asc can vouch for it
show attr distinct 1 2 3;       / ` — distinct does NOT leave `u# behind
show (`s#1 2 3) ~ 1 2 3;        / 1b — ~ compares values; an attribute is not a value
show (where (`s#1 2 3 4 5)>2) ~ where 1 2 3 4 5>2;   / 1b — same answer either way

/ --- 2. q checks the claim WHEN YOU MAKE IT -----------------------------
show @[{`s#x}; 3 1 2; {"ERROR: ",x}];   / 's-fail — you cannot simply lie
show @[{`u#x}; 1 1 2; {"ERROR: ",x}];   / 'u-fail
show @[{`p#x}; 1 2 1; {"ERROR: ",x}];   / 'u-fail as well: p# wants equal values adjacent
show attr `g#1 2 1;                     / `g — the one claim that is true of any list

/ --- 3. ...then drops it SILENTLY the moment it might not hold ----------
s1:`s#1 2 3; s1,:4;   show attr s1;   / `s — appended in order: still true, still claimed
s2:`s#1 2 3; s2,:0;   show attr s2;   / `  — appended out of order: claim withdrawn
show s2;                              / 1 2 3 0 — the DATA is intact; only the claim went
s3:`s#1 2 3; s3[2]:5; show attr s3;   / `  — dropped even though 1 2 5 IS still sorted
s4:`s#1 2 3; s4[2]:3; show attr s4;   / `  — dropped even writing back the value ALREADY there
p1:`p#`a`a`b`b; p1,:`c; show attr p1; / `  — p# is removed by ANY operation on the list
u1:`u#1 2 3; u1,:4;   show attr u1;   / `u — still unique, so still claimed
u2:`u#1 2 3; u2,:1;   show attr u2;   / `  — a duplicate arrived

/ --- 4. sort discipline: xasc stamps only the FIRST column --------------
quote:([] sym :`AAPL`MSFT`AAPL`MSFT`AAPL;
          time:10:00:02 10:00:04 10:00:00 10:00:01 10:00:05;
          bid :99.1 200.3 98.5 200.0 99.4);
show quote;                           / deliberately out of order
sorted:`sym`time xasc quote;
show sorted;                          / sym-major, time ascending WITHIN each sym
show attr sorted`sym;                 / `s — the first sort column gets the attribute
show attr sorted`time;                / `  — the second does not, and cannot: time
                                      /     ascends only within a sym, not overall

/ --- 5. what `aj` actually depends on -----------------------------------
/ aj appends "the last (in row order) matching record" from the quote table,
/ so the prevailing quote is correct ONLY if time ascends within each sym.
trade:([] sym:`AAPL`MSFT; time:10:00:03 10:00:02; price:99.25 200.1);
show trade;
/ AAPL's true prevailing bid at 10:00:03 is 99.1 (the 10:00:02 quote).
show aj[`sym`time; trade; quote];                    / 98.5 — WRONG, and silent
show aj[`sym`time; trade; update `g#sym from quote]; / 98.5 — the attribute does NOT rescue it
show aj[`sym`time; trade; sorted];                   / 99.1 — right, with NO attribute set
show aj[`sym`time; trade; update `g#sym from sorted];  / 99.1 — right, and now indexed too
/ order within the group is the whole contract — reverse it and aj breaks again:
show aj[`sym`time; trade; `sym xasc `time xdesc quote];   / 98.5 — WRONG

/ --- 6. the prescription the showcase follows ---------------------------
ready:update `g#sym from `sym`time xasc quote;
show attr ready`sym;                  / `g — grouped, per the aj reference for in-memory
show aj[`sym`time; trade; ready];
