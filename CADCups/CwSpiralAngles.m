%Given a sequence of points in 3D, calculate the corresponding spiral
%angles. x, y, z are column vectors. unit mm; angle unit radial;
%Assumptions:
%(1) The rotational axis of the spiral is the z-axis
%(2) Any two consecutive points in the sequence has angular distance < pi
%(3) Angle is linearly dependent on z-coordinates
function angle = CwSpiralAngles(x, y, z)
    
    R = abs(x + i*y);
    
    ind = find( R == 0 );
    ind = [ 0; ind; length(R)+1 ];
    
    C = [];
    for k = 1 : (length(ind)-1)
        s = ind(k);
        e = ind(k+1);
       if e - s >= 2
           [a, b] = SprialAngleNonDegenerate( x((s+1):(e-1)), y((s+1):(e-1)), z((s+1):(e-1)) );
           C = [ C; a b];
       end
    end
    
    a = mean(C(:,1));
    b = mean(C(:,2));
    angle = a*z + b;
    
    if max(abs(R.*cos(angle) - x)) > 0.1
        error('CwSpiralAngles: max x-error > 0.1 mm');
    end
    if max(abs(R.*sin(angle) - y)) > 0.1
        error('CwSpiralAngles: max y-error > 0.1 mm');
    end
end

%Nondegenerate case: no points lie on the z-axis
%theta = az + b
function [a, b] = SprialAngleNonDegenerate(x, y, z)
    theta = unwrap( angle(x + i*y) );
    w = mldivide( [z ones(size(z))] , theta );
    a = w(1);
    b = w(2);
    if max(abs(a*z + b - theta)) > (0.5*pi/180)
        error('SprialAngleNonDegenerate: linear regression failed, check input data!');
    end
end
