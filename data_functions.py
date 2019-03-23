import numpy as np
import pandas as pd

def calculate_rates(years, df, c1, c2):
    rates_list = []
    for y in years:
        data = df[df.Season==y]
        
        rates_dict = {}
        for t in data.WTeamID.unique():
            Wdf = data[data.WTeamID==t]
            Ldf = data[data.LTeamID==t]
            Wmu = np.mean(Wdf[c1])
            Lmu = np.mean(Ldf[c2])
            t_mu = np.mean([Wmu, Lmu])
           
            rates_dict[t] = t_mu
        rates_list.append(rates_dict)
        
    return rates_list


# Calculate the average for each year
def calculate_average(years, df, c1, c2):
    avg_list = []
    for y in years:
        data = df[df.Season==y]
        
        avg_dict = {}
        for t in data.WTeamID.unique():
            Wdf = data[data.WTeamID==t]
            Ldf = data[data.LTeamID==t]
            Wmu = np.mean(Wdf[c1])
            Lmu = np.mean(Ldf[c2])
            t_mu = np.mean([Wmu, Lmu])
            
            avg_dict[t] = t_mu
        avg_list.append(avg_dict)
        
    return avg_list
    
    
def build_df(d_list, years, var):
    df = pd.DataFrame()
    for i in range(0, len(d_list)-1):
        y = years[i]
        c1 = str(y)
        df[c1] = pd.Series(d_list[i])
        
    df = df.reset_index()
    c_list = ['TeamID']
    for y in years[0:len(years)-1]:
        c_list.append(str(y))
    df.columns = c_list
    df = df.set_index('TeamID').stack().reset_index()
    df.columns = ['TeamID', 'Season', var]
    df['Season'] = df['Season'].astype(int)+1
        
    return df
          
            
def average_score_diff(years, df, c):
    avg_list = []
    for y in years:
        data = df[df.Season==y]
        avg_dict = {}
        for t in data.WTeamID.unique():
            Wdf = data[data.WTeamID==t]
            Ldf = data[data.LTeamID==t]
            Wmu = np.mean(Wdf[c])
            Lmu = np.mean(Ldf[c])
            t_mu = np.mean([Wmu, Lmu])
            
            avg_dict[t] = t_mu
        avg_list.append(avg_dict)
        
    return avg_list


def rename_columns(df):
    cols = []
    old = []
    for c in df.columns:
        if c is not 'Season':
            s = str(c)
            name = 'Opp_'+s
            df[name] = df[c]
            cols.append(name)
            old.append(c)
        
            
    newdf = df.drop(old, axis=1) 
    newdf.columns = ['Season', str(cols[0]), str(cols[1])]
            
    return newdf
            
            
            
            
        