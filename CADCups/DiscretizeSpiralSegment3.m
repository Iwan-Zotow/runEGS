%REQUIREMENTS
%(1) Z-axis is the rotational axis
%(2) GC(:,1): Z-axis, GC(:,2): R-axis
function [X, Y, Z] = DiscretizeSpiralSegment3(GC, x0, y0, z0, x, y, z, tol)

    theta = CwSpiralAngles([x0; x], [y0; y], [z0; z]);

    maxr = max(abs(GC(:,2)));
    K = ceil( maxr * abs(theta(end) - theta(1)) / tol ) + 2;

    q = linspace(theta(1), theta(end), K);
    Z = ( linspace(z0, z(end), K) )';

    R = interp1(GC(:,1), GC(:,2), Z, 'linear', 'extrap');
    X = R .*  cos(q');
    Y = R .*  sin(q');
end
