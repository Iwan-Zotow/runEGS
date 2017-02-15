x = [0 1 1 0 0];
y = [0 0 1 1 0];
ispolycw(x, y)                     % Returns 0
ispolycw(fliplr(x), fliplr(y))     % Returns 1
