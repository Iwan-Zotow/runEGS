function [X, Y, Z] = DiscretizeLineSegment3(x1, y1, z1, x2, y2, z2, tol)
    p1 = [x1, y1, z1];
    p2 = [x2, y2, z2];
    K = ceil( (norm(p1-p2) / tol) ) + 2 ;
    X = (linspace(x1, x2, K))';
    Y = (linspace(y1, y2, K))';
    Z = (linspace(z1, z2, K))';
end
