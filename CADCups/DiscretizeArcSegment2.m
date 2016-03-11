function [X, Y] = DiscretizeArcSegment2(x1, y1, x2, y2, x3, y3, tol)

%determine the cartesian form
A = [
    x1*x1+y1*y1 x1 y1 1
    x2*x2+y2*y2 x2 y2 1
    x3*x3+y3*y3 x3 y3 1
    ];
Z = null(A);

assert ( size(Z,2) == 1 );

% (x*x+y*y) + bx + cy + d = 0;
assert ( Z(1) ~= 0 );
if Z(1) == 0, error('DiscretizeArcSegment input error'), end;
b = Z(2) / Z(1);
c = Z(3) / Z(1);
d = Z(4) / Z(1);

%center of the supporting circle (x-xo)^2 + (y-yo)^2 = r^2
%determine the polar form
% x = xo + r cos(theta)
% y = yo + r sin(theta)
xo = - 0.5* b;
yo = - 0.5* c;
r =  sqrt( xo*xo + yo*yo - d);

%determine clockwiseness
clockwise = ispolycw([x1 x2 x3], [y1 y2 y3]);

thetas = angle( (x1-xo) + i*(y1 - yo) );
thetae = angle( (x3-xo) + i*(y3 - yo) );

if clockwise
    if thetae > thetas
        thetas = thetas + 2*pi;
    end
else
    if thetae < thetas
        thetae = thetae + 2*pi;
    end
end

%sample

K = ceil( r * abs(thetas - thetae) / tol ) + 2;
q = linspace(thetas, thetae, K);

X = (xo + r * cos(q))';
Y = (yo + r * sin(q))';

end
