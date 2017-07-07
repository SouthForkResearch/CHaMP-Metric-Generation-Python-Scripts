import numpy
import pandas as pd
import os

def Substrate_Function(inputdata, cudata):
    print('Calculating Substrate Metrics')

    AreaTotal = []
    #print(AreaTotal)
    idx=0
    for CID in inputdata.ChannelUnitID:
        AreaTotal.append(float(cudata[cudata.ChUnitID==CID].AreaTotal))
        idx=idx+1

    inputdata['AreaTotal'] = AreaTotal
    # Remove rows where area total is NaN
    inputdata = inputdata[(numpy.isnan(inputdata.AreaTotal)==False)]

    # print(inputdata.AreaTotal)
    sumA = numpy.nansum(inputdata.AreaTotal)


    Area_Pct_by_CU = []
    for a in inputdata.AreaTotal:
        Area_Pct_by_CU.append(a / sumA)

    # numpy.nanmin has an issue with panda dataframes, and returns an array all populated with the minimum. So we need to take the
    # minimum of that array.  (or any element of it...they should all be the same)
    MinSSC = min(numpy.nanmin(inputdata.SumSubstrateCover))

    valid = MinSSC > 89.99999

    # Calculate each metric.
    Bldr_by_CU = Area_Pct_by_CU * inputdata.BouldersGT256
    SubEstBldr = numpy.nansum(Bldr_by_CU)

    Cbl_by_CU = Area_Pct_by_CU * inputdata.Cobbles65255
    SubEstCbl = numpy.nansum(Cbl_by_CU)

    CoarseGrvl_by_CU = Area_Pct_by_CU * inputdata.CoarseGravel1764
    FineGrvl_by_CU = Area_Pct_by_CU * inputdata.FineGravel316
    SubEstGrvl = numpy.nansum(CoarseGrvl_by_CU)+numpy.nansum(FineGrvl_by_CU)


    Sand_by_CU = Area_Pct_by_CU * inputdata.Sand0062
    Fines_by_CU = Area_Pct_by_CU * inputdata.FinesLT006
    SubEstSandFines = numpy.nansum(Sand_by_CU)+numpy.nansum(Fines_by_CU)

    returnlist = pd.Series([valid,SubEstBldr, SubEstCbl, SubEstGrvl, SubEstSandFines],
                           index = ['valid',   'SubEstBldr', 'SubEstCbl', 'SubEstGrvl', 'SubEstSandFines'])

    return(returnlist)




# __name__ is a specifal variable that gets set when you run this file directly
if __name__ == "__main__":

    VisitID = 2505
    VisitID = 2608
    VisitID = 1
    print(VisitID)
    inputdata=pd.read_csv('SubstrateCover.csv')
    cudata=pd.read_csv('ChannelUnitSummary.csv')

    #data = data[(D_data.SubstrateSizeClass != "1448 - 2048mm")]
    inputdata = inputdata[(inputdata.VisitID == VisitID)]
    cudata = cudata[(cudata.VisitID == VisitID)]
    cudata = cudata.reset_index(drop=True)
    inputdata = inputdata.reset_index(drop=True)

    results = Substrate_Function(inputdata, cudata)
    print(results)