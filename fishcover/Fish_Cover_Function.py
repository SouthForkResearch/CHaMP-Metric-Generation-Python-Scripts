import pandas as pd
import os
import numpy

def Fish_Cover_Function(inputdata, cusummary, cudata):
    print("Calculating Fish Cover:")
    # print(cudata)

    FishCovLW = numpy.nan
    FishCovTVeg = numpy.nan
    FishCovUcut = numpy.nan
    FishCovArt = numpy.nan
    FishCovAqVeg = numpy.nan
    FishCovNone = numpy.nan
    FishCovTotal = numpy.nan
    valid = numpy.nan
    FishCovLW_FNT = numpy.nan
    FishCovLW_FT = numpy.nan
    FishCovLW_SlowPool = numpy.nan
    FishCovLW_SSC = numpy.nan
    FishCovTVeg_FNT = numpy.nan
    FishCovTVeg_FT = numpy.nan
    FishCovTVeg_SlowPool = numpy.nan
    FishCovTVeg_SSC = numpy.nan
    FishCovUcut_FNT = numpy.nan
    FishCovUcut_FT = numpy.nan
    FishCovUcut_SlowPool = numpy.nan
    FishCovUcut_SSC = numpy.nan
    FishCovArt_FNT = numpy.nan
    FishCovArt_FT = numpy.nan
    FishCovArt_SlowPool = numpy.nan
    FishCovArt_SSC = numpy.nan
    FishCovAqVeg_FNT = numpy.nan
    FishCovAqVeg_FT = numpy.nan
    FishCovAqVeg_SlowPool = numpy.nan
    FishCovAqVeg_SSC = numpy.nan
    FishCovNone_FNT = numpy.nan
    FishCovNone_FT = numpy.nan
    FishCovNone_SlowPool = numpy.nan
    FishCovNone_SSC = numpy.nan
    FishCovTotal_FNT = numpy.nan
    FishCovTotal_FT = numpy.nan
    FishCovTotal_SlowPool = numpy.nan
    FishCovTotal_SSC = numpy.nan



