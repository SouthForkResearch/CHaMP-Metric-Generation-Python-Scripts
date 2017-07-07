import pandas as pd
import os
import numpy

def Fish_Cover_Function(inputdata, cudata):
    print("Calculating Fish Cover:")
    # print(cudata)

#    data = data[data$SumFishCover > 89.99999,]
    inputdata = inputdata[(inputdata.SumFishCover > 89.99999)]
    inputdata = inputdata.reset_index(drop=True)

    # Match AreaTotal to Channel Unit ID
    AreaTotal = []
    #print(AreaTotal)
    #idx=0
    for CID in inputdata.ChannelUnitID:
        #AreaTotal[idx]= float(cudata[cudata.ChUnitID == CID].AreaTotal)
        AreaTotal.append(float(cudata[cudata.ChUnitID==CID].AreaTotal))
        #idx=idx+1

    #print(AreaTotal)
    sumA = numpy.nansum(AreaTotal)
    Area_Pct_by_CU = []
    for a in AreaTotal:
        Area_Pct_by_CU.append(a/sumA)

    #print(Area_Pct_by_CU)

    # Fund minimu of SumFishCover.  Criteria is that it must be greater than
    # or equal to 90% for a valid metric
    MinSFC = min(inputdata.SumFishCover)
    valid = MinSFC > .8999999
    #print(valid)
    #print(MinSFC)

    # Calculate each metric.
    FishCovLW_by_CU = Area_Pct_by_CU * inputdata.WoodyDebrisFC
    FishCovLW = numpy.nansum(FishCovLW_by_CU)

    FishCovTVeg_by_CU = Area_Pct_by_CU * inputdata.OverhangingVegetationFC
    FishCovTVeg = numpy.nansum(FishCovTVeg_by_CU)

    FishCovUcut_by_CU = Area_Pct_by_CU * inputdata.UndercutBanksFC
    FishCovUcut = numpy.nansum(FishCovUcut_by_CU)

    FishCovArt_by_CU = Area_Pct_by_CU * inputdata.ArtificialFC
    FishCovArt = numpy.nansum(FishCovArt_by_CU)

    FishCovAqVeg_by_CU = Area_Pct_by_CU * inputdata.AquaticVegetationFC
    FishCovAqVeg = numpy.nansum(FishCovAqVeg_by_CU)

    FishCovNone_by_CU = Area_Pct_by_CU * inputdata.TotalNoFC
    FishCovNone = numpy.nansum(FishCovNone_by_CU)

    FishCovTotal = numpy.nansum([FishCovLW,FishCovTVeg,FishCovUcut,FishCovArt,FishCovAqVeg])

    returnlist = pd.Series([FishCovLW, FishCovTVeg, FishCovUcut, FishCovArt, FishCovAqVeg, FishCovNone, FishCovTotal,valid],
                                index=['FishCovLW', 'FishCovTVeg', 'FishCovUcut', 'FishCovArt', 'FishCovAqVeg', 'FishCovNone', 'FishCovTotal','valid'])

    return(returnlist)

    #############################################################



# __name__ is a specifal variable that gets set when you run this file directly
if __name__ == "__main__":

    print(os.listdir(os.getcwd()))

    VisitID = 2608
    print(VisitID)
    inputdata=pd.read_csv('FishCover.csv')
    cudata=pd.read_csv('ChannelUnitSummary.csv')

    #data = data[(D_data.SubstrateSizeClass != "1448 - 2048mm")]
    inputdata = inputdata[(inputdata.VisitID == VisitID)]
    cudata = cudata[(cudata.VisitID == VisitID)]
    cudata = cudata.reset_index(drop=True)
    inputdata = inputdata.reset_index(drop=True)
    results = Fish_Cover_Function(inputdata, cudata)
    print(results)
    print "Done"