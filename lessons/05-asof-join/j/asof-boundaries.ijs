NB. Lesson 05 twin — J has no as-of join, and no as-of search either. I. is
NB. an interval index: "first position whose item is >= y". Stepping back one
NB. from it LOOKS like "last item <= y", and is right only between the edges.
NB. Run: jconsole < lessons/05-asof-join/j/asof-boundaries.ijs

times =: 0 2 5                NB. AAPL's quotes, seconds past 10:00:00
bids  =: 99 99.1 99.4

echo times I. 3 2 _1          NB. inside, on a tie, before the first quote
echo bids {~ <: times I. 3 2 _1

NB. What "at or before" actually asks: how many quotes are <= t, less one.
echo <: +/ times <:/ 3 2 _1
NB. Right index — but _1 is a legal J index (count from the end), not "none".
echo bids {~ <: +/ times <:/ 3 2 _1

exit 0
