/ reference (idiomatic fix): sort quotes by time within sym, set g#, then aj
quote:([] sym:`AAPL`AAPL`MSFT; time:09:30:05 09:30:00 09:30:00;
          bid:99.4 99.0 200.0; ask:99.6 99.2 200.2);
quote:`sym`time xasc quote;
@[`quote;`sym;`g#];
trade:([] sym:`AAPL`MSFT; time:09:30:03 09:30:02; price:99.1 200.1; size:100 50);
show aj[`sym`time; trade; quote]
