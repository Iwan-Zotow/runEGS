% load .icp file to structure 'Icp'
%(1) rutype
%(2) octype
%(3) ictype
%(4) IcIw
function Icp = CwLoadDotIcp(IcpFilePath)
    assert(nargin == 1);
    
    fid = fopen(IcpFilePath, 'rt', 'native');
    if fid == -1
        error('fail to open file for read: %s', IcpFilePath);
    end

    [Icp.rutype, count] = fscanf(fid, '%d', 1);
    assert(count == 1);

    [Icp.octype, count] = fscanf(fid, '%d', 1);
    assert(count == 1);

    [Icp.ictype, count] = fscanf(fid, '%s', 1);
    assert(count == 1);

    [n3, count] = fscanf(fid, '%d', 1);
    assert(count == 1);
    assert(n3 > 0);
    
    Icp.IcIw = zeros(n3,2);
    for i = 1:n3
        [Icp.IcIw(i,1), count] = fscanf(fid, '%g', 1);
        assert(count == 1);
        [Icp.IcIw(i,2), count] = fscanf(fid, '%g', 1);
        assert(count == 1);
    end
    fclose(fid);    %we don't load outside gc for now

    %Verify the Inside Wall GC is strictly decreasing in OC-Coord.
    assert( all( Icp.IcIw(1:(n3-1), 1) > Icp.IcIw(2:n3, 1) ) );  
end
