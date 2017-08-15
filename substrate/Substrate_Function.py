import numpy
import pandas as pd


def Substrate_Function(inputdata, cusummary, cudata):

    # reset the index in case I need that
    cusummary = cusummary.reset_index(drop=True)
    cudata = cudata.reset_index(drop=True)
    inputdata = inputdata.reset_index(drop=True)

    print('Calculating Substrate Metrics')

    AreaTotal = []
    #print(AreaTotal)
    idx=0
    for CID in inputdata.ChannelUnitID:
        AreaTotal.append(float(cusummary[cusummary.ChUnitID==CID].AreaTotal))
        idx=idx+1

    ########################################################################################
    # Match Tier1 using Channel Unit ID.
    # When I first tried to do this, it kept changing hte string "Tier1" into some weird data object that I couldn't use later.
    # So I had to create an index and subset the data, force that index to be an integer, then use that to assign Tier1 into inputdata

    Tier1 = []
    cudata['idx']= list(range(len(cudata)))

    for CID in inputdata.ChannelUnitID:
       temp=cudata[(cudata.ChannelUnitID == CID)]
       Tier1.append(cudata.Tier1[int(temp.idx)])
    #print(Tier1)
    inputdata['Tier1']=Tier1

    #######################################################################################



    inputdata['AreaTotal'] = AreaTotal
    # Remove rows where area total is NaN
    inputdata = inputdata[(numpy.isnan(inputdata.AreaTotal)==False)]

    # print(inputdata.AreaTotal)
    sumA = numpy.nansum(inputdata.AreaTotal)
    sumA_FNT = numpy.nansum(inputdata.AreaTotal[(inputdata.Tier1 == "Fast-NonTurbulent/Glide")])
    sumA_FT = numpy.nansum(inputdata.AreaTotal[(inputdata.Tier1 == "Fast-Turbulent")])
    sumA_SlowPool = numpy.nansum(inputdata.AreaTotal[(inputdata.Tier1 == "Slow/Pool")])
    sumA_SSC = numpy.nansum(inputdata.AreaTotal[(inputdata.Tier1 == "Small Side Channel")])


    Area_Pct_by_CU = []
    Area_Pct_by_CU_FNT = []
    Area_Pct_by_CU_FT = []
    Area_Pct_by_CU_SlowPool = []
    Area_Pct_by_CU_SSC = []


    for a in inputdata.AreaTotal:
        Area_Pct_by_CU.append(a / sumA)
        Area_Pct_by_CU_FNT.append(a / sumA_FNT+.00000000001)
        Area_Pct_by_CU_FT.append(a / sumA_FT+.0000000001)
        Area_Pct_by_CU_SlowPool.append(a / sumA_SlowPool+.00000001)
        Area_Pct_by_CU_SSC.append(a / sumA_SSC+.0000000001)

    inputdata['Area_Pct_by_CU']= Area_Pct_by_CU
    inputdata['Area_Pct_by_CU_FNT']= Area_Pct_by_CU_FNT
    inputdata['Area_Pct_by_CU_FT'] = Area_Pct_by_CU_FT
    inputdata['Area_Pct_by_CU_SlowPool'] = Area_Pct_by_CU_SlowPool
    inputdata['Area_Pct_by_CU_SSC'] = Area_Pct_by_CU_SSC
    # numpy.nanmin has an issue with panda dataframes, and returns an array all populated with the minimum. So we need to take the
    # minimum of that array.  (or any element of it...they should all be the same)
    MinSSC = min(numpy.nanmin(inputdata.SumSubstrateCover))

    valid = MinSSC > 89.99999

    # Calculate each metric.
    ########################################################################

    Bldr_by_CU = inputdata.Area_Pct_by_CU * inputdata.BouldersGT256
    SubEstBldr = numpy.nansum(Bldr_by_CU)

    Bldr_by_CU_FNT = inputdata.Area_Pct_by_CU_FNT[(inputdata.Tier1 == "Fast-NonTurbulent/Glide")] * inputdata.BouldersGT256[(inputdata.Tier1 == "Fast-NonTurbulent/Glide")]
    SubEstBldr_FNT = numpy.nansum(Bldr_by_CU_FNT)

    Bldr_by_CU_FT = inputdata.Area_Pct_by_CU_FT[(inputdata.Tier1 == "Fast-Turbulent")] * inputdata.BouldersGT256[(inputdata.Tier1 == "Fast-Turbulent")]
    SubEstBldr_FT = numpy.nansum(Bldr_by_CU_FT)

    Bldr_by_CU_SlowPool = inputdata.Area_Pct_by_CU_SlowPool[(inputdata.Tier1 == "Slow/Pool")] * inputdata.BouldersGT256[(inputdata.Tier1 == "Slow/Pool")]
    SubEstBldr_SlowPool = numpy.nansum(Bldr_by_CU_SlowPool)

    Bldr_by_CU_SSC = inputdata.Area_Pct_by_CU_SSC[(inputdata.Tier1 == "Small Side Channel")] * inputdata.BouldersGT256[(inputdata.Tier1 == "Small Side Channel")]
    SubEstBldr_SSC = numpy.nansum(Bldr_by_CU_SSC)

    #########################################################################

    Cbl_by_CU = Area_Pct_by_CU * inputdata.Cobbles65255
    SubEstCbl = numpy.nansum(Cbl_by_CU)

    Cbl_by_CU_FNT = inputdata.Area_Pct_by_CU_FNT[(inputdata.Tier1 == "Fast-NonTurbulent/Glide")] * inputdata.Cobbles65255[(inputdata.Tier1 == "Fast-NonTurbulent/Glide")]
    SubEstCbl_FNT = numpy.nansum(Cbl_by_CU_FNT)

    Cbl_by_CU_FT = inputdata.Area_Pct_by_CU_FT[(inputdata.Tier1 == "Fast-Turbulent")] * inputdata.Cobbles65255[(inputdata.Tier1 == "Fast-Turbulent")]
    SubEstCbl_FT = numpy.nansum(Cbl_by_CU_FT)

    Cbl_by_CU_SlowPool = inputdata.Area_Pct_by_CU_SlowPool[(inputdata.Tier1 == "Slow/Pool")] * inputdata.Cobbles65255[(inputdata.Tier1 == "Slow/Pool")]
    SubEstCbl_SlowPool = numpy.nansum(Cbl_by_CU_SlowPool)

    Cbl_by_CU_SSC = inputdata.Area_Pct_by_CU_SSC[(inputdata.Tier1 == "Small Side Channel")] * inputdata.Cobbles65255[(inputdata.Tier1 == "Small Side Channel")]
    SubEstCbl_SSC = numpy.nansum(Cbl_by_CU_SSC)


    ####################################################################3

    CoarseGrvl_by_CU = Area_Pct_by_CU * inputdata.CoarseGravel1764
    FineGrvl_by_CU = Area_Pct_by_CU * inputdata.FineGravel316
    SubEstGrvl = numpy.nansum(CoarseGrvl_by_CU)+numpy.nansum(FineGrvl_by_CU)

    CoarseGrvl_by_CU_FNT = inputdata.Area_Pct_by_CU_FNT[(inputdata.Tier1 == "Fast-NonTurbulent/Glide")] * inputdata.CoarseGravel1764[(inputdata.Tier1 == "Fast-NonTurbulent/Glide")]
    FineGrvl_by_CU_FNT = inputdata.Area_Pct_by_CU_FNT[(inputdata.Tier1 == "Fast-NonTurbulent/Glide")] * inputdata.FineGravel316[(inputdata.Tier1 == "Fast-NonTurbulent/Glide")]
    SubEstGrvl_FNT = numpy.nansum(CoarseGrvl_by_CU_FNT) + numpy.nansum(FineGrvl_by_CU_FNT)

    CoarseGrvl_by_CU_FT = inputdata.Area_Pct_by_CU_FT[(inputdata.Tier1 == "Fast-Turbulent")] * inputdata.CoarseGravel1764[(inputdata.Tier1 == "Fast-Turbulent")]
    FineGrvl_by_CU_FT = inputdata.Area_Pct_by_CU_FT[(inputdata.Tier1 == "Fast-Turbulent")] * inputdata.FineGravel316[(inputdata.Tier1 == "Fast-Turbulent")]
    SubEstGrvl_FT = numpy.nansum(CoarseGrvl_by_CU_FT) + numpy.nansum(FineGrvl_by_CU_FT)

    CoarseGrvl_by_CU_SlowPool = inputdata.Area_Pct_by_CU_SlowPool[(inputdata.Tier1 == "Slow/Pool")] * inputdata.CoarseGravel1764[(inputdata.Tier1 == "Slow/Pool")]
    FineGrvl_by_CU_SlowPool = inputdata.Area_Pct_by_CU_SlowPool[(inputdata.Tier1 == "Slow/Pool")] * inputdata.FineGravel316[(inputdata.Tier1 == "Slow/Pool")]
    SubEstGrvl_SlowPool = numpy.nansum(CoarseGrvl_by_CU_SlowPool) + numpy.nansum(FineGrvl_by_CU_SlowPool)

    CoarseGrvl_by_CU_SSC = inputdata.Area_Pct_by_CU_SSC[(inputdata.Tier1 == "Small Side Channel")] * inputdata.CoarseGravel1764[(inputdata.Tier1 == "Small Side Channel")]
    FineGrvl_by_CU_SSC = inputdata.Area_Pct_by_CU_SSC[(inputdata.Tier1 == "Small Side Channel")] * inputdata.FineGravel316[(inputdata.Tier1 == "Small Side Channel")]
    SubEstGrvl_SSC = numpy.nansum(CoarseGrvl_by_CU_SSC) + numpy.nansum(FineGrvl_by_CU_SSC)


    #####################################################################
    Sand_by_CU = Area_Pct_by_CU * inputdata.Sand0062
    Fines_by_CU = Area_Pct_by_CU * inputdata.FinesLT006
    SubEstSandFines = numpy.nansum(Sand_by_CU)+numpy.nansum(Fines_by_CU)

    Sand_by_CU_FNT = inputdata.Area_Pct_by_CU_FNT[(inputdata.Tier1 == "Fast-NonTurbulent/Glide")] * inputdata.Sand0062[(inputdata.Tier1 == "Fast-NonTurbulent/Glide")]
    Fines_by_CU_FNT = inputdata.Area_Pct_by_CU_FNT[(inputdata.Tier1 == "Fast-NonTurbulent/Glide")] * inputdata.FinesLT006[(inputdata.Tier1 == "Fast-NonTurbulent/Glide")]
    SubEstSandFines_FNT = numpy.nansum(Sand_by_CU_FNT) + numpy.nansum(Fines_by_CU_FNT)

    Sand_by_CU_FT = inputdata.Area_Pct_by_CU_FT[(inputdata.Tier1 == "Fast-Turbulent")] * inputdata.Sand0062[(inputdata.Tier1 == "Fast-Turbulent")]
    Fines_by_CU_FT = inputdata.Area_Pct_by_CU_FT[(inputdata.Tier1 == "Fast-Turbulent")] * inputdata.FinesLT006[(inputdata.Tier1 == "Fast-Turbulent")]
    SubEstSandFines_FT = numpy.nansum(Sand_by_CU_FT) + numpy.nansum(Fines_by_CU_FT)

    Sand_by_CU_SlowPool = inputdata.Area_Pct_by_CU_SlowPool[(inputdata.Tier1 == "Slow/Pool")] * inputdata.Sand0062[(inputdata.Tier1 == "Slow/Pool")]
    Fines_by_CU_SlowPool = inputdata.Area_Pct_by_CU_SlowPool[(inputdata.Tier1 == "Slow/Pool")] * inputdata.FinesLT006[(inputdata.Tier1 == "Slow/Pool")]
    SubEstSandFines_SlowPool = numpy.nansum(Sand_by_CU_SlowPool) + numpy.nansum(Fines_by_CU_SlowPool)

    Sand_by_CU_SSC = inputdata.Area_Pct_by_CU_SSC[(inputdata.Tier1 == "Small Side Channel")] * inputdata.Sand0062[(inputdata.Tier1 == "Small Side Channel")]
    Fines_by_CU_SSC = inputdata.Area_Pct_by_CU_SSC[(inputdata.Tier1 == "Small Side Channel")] * inputdata.FinesLT006[(inputdata.Tier1 == "Small Side Channel")]
    SubEstSandFines_SSC = numpy.nansum(Sand_by_CU_SSC) + numpy.nansum(Fines_by_CU_SSC)


    print(SubEstSandFines_FNT)

    #######################################################################


    returnlist = pd.Series([valid, SubEstBldr, SubEstCbl, SubEstGrvl, SubEstSandFines,
                            SubEstBldr_FNT, SubEstCbl_FNT, SubEstGrvl_FNT, SubEstSandFines_FNT,
                                SubEstBldr_FT, SubEstCbl_FT, SubEstGrvl_FT, SubEstSandFines_FT,
                                    SubEstBldr_SlowPool, SubEstCbl_SlowPool, SubEstGrvl_SlowPool, SubEstSandFines_SlowPool,
                                        SubEstBldr_SSC, SubEstCbl_SSC, SubEstGrvl_SSC, SubEstSandFines_SSC],
                                           index = ['valid',   'SubEstBldr', 'SubEstCbl', 'SubEstGrvl', 'SubEstSandFines',
                                                'SubEstBldr_FNT', 'SubEstCbl_FNT', 'SubEstGrvl_FNT', 'SubEstSandFines_FNT',
                                                    'SubEstBldr_FT', 'SubEstCbl_FT', 'SubEstGrvl_FT', 'SubEstSandFines_FT',
                                                        'SubEstBldr_SlowPool', 'SubEstCbl_SlowPool', 'SubEstGrvl_SlowPool','SubEstSandFines_SlowPool',
                                                            'SubEstBldr_SSC', 'SubEstCbl_SSC', 'SubEstGrvl_SSC', 'SubEstSandFines_SSC'])

    return(returnlist)



    #### end of function ##################################################################


