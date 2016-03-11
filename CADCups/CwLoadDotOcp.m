%Load .ocp file to structure 'Ocp'
%(1) rutype
%(2) octype
%(3) D
%(4) OcIw
%(5) OcOw

function Ocp = CwLoadDotOcp(OcpFilePath)

    assert(nargin == 1);

    fid = fopen(OcpFilePath,'rt', 'native');
    if fid == -1
        error('fail to open file for read: %s', OcpFilePath);
    end

    [Ocp.rutype, count] = fscanf(fid,'%d',1);
    assert(count == 1);

    [Ocp.octype, count] = fscanf(fid, '%d', 1);
    assert(count == 1);


    [Ocp.D, count] = fscanf(fid, '%g', 1);
    assert(count == 1);
    %D is the signed distance from inside bottom of the outer cup to the
    %COUCH REFERENCE POINT; Positive if the inside bottom is below the
    %CRP, and negative otherwise.

    [n1, count] = fscanf(fid, '%d', 1);
    assert(count == 1);
    assert(n1 > 0);
    Ocp.OcIw = zeros(n1, 2);
    for i=1:n1
        Ocp.OcIw(i,1) = fscanf(fid,'%g',1);
        Ocp.OcIw(i,2) = fscanf(fid,'%g',1);
    end

    [n2, count] = fscanf(fid, '%d', 1);
    assert(count == 1);
    assert(n2 > 0);
    Ocp.OcOw = zeros(n2, 2);
    for i=1:n2
        Ocp.OcOw(i,1) = fscanf(fid,'%g',1); %z
        Ocp.OcOw(i,2) = fscanf(fid,'%g',1); %R
    end

    fclose(fid);

    %Verify the GC's are strictly decreasing in OC-Coord.
    assert( all( Ocp.OcIw(1:(n1-1), 1) > Ocp.OcIw(2:n1, 1) ) );
    assert( all( Ocp.OcOw(1:(n2-1), 1) > Ocp.OcOw(2:n2, 1) ) );

end

