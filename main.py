import pandas as pd
import numpy as np

import json

# import csv



import matplotlib.pyplot as plt 
# Import the MarkovChain class from markovchain.py
from markovchain import MarkovChain

SOURCE_FILE = 'data/Syllable Sequences - After Visual Sorting.csv'
# SOURCE_FILE = 'test.csv'

dat = pd.read_csv(SOURCE_FILE,  skiprows = 1,header = None)


# Get all states avaliable as keywords
keywords = list(dat[1].unique())
keywords.append('all')



def create_json_links(syllables, transitions_dict):

    {
    "nodes": [
        {"id": "Myriel" },
    ], 
        "links": [
        {"source": "Napoleon", "target": "Myriel", "value": 1},
        ]
    }

    data = {}
    data['nodes'] = [{'id': syllable} for syllable in syllables]
    data['links'] = [{'source': k.split('>')[0], 'target': k.split('>')[1], 'value': transitions_dict[k]} for k in transitions_dict.keys()]

    # write the dict to a json file


    return data




for keyword in keywords:
    prob_dict = {}
    all_syllables = []



    df = pd.read_csv(SOURCE_FILE,  skiprows = 1,header = None)
    if keyword != 'all': 
        df = df.loc[df[1] == keyword]



    def isBlank(val):
        if isinstance(val, str):
            return False
        elif np.isnan(val): 
            return True
        else: 
            return False 
        


    # go throught the file row by row
    for idx in range(0,len(df)-1):
        #ignore the row label (bird name)
        data = df.iloc[[idx]]
        data = data.drop(data.columns[0],axis=1)
        data = data.drop(data.columns[0],axis=1)
        
        # list comprehension to remove any value that is an empty string
        all_syllables = all_syllables + list(data.values[0])

        # loop over the "sequence"
        # we are going to look at the index and the next value
        # so the max length is -2 of the entire length of the row
        for i in range(0,len(data.columns)-1): 
            if isBlank(data.iloc[0,i+1]):
                pass
            else:
                transition = f"{str(data.iloc[0,i])}>{str(data.iloc[0,i+1])}"
                if transition not in prob_dict:
                    prob_dict[transition] = 1
                else:
                    prob_dict[transition] += 1 



    # Get unique values
    unique_list = []

    # traverse for all elements
    for x in all_syllables:
        # check if exists in unique_list or not
        if isBlank(x):
            pass
        elif x not in unique_list:
            unique_list.append(str(x))

    # # Now to actually try to make a matrix
    # # need to collect all possible elements
    # print(unique_list)
    # # Normalize the output

    # # need to update an array of arrays at a cross section
    d = pd.DataFrame(0, index=np.arange(len(unique_list)), columns=(['start'] + unique_list))
    d = d.assign(start=unique_list)

    for key in prob_dict: 
        first, second  = [str(k) for k in key.split('>')]
        d.loc[d['start'] == first, second] = prob_dict[key] 

    # df.div(df.sum(axis=1), axis=0)
    origin = d.copy(deep=True)
    print(origin)


    vals = d.iloc[0:, 1:]

    normalized = d
    normalized.iloc[0:, 1:] = vals.div(vals.sum(axis=1), axis=0).fillna(0)

    print(normalized)

    P = vals.div(vals.sum(axis=1), axis=0).to_numpy() # Transition matrix
    mc = MarkovChain(P, unique_list,
                    title = f"transition matrix for {keyword}",
                    arrow_head_width = 0.50, 
                    display_threshold = 0.2,
                    node_radius = 2.5, 
                    window_extension  = 6)
    mc.draw(f"data/{keyword}-markov-chain-states.png", show=False)



    json_data = create_json_links(syllables=unique_list, transitions_dict=prob_dict)

    with open(f'data/{keyword}-markov-chain-states.json', 'w') as f:
        json.dump(json_data, f)



    # make a normalized dataset to parse through 
    norm = normalized.set_index('start')
    

        # Save the results to output.csv as a csv
    with open(f'data/{keyword}-states-output.csv', 'w') as f:
        for key in prob_dict.keys():
            start = key.split('>')[0]
            end = key.split('>')[1]
            f.write("%s,%s,%s\n"%(key,prob_dict[key], norm.loc[start, end]))