# __name__ is a specifal variable that gets set when you run this file directly
if __name__ == "__main__":
    res = pd.DataFrame(columns=('VisitID','valid', 'SubEstBldr', 'SubEstCbl', 'SubEstGrvl', 'SubEstSandFines',
                                                'SubEstBldr_FNT', 'SubEstCbl_FNT', 'SubEstGrvl_FNT', 'SubEstSandFines_FNT',
                                                    'SubEstBldr_FT', 'SubEstCbl_FT', 'SubEstGrvl_FT', 'SubEstSandFines_FT',
                                                        'SubEstBldr_SlowPool', 'SubEstCbl_SlowPool', 'SubEstGrvl_SlowPool','SubEstSandFines_SlowPool',
                                                            'SubEstBldr_SSC', 'SubEstCbl_SSC', 'SubEstGrvl_SSC', 'SubEstSandFines_SSC'))


    VisitID = 2505
    VisitID = 2608
    VisitID = 4
    print(VisitID)
    inputdata_all=pd.read_csv('SubstrateCover.csv')
    cusummary_all=pd.read_csv('ChannelUnitSummary.csv')
    cudata_all = pd.read_csv('ChannelUnit.csv')

    VisitIDs = inputdata_all.VisitID
    VisitIDs = numpy.unique(VisitIDs)
    #VisitIDs = VisitIDs[0:100]
    #VisitIDs = [2020]

    counter = 0
    for VisitID in VisitIDs:
        print(VisitID)

        #data = data[(D_data.SubstrateSizeClass != "1448 - 2048mm")]
        inputdata = inputdata_all[(inputdata_all.VisitID == VisitID)]
        cusummary = cusummary_all[(cusummary_all.VisitID == VisitID)]
        cudata = cudata_all[(cudata_all.VisitID == VisitID)]

        if ((len(cudata) > 0 and len(cusummary) > 0) and len(inputdata) > 0):

            results = Substrate_Function(inputdata, cusummary, cudata)
            #print(results)

            res.set_value(counter, 'VisitID', VisitID)
            res.set_value(counter, ['valid', 'SubEstBldr', 'SubEstCbl', 'SubEstGrvl', 'SubEstSandFines',
                                                    'SubEstBldr_FNT', 'SubEstCbl_FNT', 'SubEstGrvl_FNT', 'SubEstSandFines_FNT',
                                                        'SubEstBldr_FT', 'SubEstCbl_FT', 'SubEstGrvl_FT', 'SubEstSandFines_FT',
                                                            'SubEstBldr_SlowPool', 'SubEstCbl_SlowPool', 'SubEstGrvl_SlowPool','SubEstSandFines_SlowPool',
                                                                'SubEstBldr_SSC', 'SubEstCbl_SSC', 'SubEstGrvl_SSC', 'SubEstSandFines_SSC'],results)
            counter=counter+1

    print "Done"

    print(res)
    res.to_csv('Substrate_Val.csv')