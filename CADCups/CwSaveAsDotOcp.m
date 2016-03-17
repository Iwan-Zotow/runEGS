%Save to .icp format
function CwSaveAsDotOcp(OcpFilePath, OcpParam)

    assert(nargin == 2);

    %conversion formulae from OCD-Coord. to OC-Coord.
    %x' = -z
    %y' = x
    %z' = -(y-yo)
    yo = OcpParam.GCi(1,2);
    disp(yo);

    fid = fopen(OcpFilePath, 'wt', 'native');
    if fid == -1
        error('fail to open file for write: %s', OcpFilePath);
    end

    fprintf(fid,'%d\n', OcpParam.rutype);
    fprintf(fid,'%d\n', OcpParam.octype);
    fprintf(fid,'%e\n', OcpParam.D);

    fprintf(fid,'%d\n', size(OcpParam.GCi,1));
    for i = 1 : size(OcpParam.GCi,1)
        fprintf(fid, '%e %e\n', -(OcpParam.GCi(i,2) - yo), OcpParam.GCi(i,1));
    end

    fprintf(fid, '%d\n', size(OcpParam.GCo, 1));
    for i = 1 : size(OcpParam.GCo,1)
        fprintf(fid, '%e %e\n', -(OcpParam.GCo(i,2) - yo), OcpParam.GCo(i,1));
    end

    V = GetVertices(OcpParam.FC);
    fprintf(fid,'%d\n', size(V, 1));
    for i = 1 : size(V, 1)
        fprintf(fid,'%e %e %e\n', -V(i,3), V(i,1), -(V(i,2) - yo) );
    end

    E = GetEdges(OcpParam.FC);
    fprintf(fid,'%d\n', size(E,1));   %single curve mode
    for i = 1 : size(E,1)
        fprintf(fid,'%d %d\n', E(i,1), E(i,2));
    end

    fclose(fid);
end

%return V, a (nVx3)-matrix
function V = GetVertices(FC)
    V = [];
    for segment = 1 : length(FC)
       V = [V; FC(segment).C];
    end
end

function E = GetEdges(FC)
    E = [];
    nV = 0;
    for segment = 1 : length(FC)
        for v = 2 : size(FC(segment).C, 1)
            e = [nV+v-2   nV+v-1];
            E = [E; e];
        end
        nV = nV + size(FC(segment).C, 1);
    end
end
