/ arithmetic mean without the built-in avg
mean:{[x] $[count x; (sum x) % count x; 0n]}

show mean 1 2 3 4 5
