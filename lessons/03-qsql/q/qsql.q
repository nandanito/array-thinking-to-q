/ Lesson 03 — qSQL: select ... by ... from. Every phrase is a COLUMN
/ expression, and `by` hands back a keyed table (i.e. a dictionary again).
/ Runnable end to end: q lessons/03-qsql/q/qsql.q -q < /dev/null

t:([] sym :`AAPL`MSFT`AAPL`MSFT`AAPL`GOOG;
      side:`B`S`S`B`B`S;
      qty :100 200 150 50 300 250;
      px  :187.5 411.2 188.1 410.9 187.9 174.3);
show t;

/ --- 1. a select phrase is a whole-COLUMN expression -------------------
show select notional:qty*px from t;   / one vector multiply, not six row visits
show select sum qty from t;           / "aggregate" = a function that reduces a vector
show cols select qty*px from t;       / unnamed: q invents a name — don't rely on it
show cols select 2*qty from t;        / ...and falls back to `x

/ --- 2. where is a boolean vector; constraints apply in sequence -------
show (t`sym)=`AAPL;                   / the where phrase, on its own: a bool vector
show select from t where sym=`AAPL;
show select from t where sym=`AAPL, qty>100;   / 2nd constraint sees only what the 1st kept

/ --- 3. by returns a KEYED TABLE — the dictionary from lesson 02 -------
r:select sum qty by sym from t;
show r;
show type r;              / 99h — a keyed table IS a dictionary
show 98h~type key r;      / key half: a table (1b)
show 98h~type value r;    / value half: a table (1b)
show r[`AAPL];            / so look-up works exactly like any dict

/ --- 4. by WITHOUT an aggregate: the groups themselves ------------------
/ SQL would reject this; q hands back one list per group. Aggregating is
/ an optional second step, not part of what `by` means.
show select px by sym from t;
show select n:count i, tot:sum qty, avg px by sym from t;

/ --- 5. the primitive under `by` is group; word frequency ---------------
w:`the`cat`sat`on`the`mat`the;
show group w;                 / value -> indices, in FIRST-APPEARANCE order
show count each group w;      / word frequency, without a table in sight
show exec count i by w from ([] w:w);   / same counts, qSQL spelling
show (count each group w) ~ exec count i by w from ([] w:w);   / 0b: ORDER differs
show attr key exec count i by w from ([] w:w);   / `s — by also SORTS its keys (lesson 04)
show (`s#1 2 3) ~ 1 2 3;  / 1b — ~ ignores attributes, so `s# is NOT what broke the ~ above

/ --- 6. windows: a moving average is not a loop either ------------------
show 3 mavg 1 2 3 4 5 6f;     / partial windows at the start: 1, then 1.5, then 3-wide
show 3 msum 1 2 3 4 5 6;      / the whole m- family ramps up the same way:
show 3 mmax 1 2 3 4 5 6;      /   6 inputs -> 6 outputs, never a shorter result
show 3 mmin 1 2 3 4 5 6;
show update ma:2 mavg px by sym from t;   / per-sym window, written back IN ROW ORDER
show update ma:2 mavg px from t;          / no `by`: averages ACROSS symbols — nonsense

/ --- 7. exec unwraps; select always returns a table ---------------------
show select sum qty by sym from t;   / a keyed TABLE
show exec sum qty by sym from t;     / a plain DICTIONARY: sym -> total
show exec qty from t;                / a plain LIST
