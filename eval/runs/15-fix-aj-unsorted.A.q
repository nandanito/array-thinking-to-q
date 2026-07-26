quote:([] sym:`AAPL`AAPL`MSFT; time:09:30:05 09:30:00 09:30:00;
          bid:99.4 99.0 200.0; ask:99.6 99.2 200.2);
trade:([] sym:`AAPL`MSFT; time:09:30:03 09:30:02; price:99.1 200.1; size:100 50);

/ aj needs the right table sorted by time within sym; sort on the join columns
quote:`sym`time xasc quote;
/ then mark sym as parted so aj can binary-search each sym block
quote:update `p#sym from quote;

show meta quote;
show aj[`sym`time; trade; quote];