#    data = data[data$SumFishCover > 89.99999,]
    inputdata = inputdata[(inputdata.SumFishCover > 89.99999)]
    inputdata = inputdata.reset_index(drop=True)

    # I need to make sure my indices go from zero to length...
    cusummary = cusummary.reset_index(drop=True)
    cudata = cudata.reset_index(drop=True)
    inputdata = inputdata.reset_index(drop=True)

    if len(inputdata) > 0:
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





        # Match AreaTotal to Channel Unit ID
        AreaTotal = []
        #print(AreaTotal)
        #idx=0
        for CID in inputdata.ChannelUnitID:
            #AreaTotal[idx]= float(cudata[cudata.ChUnitID == CID].AreaTotal)
            AreaTotal.append(float(cusummary[cusummary.ChUnitID==CID].AreaTotal))
            #idx=idx+1
        inputdata['AreaTotal'] = AreaTotal
        # Old way...
        ##print(AreaTotal)
        #sumA = numpy.nansum(AreaTotal)
        #Area_Pct_by_CU = []
        #for a in AreaTotal:
        #    Area_Pct_by_CU.append(a/sumA)

        #print(Area_Pct_by_CU)

        # Fund minimu of SumFishCover.  Criteria is that it must be greater than
        # or equal to 90% for a valid metric
        MinSFC = numpy.nanmin(inputdata.SumFishCover)
        valid = MinSFC > 89.99999

        # Figure out fraction area in each channel unit
        #Area_Pct_by_CU = inputdata.AreaTotal / numpy.nansum(inputdata.AreaTotal)
        Area_Pct_by_CU = inputdata.AreaTotal / numpy.nansum(inputdata.AreaTotal)
        Area_Pct_by_CU_FNT = inputdata.AreaTotal[(inputdata.Tier1 == "Fast-NonTurbulent/Glide")] / numpy.nansum(inputdata.AreaTotal[(inputdata.Tier1 == "Fast-NonTurbulent/Glide")])
        Area_Pct_by_CU_FT = inputdata.AreaTotal[(inputdata.Tier1 == "Fast-Turbulent")] / numpy.nansum(inputdata.AreaTotal[(inputdata.Tier1 == "Fast-Turbulent")])
        Area_Pct_by_CU_SlowPool = inputdata.AreaTotal[(inputdata.Tier1 == "Slow/Pool")] / numpy.nansum(inputdata.AreaTotal[(inputdata.Tier1 == "Slow/Pool")])
        Area_Pct_by_CU_SSC = inputdata.AreaTotal[(inputdata.Tier1 == "Small Side Channel")] / numpy.nansum(inputdata.AreaTotal[(inputdata.Tier1 == "Small Side Channel")])



        # Calculate each metric.
        #############################################################################################
        # Fich Cover Large Wood
        FishCovLW_by_CU = Area_Pct_by_CU * inputdata.WoodyDebrisFC
        FishCovLW = numpy.nansum(FishCovLW_by_CU)

        FishCovLW_by_CU_FNT = Area_Pct_by_CU_FNT * inputdata.WoodyDebrisFC[(inputdata.Tier1 == "Fast-NonTurbulent/Glide")]
        FishCovLW_FNT = numpy.nansum(FishCovLW_by_CU_FNT)

        FishCovLW_by_CU_FT = Area_Pct_by_CU_FT * inputdata.WoodyDebrisFC[(inputdata.Tier1 == "Fast-Turbulent")]
        FishCovLW_FT = numpy.nansum(FishCovLW_by_CU_FT)

        FishCovLW_by_CU_SlowPool = Area_Pct_by_CU_SlowPool * inputdata.WoodyDebrisFC[(inputdata.Tier1 == "Slow/Pool")]
        FishCovLW_SlowPool = numpy.nansum(FishCovLW_by_CU_SlowPool)

        FishCovLW_by_CU_SSC = Area_Pct_by_CU_SSC * inputdata.WoodyDebrisFC[(inputdata.Tier1 == "Small Side Channel")]
        FishCovLW_SSC = numpy.nansum(FishCovLW_by_CU_SSC)

    ############################################################################################
        # Fish Cover Total Veg
        FishCovTVeg_by_CU = Area_Pct_by_CU * inputdata.OverhangingVegetationFC
        FishCovTVeg = numpy.nansum(FishCovTVeg_by_CU)

        FishCovTVeg_by_CU_FNT = Area_Pct_by_CU_FNT * inputdata.OverhangingVegetationFC[(inputdata.Tier1 == "Fast-NonTurbulent/Glide")]
        FishCovTVeg_FNT = numpy.nansum(FishCovTVeg_by_CU_FNT)

        FishCovTVeg_by_CU_FT = Area_Pct_by_CU_FT * inputdata.OverhangingVegetationFC[(inputdata.Tier1 == "Fast-Turbulent")]
        FishCovTVeg_FT = numpy.nansum(FishCovTVeg_by_CU_FT)

        FishCovTVeg_by_CU_SlowPool = Area_Pct_by_CU_SlowPool * inputdata.OverhangingVegetationFC[(inputdata.Tier1 == "Slow/Pool")]
        FishCovTVeg_SlowPool = numpy.nansum(FishCovTVeg_by_CU_SlowPool)

        FishCovTVeg_by_CU_SSC = Area_Pct_by_CU_SSC * inputdata.OverhangingVegetationFC[(inputdata.Tier1 == "Small Side Channel")]
        FishCovTVeg_SSC = numpy.nansum(FishCovTVeg_by_CU_SSC)



        ##########################################################################################
        # Fish Cover Undercut

        FishCovUcut_by_CU = Area_Pct_by_CU * inputdata.UndercutBanksFC
        FishCovUcut = numpy.nansum(FishCovUcut_by_CU)

        FishCovUcut_by_CU_FNT = Area_Pct_by_CU_FNT * inputdata.UndercutBanksFC[(inputdata.Tier1 == "Fast-NonTurbulent/Glide")]
        FishCovUcut_FNT = numpy.nansum(FishCovUcut_by_CU_FNT)

        FishCovUcut_by_CU_FT = Area_Pct_by_CU_FT * inputdata.UndercutBanksFC[(inputdata.Tier1 == "Fast-Turbulent")]
        FishCovUcut_FT = numpy.nansum(FishCovUcut_by_CU_FT)

        FishCovUcut_by_CU_SlowPool = Area_Pct_by_CU_SlowPool * inputdata.UndercutBanksFC[(inputdata.Tier1 == "Slow/Pool")]
        FishCovUcut_SlowPool = numpy.nansum(FishCovUcut_by_CU_SlowPool)

        FishCovUcut_by_CU_SSC = Area_Pct_by_CU_SSC * inputdata.UndercutBanksFC[(inputdata.Tier1 == "Small Side Channel")]
        FishCovUcut_SSC = numpy.nansum(FishCovUcut_by_CU_SSC)


    ###########################################################################################
        # Fish Cover Artificial

        FishCovArt_by_CU = Area_Pct_by_CU * inputdata.ArtificialFC
        FishCovArt = numpy.nansum(FishCovArt_by_CU)

        FishCovArt_by_CU_FNT = Area_Pct_by_CU_FNT * inputdata.ArtificialFC[(inputdata.Tier1 == "Fast-NonTurbulent/Glide")]
        FishCovArt_FNT = numpy.nansum(FishCovArt_by_CU_FNT)

        FishCovArt_by_CU_FT = Area_Pct_by_CU_FT * inputdata.ArtificialFC[(inputdata.Tier1 == "Fast-Turbulent")]
        FishCovArt_FT = numpy.nansum(FishCovArt_by_CU_FT)

        FishCovArt_by_CU_SlowPool = Area_Pct_by_CU_SlowPool * inputdata.ArtificialFC[(inputdata.Tier1 == "Slow/Pool")]
        FishCovArt_SlowPool = numpy.nansum(FishCovArt_by_CU_SlowPool)

        FishCovArt_by_CU_SSC = Area_Pct_by_CU_SSC * inputdata.ArtificialFC[(inputdata.Tier1 == "Small Side Channel")]
        FishCovArt_SSC = numpy.nansum(FishCovArt_by_CU_SSC)



        ###########################################################################################
        # Fish Cover Aquatic Veg

        FishCovAqVeg_by_CU = Area_Pct_by_CU * inputdata.AquaticVegetationFC
        FishCovAqVeg = numpy.nansum(FishCovAqVeg_by_CU)

        FishCovAqVeg_by_CU_FNT = Area_Pct_by_CU_FNT * inputdata.AquaticVegetationFC[(inputdata.Tier1 == "Fast-NonTurbulent/Glide")]
        FishCovAqVeg_FNT = numpy.nansum(FishCovAqVeg_by_CU_FNT)

        FishCovAqVeg_by_CU_FT = Area_Pct_by_CU_FT * inputdata.AquaticVegetationFC[(inputdata.Tier1 == "Fast-Turbulent")]
        FishCovAqVeg_FT = numpy.nansum(FishCovAqVeg_by_CU_FT)

        FishCovAqVeg_by_CU_SlowPool = Area_Pct_by_CU_SlowPool * inputdata.AquaticVegetationFC[(inputdata.Tier1 == "Slow/Pool")]
        FishCovAqVeg_SlowPool = numpy.nansum(FishCovAqVeg_by_CU_SlowPool)

        FishCovAqVeg_by_CU_SSC = Area_Pct_by_CU_SSC * inputdata.AquaticVegetationFC[(inputdata.Tier1 == "Small Side Channel")]
        FishCovAqVeg_SSC = numpy.nansum(FishCovAqVeg_by_CU_SSC)



        ##########################################################################################
        # Fish Cover None

        FishCovNone_by_CU = Area_Pct_by_CU * inputdata.TotalNoFC
        FishCovNone = numpy.nansum(FishCovNone_by_CU)

        FishCovNone_by_CU_FNT = Area_Pct_by_CU_FNT * inputdata.TotalNoFC[(inputdata.Tier1 == "Fast-NonTurbulent/Glide")]
        FishCovNone_FNT = numpy.nansum(FishCovNone_by_CU_FNT)

        FishCovNone_by_CU_FT = Area_Pct_by_CU_FT * inputdata.TotalNoFC[(inputdata.Tier1 == "Fast-Turbulent")]
        FishCovNone_FT = numpy.nansum(FishCovNone_by_CU_FT)

        FishCovNone_by_CU_SlowPool = Area_Pct_by_CU_SlowPool * inputdata.TotalNoFC[(inputdata.Tier1 == "Slow/Pool")]
        FishCovNone_SlowPool = numpy.nansum(FishCovNone_by_CU_SlowPool)

        FishCovNone_by_CU_SSC = Area_Pct_by_CU_SSC * inputdata.TotalNoFC[(inputdata.Tier1 == "Small Side Channel")]
        FishCovNone_SSC = numpy.nansum(FishCovNone_by_CU_SSC)




    ##########################################################################################
        # Fish Cover Total
        FishCovTotal = numpy.nansum([FishCovLW,FishCovTVeg,FishCovUcut,FishCovArt,FishCovAqVeg])
        FishCovTotal_FNT = numpy.nansum([FishCovLW_FNT, FishCovTVeg_FNT, FishCovUcut_FNT, FishCovArt_FNT, FishCovAqVeg_FNT])
        FishCovTotal_FT = numpy.nansum([FishCovLW_FT, FishCovTVeg_FT, FishCovUcut_FT, FishCovArt_FT, FishCovAqVeg_FT])
        FishCovTotal_SlowPool = numpy.nansum([FishCovLW_SlowPool, FishCovTVeg_SlowPool, FishCovUcut_SlowPool, FishCovArt_SlowPool, FishCovAqVeg_SlowPool])
        FishCovTotal_SSC = numpy.nansum([FishCovLW_SSC, FishCovTVeg_SSC, FishCovUcut_SSC, FishCovArt_SSC, FishCovAqVeg_SSC])

        #print(FishCovTotal_SlowPool)



    returnlist = pd.Series([FishCovLW, FishCovTVeg, FishCovUcut, FishCovArt, FishCovAqVeg, FishCovNone, FishCovTotal,valid,
                               FishCovLW_FNT,FishCovLW_FT,FishCovLW_SlowPool,FishCovLW_SSC,
                                   FishCovTVeg_FNT, FishCovTVeg_FT, FishCovTVeg_SlowPool, FishCovTVeg_SSC,
                                       FishCovUcut_FNT, FishCovUcut_FT, FishCovUcut_SlowPool, FishCovUcut_SSC,
                                           FishCovArt_FNT, FishCovArt_FT, FishCovArt_SlowPool, FishCovArt_SSC,
                                               FishCovAqVeg_FNT, FishCovAqVeg_FT, FishCovAqVeg_SlowPool, FishCovAqVeg_SSC,
                                                   FishCovNone_FNT, FishCovNone_FT, FishCovNone_SlowPool, FishCovNone_SSC,
                                                       FishCovTotal_FNT, FishCovTotal_FT, FishCovTotal_SlowPool, FishCovTotal_SSC
                               ],
                                       index=['FishCovLW', 'FishCovTVeg', 'FishCovUcut', 'FishCovArt', 'FishCovAqVeg', 'FishCovNone', 'FishCovTotal','valid',
                                              'FishCovLW_FNT','FishCovLW_FT','FishCovLW_SlowPool','FishCovLW_SSC',
                                                  'FishCovTVeg_FNT', 'FishCovTVeg_FT', 'FishCovTVeg_SlowPool', 'FishCovTVeg_SSC',
                                                       'FishCovUcut_FNT', 'FishCovUcut_FT', 'FishCovUcut_SlowPool', 'FishCovUcut_SSC',
                                                          'FishCovArt_FNT', 'FishCovArt_FT', 'FishCovArt_SlowPool', 'FishCovArt_SSC',
                                                              'FishCovAqVeg_FNT', 'FishCovAqVeg_FT', 'FishCovAqVeg_SlowPool', 'FishCovAqVeg_SSC',
                                                                  'FishCovNone_FNT', 'FishCovNone_FT', 'FishCovNone_SlowPool', 'FishCovNone_SSC',
                                                                       'FishCovTotal_FNT', 'FishCovTotal_FT', 'FishCovTotal_SlowPool', 'FishCovTotal_SSC'])

    return(returnlist)

    ###########################################################################################################################################################
