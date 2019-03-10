import numpy as np
import pandas as pd

# Calculate the cumulative rate given two columns: number made and number attempted
def calculate_cumulative_rate(c1, c2):
    col = []
    for i in range(0, max(len(c1), len(c2))):
        if i==0:
            col.append(np.nan)
        else:
            made = np.sum(c1[0:i])
            attempted = np.sum(c2[0:i])
            rate = float(made/attempted)
            col.append(rate)
    
    return col

# Create a column of the cumulative season rate for a team
def create_rate_column(df, year, teamid, c1, c2):
    c_rate = []
    for k in df[year].unique():
        data = df[df[year]==k]
        for i in data[teamid].unique():
            team_data = data[data[teamid]==i]
            r1 = team_data[c1]
            r2 = team_data[c2]
            r_col = calculate_cumulative_rate(r1, r2)
            for a in r_col:
                c_rate.append(a)
    return c_rate
            
            
#calculate cumulative average for current season
def calculate_cumulative_avg(c1):
    col = []
    for i in range(0, len(c1)):
        if i == 0:
            col.append(np.nan)
        elif i > 0:
            avg = np.mean(c1[0:i])
            col.append(avg)
    return col

# Create a column of the cumulative average for the season
def create_average_column(df, year, vals, teamid):
    avg_col = []
    for k in df[year].unique():
        data = df[df[year]==k]
        for i in data[teamid].unique():
            team_data = data[data[teamid]==i]
            x = team_data[vals].values
            c = calculate_cumulative_avg(x)
            avg_col.append(c)
    new_col = []
    for a in avg_col:
        for b in a:
            new_col.append(b)
    return new_col

