function  IcpGen(RadiationUnitType, OuterCupType, InnerCupType)

    assert( nargin == 3 );

    %Load .icpparam file
    IcpParamFilePath = sprintf('InnerCups\\In\\R%dO%dI%s.icpparam', RadiationUnitType, OuterCupType, InnerCupType);
    IcpParam = CwLoadIcpParam(IcpParamFilePath);
    assert(IcpParam.rutype == RadiationUnitType);
    assert(IcpParam.octype == OuterCupType);
    assert(strcmp(IcpParam.ictype, InnerCupType) == true);

    %fcrv = fopen('zzz.dat', 'wt', 'native');
    %if fcrv == -1
    %    error('fail to open file for write: %s', 'zzz.dat');
    %end
    %for i = 1 : size(IcpParam.GCi, 1)
    %    fprintf(fcrv, '%e   %e\n', IcpParam.GCi(i,1), IcpParam.GCi(i,2));
    %end
    %fclose(fcrv);

    %Plot for verification
    scrsz = get(0,'ScreenSize');
    set(gcf,'position',[1 1 1024 768])
    axis equal;
    plot(IcpParam.GCi(:,1), IcpParam.GCi(:,2),'r-', ...
         IcpParam.XCiw, IcpParam.YCiw, 'r+', ...
         IcpParam.GCo(:,1), IcpParam.GCo(:,2), 'b-', ...
         IcpParam.XCow, IcpParam.YCow, 'b+');
    title(sprintf('RadiationUnit %d / OuterCup %d / InnerCup %s \n', ...
        RadiationUnitType, OuterCupType, InnerCupType));
    xlabel('X');
    ylabel('Y');
    pause(1.0);       %wait 1.0 second
    saveas(gcf, sprintf('InnerCups\\Out\\Verify_R%dO%dI%s.fig',RadiationUnitType,OuterCupType, InnerCupType) );
    close all

    %Save Inside Wall GC to plain text files for verification. In SWK-Coord.
    iwtxtfilename = sprintf('InnerCups\\Out\\Verify_R%dO%dI%s_InsideWall.txt', RadiationUnitType, OuterCupType, InnerCupType);
    fid = fopen(iwtxtfilename, 'wt', 'native');
    if fid == -1
        error('fail to open file for write: %s', iwtxtfilename);
    end
    for i = 2 : size(IcpParam.GCi, 1)
        xtemp = linspace(IcpParam.GCi(i-1,1),IcpParam.GCi(i,1)) + IcpParam.icdOrigin(1);
        ytemp = linspace(IcpParam.GCi(i-1,2),IcpParam.GCi(i,2)) + IcpParam.icdOrigin(2);
        ztemp = linspace(0,0) + IcpParam.icdOrigin(3);
        if i == 2
            fprintf(fid, '%e %e %e\n', [xtemp; ytemp; ztemp]);
        else
            fprintf(fid, '%e %e %e\n', [xtemp(2:end); ytemp(2:end); ztemp(2:end)]);
        end
    end
    fclose(fid);

    %Save Outside Wall GC to plain text files for verification. In SWK-Coord.
    owtxtfilename = sprintf('InnerCups\\Out\\Verify_R%dO%dI%s_OutsideWall.txt', RadiationUnitType, OuterCupType, InnerCupType);
    fid = fopen(owtxtfilename, 'wt', 'native');
    if fid == -1
        error('fail to open file for write: %s', owtxtfilename);
    end

    for i = 2 : size(IcpParam.GCo, 1)
        xtemp = linspace(IcpParam.GCo(i-1,1),IcpParam.GCo(i,1))+ IcpParam.icdOrigin(1);
        ytemp = linspace(IcpParam.GCo(i-1,2),IcpParam.GCo(i,2))+ IcpParam.icdOrigin(2);
        ztemp = linspace(0,0)+ IcpParam.icdOrigin(3);
        if i == 2
            fprintf(fid, '%e %e %e\n', [xtemp; ytemp; ztemp]);
        else
            fprintf(fid, '%e %e %e\n', [xtemp(2:end); ytemp(2:end); ztemp(2:end)]);
        end
    end
    fclose(fid);

    %Save to .icp format
    IcpFilePath = sprintf('InnerCups\\Out\\R%dO%dI%s.icp', RadiationUnitType, OuterCupType, InnerCupType);
    CwSaveAsDotIcp(IcpFilePath, IcpParam)

end
