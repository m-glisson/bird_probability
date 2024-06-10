import pandas as pd 
import sys
 
# total arguments
n = len(sys.argv)
file = "./data/Cross Correlation Pre Processiong.xlsx"   
if len(sys.argv)>1:
    file = sys.argv[1]  

print("Total arguments passed:", n)
print("\n File name:", file)



data_set = pd.read_excel(open(file, 'rb'))

for column in data_set.columns:
    if 'Unnamed' in column:
        del data_set[column]



# I'm going to make all the column names lower case to make it easier to work with
data_set.columns = [x.lower() for x in data_set.columns]

## Calculate the Median
# use group by to group the data by date, then run median on the score column over those groups
median_set = data_set.groupby('date')['score'].median()



# At this point we can really just output the data to a csv file and be done with it
# that would look like this
# median_set.to_csv('median_frame.csv') 
# but you want everything in the same file, so lets do that

# the above produced a series, so we need to convert it to a frame just to make it easier to work with
median_frame = median_set.to_frame()

# Then I reset the index so I can make the date a colum that I can work with 
median_frame.reset_index(inplace=True)


# while everything is open, lets try to get the average from the last three days 

# do it raw
# take the tail of the data set, and then take the mean of the score column
raw_last_three = median_frame.tail(3)['score'].mean()



# Now I can merge the two dataframes together using a horrible loop 
# loops are looked down on in pandas since they don't scale well, but this is a small data set so it should be fine

# make an empty list to hold the new data
new_set = []
# loop through the rows in the original data set
for x in range(0, len(data_set)):
    row = data_set.iloc[x]
    new_row = row.copy()

    # check if the date is in the median set
    # if it is, then we add that in, or ignore it
    if x < len(median_set): 
        new_row['median_date'] = median_frame.iloc[x]['date']
        new_row['median_score'] = median_frame.iloc[x]['score']
    else: 
        new_row['median_date'] = None
        new_row['median_score'] = None  

    if x == 0: 
        new_row['raw_last_three'] = "average_last_three"
    if x == 0: 
        new_row['raw_last_three'] = raw_last_three

    new_set.append(new_row)



# now write that block out to a CSV file so we can look at it
new_filename = file.replace('.xlsx', '_processed.csv')
pd.DataFrame(new_set).to_csv(new_filename)

