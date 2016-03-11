%return column vector X and Y
function [X, Y] = DiscretizeLineSegment2(x1, y1, x2, y2, tol)
    p1 = [x1, y1];
    p2 = [x2, y2];
    K = ceil( (norm(p1-p2) / tol) ) + 2 ;
    X = (linspace(x1, x2, K))';
    Y = (linspace(y1, y2, K))';
end
