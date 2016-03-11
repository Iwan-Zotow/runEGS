%Save to .icp format
function CwSaveAsDotIcp(IcpFilePath, IcpParam)

    assert(nargin == 2);

    %Conversion formulae from ICD-Coord. to OC-Coord.
    %x' = -z
    %y' = x
    %z' = -(y-yo) - Dinout
    %yo = IcpParam.Yiw(1);
    yo = IcpParam.GCi(1,2);

    fid = fopen(IcpFilePath, 'wt', 'native');
    if fid == -1
        error('fail to open file for write: %s', IcpFilePath);
    end

    fprintf(fid,'%d\n', IcpParam.rutype);
    fprintf(fid,'%d\n', IcpParam.octype);
    fprintf(fid,'%s\n', IcpParam.ictype);

    fprintf(fid,'%d\n', size(IcpParam.GCi,1));
    for i = 1 : size(IcpParam.GCi, 1)
        fprintf(fid,'%e %e\n', -(IcpParam.GCi(i,2) - yo) - IcpParam.Dinout, IcpParam.GCi(i,1) );
    end

    fprintf(fid,'%d\n', size(IcpParam.GCo,1));
    for i = 1 : size(IcpParam.GCo, 1)
        fprintf(fid,'%e %e\n', -(IcpParam.GCo(i,2) - yo) - IcpParam.Dinout, IcpParam.GCo(i,1) );
    end

    fclose(fid);
end
