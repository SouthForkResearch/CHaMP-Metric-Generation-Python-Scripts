# Generally try to put imports at the top of a file
import math

# ###############################################################################
# Start function here... D_data will be argument passed to function
def D16_D50_D84(D_data):


    data  = D_data[(D_data.SubstrateSizeClass != ">4000mm")]
    data  = data[(D_data.SubstrateSizeClass !="1448 - 2048mm")]
    data  = data[(D_data.SubstrateSizeClass !="2048 - 2896mm")]
    data  = data[(D_data.SubstrateSizeClass != "2896 - 4000mm")]
    data  = data[(D_data.SubstrateSizeClass != "512 - 724mm")]
    data  = data[(D_data.SubstrateSizeClass != "724 - 1024mm")]
    data  = data[(D_data.SubstrateSizeClass != "1024 - 1448mm")]
    data  = data[(D_data.SubstrateSizeClass != "Bedrock")]
    data = data[(data.Tier1 != "Slow/Pool")]
    data = data[(data.SubstrateSizeClass != "")]
    # TODO: istead of using print state meants try dropping a breakpoint on this line
    # You can then inspect the contents of the variables directly
    # print(data)

    data.SubstrateSizeClass

    UL=[]
    LL=[]

    for str in data.SubstrateSizeClass:
        # print(str)
        if str == ">510":
            UL.append(510.1)
            LL.append(510.0)
        else:
            if str == ">4000mm":
                UL.append(4001)
                LL.append(4000)
            else:
                left =(str.index("-"))+2
                right=(str.index("m"))
                #print(str[left:right])
                UL.append(str[left:right])
                right =(str.index("-"))-1
                LL.append(str[0:right])

    #print(data.SubstrateSizeClass)
    #print(UL)
    #print(LL)

    fUL = []
    for val in UL:
        #print(val)
        fUL.append(float(val))

    fLL = []
    for val in LL:
        fLL.append(float(val))

    sUL=sorted(fUL)
    sLL=sorted(fLL)

    lnUL = []
    for value in sUL:
        val= float(value)
        val = math.log(val)
        lnUL.append(val)

    lnLL = []
    for value in sLL:
        val= float(value)
        val = math.log(val)
        lnLL.append(val)


    #val = .222

    # extract the levels for the log lower limits and log upper limits...
    levelsLL = []
    for val in lnLL:
        if (val in levelsLL) == False:
            levelsLL.append(val)

    levelsUL = []
    for val in lnUL:
        if (val in levelsUL) == False:
            levelsUL.append(val)

    n_per_level = []

    for val in levelsLL:
          count = 0
          for val2 in lnLL:
              if val2 == val:
                  count = count + 1
          n_per_level.append(count)

    #lnLL
    #levelsLL
    #n_per_level


    ln_interp = []
    for i in range(0,len(levelsLL)):
        low = levelsLL[i]
        hi = levelsUL[i]
        n = n_per_level[i]
        for j in range(0,n):
            val = low + j*(hi-low)/n
            ln_interp.append(val)

    #lnLL
    #ln_interp


    idx_exact = (0.16 * len(ln_interp))
    idx = int(math.floor((0.16 * len(ln_interp))))
    lD16 = ln_interp[idx] + (ln_interp[idx+1]-ln_interp[idx])* (idx_exact-idx)/1
    D16=math.exp(lD16)
    #print(D16)


    idx_exact = (0.5 * len(ln_interp))
    idx = int(math.floor((0.5 * len(ln_interp))))
    lD50 = ln_interp[idx] + (ln_interp[idx+1]-ln_interp[idx])* (idx_exact-idx)/1
    D50=math.exp(lD50)
    #print(D50)

    idx_exact = (0.84 * len(ln_interp))
    idx = int(math.floor((0.84 * len(ln_interp))))
    lD84 = ln_interp[idx] + (ln_interp[idx+1]-ln_interp[idx])* (idx_exact-idx)/1
    D84=math.exp(lD84)
    #print(D84)

    #print("end of function")
    returnlist = pd.Series([D16, D50, D84], index=['SubD16', 'SubD50', 'SubD84'])

    return(returnlist)


# __name__ is a special variable that gets set when you run this file directly
if __name__ == "__main__":
    import pandas as pd
    D16_D50_D84_Input_Data = pd.read_csv('test.csv')
    results = D16_D50_D84(D16_D50_D84_Input_Data)
    print(results)