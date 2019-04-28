import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.metrics import confusion_matrix

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
    
    
def build_df(d_list, years, var, yrs_prior):
    df = pd.DataFrame()
    for i in range(0, len(d_list)-1):
        y = years[i]
        c1 = str(y)
        df[c1] = pd.Series(d_list[i])
        
    df = df.reset_index()
    c_list = ['TeamID']
    for y in years[0:len(years)-1]:
        c_list.append(str(y))
    # name the columns with the year
    df.columns = c_list
    # stack the data
    df = df.set_index('TeamID').stack().reset_index()
    df.columns = ['TeamID', 'Season', var]
    df['Season'] = df['Season'].astype(int)+yrs_prior
        
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
            
          
def get_corr_heat_map(data, ignore_cancelled = True):
    if ignore_cancelled:
        data = data[data['is_cancelled'] == 0].drop('is_cancelled', axis = 1)
    data_to_visualize = data[~data.isin([np.nan, np.inf, -np.inf]).any(1)]
    # Create Correlation df
    corr = data_to_visualize.corr()
    # Plot figsize
    fig, ax = plt.subplots(figsize=(15, 10))
    # Generate Color Map
    colormap = sns.diverging_palette(220, 10, as_cmap=True)
    # Generate Heat Map, allow annotations and place floats in map
    sns.heatmap(corr, cmap=colormap, annot=True, fmt=".2f")
    # Apply xticks
    plt.xticks(range(len(corr.columns)), corr.columns);
    # Apply yticks
    plt.yticks(range(len(corr.columns)), corr.columns)
    # show plot
    plt.show()
            
# Test whether the difference between features for winners and losers is significant         
def test_for_difference(df1, df2, alt):
    for c in df1.columns:
        p1 = df1[c]
        p2 = df2[c]
        test = stats.mannwhitneyu(p1, p2, alternative = alt)
        # print the p-value
        print('The p-value for the difference between ', c , 'is: ', test[1])
    
    
def draw_confusion_matrix(actuals, predicted, actual_labels, predicted_labels):
    fig, ax = plt.subplots(figsize=(15, 10))

    sns.heatmap(confusion_matrix(actuals, predicted), annot=True,
                ax=ax);  # annot=True to annotate cells

    # labels, title and ticks
    ax.set_xlabel('Predicted labels');
    ax.set_ylabel('True labels');
    ax.set_title('Confusion Matrix');
    ax.xaxis.set_ticklabels(actual_labels);
    ax.yaxis.set_ticklabels(predicted_labels)
    plt.show()