function i = ispolycw(x, y)

assert ( isvector(x) );
assert ( isvector(y) );

assert ( size(x) == size(y) );

l = length(x);

s = 0.0;
for k = 1:l;
    kn = k + 1; % index of the next point
    if kn > l
        kn = 1;
    end

    s = s + (x(kn) - x(k))*(y(kn) + y(k));
end

i = 1; % CW
if s < 0.0
    i = 0; % CCW
end

end
