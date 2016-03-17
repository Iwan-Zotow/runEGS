%The origin of the KDD_CoordinateSystem is above the COUCH REFERENCE POINT by UpperMargin (mm)
function KddCupsGeoGen(RadiationUnitType, OuterCupType, InnerCupType, UpperMargin)

    assert(nargin == 4);

    %Load OuterCup (in OC-Coord.)
    if OuterCupType ~= 0
        OcpFilePath = sprintf('OuterCups\\Out\\R%dO%d.ocp',RadiationUnitType,OuterCupType);
        Ocp =  CwLoadDotOcp(OcpFilePath);
        assert(Ocp.rutype == RadiationUnitType);
        assert(Ocp.octype == OuterCupType);
    else
        Ocp.rutype = RadiationUnitType;
        Ocp.octype = OuterCupType; %imaginery outercup 0
        Ocp.D = 0;
    end

    %Load InnerCup
    if OuterCupType ~= 0
        IcpFilePath = sprintf('InnerCups\\Out\\R%dO%dI%s.icp',RadiationUnitType,OuterCupType,InnerCupType);
        Icp = CwLoadDotIcp(IcpFilePath);
        assert(Icp.rutype == RadiationUnitType);
        assert(Icp.octype == OuterCupType);
        assert(strcmp(Icp.ictype, InnerCupType) == true);

        %Convert from OC-Coord. to Kdd-Coord.
        IcIw = Icp.IcIw;
        OcIw = Ocp.OcIw;
        OcOw = Ocp.OcOw;
        IcIw(:,1) = IcIw(:,1) + (Ocp.D + UpperMargin);
        OcIw(:,1) = OcIw(:,1) + (Ocp.D + UpperMargin);
        OcOw(:,1) = OcOw(:,1) + (Ocp.D + UpperMargin);

        %Export Curve A
        CurveAFileName = sprintf('Kdd_CupGeometry\\Out\\R%dO%dI%s_KddCurveA.txt', ...
                                  RadiationUnitType, OuterCupType, InnerCupType);
        fid = fopen(CurveAFileName, 'wt', 'native');
        if fid == -1
            error('fail to open file for write: %s', CurveAFileName);
        end
        fprintf(fid, '%g %g\n', IcIw');
        fclose(fid);

        %Export Curve B
        CurveBFileName = sprintf('Kdd_CupGeometry\\Out\\R%dO%dI%s_KddCurveB.txt', ...
                                  RadiationUnitType, OuterCupType, InnerCupType);
        fid = fopen(CurveBFileName, 'wt', 'native');
        if fid == -1
            error('fail to open file for write: %s', CurveBFileName);
        end
        fprintf(fid, '%g %g\n', OcIw');
        fclose(fid);

        %Export Curve C
        CurveCFileName = sprintf('Kdd_CupGeometry\\Out\\R%dO%dI%s_KddCurveC.txt', ...
                         RadiationUnitType, OuterCupType, InnerCupType);
        fid = fopen(CurveCFileName, 'wt', 'native');
        if fid == -1
            error('fail to open file for write: %s', CurveCFileName);
        end
        fprintf(fid, '%g %g\n', OcOw');
        fclose(fid);

        %Plot the curves
        plot(IcIw(:,1), IcIw(:,2), 'g-v', 'LineWidth', 2);
        hold on;
        plot(OcIw(:,1), OcIw(:,2), 'b-d', 'LineWidth', 2);
        plot(OcOw(:,1), OcOw(:,2), 'r-+', 'LineWidth', 2);

        xlabel('Z (mm)');
        ylabel('Y (mm)');
        title(sprintf('RadiationUnit %d / OuterCup %d / InnerCup %s \n', ...
                       RadiationUnitType, OuterCupType, InnerCupType));
        grid on;
        axis equal;
        scrsz = get(0,'ScreenSize');
        set(0,'DefaultFigurePosition', [scrsz(1) scrsz(2) scrsz(3) scrsz(4)]);
        pause(0.5);       %wait 0.5 second

        saveas(gcf, sprintf('Kdd_CupGeometry\\Out\\R%dO%dI%s_Kdd.fig',RadiationUnitType,OuterCupType, InnerCupType));
        %plot2svg('QQQ.svg');
        close all
    else
        Icp.rutype = RadiationUnitType;
        Icp.octype = OuterCupType;
        Icp.ictype = InnerCupType;
    end

    %Save *.kddparam
    KddParamFilePath = sprintf('Kdd_CupGeometry\\Out\\R%dO%dI%s.kddparam', ...
                       RadiationUnitType,OuterCupType, InnerCupType);
    CwSaveAsKddParam(KddParamFilePath, Ocp, Icp, UpperMargin);

end
