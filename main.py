import pandas as pd
import numpy as np

import csv



import matplotlib.pyplot as plt 
# Import the MarkovChain class from markovchain.py
from markovchain import MarkovChain

SOURCE_FILE = 'data_set_sample.csv'

source_data = []

prob_dict = {}
all_syllables = []



df = pd.read_csv(SOURCE_FILE,  skiprows = 1,header = None)


# go throught the file row by row
for idx in range(0,len(df)-1):
    #ignore the row label (bird name)
    data = df.iloc[[idx]]
    data = data.drop(data.columns[0],axis=1)
    
    # list comprehension to remove any value that is an empty string
    all_syllables = all_syllables + list(data.values[0])

    # loop over the "sequence"
    # we are going to look at the index and the next value
    # so the max length is -2 of the entire length of the row
    for i in  range(1,len(data.columns)-1): 
        if np.isnan(data.iloc[0,i+1]):
            pass
        else:
            transition = f"{int(data.iloc[0,i])}>{int(data.iloc[0,i+1])}"
            if transition not in prob_dict:
                prob_dict[transition] = 1
            else:
                prob_dict[transition] += 1 



# print it to the console
# print(prob_dict)

# Save the results to output.csv as a csv
with open('output.csv', 'w') as f:
    for key in prob_dict.keys():
        f.write("%s,%s\n"%(key,prob_dict[key]))

        


# Get unique values
unique_list = []

# traverse for all elements
for x in all_syllables:
    # check if exists in unique_list or not
    if np.isnan(x):
        pass
    elif x not in unique_list:
        unique_list.append(int(x))

# # Now to actually try to make a matrix
# # need to collect all possible elements
# print(unique_list)
# # Normalize the output

# # need to update an array of arrays at a cross section
d = pd.DataFrame(0, index=np.arange(len(unique_list)), columns=(['start'] + unique_list))
d = d.assign(start=unique_list)

for key in prob_dict: 
    first, second  = [int(k) for k in key.split('>')]
    d.loc[d['start'] == first, second] = prob_dict[key] 

# df.div(df.sum(axis=1), axis=0)
origin = d.copy(deep=True)
print(origin)


vals = d.iloc[0:, 1:]

normalized = d
normalized.iloc[0:, 1:] = vals.div(vals.sum(axis=1), axis=0).fillna(0)

print(normalized)

P = vals.div(vals.sum(axis=1), axis=0).to_numpy() # Transition matrix
mc = MarkovChain(P, unique_list)
mc.draw("markov-chain-states.png")