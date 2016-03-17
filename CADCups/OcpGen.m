function  OcpGen(RadiationUnitType, OuterCupType)
    
    assert( nargin == 2 );
    
    OcpParamFilePath = sprintf('OuterCups\\In\\R%dO%d.ocpparam',RadiationUnitType,OuterCupType);
    OcpParam = CwLoadOcpParam(OcpParamFilePath);
    assert(OcpParam.rutype == RadiationUnitType);
    assert(OcpParam.octype == OuterCupType);
    
    scrsz = get(0,'ScreenSize');
    set(gcf,'position',[1 1 1024 768])
    axis equal;
    for segment = 1 : length(OcpParam.FC)
        plot3(OcpParam.FC(segment).C(:,1),OcpParam.FC(segment).C(:,2),OcpParam.FC(segment).C(:,3),'g-', ...
              OcpParam.FC(segment).XC, OcpParam.FC(segment).YC, OcpParam.FC(segment).ZC, 'gx');
        hold on;
    end
    xlabel('X');    ylabel('Y');    zlabel('Z');
    title(sprintf('RadiationUnit %d / OuterCup %d \n', RadiationUnitType, OuterCupType));
    pause(1.0); %wait 1.0 second
    saveas(gcf, sprintf('OuterCups\\Out\\Verify_R%dO%d_Fiducial.fig', RadiationUnitType, OuterCupType));
    close all

    scrsz = get(0,'ScreenSize');
    set(gcf,'position',[1 1 1024 768])
    axis equal;
    plot(OcpParam.GCi(:,1), OcpParam.GCi(:,2),'r-', ...
        OcpParam.XCiw, OcpParam.YCiw, 'r+', ...
        OcpParam.GCo(:,1), OcpParam.GCo(:,2), 'b-', ...
        OcpParam.XCow, OcpParam.YCow, 'b+');
    xlabel('X');    ylabel('Y');
    title(sprintf('RadiationUnit %d / OuterCup %d \n', RadiationUnitType, OuterCupType));
    pause(1.0); %wait 1.0 second
    saveas(gcf, sprintf('OuterCups\\Out\\Verify_R%dO%d_Walls.fig', RadiationUnitType, OuterCupType));
    close all

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %EXPORT
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %for verification in Solidworks that designs the cup
    %Export Fiducial curve segments
    for segment = 1 : length(OcpParam.FC)
        fiducialsegtxtfilename = sprintf('OuterCups\\Out\\Verify_R%dO%d_Fiducial_Seg%d.txt', RadiationUnitType,OuterCupType,segment);
        fid = fopen(fiducialsegtxtfilename, 'wt', 'native');
        if fid == -1
            error('fail to open file for write: %s', fiducialsegtxtfilename);
        end

        for i = 2 : size(OcpParam.FC(segment).C,1)
            xtemp = linspace(OcpParam.FC(segment).C(i-1,1),OcpParam.FC(segment).C(i,1)) + OcpParam.ocdOrigin(1);
            ytemp = linspace(OcpParam.FC(segment).C(i-1,2),OcpParam.FC(segment).C(i,2)) + OcpParam.ocdOrigin(2);
            ztemp = linspace(OcpParam.FC(segment).C(i-1,3),OcpParam.FC(segment).C(i,3)) + OcpParam.ocdOrigin(3);
            if i == 2
                fprintf(fid, '%e %e %e\n', [xtemp; ytemp; ztemp]);
            else
                fprintf(fid, '%e %e %e\n', [xtemp(2:end); ytemp(2:end); ztemp(2:end)]);
            end
        end
        fclose(fid);
    end
    
    
    %Export Inside Wall GC
    insidewalltxtfilename = sprintf('OuterCups\\Out\\Verify_R%dO%d_InsideWall.txt', RadiationUnitType,OuterCupType);
    fid = fopen(insidewalltxtfilename, 'wt', 'native');
    if fid == -1
        error('fail to open file for write: %s', insidewalltxtfilename);
    end
    for i = 2 : size(OcpParam.GCi,1)
        xtemp = linspace(OcpParam.GCi(i-1,1),OcpParam.GCi(i,1)) + OcpParam.ocdOrigin(1);
        ytemp = linspace(OcpParam.GCi(i-1,2),OcpParam.GCi(i,2)) + OcpParam.ocdOrigin(2);
        ztemp = linspace(0,0) + - OcpParam.ocdOrigin(3);
        if i == 2
            fprintf(fid, '%e %e %e\n', [xtemp; ytemp; ztemp]);
        else
            fprintf(fid, '%e %e %e\n', [xtemp(2:end); ytemp(2:end); ztemp(2:end)]);
        end
    end
    fclose(fid);

    %Export Outside Wall GC
    outsidewalltxtfilename = sprintf('OuterCups\\Out\\Verify_R%dO%d_OutsideWall.txt', RadiationUnitType,OuterCupType);
    fid = fopen(outsidewalltxtfilename, 'wt', 'native');
    if fid == -1
        error('fail to open file for write: %s', outsidewalltxtfilename);
    end

    for i = 2 : size(OcpParam.GCo,1)
        xtemp = linspace(OcpParam.GCo(i-1,1),OcpParam.GCo(i,1)) + OcpParam.ocdOrigin(1);
        ytemp = linspace(OcpParam.GCo(i-1,2),OcpParam.GCo(i,2)) + OcpParam.ocdOrigin(2);
        ztemp = linspace(0,0) + OcpParam.ocdOrigin(3);
        if i == 2
            fprintf(fid, '%e %e %e\n', [xtemp; ytemp; ztemp]);
        else
            fprintf(fid, '%e %e %e\n', [xtemp(2:end); ytemp(2:end); ztemp(2:end)]);
        end
    end
    fclose(fid);
        
    
    %Save to .ocp format
    OcpFilePath = sprintf('OuterCups\\Out\\R%dO%d.ocp', RadiationUnitType,OuterCupType);
    CwSaveAsDotOcp(OcpFilePath, OcpParam);
    
end
