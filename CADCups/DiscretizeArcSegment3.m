function [X, Y, Z] = DiscretizeArcSegment3(x1, y1, z1, x2, y2, z2, x3, y3, z3, tol)
%transform to 2D
%ax + by + cz + d = 0
A = [
    x1 y1 z1 1
    x2 y2 z2 1
    x3 y3 z3 1
    ];
ZA = null(A);
assert( size(ZA,2) == 1 );

Z= null(ZA(1:3)');
assert( size(Z,2) == 2);
Rx = Z(:, 1);
Ry = Z(:, 2);
Rz = cross(Rx', Ry')';
T = [Rx Ry Rz]';

P = T * [x1 x2 x3
         y1 y2 y3
         z1 z2 z3];

[Xt Yt] = DiscretizeArcSegment2( P(1,1), P(2,1), P(1,2), P(2,2), P(1,3), P(2,3), tol);
Zt = ones(length(Xt),1) * mean(P(3,:));

%transform back to 3D space
Q = ( T' * [Xt Yt Zt]' )';
X = Q(:, 1);
Y = Q(:, 2);
Z = Q(:, 3);
end
