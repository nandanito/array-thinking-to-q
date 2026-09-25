/ Lesson 05 — the as-of join. `aj` is not a special feature bolted onto q: it
/ is `group` (which rows are this sym?) plus `bin` (which is the last time at
/ or before t?), over a table whose row order lesson 04 made you responsible
/ for. The showcase's sort-then-attribute preamble is derived here, not copied.
/ Run from the repo root (the last section reads the showcase's golden file):
/   q lessons/05-asof-join/q/asof.q -q < /dev/null

/ --- 0. the showcase's data, still in arrival order ----------------------
quote:([] sym :`AAPL`MSFT`AAPL`MSFT`AAPL;
          time:10:00:02 10:00:04 10:00:00 10:00:01 10:00:05;
          bid :99.1 200.3 99.0 200.0 99.4;
          ask :99.3 200.5 99.2 200.2 99.6 );
trade:([] sym :`AAPL`AAPL`MSFT`AAPL`MSFT;
          time:10:00:01 10:00:03 10:00:02 10:00:06 10:00:06;
          price:99.15 99.25 200.1 99.5 200.4;
          size:100 200 50 150 75 );
show quote;
show trade;

/ --- 1. the join you already know, asked the loop way --------------------
/ "for each trade, the quote with the greatest time at or before it" — a
/ correlated subquery. Correct on unsorted data (ties at the same time fall
/ back to row order: `last`, as aj does), and re-filters every quote for
/ every trade.
prevailing:{[s;t] exec last bid where time=max time from quote where sym=s, time<=t};
show prevailing'[trade`sym; trade`time];

/ --- 2. question one, "which rows are this sym?", has a per-TABLE answer --
show group quote`sym;                 / lesson 03's group; `g# keeps exactly this

/ --- 3. question two, "latest at or before t?", is `bin` ----------------
/ AAPL's three quotes, as seconds past 10:00:00 and their bids.
times:0 2 5; bids:99 99.1 99.4;
show times bin 3;                     / 1 — index of the last element <= 3
show times bin 2;                     / 1 — a tie counts: <=, not <
show times bin -1;                    / -1 — nothing at or before: off the front
show 2 0 5 bin 3;                     / 1 — unsorted: a confident, wrong index
show bids times bin 3 2 -1;           / 99.1 99.1 0n — and index -1 is null

/ --- 4. sort once, and both questions become lookups ---------------------
sorted:`sym`time xasc quote;
show sorted;
show group sorted`sym;                / contiguous blocks, each time-ascending

/ --- 5. aj, built by hand from those two pieces --------------------------
g:group sorted`sym;
idx:{[r;t] r sorted[`time][r] bin t}'[g trade`sym; trade`time];
show idx;                             / one quote row per trade
hand:trade,'`bid`ask#sorted idx;
show hand;
show hand ~ aj[`sym`time; trade; sorted];

/ --- 6. the edges fall out of bin, not out of special cases --------------
edge:([] sym:`AAPL`AAPL`IBM; time:09:59:59 10:00:02 10:00:03; price:98.9 99.12 150.0);
show aj[`sym`time; edge; sorted];
eidx:{[r;t] r sorted[`time][r] bin t}'[g edge`sym; edge`time];
show eidx;
show (edge,'`bid`ask#sorted eidx) ~ aj[`sym`time; edge; sorted];

/ --- 7. the showcase preamble, now every line has a reason ---------------
quote:`sym`time xasc quote;           / correctness: blocks by sym, time ascending in each
@[`quote;`sym;`g#];                   / optional: record the group half, set LAST
res:aj[`sym`time; trade; quote];
show res;
/ This must be byte-for-byte the showcase's golden file. Fail loudly if not.
golden:read0 `:showcase/aj/expected.txt;
same:golden ~ -1 _ "\n" vs .Q.s res;
if[not same; -2 "lesson 05: result differs from showcase/aj/expected.txt"; exit 1];
show same;
