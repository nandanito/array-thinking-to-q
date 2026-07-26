t:([] sym:`AAPL`AAPL`MSFT`AAPL`MSFT; side:`buy`sell`buy`buy`sell)
show select n:count i by sym,side from t
