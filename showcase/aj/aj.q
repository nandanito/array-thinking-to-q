/ Showcase: as-of join (aj) — match each trade to the prevailing quote.
/ "Prevailing" = the most recent quote at or before the trade time, per sym.
/ This is the M1 gate artifact; its output is golden-filed in expected.txt.

/ --- quotes -------------------------------------------------------------
/ Deliberately entered out of order to make the sort-discipline step explicit.
quote:([] sym :`AAPL`MSFT`AAPL`MSFT`AAPL;
          time:10:00:02 10:00:04 10:00:00 10:00:01 10:00:05;
          bid :99.1 200.3 99.0 200.0 99.4;
          ask :99.3 200.5 99.2 200.2 99.6 );

/ aj is correct ONLY if the quote table is sorted by the as-of column (time)
/ within the equality column (sym): aj takes the last MATCHING ROW in row order,
/ so wrong row order => silently wrong prevailing quote, no error. Sort, then
/ set `g#` on the first join column — the in-memory attribute prescription.
quote:`sym`time xasc quote;
@[`quote;`sym;`g#];

/ --- trades -------------------------------------------------------------
trade:([] sym :`AAPL`AAPL`MSFT`AAPL`MSFT;
          time:10:00:01 10:00:03 10:00:02 10:00:06 10:00:06;
          price:99.15 99.25 200.1 99.5 200.4;
          size:100 200 50 150 75 );

/ Join columns are passed explicitly as a symbol vector, common to both tables:
/ all but the last match by equality (sym), the last matches as-of, <= (time).
res:aj[`sym`time; trade; quote];
show res;
exit 0
