import numpy
import pandas as pd
import os

def Riparian_Cover_Function(inputdata):
    print("calculating riparian cover metrics")

    # RipCovBigTree
    RipCovBigTree = numpy.mean([inputdata.LBCanopyBigTreesGT30CmDBH, inputdata.RBCanopyBigTreesGT30CmDBH])
    print(RipCovBigTree)

    #LB = tapply((Vdata$LBCanopyWoodyConiferous + Vdata$LBUnderstoryWoodyConiferous), Vdata$TransectID, sum)
    #RB = tapply((Vdata$RBCanopyWoodyConiferous + Vdata$RBUnderstoryWoodyConiferous), Vdata$TransectID, sum)
    #RipCovConif[i] = mean(c(LB, RB))

    # RipCovConif
    # substitute for 'tapply' in R
    grouped = inputdata.groupby('TransectID')
    temp = grouped.sum()
    LB = temp.LBCanopyWoodyConiferous + temp.LBUnderstoryWoodyConiferous
    RB = temp.RBCanopyWoodyConiferous + temp.RBUnderstoryWoodyConiferous
    RipCovConif = numpy.mean([LB, RB])
    print(RipCovConif)

    # RipCovGrnd
    RipCovGrnd = numpy.mean([(inputdata.LBGroundcoverWoodyShrubs + inputdata.LBGroundcoverNonWoodyShrubs),
                             (inputdata.RBGroundcoverWoodyShrubs + inputdata.RBGroundcoverNonWoodyShrubs)])
    print(RipCovGrnd)

    # RipCovNonWood
    RipCovNonWood = numpy.mean([(inputdata.LBUnderstoryNonWoodyShrubs + inputdata.LBGroundcoverNonWoodyShrubs),
                                (inputdata.RBUnderstoryNonWoodyShrubs + inputdata.RBGroundcoverNonWoodyShrubs)])
    print(RipCovNonWood)

    RipCovUstory = numpy.mean([(inputdata.LBUnderstoryWoodyShrubs + inputdata.LBUnderstoryNonWoodyShrubs),
                                (inputdata.RBUnderstoryWoodyShrubs + inputdata.RBUnderstoryNonWoodyShrubs)])

    RipCovWood = numpy.mean([(inputdata.LBCanopyBigTreesGT30CmDBH + inputdata.LBCanopySmallTreesLT30CmDBH
                                + inputdata.LBUnderstoryWoodyShrubs + inputdata.LBGroundcoverWoodyShrubs),
                                (inputdata.RBCanopyBigTreesGT30CmDBH + inputdata.RBCanopySmallTreesLT30CmDBH
                                + inputdata.RBUnderstoryWoodyShrubs + inputdata.RBGroundcoverWoodyShrubs)])

    # Doesn't work for 2011 data.  No documentation on how this was calculated then.
    RipCovCanNone = 100 - numpy.mean([(inputdata.LBCanopyWoodyConiferous + inputdata.LBCanopyWoodyDeciduous +
                                inputdata.LBCanopyWoodyBroadleafEvergreen + inputdata.LBCanopyStandingDeadVegetation),
                                (inputdata.RBCanopyWoodyConiferous + inputdata.RBCanopyWoodyDeciduous +
                                inputdata.RBCanopyWoodyBroadleafEvergreen + inputdata.RBCanopyStandingDeadVegetation)])

    #returnlist = pd.Series([D16, D50, D84], index=['SubD16', 'SubD50', 'SubD84'])

    returnlist = pd.Series([RipCovBigTree, RipCovConif, RipCovGrnd, RipCovNonWood,RipCovUstory, RipCovWood, RipCovCanNone],
                           index=['RipCovBigTree', 'RipCovConif', 'RipCovGrnd', 'RipCovNonWood','RipCovUstory', 'RipCovWood', 'RipCovCanNone'])
    return(returnlist)


    print("all done")


# __name__ is a specifal variable that gets set when you run this file directly
if __name__ == "__main__":

    #VisitID = 1
    #VisitID = 2608
    VisitID = 2505

    inputdata=pd.read_csv('RiparianStructure.csv')

    inputdata = inputdata[(inputdata.VisitID == VisitID)]
    inputdata = inputdata.reset_index(drop=True)
    results=Riparian_Cover_Function(inputdata)
    print(results)
    #print(inputdata)
