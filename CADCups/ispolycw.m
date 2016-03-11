function i = ispolycw(x, y)

assert ( isvector(x) );
assert ( isvector(y) );

assert ( size(x) == size(y) );

l = length(x);

s = 0.0;
for k = 1:l;
    k1 = k + 1;
    if k1 > l
        k1 = 1;
    end
    
    s = s + (x(k1) - x(k))*(y(k1) + y(k));
end

i = 1; % CW
if s < 0.0
    i = 0; % CCW
end

end
