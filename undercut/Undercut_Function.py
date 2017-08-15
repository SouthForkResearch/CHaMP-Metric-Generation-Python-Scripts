# Undercut Metrics Function
import numpy
import pandas as pd

def Undercut_Function(inputdata, Lgth_Wet, Area_Wet):
    print('calculating undercut metrics')

    Ucut_Lgth = numpy.nansum(inputdata.EstimatedLength)
    # AverageWidth isn't available via api call, so calculate it from Width25, Width50, Width75
    AverageWidth= 1.0/3.0 * (inputdata.Width25+inputdata.Width50+inputdata.Width75)
    #Ucut_Area = numpy.nansum(inputdata.AverageWidth * inputdata.EstimatedLength)
    Ucut_Area = numpy.nansum(AverageWidth * inputdata.EstimatedLength)

    # Ucut_Lgth_Pct is divided by two, I assume to acct for stream left and stream right
    UcutLgth_Pct = Ucut_Lgth / Lgth_Wet * 100 / 2
    UcutArea_Pct = Ucut_Area / Area_Wet * 100

    if len(inputdata) == 0:
        Ucut_Lgth = numpy.nan
        UcutLgth_Pct = numpy.nan
        Ucut_Area = numpy.nan
        UcutArea_Pct = numpy.nan

    returnlist = pd.Series([Ucut_Lgth, UcutLgth_Pct,Ucut_Area, UcutArea_Pct],
                            index = ['Ucut_Lgth', 'UcutLgth_Pct','Ucut_Area', 'UcutArea_Pct'])

    return(returnlist)


# __name__ is a specifal variable that gets set when you run this file directly
if __name__ == "__main__":

    res = pd.DataFrame(columns=('VisitID','Ucut_Lgth', 'UcutLgth_Pct','Ucut_Area', 'UcutArea_Pct'))

    #VisitID = 1
    #xzVisitID = 2608
    VisitID = 2505
    print(VisitID)
    inputdata_all=pd.read_csv('UndercutBank.csv')
    MVI_all = pd.read_csv('MetricVisitInformation.csv')

    VisitIDs = inputdata_all.VisitID
    VisitIDs = numpy.unique(VisitIDs)
    # VisitIDs = VisitIDs[0:100]
    # VisitIDs = [2020]

    counter = 0
    for VisitID in VisitIDs:
        print(VisitID)

        #data = data[(D_data.SubstrateSizeClass != "1448 - 2048mm")]
        inputdata = inputdata_all[(inputdata_all.VisitID == VisitID)]
        inputdata = inputdata.reset_index(drop=True)
        MVI = MVI_all[(MVI_all.VisitID == VisitID)]

        #print(float(MVI.Lgth_Wet))
        #print(float(MVI.Area_Wet))

        results = Undercut_Function(inputdata, float(MVI.Lgth_Wet), float(MVI.Area_Wet))

        res.set_value(counter, 'VisitID', VisitID)
        res.set_value(counter, ['Ucut_Lgth', 'UcutLgth_Pct','Ucut_Area', 'UcutArea_Pct'], results)
        counter = counter + 1
        #print(results)


        #print(res)

    res.to_csv('Undercut_Val.csv')