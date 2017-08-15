# Large Wood Frequency  - for 2011 - 2013 input data (method and input data is different for 2014+)
import numpy
import pandas as pd

def LWFreq_Function_2011_2013(inputdata, Lgth_Wet):
    print('calculating LWF')

    # Split into wet and dry components
    LWD_Dry = inputdata[(inputdata.LargeWoodType == "Dry")]
    LWD_Wet = inputdata[(inputdata.LargeWoodType == "Wet")]

    # Pull total number of LW pieces from the total column.
    LWD_Dry_sum = sum(LWD_Dry.SumLWDCount)
    LWD_Wet_sum = sum(LWD_Wet.SumLWDCount)

    # Documentation says to round off, actual results are not rounded off.
    LWFreq_Wet = 100 * LWD_Wet_sum / Lgth_Wet
    LWFreq_Bf = 100 * ((LWD_Dry_sum + LWD_Wet_sum) / Lgth_Wet)

    returnlist = pd.Series([LWFreq_Wet, LWFreq_Bf], index=['LWFreq_Wet', 'LWFreq_Bf'])
    return(returnlist)

    print('All Done!')

# __name__ is a special variable that gets set when you run this file directly
if __name__ == "__main__":

    #VisitID = 1
    #VisitID = 10
    VisitID = 1098
    #VisitID = 2608
    #VisitID = 2505


    res = pd.DataFrame(columns=('VisitID','LWFreq_Wet', 'LWFreq_Bf' ))
    counter = 0

    inputdata_all = pd.read_csv('LargeWoodyDebris.csv')
    MVI_all = pd.read_csv('MetricVisitInformation.csv')

    VisitIDs = inputdata_all.VisitID
    VisitIDs = numpy.unique(VisitIDs)
    #VisitIDs = VisitIDs[0:100]

    #VisitIDs = [4]
    for VisitID in VisitIDs:
        print(VisitID)

      # data = data[(D_data.SubstrateSizeClass != "1448 - 2048mm")]
        inputdata = inputdata_all[(inputdata_all.VisitID == VisitID)]
        inputdata = inputdata.reset_index(drop=True)
        MVI = MVI_all[(MVI_all.VisitID == VisitID)]

        results = LWFreq_Function_2011_2013(inputdata, float(MVI.Lgth_Wet))
        print(results)

        res.set_value(counter, 'VisitID', VisitID)
        res.set_value(counter, ['LWFreq_Wet', 'LWFreq_Bf'], results)
        counter = counter+1

    res.to_csv('LWFreq_2011_2013_Val.csv')