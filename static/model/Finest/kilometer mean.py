import pandas as pd

def loadExcelFile():
    colnames = ['brand', 'model', 'model_year', 'transmission', 'engine_size',
                'drivetrain', 'fuel_type', 'colour', 'lot',
                'kilometer', 'status', 'price']
    dataframe = pd.read_csv(r"C:\Users\rabin\Desktop\hello/ScrappedData.csv", sep=",", names=colnames, header=None)
    return dataframe.dropna()

def filterDataFrame():
    dataframe = loadExcelFile()
    df = dataframe.fillna(0)
    df = df.dropna()
   
    df.kilometer = pd.to_numeric(df.kilometer, errors='coerce', downcast='integer')
    
    count = 0
    for index, row in df.iterrows():
        if row['kilometer'] <= 1500:
            count = count + 1
            df.loc[index, 'kilometer'] = getYearKilometerMeanValue(dataframe, row['model_year'])
    print('Total Changed:', count)
    df.to_csv('hero.csv',index=False)
    return df.dropna()
    


def getYearKilometerMeanValue(dataframe, value):
    date = str(value).split('.')[0]
    df = dataframe.dropna()
    df.kilometer = pd.to_numeric(df.kilometer, errors='coerce', downcast='integer')
    df = round(df.groupby('model_year', as_index=False)['kilometer'].mean())
    mean_dict = dict(zip(df.model_year, df.kilometer))
    data = mean_dict.get(date)
    return data

filterDataFrame()
