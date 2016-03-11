
function CwSaveAsKddParam(KddParamFilePath, Ocp, Icp, UpperMargin)
    assert(nargin == 4);
    assert(Ocp.rutype == Icp.rutype);
    assert(Ocp.octype == Icp.octype);
    
    fid = fopen(KddParamFilePath, 'wt', 'native');
    if fid == -1
        error('fail to open file for write: %s', KddParamFilePath);
    end

    fprintf(fid, '%d\n', Icp.rutype);
    fprintf(fid, '%d\n', Icp.octype);
    fprintf(fid, '%s\n', Icp.ictype);
    fprintf(fid, '%e\n', Ocp.D + UpperMargin);
    fclose(fid);
end
