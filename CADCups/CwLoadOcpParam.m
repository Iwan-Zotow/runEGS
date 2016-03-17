%OcpParam [in OCD-Coord]
%(1) rutype
%(2) octype
%(3) D
%(4) ocdOrigin (in solidworks coord)
%(4) XCiw, YCiw, GCi
%(5) XCow, YCow, GCo
%(6) FC
%     C (simplified curve)
%     X, Y, Z,(unsimplified curve)
%     XC, YC, ZC (control points)
function OcpParam = CwLoadOcpParam(OcpParamFilePath)
    assert(nargin == 1);

    fid = fopen(OcpParamFilePath, 'rt', 'native');
    if fid == -1
        error('fail to open file for read: %s', OcpParamFilePath);
    end

    [OcpParam.rutype, count] = fscanf(fid, '%d', 1);
    assert( count == 1);

    [OcpParam.octype, count] = fscanf(fid, '%d', 1);
    assert( count == 1);

    [OcpParam.D, count] = fscanf(fid, '%g', 1);
    assert( count == 1);

    [OcpParam.ocdOrigin, count] = fscanf(fid, '%g', 3);  %in solidworks coord
    assert( count == 3);

    [coordType, count] = fscanf(fid, '%d', 1);
    assert( count == 1);
    assert( coordType == 1 || coordType == 2);

    %load and simplify inside wall
    %the inside wall path must be strictly y-sorted
    [Xiw, Yiw, XCiw, YCiw] = CwReadPath2D(fid, 0.01);
    if coordType == 2
        Xiw = Xiw - OcpParam.ocdOrigin(1);
        Yiw = Yiw - OcpParam.ocdOrigin(2);
        XCiw = XCiw - OcpParam.ocdOrigin(1);
        YCiw = YCiw - OcpParam.ocdOrigin(2);
    end
    assert( 1.0 + Xiw(1) == 1.0 );  %curve must start from inside bottom whose x-coord = 0 in OCD-Coord.
    [GCi, ix] = dpsimplify([Xiw Yiw], 0.05);   %tol = 0.05mm
    GCi(:,2) = CwMonotonize(GCi(:,2), 0.001);
    OcpParam.XCiw = XCiw;
    OcpParam.YCiw = YCiw;
    OcpParam.GCi = GCi;

    %load and simplify outside wall
    %the outside wall path must be strictly y-sorted
    [Xow, Yow, XCow, YCow] = CwReadPath2D(fid, 0.01);
    if coordType == 2
        Xow = Xow - OcpParam.ocdOrigin(1);
        Yow = Yow - OcpParam.ocdOrigin(2);
        XCow = XCow - OcpParam.ocdOrigin(1);
        YCow = YCow - OcpParam.ocdOrigin(2);
    end
    assert( 1.0 + Xow(1) == 1.0 );  %curve must start from outside bottom whose x-coord = 0 in OCD-Coord.
    [GCo, ix] = dpsimplify([Xow Yow], 0.05);   %tol = 0.05mm
    GCo(:,2) = CwMonotonize(GCo(:,2), 0.001);
    OcpParam.XCow = XCow;
    OcpParam.YCow = YCow;
    OcpParam.GCo = GCo;

    %load and simplify fiducial curve
    FC = CwReadFiducialCurve(fid, [GCi(:,2) GCi(:,1)], 0.01);
    for segment = 1 : length(FC)
        if coordType == 2
            FC(segment).X = FC(segment).X - OcpParam.ocdOrigin(1);
            FC(segment).Y = FC(segment).Y - OcpParam.ocdOrigin(2);
            FC(segment).Z = FC(segment).Z - OcpParam.ocdOrigin(3);
            FC(segment).XC = FC(segment).XC - OcpParam.ocdOrigin(1);
            FC(segment).YC = FC(segment).YC - OcpParam.ocdOrigin(2);
            FC(segment).ZC = FC(segment).ZC - OcpParam.ocdOrigin(3);
        end
    end
    for segment = 1 : length(FC)
        [FC(segment).C, ix] = dpsimplify([FC(segment).X FC(segment).Y FC(segment).Z], 0.05);   %tol = 0.05mm
    end
    OcpParam.FC = FC;

    fclose(fid);
end
