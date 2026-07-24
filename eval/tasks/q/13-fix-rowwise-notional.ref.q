/ reference (idiomatic fix of row-wise iteration): one vectorized update
t:([] price:190.0 410.0 191.0; qty:100 50 200);
show update notional:price*qty from t
