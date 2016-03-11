function [X, Y] = DiscretizeEllipticalSegment2(x1, y1, x2, y2, x3, y3, x4, y4, tol)
%determine the cartesian form
A = [
    x1*x1 y1*y1 x1 y1 1
    x2*x2 y2*y2 x2 y2 1
    x3*x3 y3*y3 x3 y3 1
    x4*x4 y4*y4 x4 y4 1
    ];
Z = null(A);

% Z(1)*x^2 + Z(2)*y^2 + Z(3)*x + Z(4)*y + Z(5) = 0
assert( size(Z,2) == 1 );
assert( Z(1) ~= 0 );
assert( Z(2) ~= 0 );
assert( sign(Z(1)) == sign(Z(2)));

%convert to (x-xo)^2/a^2 + (y-yo)^2/b^2 = 1
xo = -0.5 * Z(3) / Z(1);
yo = -0.5 * Z(4) / Z(2);
a = sqrt( (Z(1)*xo*xo + Z(2)*yo*yo - Z(5))/Z(1) );
b = sqrt( (Z(1)*xo*xo + Z(2)*yo*yo - Z(5))/Z(2) );

%determine clockwiseness
clockwise = ispolycw([x1 x2 x3], [y1 y2 y3]);

assert( clockwise == ispolycw([x2 x3 x4], [y2 y3 y4]) );

thetas = angle( (x1-xo)/a + i*(y1-yo)/b );
thetae = angle( (x4-xo)/a + i*(y4-yo)/b );
if clockwise
    if thetae > thetas
        thetas = thetas + 2*pi;
    end
else
    if thetae < thetas
        thetae = thetae + 2*pi;
    end
end

K = ceil( sqrt(a*a+b*b) * abs(thetas - thetae) / tol ) + 2;
q = linspace(thetas, thetae, K);
X = (xo + a * cos(q))';
Y = (yo + b * sin(q))';

end
