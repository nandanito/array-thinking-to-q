/ Lesson 02 — dict -> table. A table is a flip of a column dictionary;
/ a keyed table is a dictionary. Runnable end to end:
/   q lessons/02-dict-to-table/q/dict-to-table.q -q < /dev/null

/ --- 1. a dictionary is just two lists: keys ! values ------------------
d:`a`b`c!10 20 30;
show d;
show type d;             / 99h — the dictionary type (remember this for step 6)
show d[`b];              / look up by key
show key d;              / the keys  (a list)
show value d;            / the values (a list)

/ --- 2. a COLUMN dictionary: the values are equal-length lists ---------
cd:`sym`px!(`AAPL`MSFT`GOOG; 100 200 300);
show cd;

/ --- 3. flip is transpose; flipping a NAMED column dict makes a table --
show flip (1 2 3; 4 5 6);   / flip on plain lists = matrix transpose
t:flip cd;                  / flip on a column dict = a TABLE
show t;
show type t;                / 98h — a table is its own type...
show t ~ flip cd;           / ...but it is literally flip cd: 1b

/ --- 4. the ([] ...) table literal is sugar for that flipped dict ------
show t ~ ([] sym:`AAPL`MSFT`GOOG; px:100 200 300);   / 1b

/ --- 5. rows are dictionaries, columns are lists — both views free -----
show t 0;                / row 0 is a DICTIONARY (one record)
show t[`px];             / a column is a LIST
show exec sym from t;    / same list, via qSQL

/ --- 6. a keyed table IS a dictionary: (key table) ! (value table) -----
kt:`sym xkey t;
show kt;
show type kt;            / 99h — the dict type, not 98h
show 98h~type key kt;    / its key half is a table  (1b)
show 98h~type value kt;  / its value half is a table (1b)
show kt[`AAPL];          / look up a key row -> a value record (a dict)
