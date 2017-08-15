# Large Wood Volum  - for 2014 and newer input data (method and input data is different for 2011-2013 data)
import numpy
import pandas as pd

def LWVol_Function_2011_2013(inputdata, cudata):
    print('calculating LWF')

    def volume(LWVol):
        v1 = numpy.nansum(LWVol.SmallSmall * 0.02035)
        v2 = numpy.nansum(LWVol.SmallMedium * 0.04878)
        v3 = numpy.nansum(LWVol.SmallLarge * 0.10758)
        v4 = numpy.nansum(LWVol.MediumSmall * 0.05981)
        v5 = numpy.nansum(LWVol.MediumMedium * 0.15101)
        v6 = numpy.nansum(LWVol.MediumLarge * 0.40012)
        v7 = numpy.nansum(LWVol.LargeSmall * 0.22887)
        v8 = numpy.nansum(LWVol.LargeMedium * 0.57739)
        v9 = numpy.nansum(LWVol.LargeLarge * 1.72582)
        v10 = numpy.nansum(LWVol.SmallMidLarge * 0.10470)
        v11 = numpy.nansum(LWVol.SmallExtraLarge * 0.23794)
        v12 = numpy.nansum(LWVol.MediumMidLarge * 0.33875)
        v13 = numpy.nansum(LWVol.MediumExtraLarge * 0.82393)
        v14 = numpy.nansum(LWVol.MidLargeSmall * 0.21187)
        v15 = numpy.nansum(LWVol.MidLargeMedium * 0.51680)
        v16 = numpy.nansum(LWVol.MidLargeMidLarge * 1.12232)
        v17 = numpy.nansum(LWVol.MidLargeExtraLarge * 2.71169)
        v18 = numpy.nansum(LWVol.ExtraLargeSmall * 0.84320)
        v19 = numpy.nansum(LWVol.ExtraLargeMedium * 1.89000)
        v20 = numpy.nansum(LWVol.ExtraLargeMidLarge * 3.82249)
        v21 = numpy.nansum(LWVol.ExtraLargeExtraLarge * 10.54683)
        volume = numpy.nansum([v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15,v16,v17,v18,v19,v20,v21])

        #print(volume)
        return(volume)



    ########################################################################################
    # Match Tier1 using Channel Unit ID.
    # When I first tried to do this, it kept changing hte string "Tier1" into some weird data object that I couldn't use later.
    # So I had to create an index and subset the data, force that index to be an integer, then use that to assign Tier1 into inputdata

    # I need to make sure my indices go from zero to length...
    cudata = cudata.reset_index(drop=True)
    Tier1 = []
    cudata['idx']= list(range(len(cudata)))

    for CID in inputdata.ChannelUnitID:
       temp=cudata[(cudata.ChannelUnitID == CID)]
       Tier1.append(cudata.Tier1[int(temp.idx)])
    #print(Tier1)
    inputdata['Tier1']=Tier1

    #######################################################################################

    # Split into wet and dry parts for the different metrics.
    LWD_Dry = inputdata[(inputdata.LargeWoodType == "Dry")]
    LWD_Wet = inputdata[(inputdata.LargeWoodType == "Wet")]

    LWVol_Dry = volume(LWD_Dry)
    LWVol_Wet = volume(LWD_Wet)
    LWVol_Bf = LWVol_Dry + LWVol_Wet

    # for Tier1 metrics, assign Temp for various Tier1 groups

    # Fast NonTurbulent
    Temp_Dry = LWD_Dry[(LWD_Dry.Tier1 == "Fast-NonTurbulent/Glide")]
    Temp_Wet = LWD_Wet[(LWD_Wet.Tier1 == "Fast-NonTurbulent/Glide")]
    LWVol_DryFstNT = volume(Temp_Dry)
    LWVol_WetFstNT = volume(Temp_Wet)
    LWVol_BfFstNT = LWVol_DryFstNT + LWVol_WetFstNT

    # Fast NonTurbulent
    Temp_Dry = LWD_Dry[(LWD_Dry.Tier1 == "Fast-Turbulent")]
    Temp_Wet = LWD_Wet[(LWD_Wet.Tier1 == "Fast-Turbulent")]
    LWVol_DryFstTurb = volume(Temp_Dry)
    LWVol_WetFstTurb = volume(Temp_Wet)
    LWVol_BfFstTurb = LWVol_DryFstTurb + LWVol_WetFstTurb

    # Slow/Pool
    Temp_Dry = LWD_Dry[(LWD_Dry.Tier1 == "Slow/Pool")]
    Temp_Wet = LWD_Wet[(LWD_Wet.Tier1 == "Slow/Pool")]
    LWVol_DrySlow = volume(Temp_Dry)
    LWVol_WetSlow = volume(Temp_Wet)
    LWVol_BfSlow = LWVol_DrySlow + LWVol_WetSlow

    # Small Side Channel
    Temp_Dry = LWD_Dry[(LWD_Dry.Tier1 == "Small Side Channel")]
    Temp_Wet = LWD_Wet[(LWD_Wet.Tier1 == "Small Side Channel")]
    LWVol_Dry_SSC = volume(Temp_Dry)
    LWVol_Wet_SSC = volume(Temp_Wet)
    LWVol_Bf_SSC = LWVol_Dry_SSC + LWVol_Wet_SSC


    returnlist = pd.Series([LWVol_Wet,LWVol_Bf, LWVol_WetFstNT,LWVol_BfFstNT, LWVol_WetFstTurb,LWVol_BfFstTurb,LWVol_WetSlow,LWVol_BfSlow,LWVol_Wet_SSC,LWVol_Bf_SSC],
                           index = ['LWVol_Wet','LWVol_Bf','LWVol_WetFstNT','LWVol_BfFstNT','LWVol_WetFstTurb','LWVol_BfFstTurb','LWVol_WetSlow','LWVol_BfSlow','LWVol_Wet_SSC','LWVol_Bf_SSC'])

    return(returnlist)


# __name__ is a special variable that gets set when you run this file directly
if __name__ == "__main__":

    VisitID = 1
    #VisitID = 10
    #VisitID = 1098

    inputdata = pd.read_csv('LargeWoodyDebris.csv')
    inputdata = inputdata[(inputdata.VisitID == VisitID)]
    inputdata = inputdata.reset_index(drop=True)

    # read in the channel unit data
    cudata = pd.read_csv('ChannelUnit.csv')
    cudata = cudata[(cudata.VisitID == VisitID)]
    cudata = cudata.reset_index(drop=True)
    #
    #MVI = pd.read_csv('MetricVisitInformation.csv')
    #MVI = MVI[(MVI.VisitID == VisitID)]

    results = LWVol_Function_2011_2013(inputdata, cudata)
    print(results)

