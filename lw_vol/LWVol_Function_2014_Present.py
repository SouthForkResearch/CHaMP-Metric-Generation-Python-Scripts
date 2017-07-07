# Large Wood Volum  - for 2014 and newer input data (method and input data is different for 2011-2013 data)
import numpy
import pandas as pd

def LWVol_Function_2014_Present(inputdata, cudata):
    print('calculating LWF')

    def volume(diameter, length):
        volume = 3.14159 * sum((0.5 * diameter) ** 2 * length)
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




    # Split into wet and dry components
    LWD_Dry = inputdata[(inputdata.LargeWoodType == "Dry")]
    LWD_Wet = inputdata[(inputdata.LargeWoodType == "Wet")]

    #LWVol_Dry = 3.14159 * sum((0.5 * LWD_Dry.Diameter) ** 2 * LWD_Dry.Length)
    #LWVol_Wet = 3.14159 * sum((0.5 * LWD_Wet.Diameter) ** 2 * LWD_Wet.Length)
    LWVol_Dry = volume(LWD_Dry.Diameter, LWD_Dry.Length)
    LWVol_Wet = volume(LWD_Wet.Diameter, LWD_Wet.Length)
    LWVol_Bf = LWVol_Wet + LWVol_Dry


    # for Tier1 metrics, assign Temp for various Tier1 groups

    # Fast NonTurbulent
    Temp_Dry = LWD_Dry[(LWD_Dry.Tier1 == "Fast-NonTurbulent/Glide")]
    Temp_Wet = LWD_Wet[(LWD_Wet.Tier1 == "Fast-NonTurbulent/Glide")]
    LWVol_DryFstNT = volume(Temp_Dry.Diameter, Temp_Dry.Length)
    LWVol_WetFstNT = volume(Temp_Wet.Diameter, Temp_Wet.Length)
    LWVol_BfFstNT = LWVol_DryFstNT + LWVol_WetFstNT

    # Fast NonTurbulent
    Temp_Dry = LWD_Dry[(LWD_Dry.Tier1 == "Fast-Turbulent")]
    Temp_Wet = LWD_Wet[(LWD_Wet.Tier1 == "Fast-Turbulent")]
    LWVol_DryFstTurb = volume(Temp_Dry.Diameter, Temp_Dry.Length)
    LWVol_WetFstTurb = volume(Temp_Wet.Diameter, Temp_Wet.Length)
    LWVol_BfFstTurb = LWVol_DryFstTurb + LWVol_WetFstTurb


    # Slow/Pool
    Temp_Dry = LWD_Dry[(LWD_Dry.Tier1 == "Slow/Pool")]
    Temp_Wet = LWD_Wet[(LWD_Wet.Tier1 == "Slow/Pool")]
    LWVol_DrySlow = volume(Temp_Dry.Diameter, Temp_Dry.Length)
    LWVol_WetSlow = volume(Temp_Wet.Diameter, Temp_Wet.Length)
    LWVol_BfSlow =  LWVol_DrySlow+ LWVol_WetSlow

    #print(cudata)

    returnlist = pd.Series([LWVol_Wet,LWVol_Bf, LWVol_WetFstNT,LWVol_BfFstNT, LWVol_WetFstTurb,LWVol_BfFstTurb,LWVol_WetSlow,LWVol_BfSlow],
                           index = ['LWVol_Wet','LWVol_Bf','WetFstNT','LWVol_BfFstNT','LWVol_WetFstTurb','LWVol_BfFstTurb','LWVol_WetSlow','LWVol_BfSlow'])
    return(returnlist)

    #print('All Done!')





# __name__ is a special variable that gets set when you run this file directly
if __name__ == "__main__":

    #VisitID = 1
    VisitID = 2608
    #VisitID = 2505

    inputdata = pd.read_csv('LargeWoodPiece.csv')

    inputdata = inputdata[(inputdata.VisitID == VisitID)]
    inputdata = inputdata.reset_index(drop=True)

    # read in the channel unit data
    cudata = pd.read_csv('ChannelUnit.csv')
    cudata = cudata[(cudata.VisitID == VisitID)]
    cudata = cudata.reset_index(drop=True)
    #
    #MVI = pd.read_csv('MetricVisitInformation.csv')
    #MVI = MVI[(MVI.VisitID == VisitID)]

    results = LWVol_Function_2014_Present(inputdata, cudata)
    print(results)
