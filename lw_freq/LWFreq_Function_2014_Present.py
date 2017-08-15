# Large Wood Frequency  - for 2014 and newer input data (method and input data is different for 2011-2013 data)
import numpy
import pandas as pd

def LWFreq_Function_2014_Present(inputdata, Lgth_Wet):
    print('calculating LWF')

    # Split into wet and dry components
    LWD_Dry = inputdata[(inputdata.LargeWoodType == "Dry")]
    LWD_Wet = inputdata[(inputdata.LargeWoodType == "Wet")]

    # There is one row of data for each VisitID, so the number of rows equals
    # the number of pieces of large wood.
    LWD_Dry_sum = len(LWD_Dry)
    LWD_Wet_sum = len(LWD_Wet)

    # Results aren't rounded, despite what the documentation says.
    # Also, wetted site length is used as the denominator, even though the documentation says to use BF.
    LWFreq_Wet = 100 * LWD_Wet_sum / Lgth_Wet
    LWFreq_Bf = 100 * ((LWD_Dry_sum + LWD_Wet_sum) / Lgth_Wet)

    # NA values (no rows of data) should be zero LW
    if len(inputdata)==0:
        LWFreq_Wet = 0
        LWFreq_Bf = 0


    returnlist = pd.Series([LWFreq_Wet, LWFreq_Bf], index=['LWFreq_Wet', 'LWFreq_Bf'])
    return(returnlist)

    print('All Done!')

# __name__ is a special variable that gets set when you run this file directly
if __name__ == "__main__":

    #VisitID = 1
    VisitID = 2608
    #VisitID = 2505

    res = pd.DataFrame(columns=('VisitID', 'LWFreq_Wet', 'LWFreq_Bf'))
    counter = 0

    inputdata_all = pd.read_csv('LargeWoodPiece.csv')
    MVI_all = pd.read_csv('MetricVisitInformation.csv')

    VisitIDs = inputdata_all.VisitID
    VisitIDs = numpy.unique(VisitIDs)
    #VisitIDs = VisitIDs[0:100]

    for VisitID in VisitIDs:
        print(VisitID)

        # data = data[(D_data.SubstrateSizeClass != "1448 - 2048mm")]
        inputdata = inputdata_all[(inputdata_all.VisitID == VisitID)]
        inputdata = inputdata.reset_index(drop=True)
        MVI = MVI_all[(MVI_all.VisitID == VisitID)]

        results = LWFreq_Function_2014_Present(inputdata, float(MVI.Lgth_Wet))
        print(results)
        res.set_value(counter, 'VisitID', VisitID)
        res.set_value(counter, ['LWFreq_Wet', 'LWFreq_Bf'], results)
        counter = counter+1

    res.to_csv('LWFreq_2014_2016_Val.csv')