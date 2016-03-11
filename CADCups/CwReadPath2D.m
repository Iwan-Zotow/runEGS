%X, Y: samples points
%XC, YC: control points
function [X, Y, XC, YC] = CwReadPath2D(fid, Tol)

assert( nargin == 2 );

X = []; Y = [];     %discretized points
XC = []; YC = [];   %control points
while 1
    [command, count] = fscanf(fid, '%s', 1);
    assert(count == 1 );

    switch lower(command)
        case 'newpath'
            [P, count] = fscanf(fid, '%g', 2);
            assert(count == 2);
            x = P(1); y = P(2);
            X = x;          Y = y;
            XC = x;         YC = y;
            xcurrent = x;   ycurrent = y;

        case 'lineto'
            [P, count] = fscanf(fid, '%g', 2);
            assert (count == 2 );
            x = P(1); y = P(2);

            [Xline, Yline] = DiscretizeLineSegment2(xcurrent, ycurrent, x, y, Tol);
            X = [X; Xline];     Y = [Y; Yline];
            XC = [XC; x];       YC = [YC; y];
            xcurrent = x;       ycurrent = y;

        case 'arcto'
            [P, count] = fscanf(fid, '%g', 4);
            assert (count == 4 );
            x1 = P(1); y1 = P(2);
            x2 = P(3); y2 = P(4);

            [Xarc, Yarc] = DiscretizeArcSegment2(xcurrent, ycurrent, x1, y1, x2, y2, Tol);
            X = [X; Xarc];      Y = [Y; Yarc];
            XC = [XC; x1; x2];  YC = [YC; y1; y2];
            xcurrent = x2;      ycurrent = y2;

        case 'ellipseto'
            [P, count] = fscanf(fid, '%g', 6);
            assert (count == 6 );
            x1 = P(1); y1 = P(2); x2 = P(3); y2 = P(4); x3 = P(5); y3 = P(6);

            [Xellipse, Yellipse] = DiscretizeEllipticalSegment2(xcurrent, ycurrent, x1, y1, x2, y2, x3, y3, Tol);
            X = [X; Xellipse];      Y = [Y; Yellipse];
            XC = [XC; x1; x2; x3];   YC = [YC; y1; y2; y3];
            xcurrent = x3;          ycurrent = y3;

        case 'closepath'
            break;

        otherwise
            error('Unknown command');
    end
end

end %function
