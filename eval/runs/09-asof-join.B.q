quote:([] sym:`AAPL`AAPL`MSFT`MSFT; time:09:30:00 09:30:04 09:30:01 09:30:05;
          bid:99.0 99.2 200.0 200.3; ask:99.2 99.4 200.2 200.5);
trade:([] sym:`AAPL`MSFT`AAPL; time:09:30:02 09:30:03 09:30:06;
          price:99.1 200.1 99.3; size:100 50 150);

show aj[`sym`time; trade; quote];
