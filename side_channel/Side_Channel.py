# Undercut Metrics Function
import numpy
import pandas as pd

def SideChannel_Function(inputdata):
    print('calculating undercut metrics')

    SC_Area = numpy.nan
    SC_Area_Pct = numpy.nan

    ssc = inputdata[(inputdata.SegmentType == "Small Side Channel")]
    area = ssc.SideChannelLength * ssc.SideChannelWidth
    SC_Area = sum(area)
    #SC_Area_PCT = SC_Area / (?????? what's the denominator here ????')

    returnlist = pd.Series([SC_Area, SC_Area_Pct],
                            index = ['SC_Area', 'SC_Area_Pct'])

    return(returnlist)


# __name__ is a specifal variable that gets set when you run this file directly
if __name__ == "__main__":

    res = pd.DataFrame(columns=('VisitID','SC_Area', 'SC_Area_Pct'))
    inputdata_all=pd.read_csv('ChannelSegment.csv')

    VisitIDs = inputdata_all.VisitID
    VisitIDs = numpy.unique(VisitIDs)
    # VisitIDs = VisitIDs[0:100]
    VisitIDs = [3422]

    counter = 0
    for VisitID in VisitIDs:
        print(VisitID)

        #data = data[(D_data.SubstrateSizeClass != "1448 - 2048mm")]
        inputdata = inputdata_all[(inputdata_all.VisitID == VisitID)]
        inputdata = inputdata.reset_index(drop=True)


        results = SideChannel_Function(inputdata)
        print(results)
        res.set_value(counter, 'VisitID', VisitID)
        res.set_value(counter, ['SC_Area', 'SC_Area_Pct'], results)
        counter = counter + 1
        #print(results)


        print(res)

    res.to_csv('SideChannel_Val.csv')