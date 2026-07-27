t:([] sym:`AAPL`MSFT`AAPL; price:190.0 410.0 191.0; qty:100 50 200)
t:update notional:price*qty from t
show t
