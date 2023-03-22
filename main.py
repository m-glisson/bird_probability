import csv 
 

SOURCE_FILE = 'data_set_sample.csv'


source_data = []

prob_dict = {}

with open(SOURCE_FILE, mode ='r') as file:
  csvFile = csv.reader(file)
 
  # displaying the contents of the CSV file
  for lines in csvFile:
    source_data.append(lines)



print(source_data)

source_data.pop(0)


# go throught the file row by row
for sequence in source_data:
    #ignore the row label (bird name)
    data = sequence[1:]
    # list comprehension to remove any value that is an empty string
    data = [d for d in data if d != '']

    # loop over the "sequence"
    # we are going to look at the index and the next value
    # so the max length is -2 of the entire length of the row
    for idx in  range(0,len(data)-2): 
        transition = f"{data[idx]}>{data[idx+1]}"
        if transition not in prob_dict:
            prob_dict[transition] = 1
        else:
            prob_dict[transition] += 1 


print(prob_dict)


with open('output.csv', 'w') as f:
    for key in prob_dict.keys():
        f.write("%s,%s\n"%(key,prob_dict[key]))

        

        
