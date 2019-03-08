import numpy as np
import pandas as pd

# Calculate the cumulative rate given two columns: number made and number attempted
def calculate_cumulative_rate(c1, c2):
    col = []
    for i in range(0, max(len(c1), len(c2))):
        made = np.sum(c1[0:i+1])
        attempted = np.sum(c2[0:i+1])
        rate = float(made/attempted)
        col.append(rate)
    
    return col
