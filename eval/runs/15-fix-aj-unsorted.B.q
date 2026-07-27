/ aj needs the right table ordered by the last join column (time) within the
/ preceding one (sym); with quote unsorted, AAPL's trade at 09:30:03 matched the
/ 09:30:05 row -- a quote from the future.

quote:([] sym:`AAPL`AAPL`MSFT; time:09:30:05 09:30:00 09:30:00;
          bid:99.4 99.0 200.0; ask:99.6 99.2 200.2);
trade:([] sym:`AAPL`MSFT; time:09:30:03 09:30:02; price:99.1 200.1; size:100 50);

quote:`sym`time xasc quote;              / time ascending within sym
quote:update `p#sym from quote;          / parted on sym - the attribute aj exploits in memory

show meta quote;
show aj[`sym`time; trade; quote];
