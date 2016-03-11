%Be sure to map X, Y, Z correctly
%(1)X+, Y+, Z+ right-handed
%(2)Z : rotational axis
%GC = [Z R ] (cylindrical coord.)

%Returns a struct array S of {X, Y, Z, XC, YC, ZC}

function S = CwReadFiducialCurve(fid, GC, Tol)

assert( nargin == 3 );
assert( all( GC(:,2) >= 0 ) );

S = [];

while 1
    [command, count] = fscanf(fid, '%s', 1);
    assert(count == 1);
    switch(lower(command))
        case 'newfc'
            A = [];
            [A.X, A.Y, A.Z, A.XC, A.YC, A.ZC] = CwReadFiducialCurveSegment(fid, GC, Tol);
            S = [ S; A];
        case 'closefc'
            break;
        otherwise
            error('Unknown command');
    end
end

end
