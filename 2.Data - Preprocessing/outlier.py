class univariate():
    def QuanQual(dataset):
        Quan=[]
        Qual=[]
        for columnName in dataset.columns:
            #print(columnName)
            if(dataset[columnName].dtype=='O'):
                #print("Qual")
                Qual.append(columnName)
            else:
                #print("Quan")
                Quan.append(columnName)
        return Quan,Qual
    
def freqtable(columnName,dataset):
    freqtable=pd.DataFrame(columns=["unique_values","Frequency","Relative_Frequency","cumsum"])
    freqtable["unique_values"]=dataset[columnName].value_counts().index
    freqtable["Frequency"]=dataset[columnName].value_counts().values
    freqtable["Relative_Frequency"]=(freqtable["Frequency"]/103)
    freqtable["cumsum"]=freqtable["Relative_Frequency"].cumsum()
    return freqtable
def univariate(dataset,Quan):
    descriptive=pd.DataFrame(index=["Mean","Median","Mode","Q1:25%","Q2:50%","Q3:75%","99%","Q4:100%","IQR","1.5RULE","LESSER","GREATER","MIN","MAX","kurtosis","skew"],columns=Quan)
    for columnName in Quan:
        descriptive[columnName]["Mean"]=dataset[columnName].mean()
        descriptive[columnName]["Median"]=dataset[columnName].median()
        descriptive[columnName]["Mode"]=dataset[columnName].mode()[0]
        descriptive[columnName]["Q1:25%"]=dataset.describe()[columnName]["25%"]
        descriptive[columnName]["Q2:50%"]=dataset.describe()[columnName]["50%"]
        descriptive[columnName]["Q3:75%"]=dataset.describe()[columnName]["75%"]
        descriptive[columnName]["99%"]=np.percentile(dataset[columnName],99)
        descriptive[columnName]["Q4:100%"]=dataset.describe()[columnName]["max"]
        descriptive[columnName]["IQR"]=descriptive[columnName]["Q3:75%"]-descriptive[columnName]["Q1:25%"]
        descriptive[columnName]["1.5RULE"]=1.5*descriptive[columnName]["IQR"]
        descriptive[columnName]["LESSER"]=descriptive[columnName]["Q1:25%"]-descriptive[columnName]["1.5RULE"]
        descriptive[columnName]["GREATER"]=descriptive[columnName]["Q3:75%"]+descriptive[columnName]["1.5RULE"]
        descriptive[columnName]["MIN"]=dataset[columnName].min()
        descriptive[columnName]["MAX"]=dataset[columnName].max()
        descriptive[columnName]["kurtosis"]=dataset[columnName].kurtosis()
        descriptive[columnName]["skew"]=dataset[columnName].skew()
    return descriptive 

def outlierColumnNames(Quan,columnName):
    LESSER=[]
    GREATER=[]
    for columnName in Quan:
        if(descriptive[columnName]["MIN"]<descriptive[columnName]["LESSER"]):
            LESSER.append(columnName)
        if(descriptive[columnName]["MAX"]>descriptive[columnName]["GREATER"]):
            GREATER.append(columnName)
    return LESSER,GREATER

def replacing_outliers(dataset,columnName):
    for columnName in LESSER:
        dataset[columnName][dataset[columnName]<descriptive[columnName]["LESSER"]]=descriptive[columnName]["LESSER"]
    for columnName in GREATER:
        dataset[columnName][dataset[columnName]>descriptive[columnName]["GREATER"]]=descriptive[columnName]["GREATER"]
    return descriptive