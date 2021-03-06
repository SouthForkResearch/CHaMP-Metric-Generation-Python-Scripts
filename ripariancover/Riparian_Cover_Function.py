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

    # Enter a visit ID to test the algorithm
    #VisitID = 1

    res = pd.DataFrame(columns=('VisitID','RipCovBigTree', 'RipCovConif', 'RipCovGrnd', 'RipCovNonWood','RipCovUstory', 'RipCovWood', 'RipCovCanNone'))

    VisitID = 2608
    idx = 0
    #VisitID = 2505

    inputdata_all=pd.read_csv('RiparianStructure.csv')

    VisitIDs = inputdata_all.VisitID
    VisitIDs = numpy.unique(VisitIDs)
    print(VisitIDs)
    #VisitIDs = VisitIDs[0:3]
    print(VisitIDs)

    print(VisitIDs)
    for VisitID in VisitIDs:
        print(VisitID)
        inputdata = inputdata_all[(inputdata_all.VisitID == VisitID)]
        inputdata = inputdata.reset_index(drop=True)
        results=Riparian_Cover_Function(inputdata)
    #res.append(results, index='RipCovBigTree', 'RipCovConif', 'RipCovGrnd', 'RipCovNonWood','RipCovUstory', 'RipCovWood', 'RipCovCanNone')
    #res.set_value(0, 'RipCovBigTree', 10)
    #res.set_value(0, ['RipCovBigTree', 'RipCovConif', 'RipCovGrnd', 'RipCovNonWood','RipCovUstory', 'RipCovWood', 'RipCovCanNone'],[1,2,3,4,5,6,7])
        res.set_value(idx, 'VisitID', VisitID)
        res.set_value(idx, ['RipCovBigTree', 'RipCovConif', 'RipCovGrnd', 'RipCovNonWood','RipCovUstory', 'RipCovWood', 'RipCovCanNone'],results)

        idx = idx+1
    #res.append([1,2,3,4,5,6,7], columns=['RipCovBigTree', 'RipCovConif', 'RipCovGrnd', 'RipCovNonWood','RipCovUstory', 'RipCovWood', 'RipCovCanNone'])
    print(results[1])
    print(res)
    res.to_csv('RiparianCover.csv')
    #res = res.set_value(results[1], results[2], results[3],results[4],results[5], results[6],results[7])
    print(results)

