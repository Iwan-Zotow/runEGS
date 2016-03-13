function [X,Y,Z,XC,YC,ZC] = CwReadFiducialCurveSegment(fid, GC, Tol)

assert( nargin == 3 );
assert( all( GC(:,2) >= 0 ) );

X = []; Y = []; Z = [];
XC = []; YC = []; ZC = [];

while 1
    [command, count] = fscanf(fid, '%s', 1);
    assert(count == 1);

    switch(lower(command))
        case 'newfcsegment'
            [P, count] = fscanf(fid, '%g', 3);
            assert(count == 3);
            x = P(1); y = P(2); z = P(3);

            X = x;  Y = y;  Z = z;
            XC = x; YC = y; ZC = z;
            xcurrent = x;   ycurrent = y; zcurrent = z;

        case 'lineto'
            [P, count] = fscanf(fid, '%g', 3);
            assert(count == 3);
            x = P(1); y = P(2); z = P(3);

            [Xline, Yline, Zline] = DiscretizeLineSegment3(xcurrent, ycurrent, zcurrent, x,y,z, Tol);
            X = [X; Xline]; Y = [Y; Yline]; Z = [Z; Zline];
            XC = [XC; x];   YC = [YC; y];   ZC = [ZC; z];
            xcurrent = x;   ycurrent = y; zcurrent = z;

        case 'arcto'
            [P, count] = fscanf(fid, '%g', 6);
            assert(count == 6);
            x1 = P(1); y1 = P(2); z1 = P(3);
            x2 = P(4); y2 = P(5); z2 = P(6);

            [Xarc, Yarc, Zarc] = DiscretizeArcSegment3(xcurrent, ycurrent, zcurrent, x1, y1, z1, x2, y2, z2, Tol);
            %plot3(Xarc, Yarc, Zarc, 'b-*', [xcurrent x1 x2]', [ycurrent y1 y2]', [zcurrent z1 z2]', 'rx--');

            X = [X; Xarc];  Y = [Y; Yarc];  Z = [Z; Zarc];
            XC = [XC; x1; x2];  YC = [YC; y1; y2];  ZC = [ZC; z1; z2];
            xcurrent = x2;  ycurrent = y2;  zcurrent = z2;

        case 'spiralto'
            [n, count] = fscanf(fid, '%d', 1);
            assert(count == 1);
            [P, count] = fscanf(fid, '%g', n*3);
            assert(count == n*3);
            Q = reshape(P, 3, n)';
            x = Q(:,1); y = Q(:,2); z = Q(:,3);

            %Since Outer Cup Design Coord. uses Y-axis as the rotational
            %axis, and the DiscretizeSpiralSegment3 requires Z-axis to be
            %the rotational axis, we map X->Y', Y->Z', Z->X' so that the
            %Z-axis is now the rotational axis
            [Zspiral, Xspiral, Yspiral] = DiscretizeSpiralSegment3(GC, zcurrent, xcurrent, ycurrent, z, x, y, Tol);
            %plot3(Xspiral, Yspiral, Zspiral, 'b-',[xcurrent; x], [ycurrent; y], [zcurrent; z], 'rx--');

            X = [X; Xspiral]; Y = [Y; Yspiral]; Z = [Z; Zspiral];
            XC = [XC; x];   YC = [YC; y]; ZC = [ZC; z];
            xcurrent = x(end); ycurrent = y(end); zcurrent = z(end);
        case 'closefcsegment'
            break;

        otherwise
            error('Unknown command');
    end
end

end
