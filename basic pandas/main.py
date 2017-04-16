import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

# Not necessary, I just do this so I do not show my API key.
#api_key = open('quandlapikey.txt','r').read()

def state_list():
    fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return fiddy_states[0][0][1:]
    

def grab_initial_state_data():
    states = state_list()

    main_df = pd.DataFrame()

    for abbv in states:
        query = "FMAC/HPI_"+str(abbv)
        df = quandl.get(query, authtoken='SCN2zdveEYwG1B82t6B1')
        df.rename(columns={'Value': abbv}, inplace=True)
        df[abbv] = (df[abbv]-df[abbv][0]) / df[abbv][0] * 100.0
        print(df.head())
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)
            
    pickle_out = open('fiddy_states.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()

def HPI_Benchmark():
    df = quandl.get("FMAC/HPI_USA", authtoken='SCN2zdveEYwG1B82t6B1')
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df.rename(columns={'Value':'US_HPI'}, inplace=True)
    return df

def mortgage_30y():
    df = quandl.get("FMAC/MORTG", trim_start="1975-01-01", authtoken='SCN2zdveEYwG1B82t6B1')
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df.rename(columns={'Value':'M30'}, inplace=True)
    #df=df.resample('1D').mean()
    df=df.resample('M').mean()
    return df


grab_initial_state_data() 
HPI_data = pd.read_pickle('fiddy_states.pickle')
m30 = mortgage_30y()
HPI_Bench = HPI_Benchmark()
HPI = HPI_Bench.join(m30,)
HPI.dropna(inplace=True)
print(HPI.corr())