###############################################################################################################################################################
# __name__ is a specifal variable that gets set when you run this file directly
if __name__ == "__main__":

    print(os.listdir(os.getcwd()))

    res = pd.DataFrame(columns=('VisitID', 'FishCovLW', 'FishCovTVeg', 'FishCovUcut', 'FishCovArt', 'FishCovAqVeg', 'FishCovNone', 'FishCovTotal','valid',
                                       'FishCovLW_FNT','FishCovLW_FT','FishCovLW_SlowPool','FishCovLW_SSC',
                                            'FishCovTVeg_FNT', 'FishCovTVeg_FT', 'FishCovTVeg_SlowPool', 'FishCovTVeg_SSC',
                                                 'FishCovUcut_FNT', 'FishCovUcut_FT', 'FishCovUcut_SlowPool', 'FishCovUcut_SSC',
                                                     'FishCovArt_FNT', 'FishCovArt_FT', 'FishCovArt_SlowPool', 'FishCovArt_SSC',
                                                         'FishCovAqVeg_FNT', 'FishCovAqVeg_FT', 'FishCovAqVeg_SlowPool', 'FishCovAqVeg_SSC',
                                                             'FishCovNone_FNT', 'FishCovNone_FT', 'FishCovNone_SlowPool', 'FishCovNone_SSC',
                                                                  'FishCovTotal_FNT', 'FishCovTotal_FT', 'FishCovTotal_SlowPool', 'FishCovTotal_SSC'))
    counter = 0

    VisitID = 2015
   # VisitID = 1770
    #VisitID = 5

    print(VisitID)
    inputdata_all=pd.read_csv('FishCover.csv')
    cusummary_all=pd.read_csv('ChannelUnitSummary.csv')
    cudata_all=pd.read_csv('ChannelUnit.csv')

    #cudata=pd.read_csv('ChannelUnitSummary.csv')

    VisitIDs = inputdata_all.VisitID
    VisitIDs = numpy.unique(VisitIDs)
    #VisitIDs = VisitIDs[0:100]
    #VisitIDs = [4]
    for VisitID in VisitIDs:
        print(VisitID)


        #data = data[(D_data.SubstrateSizeClass != "1448 - 2048mm")]
        inputdata = inputdata_all[(inputdata_all.VisitID == VisitID)]
        cudata = cudata_all[(cudata_all.VisitID == VisitID)]
        cusummary = cusummary_all[(cusummary_all.VisitID == VisitID)]
        cudata = cudata.reset_index(drop=True)
        inputdata = inputdata.reset_index(drop=True)

        print(len(cudata))
        print(len(cusummary))
        print(len(inputdata))

        if ((len(cudata)>0 and len(cusummary)>0) and len(inputdata)>0):
            print("AOK")

            results = Fish_Cover_Function(inputdata, cusummary, cudata)
            print(results)
            res.set_value(counter, 'VisitID', VisitID)
            res.set_value(counter, ['FishCovLW', 'FishCovTVeg', 'FishCovUcut', 'FishCovArt', 'FishCovAqVeg', 'FishCovNone', 'FishCovTotal','valid',
                                           'FishCovLW_FNT','FishCovLW_FT','FishCovLW_SlowPool','FishCovLW_SSC',
                                                'FishCovTVeg_FNT', 'FishCovTVeg_FT', 'FishCovTVeg_SlowPool', 'FishCovTVeg_SSC',
                                                     'FishCovUcut_FNT', 'FishCovUcut_FT', 'FishCovUcut_SlowPool', 'FishCovUcut_SSC',
                                                         'FishCovArt_FNT', 'FishCovArt_FT', 'FishCovArt_SlowPool', 'FishCovArt_SSC',
                                                             'FishCovAqVeg_FNT', 'FishCovAqVeg_FT', 'FishCovAqVeg_SlowPool', 'FishCovAqVeg_SSC',
                                                                 'FishCovNone_FNT', 'FishCovNone_FT', 'FishCovNone_SlowPool', 'FishCovNone_SSC',
                                                                      'FishCovTotal_FNT', 'FishCovTotal_FT', 'FishCovTotal_SlowPool', 'FishCovTotal_SSC'], results)

            counter = counter+1

    print "Done"

    print(res)
    res.to_csv('FishCover_Val.csv')