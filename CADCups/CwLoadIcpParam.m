% Structure IcpParam:
%(1) rutype
%(2) octype
%(3) ictype
%(4) Dinout
%(5) icdOrigin (in solidworks coord)
%(6) XCiw, YCiw, GCi
%(7) XCow, YCow, GCo

function IcpParam = CwLoadIcpParam(IcpParamFilePath)
    assert(nargin == 1);

    fid  = fopen(IcpParamFilePath, 'rt', 'native');
    if fid == -1
        error('fail to open file for read: %s', IcpParamFilePath);
    end

    [IcpParam.rutype, count] = fscanf(fid, '%d', 1);
    assert(count == 1);

    [IcpParam.octype, count] = fscanf(fid, '%d', 1);
    assert(count == 1);

    [IcpParam.ictype, count] = fscanf(fid, '%s', 1);
    assert(count == 1);

    [IcpParam.Dinout, count] = fscanf(fid, '%g', 1);
    assert(count == 1);

    [IcpParam.icdOrigin, count] = fscanf(fid, '%g', 3);  %in solidworks coord
    assert( count == 3);

    [coordType, count] = fscanf(fid, '%d', 1);
    assert( count == 1);
    assert( coordType == 1 || coordType == 2);

    [Xiw, Yiw, XCiw, YCiw] = CwReadPath2D(fid, 0.01);
    if coordType == 2
        Xiw = Xiw - IcpParam.icdOrigin(1);
        Yiw = Yiw - IcpParam.icdOrigin(2);
        XCiw = XCiw - IcpParam.icdOrigin(1);
        YCiw = YCiw - IcpParam.icdOrigin(2);
    end
    assert( 1.0 + Xiw(1) == 1.0 );  %curve must start from inside bottom whose x-coord = 0 in ICD-Coord.
    [GCi, ix] = dpsimplify([Xiw Yiw], 0.05);   %tol = 0.05mm
    GCi(:,2) = CwMonotonize(GCi(:,2), 0.001);
    IcpParam.XCiw = XCiw;
    IcpParam.YCiw = YCiw;
    IcpParam.GCi = GCi;

    [Xow, Yow, XCow, YCow] = CwReadPath2D(fid, 0.01);
    if coordType == 2
        Xow = Xow - IcpParam.icdOrigin(1);
        Yow = Yow - IcpParam.icdOrigin(2);
        XCow = XCow - IcpParam.icdOrigin(1);
        YCow = YCow - IcpParam.icdOrigin(2);
    end
    assert( 1.0 + Xow(1) == 1.0 );  %curve must start from outside bottom whose x-coord = 0 in ICD-Coord.
    [GCo, ix] = dpsimplify([Xow Yow], 0.05);   %tol = 0.05mm
    GCo(:,2) = CwMonotonize(GCo(:,2), 0.001);
    IcpParam.XCow = XCow;
    IcpParam.YCow = YCow;
    IcpParam.GCo = GCo;

    fclose(fid);

end
